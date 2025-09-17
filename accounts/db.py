# import psycopg2

# def create_database():
#     try:
#         # Connect to default postgres DB
#         conn = psycopg2.connect(
#             dbname="accounts",       # default database
#             user="root",         # your postgres username
#             password="7701717", # your postgres password
#             host="localhost",
#             port="5432"
#         )
#         conn.autocommit = True
#         cursor = conn.cursor()

#         # Name of the new DB
#         db_name = "mynewdb"

#         # Execute CREATE DATABASE only if not exists
#         cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
#         exists = cursor.fetchone()

#         if not exists:
#             cursor.execute(f"CREATE DATABASE {db_name};")
#             print(f"Database '{db_name}' created successfully!")
#         else:
#             print(f"Database '{db_name}' already exists.")

#         cursor.close()
#         conn.close()

#     except Exception as e:
#         print("Error:", e)

# if __name__ == "__main__":
#     create_database()
