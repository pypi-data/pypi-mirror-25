__author__ = 'sneurlax'

from tuxexchange import Tuxexchange
import unittest


def test_basic_response(unit_test, result, method_name):
  if 'success' in result:
    unit_test.assertTrue(result['success'] is 0, 'success is 0')
  if 'error' in result:
    unit_test.assertTrue(result['error'] is None, 'error is present in response')


class TestTuxexchangePublicAPI(unittest.TestCase):
  '''
  Integration tests for the Tux Exchange public API.
  These will fail in the absence of an internet connection or if the Tux Exchange API goes down
  '''
  def setUp(self):
    self.tuxexchange = Tuxexchange()

  def test_get_ticker(self):
    actual = self.tuxexchange.api_query('getticker')
    test_basic_response(self, actual, 'getticker')
    pass

  def test_get_coins(self):
    actual = self.tuxexchange.api_query('getcoins')
    test_basic_response(self, actual, 'getcoins')
    pass


if __name__ == '__main__':
  unittest.main()
