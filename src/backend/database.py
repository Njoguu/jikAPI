# Import Necessary modules
import psycopg2
import configparser
import logging
import datetime 

# Function to get a database connection
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

# Function to insert data into the database
def insertData(job, tableName):
    conn = getConnection()
    cur = conn.cursor()

    try:
        ## Check to see if item is already in database 
        cur.execute(f"select * from {tableName} where jobURL = %s", (job[1],))
        result = cur.fetchone()

        if result:
            logging.warning("Posting already exists in Database")
        else:
            cur.execute(f'''
                insert into {tableName}(jobName, jobURL, dayOfJobPost)
                values('{job[0]}','{job[1]}','{job[2]}')
            ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as err:
        print(f"Error! Program is not working as expected! {err}")

# Function to get data from the database
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

# Function to get data from the database using a specific keyword
def get_specific_job(keywords, tableName):
    conn = getConnection()
    cur = conn.cursor()
   
    getSpecificSQL = f'''
    SELECT array_to_json(array_agg(row_to_json(postedjobs)))
    FROM (SELECT id, jobname, joburl, TO_DATE(dayofjobpost || TO_CHAR(CURRENT_DATE, 'YYYY'), 'DD MONTH YYYY') AS dateofjobpost FROM {tableName} ORDER BY dateofjobpost DESC) postedjobs
    WHERE jobname LIKE '%{keywords}%'
    '''
    
    try:
        cur.execute(getSpecificSQL)
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data
    except Exception as err:
        print(f"Error! Program is not working as expected! {err}")

# Function to get data from the database posted on a specific date
def get_job_of_specific_date(specified_dates, tableName):
    conn = getConnection()
    cur = conn.cursor()

    getSpecificDateSQL = f'''
    SELECT array_to_json(array_agg(row_to_json(postedjobs)))
    FROM (SELECT id, jobname, joburl, TO_DATE(dayofjobpost || TO_CHAR(CURRENT_DATE, 'YYYY'), 'DD MONTH YYYY') AS dateofjobpost FROM {tableName} ORDER BY dateofjobpost DESC) postedjobs
    WHERE dateofjobpost = '{specified_dates}'
    
    '''

    try:
        cur.execute(getSpecificDateSQL)
        data = cur.fetchall()
        conn.commit()
        conn.close()
        return data
    except Exception as err:
        print(f"Error! Program is not working as expected! {err}")

# Function to UPDATE data in the database 
def updateData(jobname, joburl,id, tableName):
    conn = getConnection()
    cur = conn.cursor()

    try:     
        cur.execute(f'''
        UPDATE {tableName}
        SET jobname = %s, joburl = %s
        WHERE id = %s
        ''', (jobname, joburl, id)
    )
    
        # Commit the changes to the database
        conn.commit()
        
        # Close the cursor and connection
        cur.close()
        conn.close()
    except Exception as err:
        print(f"Error! Program is not working as expected! {err}")

# Function to POST new data in the database 
def addData(job, tableName):
    conn = getConnection()
    cur = conn.cursor()

    try:
        # Clear the existing data in the table
        # cur.execute("DELETE FROM {}".format(tableName))

        current_date = datetime.datetime.today().strftime('%Y-%m-%d')        
        date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        new_format = date.strftime('%d %B')

        # Check to see if item is already in database 
        cur.execute(f"select * from {tableName} where joburl = %s", (job['joburl'],))
        result = cur.fetchone()

        if result:
            logging.warning("Posting already exists in Database")
        else:
            cur.execute(f'''
                insert into {tableName}(jobname, joburl, dayofjobpost)
                values('{job['jobname']}','{job['joburl']}','{new_format}')
            ''')
    
        # Commit the changes to the database
        conn.commit()
        
        # Close the cursor and connection
        cur.close()
        conn.close()
    except Exception as err:
        print(f"Error! Program is not working as expected! {err}")

# Function to DELETE data from the database 
def deleteData(id, tableName):
    conn = getConnection()
    cur = conn.cursor()

    try:     
        cur.execute(f'''
        DELETE FROM {tableName}
        WHERE id = %s
        ''', ([id])
    )
    
        # Commit the changes to the database
        conn.commit()
        
        # Close the cursor and connection
        cur.close()
        conn.close()
    except Exception as err:
        print(f"Error! Program is not working as expected! {err}")