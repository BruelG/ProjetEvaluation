
import snowflake.connector

def create_snowflake_connection():
    conn = snowflake.connector.connect(
        user='HOUSSAM',  
        password='Houssamito09500',  
        account='mmlxsql-vq52188',  
        warehouse='COMPUTE_WH',  
        database='DB_USERS',  
        schema='PUBLIC'  
    )
    return conn

