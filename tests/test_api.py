try:
    
    from backend import *
    import unittest
except Exception as err:
    print(f"Some modules are missing! {err}")

class APIConnectionTestCases(unittest.TestCase):
    
    pass
    # check content is JSON
    # def test_isJSON(self):
    #     app= create_app()
    #     tester = app.test_client(self)  # type: ignore
    #     response = tester.get('/api/v1/jobs')   
    #     self.assertEqual(response.content_type, "application/json")

    # check data returned
    # def test_API_data(self):
    #     app= create_app()
    #     tester = app.test_client(self)  # type: ignore
    #     response = tester.get('/api/v1/jobs')
    #     self.assertTrue(b'Title' in response.data)


if __name__ == '__main__':
    unittest.main()
