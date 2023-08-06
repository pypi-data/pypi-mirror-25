'''This module contains the basic stream interfaces unit tests'''

from unittest import TestCase
from ....streams.streams import IStream, OStream

MOCK_DATA = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'

class IStreamImpl(IStream):
    '''IStream testing implementation'''
    def __init__(self):
        IStream.__init__(self)
        self.__data = MOCK_DATA

    def _read(self, size):
        result = None
        if self._closed is not True:
            if size < 0:
                result = self.__data
            else:
                result = self.__data[:size]
            self._closed = True
        return result

class IStreamTest(TestCase):
    '''IStream unit test'''
    def setUp(self):
        self.__istream = IStreamImpl()

    def test_read_all__data(self):
        '''When read is called without size, all data should be read.'''
        self.assertFalse(self.__istream.closed)
        result = self.__istream.read()
        self.assertIsNotNone(result)
        self.assertEqual(result, MOCK_DATA)

        self.assertTrue(self.__istream.closed)
        result = self.__istream.read()
        self.assertIsNone(result)

    def test_read_one__data(self):
        '''When read is called with size, the selected size of data should be read.'''
        size = 10
        self.assertFalse(self.__istream.closed)
        result = self.__istream.read(size)
        self.assertIsNotNone(result)
        self.assertEqual(result, MOCK_DATA[:size])

class OStreamImpl(OStream):
    '''OStream testing implementation'''
    def __init__(self):
        OStream.__init__(self)
        self.saved = None
        self.closed = False

    def _write(self, data):
        self.saved = data

    def _close(self):
        self.closed = True

class OStreamTest(TestCase):
    '''OStream unit test'''
    def setUp(self):
        self.__ostream = OStreamImpl()

    def test_write(self):
        '''When write is called, all passed _data should be written'''
        self.__ostream.write(MOCK_DATA)
        self.assertEqual(self.__ostream.saved, MOCK_DATA)

    def test_close(self):
        '''When close is called, close sequence should be executed'''
        self.assertFalse(self.__ostream.closed)
        self.__ostream.close()
        self.assertTrue(self.__ostream.closed)
