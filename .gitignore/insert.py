import pg8000
from config import load_config

def insert_username(username):
    """ Insert a new username into the TFTGraphs table """

    sql = """INSERT INTO TFTGraphs(username)
             VALUES(%s) RETURNING user_id;"""
    
    user_id = None
    config = load_config()

    try:
        conn = pg8000.connect(**config)
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (username,))
        # get the generated id back                
        rows = cur.fetchone()
        if rows:
            user_id = rows[0]
        # commit the changes to the database
        conn.commit()
        cur.close()
        conn.close()
    except (Exception, pg8000.dbapi.ProgrammingError) as error:
        print(error)
    
    return user_id

if __name__ == '__main__':
    user_id = insert_username("ren#icant")
    print(f"Inserted user ID: {user_id}")
