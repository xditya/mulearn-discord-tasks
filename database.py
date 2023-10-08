import json
import mysql.connector
from decouple import config

db_host = config("DB_HOST")
db_user = config("DB_USER")
db_password = config("DB_PASSWORD")
db_name = "mydb"


def add_roles_to_db(role_info_list):
    try:
        connection = mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        )
    except mysql.connector.Error as error:
        print(f"Error: {error}")
    # Create a cursor
    cursor = connection.cursor()
    # create db if not exists
    cursor.execute("CREATE DATABASE IF NOT EXISTS mydb")
    connection.commit()

    # create table if not exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS roles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id TEXT,
            role_names JSON
        );
        """
    )
    connection.commit()

    try:
        insert_query = """
        INSERT INTO roles (user_id, role_names)
        VALUES (%s, %s);
        """

        for user_id, role_names in role_info_list:
            # Serialize the list of role names to JSON
            role_names_json = json.dumps(role_names)
            data = (user_id, role_names_json)
            cursor.execute(insert_query, data)

        connection.commit()

        cursor.close()
        connection.close()

        return True
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return False


def get_roles_from_db():
    try:
        connection = mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        )
    except mysql.connector.Error as error:
        print(f"Error: {error}")
    cursor = connection.cursor()
    try:
        select_query = """
        SELECT user_id, role_names FROM roles;
        """

        cursor.execute(select_query)

        role_info_list = []
        for user_id, role_names_json in cursor.fetchall():
            role_names = json.loads(role_names_json)
            role_info_list.append((user_id, role_names))

        cursor.close()
        connection.close()

        return role_info_list
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return []


def delete_all_roles_from_db():
    try:
        connection = mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        )

        cursor = connection.cursor()

        delete_query = """
        DELETE FROM roles;
        """
        cursor.execute(delete_query)
        connection.commit()
        cursor.close()
        connection.close()

        return True
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return False


# TESTS:
# add role:
# role_info_list = [
#     ("abc", ["Role1", "Role2"]),
#     ("def", ["Role3", "Role4", "Role5"]),
#     # Add more role information as needed
# ]

# if add_roles_to_db(role_info_list):
#     print("Roles added to the database successfully.")
# else:
#     print("Failed to add roles to the database.")

# get all roles:
# print(get_roles_from_db())

# delete all data
# delete_all_roles_from_db()
