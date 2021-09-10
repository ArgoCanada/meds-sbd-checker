
import unittest

import argopandas as argo
from checker import util

class TestUtil(unittest.TestCase):

    def test_index(self):

        wmo_list = [4902480, 4902481]
        ix = argo.prof[[argo.prof['file'].str.contains(str(wmo)) for wmo in wmo_list]]

        ix = util.last_profiles(ix)
        ix = util.next_profiles(ix, 245)
        ix = util.expected_profiles(ix)

        print(ix)

    def test_sbd(self):

        sbd_files = util.fetch_sbd()


if __name__ == '__main__':
    unittest.main()