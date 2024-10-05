import psycopg2
from config import load_config

def connect():
    connection = None
    params = load_config()
    try:
        # Establish connection using parameters from the config
        connection = psycopg2.connect(**params)
        
        with connection.cursor() as curs:

            try:
                # 1. Create a new schema (table) if it doesn't already exist
                create_table_query = '''
                CREATE TABLE IF NOT EXISTS test_schema (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    age INT NOT NULL
                )
                '''
                curs.execute(create_table_query)
                print("Table created successfully.")

                # 2. Insert a value into the table
                insert_query = '''
                INSERT INTO test_schema (name, age)
                VALUES (%s, %s) RETURNING id
                '''
                curs.execute(insert_query, ('John Doe', 30))
                new_id = curs.fetchone()[0]
                print(f"Inserted value with id: {new_id}")

                # Commit the changes after insertion
                connection.commit()

                # 3. Update the value (change 'age' for the inserted record)
                update_query = '''
                UPDATE test_schema
                SET age = %s
                WHERE id = %s
                '''
                curs.execute(update_query, (35, new_id))
                connection.commit()
                print(f"Updated value with id: {new_id}")

                # 4. Retrieve and print the updated value
                select_query = '''
                SELECT id, name, age FROM test_schema WHERE id = %s
                '''
                curs.execute(select_query, (new_id,))
                row = curs.fetchone()

                print(f"Retrieved record: ID = {row[0]}, Name = {row[1]}, Age = {row[2]}")

            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Error: {error}")

    except Exception as error:
        print(f"Unable to connect to the database: {error}")

    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')

if __name__ == "__main__":
    connect()
