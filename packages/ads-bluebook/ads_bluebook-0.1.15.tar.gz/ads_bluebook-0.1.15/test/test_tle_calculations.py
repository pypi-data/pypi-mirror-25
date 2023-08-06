# Note: Python uses the __name__ for relative imports. The name will be
# whatever you entered on the command line to run the module. If you run
# as a script, the name will be "main".
#print (__name__)

# IMORTANT FOR RUNNING TESTS!!!
# To run tests, go to the bluebook/bluebook directory and use this command: python -m unittest -v test.test_tle_calculations
# If you don't do it this way, the relative import will not work correctly
import unittest
#import src.calculations.tle as cp
from bluebook import tle as cp

class TestComputedProperties(unittest.TestCase):
    # Examples
    def test_upper(self):
        """ this is a doc string..."""
        self.assertEqual("foo".upper(), "FOO")
    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    
    # Real tests based on 39508
    def test_u_constant(self):
        self.assertAlmostEqual(cp.U, 398600441800000)
    def test_earth_radius_constant(self):
        self.assertAlmostEqual(cp.EARTHS_RADIUS_IN_KELOMETERS, 6378.137)
    def test_get_period(self):
        mean_motion = 1.00272074
        period_in_minutes = cp.get_period_in_minutes(mean_motion)
        self.assertAlmostEqual(period_in_minutes, 1436.09276497)
    def test_get_semi_major_axis(self):
        period_in_minutes = 1436.09276497
        semi_major_axis_in_kilometers = cp.get_semi_major_axis_in_kilometers(period_in_minutes)
        self.assertAlmostEqual(semi_major_axis_in_kilometers, 42164.65094419)
    def test_get_apogee_radius(self):
        semi_major_axis_in_kilometers = 42164.65094419
        eccentricity = 0.0003024
        apogee_radius_in_kilometers = cp.get_apogee_radius_in_kilometers(semi_major_axis_in_kilometers, eccentricity)
        self.assertAlmostEqual(apogee_radius_in_kilometers, 42177.40153464)
    def test_get_perigee_radius(self):
        semi_major_axis_in_kilometers = 42164.65094419
        eccentricity = 0.0003024
        perigee_radius_in_kilometers = cp.get_perigee_radius_in_kilometers(semi_major_axis_in_kilometers, eccentricity)
        self.assertAlmostEqual(perigee_radius_in_kilometers, 42151.90035374)
    def test_get_perigee_altitude(self):
        semi_major_axis_in_kilometers = 42164.65094419
        eccentricity = 0.0003024
        perigee_altitude = cp.get_perigee_altitude_in_kelometers(semi_major_axis_in_kilometers, eccentricity)
        self.assertAlmostEqual(perigee_altitude, 35773.76335374)
    def test_get_apogee_altitude(self):
        semi_major_axis_in_kilometers = 42164.65094419
        eccentricity = 0.0003024
        apogee_altitude = cp.get_apogee_altitude_in_kelometers(semi_major_axis_in_kilometers, eccentricity)
        self.assertAlmostEqual(apogee_altitude, 35799.26453464)
# Not sure what the point of this is if you run tests as modules?
#if __name__ == "__main__":
#    unittest.main()