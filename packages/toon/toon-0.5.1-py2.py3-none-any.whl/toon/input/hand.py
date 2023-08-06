"""
.. module:: input
     :platform: Unix, Windows
     :synopsis: Tools for dealing with input devices.

.. moduleauthor:: Alexander Forrence <aforren1@jhu.edu>

"""
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from builtins import super
from future import standard_library
standard_library.install_aliases()
import struct
import numpy as np
from toon.input.base_input import BaseInput, DummyTime
import hid


class Hand(BaseInput):
    """Interface to HAND.

    This provides an interface to HAND, which is developed by members of
    Kata and the BLAM Lab.

    """
    def __init__(self, clock_source=DummyTime(),
                 multiprocess=False,
                 dims=(50, 15),
                 nonblocking=True):
        """Interface to HAND.

        Kwargs:
            clock_source: Class that provides a `getTime` method. Default object calls :fun:`time.time()`.
            multiprocess (bool): Whether multiprocessing is enabled or not.
            buffer_rows (int): Sets the number of rows in the shared array.
            nonblocking (bool): Whether the HID interface blocks for input.
            _ncol (int): Sets the number of columns in the shared array (depends on the length of
                         the data provided by the `_read` method.

        Notes:
            `nonblocking` should typically remain `True`, as I doubt there's any performance
            benefit and it leads to difficult debugging.

            Data is formatted as [x, y, z] per finger (15 elements, 3 per finger).

        Examples:
            Initialization should be straightforward.

            >>> device = Hand(multiprocess=True)
        """
        if dims[1] is not 15:
            raise ValueError('The second dimension must be 15.')

        super(Hand, self).__init__(clock_source, multiprocess, dims)

        self._rotval = np.pi / 4.0
        self._sinval = np.sin(self._rotval)
        self._cosval = np.cos(self._rotval)
        self.nonblocking = nonblocking
        self._force_data = np.full(dims[1], np.nan)
        self._device = None

    def _init_device(self):
        """HAND-specific initialization.
        """
        self._device = hid.device()
        for d in hid.enumerate():
            if d['product_id'] == 1158 and d['usage'] == 512:
                dev_path = d['path']
        self._device.open_path(dev_path)
        self._device.set_nonblocking(self.nonblocking)

    def _read(self):
        """HAND-specific read function.
        """
        timestamp = self.time.getTime()
        data = self._device.read(46)
        if data:
            data = struct.unpack('>LhHHHHHHHHHHHHHHHHHHHH', bytearray(data))
            data = np.array(data, dtype='d')
            data[0] /= 1000.0  # device timestamp (since power-up, in milliseconds)
            data[1:] /= 65535.0
            self._force_data[0::3] = data[2::4] * self._cosval - data[3::4] * self._sinval  # x
            self._force_data[1::3] = data[2::4] * self._sinval + data[3::4] * self._cosval  # y
            self._force_data[2::3] = data[4::4] + data[5::4]  # z
            return timestamp, self._force_data
        return None, None

    def _stop_device(self):
        """HAND does not need to be stopped."""
        pass

    def _close_device(self):
        """Close the HID interface."""
        self._device.close()
