try:
    import sys
    sys.path.insert(0, '/media/njoguu/New Volume/Projects/Web Projects/jik-api-v2.0-Alpha/src')
    from backend import *
    import unittest
except Exception as err:
    print(f"Some modules are missing! {err}")

class TestMailChimpAPI(unittest.TestCase):
   
    def testConnection(self):
        app = create_app()
        tester = app.test_client(self)  # type: ignore
        response = tester.get('/api/mailchimp/ping').status_code
        self.assertEqual(response, 200)


if __name__ == '__main__':
    unittest.main()
