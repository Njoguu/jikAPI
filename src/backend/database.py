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
        SELECT array_to_json(array_agg(row_to_json(postedjobs)))
        FROM (SELECT id, jobname, joburl, TO_DATE(dayofjobpost || TO_CHAR(CURRENT_DATE, 'YYYY'), 'DD MONTH YYYY') AS dateofjobpost FROM {tableName} ORDER BY dateofjobpost DESC) postedjobs            
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
    SELECT array_to_json(array_agg(row_to_json(postedjobs)))
    FROM (SELECT id, jobname, joburl, TO_DATE(dayofjobpost || TO_CHAR(CURRENT_DATE, 'YYYY'), 'DD MONTH YYYY') AS dateofjobpost FROM {tableName} ORDER BY dateofjobpost DESC) postedjobs
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

def get_job_of_specific_date(tableName):
    conn = getConnection()
    cur = conn.cursor()

    getSpecificDateSQL = f'''
    SELECT array_to_json(array_agg(row_to_json(postedjobs)))
    FROM (SELECT id, jobname, joburl, TO_DATE(dayofjobpost || TO_CHAR(CURRENT_DATE, 'YYYY'), 'DD MONTH YYYY') AS dateofjobpost FROM {tableName} ORDER BY dateofjobpost DESC) postedjobs
    WHERE dateofjobpost = '{dbcons.specified_date}'
    
    '''

    try:
        cur.execute(getSpecificDateSQL)
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

# def subscribe_user(email, user_group_email, api_key):

#         res = requests.post(f"https://api.mailgun.net/v3/lists/{user_group_email}/members",
#             auth=("api", api_key), data={"subscribed": True, "address": email})

#         return res
