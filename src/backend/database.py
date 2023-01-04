# Import Modules
import psycopg2
import configparser
import src.backend as dbcons

def getConnection():
    config = configparser.ConfigParser()
    config.readfp(open(f'config.ini'))

    DB = config.get('DB', 'database')
    UID = config.get('DB', 'user')
    PWD = config.get('DB', 'password')
    DSN = config.get('DB', 'host')
    PRT = config.get('DB', 'port')

    conn = psycopg2.connect(
        host = DSN,
        database = DB,
        user = UID,
        password = PWD,
        port = PRT,
    )
    
    return conn

def insertData(job, tableName):
    conn = getConnection()
    cur = conn.cursor()

    insertSQL = f'''
        insert into {tableName}(jobName, jobURL, dayOfJobPost)
        values('{job[0]}','{job[1]}','{job[2]}')
    '''

    try:
        cur.execute(insertSQL)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as err:
        print(f"Error! Program is not working as expected! {err}")

def getData(tableName):
    conn = getConnection()
    cur = conn.cursor()

    getSQL = f'''
        SELECT array_to_json(array_agg(row_to_json(posted_jobs)))
        FROM (SELECT id, jobname, joburl, dayofjobpost FROM {tableName}) posted_jobs            
    '''

    try:
        cur.execute(getSQL)
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data
    except Exception as err:
        print(f"Error! Program is not working as expected! {err}")

def get_specific_job(tableName):
    conn = getConnection()
    cur = conn.cursor()

    getSpecificSQL = f'''
    SELECT array_to_json(array_agg(row_to_json(posted_jobs)))
    FROM (SELECT id, jobname, joburl, dayofjobpost FROM {tableName}) posted_jobs
    WHERE jobname LIKE '%{dbcons.keyword}%'
    '''
    
    try:
        cur.execute(getSpecificSQL)
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data
    except Exception as err:
        print(f"Error! Program is not working as expected! {err}")
    
        
def truncateTable(tableName):

    conn = getConnection()
    cur = conn.cursor()

    truncateSQL = f'''
        truncate table {tableName}
    '''

    cur.execute(truncateSQL)
    conn.commit()
    cur.close()
    conn.close()
    