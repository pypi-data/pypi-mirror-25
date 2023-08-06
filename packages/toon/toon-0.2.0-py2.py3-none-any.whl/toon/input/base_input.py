"""
.. module:: input
     :platform: Unix, Windows
     :synopsis: Input devices for experiments.

.. moduleauthor:: Alexander Forrence <aforren1@jhu.edu>

"""

import abc
from time import time
import multiprocessing as mp
import ctypes
import numpy as np


def shared_to_numpy(mp_arr, dims):
    """Convert a :class:`multiprocessing.Array` to a numpy array.
    Helper function to allow use of a :class:`multiprocessing.Array` as a numpy array.
    Derived from the answer at:
    <https://stackoverflow.com/questions/7894791/use-numpy-array-in-shared-memory-for-multiprocessing>
    """
    return np.frombuffer(mp_arr.get_obj()).reshape(dims)


class DummyTime(object):
    """Default timer.
    Provides a `getTime()` method as to be compatible with psychopy's `monotonicClock`.
    """

    @staticmethod
    def getTime():
        return time()


class BaseInput(object):
    """Abstract Base Class for :mod:`multiprocessing`-empowered input devices.

    Multiprocessing allows us to poll an input device on a separate process without
    interfering with the execution of the main process.

    Notes:
        Derived classes must provide a `_read` method which returns a single, 1-dimensional
        observation. See :class:`toon.input.Hand` and :class:`toon.input.BlamBirds` for examples.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self,
                 clock_source=DummyTime,
                 multiprocess=False,
                 dims=(50, 1)):
        """Abstract Base Class for :mod:`multiprocessing`-empowered input devices.

        Kwargs:
            clock_source: Class that provides a `getTime` method. Default object calls :fun:`time.time()`.
            multiprocess (bool): Whether multiprocessing is enabled or not.
            dims (tuple or list): Sets the dimensions in the shared array. The first dimension represents
                                  time, while subsequent ones represent data at that time point.

        We use :class:`abc.ABCMeta` to help ensure the same API is provided across devices.

        Notes:
            Don't be afraid to set a relatively large `buffer_rows`, e.g. 10 times larger than the
            expected data in a given frame.

            The `clock_source` was written with :class:`psychopy.core.monotonicClock` in mind.
            If I understand correctly, using this will allow for a sub-millisecond timer where the
            origin of the remote timer matches that of a clock on the local process. In other words,
            we can share a high-resolution clock across processes. Testing should be done though.
        """

        self.time = clock_source
        self.multiprocess = multiprocess
        self._start_time = None
        self.dims = dims
        self._stopped = False

        if multiprocess:
            self._shared_mp_buffer = mp.Array(ctypes.c_double, int(np.prod(self.dims)))
            self._shared_np_buffer = shared_to_numpy(self._shared_mp_buffer, self.dims)
            self._shared_np_buffer.fill(np.nan)

            self._shared_mp_time_buffer = mp.Array(ctypes.c_double, self.dims[0])
            self._shared_np_time_buffer = shared_to_numpy(self._shared_mp_time_buffer,
                                                          (self.dims[0], 1))
            self._shared_np_time_buffer.fill(np.nan)

            self._read_buffer = np.full(self.dims, np.nan)
            self._read_time_buffer = np.full((self.dims[0], 1), np.nan)
            self._poison_pill = mp.Value(ctypes.c_bool)
            self._poison_pill.value = False
            self._process = None

    def __enter__(self):
        """Start reading from the device.

        This either starts the device on the main process (`multiprocess=False`),
        or on a separate process (`multiprocess=True`).
        """
        self._start_time = self.time.getTime()
        if self.multiprocess:
            self._poison_pill.value = False
            self._process = mp.Process(target=self._mp_worker,
                                       args=(self._shared_mp_buffer,
                                             self._shared_mp_time_buffer,
                                             self._poison_pill))
            self._process.daemon = True
            self._process.start()
        else:  # start device on original processor
            self._init_device()
        return self

    def read(self):
        """Read data from the device.

        Returns:
            A tuple containing the data and timestamp, respectively.
            (None, None) if no data is available.

        In the multiprocessing case, the returned data will be a 2-dimensional
        array, and the timestamp will be a 1-dimensional array with a length
        matching the number of rows in the data. In other words, there is one
        timestamp per measurement.

        Also, in the multiprocessing case, if the buffer is filled before it is read,
        subsequent readings will overwrite the oldest readings.
        """
        if self.multiprocess:
            with self._shared_mp_buffer.get_lock(), self._shared_mp_time_buffer.get_lock():
                np.copyto(self._read_buffer, self._shared_np_buffer)
                np.copyto(self._read_time_buffer, self._shared_np_time_buffer)
            self.clear()
            if np.isnan(self._read_buffer).all():
                return None, None
            return (self._read_buffer[~np.isnan(self._read_buffer).any(axis=1)],
                    self._read_time_buffer[~np.isnan(self._read_time_buffer).any(axis=1)])
        # no multiprocessing (returns tuple (data, timestamp))
        return self._read()

    def __exit__(self, type, value, traceback):
        """End connection with device.

        Calls `_stop_device()` and `_close_device()` or toggles the poison pill.
        """
        if self.multiprocess:
            self._poison_pill.value = True  # also causes remote device to *close*
            self._process.join()
        else:
            self._stop_device()
            self._close_device()

    def clear(self):
        """Removes all pending data from the shared buffer.
        """
        if self.multiprocess:
            with self._shared_mp_buffer.get_lock(), self._shared_mp_time_buffer.get_lock():
                self._shared_np_buffer.fill(np.nan)
                self._shared_np_time_buffer.fill(np.nan)

    def _mp_worker(self, shared_mp_buffer, shared_mp_time_buffer, poison_pill):
        """Polls the device on a separate process.

        Only utilized when `multiprocessing=True`. Manages the device state,
        and updates the shared array.

        Note:
            Avoid interacting with the device on the main process/interactively
            when using multiprocessing, or understand that you may not get
            sensible results.
        """
        self._init_device()
        self.clear()  # purge buffers (in case there's residual stuff from previous run)
        shared_np_buffer = shared_to_numpy(shared_mp_buffer, self.dims)
        shared_np_time_buffer = shared_to_numpy(shared_mp_time_buffer, (self.dims[0], 1))
        while not poison_pill.value:
            data, timestamp = self._read()
            if data is not None:
                with shared_mp_buffer.get_lock(), shared_mp_time_buffer.get_lock():
                    current_nans = np.isnan(shared_np_buffer).any(axis=1)
                    if current_nans.any():
                        # fill in the next nan row
                        next_index = np.where(current_nans)[0][0]
                        shared_np_buffer[next_index, :] = data
                        shared_np_time_buffer[next_index, 0] = timestamp
                    else:
                        # replace the oldest data in the buffer with new data
                        shared_np_buffer[:] = np.roll(shared_np_buffer, -1, axis=0)
                        shared_np_time_buffer[:] = np.roll(shared_np_time_buffer, -1, axis=0)
                        shared_np_buffer[-1, :] = data
                        shared_np_time_buffer[-1, 0] = timestamp
        self._stop_device()
        self._close_device()

    # The following four functions must be implemented by derived input devices,
    # along with `__init__()`.
    @abc.abstractmethod
    def _read(self):
        """Core read method, implemented by the subclass.
        Read a single line (assumes vector is outcome)
        Return data, timestamp as separate!
        """
        return 0, 0

    @abc.abstractmethod
    def _init_device(self):
        """Start talking to the device.

        Called by `__enter__()` or the `_mp_worker()` function.
        """
        pass

    @abc.abstractmethod
    def _stop_device(self):
        """Stop device (without closing).

        Called by `__exit__()` or the `_mp_worker()` function (which will also call `_close_device()`).
        """
        pass

    @abc.abstractmethod
    def _close_device(self):
        """Disconnect from the device.

        Called by `__exit__()` or the `_mp_worker()`.
        """
        pass
