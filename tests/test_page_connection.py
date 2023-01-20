try:
    import sys
    sys.path.insert(0, '/media/njoguu/New Volume/Projects/Web Projects/jik-api-v2.0-Alpha/src')
    from backend import *
    import unittest
except Exception as err:
    print(f"Some modules are missing! {err}")


class PageConnectionTestCases(unittest.TestCase):
    # Check connection to index page
    def test_index_connection(self):
        app = create_app()
        tester = app.test_client(self)  # type: ignore
        response = tester.get('/').status_code
        self.assertEqual(response, 200)

    # Check connection to versions page
    def test_api_page(self):
        app = create_app()
        tester = app.test_client(self)   # type: ignore
        response = tester.get('/api/v2/').status_code
        self.assertEqual(response, 200)

    # Check connection to api page
    # def test_api_page(self):
    #     app = create_app()
    #     tester = app.test_client(self)
    #     response = tester.get('/api/v1/jobs').status_code
    #     self.assertEqual(response, 200)

if __name__ == '__main__':
    unittest.main()
