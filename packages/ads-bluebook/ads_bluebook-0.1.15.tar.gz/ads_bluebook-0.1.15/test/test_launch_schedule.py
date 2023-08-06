import unittest
from bluebook import 
# To run tests, go to the bluebook/bluebook directory and use this command: 
# python -m unittest -v test.test_launch_schedule
# The above will run the unittest module with the "-v test.test_launch_schedule" as the argument.
# When this file is actually being executed, __name__ will be that argument "test.test_launch_schedule"
# So really the cwd is where your imports are relative to.

class TestLaunchSchedule(unittest.TestCase):
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
    
    def test_test(self):
        print("hi")
        print("here")
        print(__name__)
        #test.my_test()

# Not sure what the point of this is if you run tests as modules?
if __name__ == "__main__":
    unittest.main()