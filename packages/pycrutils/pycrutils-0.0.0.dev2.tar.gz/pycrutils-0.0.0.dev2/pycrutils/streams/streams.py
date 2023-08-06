'''This module contains the basic stream interfaces'''

class Stream:
    '''Interface for general data streams'''
    pass

class IStream(Stream):
    '''Interface for input data streams'''
    def __init__(self):
        self._closed = False

    @property
    def closed(self):
        '''Returns the close status of the stream'''
        return self._closed

    def read(self, size=-1):
        '''Read data from the stream'''
        return self._read(size)

    def _read(self, size):
        raise NotImplementedError

class OStream(Stream):
    '''Interface for output data streams'''
    def write(self, data):
        '''Write data into the stream'''
        self._write(data)

    def close(self):
        '''Close the stream'''
        self._close()

    def _write(self, data):
        raise NotImplementedError

    def _close(self):
        raise NotImplementedError

class IOStream(IStream, OStream):
    '''Interface for input and output streams'''
    def _read(self, size):
        raise NotImplementedError

    def _write(self, data):
        raise NotImplementedError

    def _close(self):
        raise NotImplementedError
