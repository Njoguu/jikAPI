try:
    import sys
    sys.path.insert(0, '/media/njoguu/New Volume/Projects/Web Projects/jik-api-v2.0-Alpha/src')
    from backend import *
    import unittest
except Exception as err:
    print(f"Some modules are missing! {err}")


class DBConnectionTestCases(unittest.TestCase):
    
    pass


if __name__ == '__main__':
    unittest.main()
