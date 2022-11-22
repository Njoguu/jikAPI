try:
    from backend import database
    import unittest
except Exception as err:
    print(f"Some modules are missing! {err}")


class DBConnectionTestCases(unittest.TestCase):
    def test_data_source_available(self):
        pass
    
    def test_db_connection(self):
        pass

    def test_data_is_inserted(self):
        pass

    def test_table_is_truncated(self):
        pass

if __name__ == '__main__':
    unittest.main()
