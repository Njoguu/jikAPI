import pytest
import sys
import os
path = os.getcwd()
sys.path.append(path+"/src/")
from backend import database as dbcons


# test a connection to PostgreSQL jikAPI database
def test_db_connection():
    try:
        conn = dbcons.getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        assert cursor.fetchone() == (1,)
    except Exception as e:
        pytest.fail(f"Failed to connect to the database: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    pytest.main()
