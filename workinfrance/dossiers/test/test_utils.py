from django.test import TestCase

from workinfrance.dossiers import utils


class UtilsTest(TestCase):

    def test_json_date_to_python(self):
        d = utils.json_date_to_python('2018-03-27')
        self.assertEqual(d.year, 2018)
        self.assertEqual(d.month, 3)
        self.assertEqual(d.day, 27)

    def test_json_datetime_to_python(self):
        dt = utils.json_datetime_to_python('2018-03-27T08:49:51.491Z')
        self.assertEqual(dt.year, 2018)
        self.assertEqual(dt.month, 3)
        self.assertEqual(dt.day, 27)
        self.assertEqual(dt.hour, 8)
        self.assertEqual(dt.minute, 49)
        self.assertEqual(dt.second, 51)
        self.assertEqual(dt.microsecond, 491000)
        self.assertEqual(str(dt.tzinfo), 'UTC')

    def test_obfuscate(self):
        obfuscated_string = utils.obfuscate(' Emma Louise    ')
        expected_result = '*m** ******'
        self.assertEqual(obfuscated_string, expected_result)
