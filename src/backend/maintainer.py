'''
Maintainer: Deletes records older than 10 days;
'''

import os
from dotenv import load_dotenv
from database import getConnection

load_dotenv()

def delete_jobs(tableName):
    conn = getConnection()
    cur = conn.cursor()
    cur.execute(f'''
        DELETE FROM {tableName} WHERE TO_DATE(dayofjobpost || TO_CHAR(CURRENT_DATE, 'YYYY'), 'DD MONTH YYYY') < (current_timestamp - interval '10 days');
    ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    tableName = os.getenv('TABLENAME')
    delete_jobs(tableName)
