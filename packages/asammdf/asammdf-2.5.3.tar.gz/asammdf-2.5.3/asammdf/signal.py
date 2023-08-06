# -*- coding: utf-8 -*-
"""
asammdf *Signal* class module for time correct signal processing
"""
import numpy as np
import matplotlib.pyplot as plt

from .utils import MdfException


class Signal(object):
    """
    The Signal represents a signal described by it's samples and timestamps.
    It can do aritmethic operations agains other Signal or numeric type.
    The operations are computed in respect to the timestamps (time correct).
    The integer signals are not interpolated, instead the last value relative to the current timestamp is used.
    *samples*, *timstamps* and *name* are mandatory arguments.

    Parameters
    ----------
    samples : numpy.array | list | tuple
        signal samples
    timestamps : numpy.array | list | tuple
        signal timestamps
    unit : str
        signal unit
    name : str
        signal name
    conversion : dict
        dict describing the channel conversion , default *None*
    comment : str
        signal comment, default ''

    """
    def __init__(self, samples=None, timestamps=None, unit='', name='', conversion=None, comment=''):
        if samples is None or timestamps is None or name == '':
            raise MdfException('"samples", "timestamps" and "name" are mandatory arguments for Signal class instance')
        elif len(samples) != len(timestamps):
            raise MdfException('samples and timestamps lenght do not match ({} vs {})'.format(len(samples), len(timestamps)))
        else:
            if isinstance(samples, list) or isinstance(samples, tuple):
                samples = np.array(samples)
            if isinstance(timestamps, list) or isinstance(samples, tuple):
                timestamps = np.array(timestamps, dtype=np.float64)
            self.samples = samples
            self.timestamps = timestamps
            self.unit = unit
            self.name = name
            self.conversion = conversion
            self.comment = comment

    def __str__(self):
        return 'Signal {{ name="{}":\ts={}\tt={}\tunit="{}"\tconversion={} \tcomment="{}"}}'.format(self.name, self.samples, self.timestamps, self.unit, self.conversion, self.comment)

    def __repr__(self):
        return 'Signal {{ {}:\ts={}\tt={} }}'.format(self.name, repr(self.samples), repr(self.timestamps))

    def plot(self):
        """plot Signal samples"""
        fig = plt.figure()
        fig.canvas.set_window_title(self.name)
        if self.comment:
            plt.title('{}\n({})'.format(self.name, self.comment))
        else:
            plt.title(self.name)
        plt.xlabel('Time [s]')
        plt.ylabel('[{}]'.format(self.unit))
        plt.plot(self.timestamps, self.samples, 'b')
        plt.plot(self.timestamps, self.samples, 'b.')
        plt.grid(True)
        plt.show()

    def cut(self, start=None, stop=None):
        """
        Cuts the signal according to the *start* and *stop* values, by using the insertion indexes in the signal's *time* axis.

        Parameters
        ----------
        start : float
            start timestamp for cutting
        stop : float
            stop timestamp for cutting

        Returns
        -------
        result : Signal
            new *Signal* cut from the original

        Examples
        --------
        >>> new_sig = old_sig.cut(1.0, 10.5)
        >>> new_sig.timestamps[0], new_sig.timestamps[-1]
        0.98, 10.48

        """

        if start is None and stop is None:
            # return the channel uncut
            result = self

        else:
            if start is None:
                # cut from beggining to stop
                stop = np.searchsorted(self.timestamps, stop, side='right')
                if stop:
                    result = Signal(self.samples[: stop],
                                    self.timestamps[:stop],
                                    self.unit,
                                    self.name,
                                    self.conversion,
                                    self.comment)
                else:
                    result = Signal(np.array([]),
                                    np.array([]),
                                    self.unit,
                                    self.name,
                                    self.conversion,
                                    self.comment)

            elif stop is None:
                # cut from start to end
                start = np.searchsorted(self.timestamps, start, side='left')
                result = Signal(self.samples[start: ],
                                self.timestamps[start: ],
                                self.unit,
                                self.name,
                                self.conversion,
                                self.comment)

            else:
                # cut between start and stop
                start_ = np.searchsorted(self.timestamps, start, side='left')
                stop_ = np.searchsorted(self.timestamps, stop, side='right')
                if stop_ == start_:

                    if len(self.timestamps) and stop >= self.timestamps[0] and start <= self.timestamps[-1]:
                        # start and stop are found between 2 signal samples
                        # so return the previous sample
                        result = Signal(self.samples[start_ - 1: start_],
                                        self.timestamps[start_ - 1: start_],
                                        self.unit,
                                        self.name,
                                        self.conversion,
                                        self.comment)
                    else:
                        # signal is empty or start and stop are outside the signal time base
                        result = Signal(np.array([]),
                                        np.array([]),
                                        self.unit,
                                        self.name,
                                        self.conversion,
                                        self.comment)
                else:
                    result = Signal(self.samples[start_: stop_],
                                    self.timestamps[start_: stop_],
                                    self.unit,
                                    self.name,
                                    self.conversion,
                                    self.comment)
        return result

    def extend(self, other):
        """ extend signal with samples from another signal

        Parameters
        ----------
        other : Signal

        """
        last_stamp = self.timestamps[-1]
        delta = last_stamp / len(self) + last_stamp
        if len(other):
            other_first_sample = other.timestamps[0]
            if last_stamp >= other_first_sample:
                timestamps = other.timestamps + delta - other_first_sample
            else:
                timestamps = other.timestamps

            result = Signal(np.append(self.samples, other.samples),
                            np.append(self.timestamps, timestamps),
                            self.unit,
                            self.name,
                            self.conversion,
                            self.comment)
        else:
            result = self
        return result

    def interp(self, new_timestamps):
        """ returns a new *Signal* interpolated using the *new_timestamps*"""
        if self.samples.dtype in ('float64', 'float32'):
            s = np.interp(new_timestamps, self.timestamps, self.samples)
        else:
            idx = np.searchsorted(self.timestamps, new_timestamps, side='right') - 1
            idx = np.clip(idx, 0, idx[-1])
            s = self.samples[idx]
        return Signal(s, new_timestamps, self.unit, self.name, self.conversion)

    def __apply_func(self, other, func_name):

        if isinstance(other, Signal):
            time = np.union1d(self.timestamps, other.timestamps)
            s = self.interp(time).samples
            o = other.interp(time).samples
            func = getattr(s, func_name)
            s = func(o)
        elif other is None:
            s = self.samples
            time = self.timestamps
        else:
            func = getattr(self.samples, func_name)
            s = func(other)
            time = self.timestamps
        return Signal(s, time, self.unit, self.name, self.conversion)

    def __pos__(self):
        return Signal(self.samples, self.timestamps, self.unit, self.name, self.conversion)

    def __neg__(self):
        return Signal(np.negative(self.samples), self.timestamps, self.unit, self.name, self.conversion)

    def __round__(self, n):
        return Signal(np.around(self.samples, n), self.timestamps, self.unit, self.name, self.conversion)

    def __sub__(self, other):
        return self.__apply_func(other, '__sub__')

    def __isub__(self, other):
        return self.__sub__(other)

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __add__(self, other):
        return self.__apply_func(other, '__add__')

    def __iadd__(self, other):
        return self.__add__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return self.__apply_func(other, '__mul__')

    def __imul__(self, other):
        return self.__mul__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self.__apply_func(other, '__truediv__')

    def __itruediv__(self, other):
        return self.__truediv__(other)

    def __rtruediv__(self, other):
        return self.__apply_func(other, '__rtruediv__')

    def __mod__(self, other):
        return self.__apply_func(other, '__mod__')

    def __pow__(self, other):
        return self.__apply_func(other, '__pow__')

    def __and__(self, other):
        return self.__apply_func(other, '__and__')

    def __or__(self, other):
        return self.__apply_func(other, '__or__')

    def __xor__(self, other):
        return self.__apply_func(other, '__xor__')

    def __invert__(self):
        s = ~self.samples
        time = self.timestamps
        return Signal(s, time, self.unit, self.name, self.conversion)

    def __lshift__(self, other):
        return self.__apply_func(other, '__lshift__')

    def __rshift__(self, other):
        return self.__apply_func(other, '__rshift__')

    def __lt__(self, other):
        return self.__apply_func(other, '__lt__')

    def __le__(self, other):
        return self.__apply_func(other, '__le__')

    def __gt__(self, other):
        return self.__apply_func(other, '__gt__')

    def __ge__(self, other):
        return self.__apply_func(other, '__ge__')

    def __eq__(self, other):
        return self.__apply_func(other, '__eq__')

    def __ne__(self, other):
        return self.__apply_func(other, '__ne__')

    def __iter__(self):
        return zip(self.samples, self.timestamps)

    def __reversed__(self):
        return enumerate(zip(reversed(self.samples), reversed(self.timestamps)))

    def __len__(self):
        return len(self.samples)

    def __abs__(self):
        return Signal(np.fabs(self.samples), self.timestamps, self.unit, self.name, self.conversion)

    def __getitem__(self, val):
        return self.samples[val]

    def __setitem__(self, idx, val):
        self.samples[idx] = val

    def astype(self, np_type):
        """ returns new *Signal* with samples of dtype *np_type*"""
        return Signal(self.samples.astype(np_type), self.timestamps, self.unit, self.name, self.conversion)


if __name__ == '__main__':
    pass
