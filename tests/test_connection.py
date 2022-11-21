try:
    import sys
    sys.path.insert(0, '/media/njoguu/New Volume/Projects/Web Projects/jik-api-v2.0-Alpha/src')
    from backend import *
    import unittest
except Exception as err:
    print(f"Some modules are missing! {err}")


class TestCases(unittest.TestCase):
    # Check connection to index page
    def test_index_connection(self):
        app= create_app()
        tester = app.test_client(self)
        response = tester.get('/').status_code
        self.assertEqual(response, 200)

    # # check API connection
    # def test_status(self):
    #     app= create_app()
    #     tester = app.test_client(self)
    #     response = tester.get('/api/v1/jobs').status_code
    #     self.assertEqual(response, 200)

    # # check content is JSON
    # def test_API_contentType(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/api/v1/jobs')
    #     self.assertEqual(response.content_type, "application/json")

    # # check data returned
    # def test_API_data(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/api/v1/jobs')
    #     self.assertTrue(b'Title' in response.data)



if __name__ == '__main__':
    unittest.main()