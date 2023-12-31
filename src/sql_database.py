"""
SQL Database Interaction Module
-------------------------------

This module provides functionalities for interaction with a MySQL database,
including schema creation and basic CRUD operations through various functions
and context managers.

Usage:
    Make sure that there is a MySQL-Server running at local host.

:Modul: sql_database
:Author: Benjamin Gaube
:Date: 2023-10-12
"""

from time import sleep
from contextlib import contextmanager

import mysql.connector

schema = 'application_project_gaube'


@contextmanager
def connect_to_localhost(database=None):
    """
    Establish and manage a connection to a MySQL database on localhost.

    :param database: str, Optional. The name of the database to connect to.
                     Default is None.
    :yield: MySQLConnection, The database connection object.
    :raise mysql.connector.Error: If unable to establish connection after 5 retries.
    """
    db = None
    try:
        try:
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database=database
            )
        except mysql.connector.Error:
            tries = 0
            while True:
                if tries > 5:
                    raise mysql.connector.Error('Could not connect to database')
                sleep(60)
                try:
                    db = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        password='',
                        database=database
                    )
                    break

                except mysql.connector.Error:
                    tries += 1

        yield db  # The connection is used here

    finally:
        if db is not None:
            db.close()


def create_schema(schema_name: str):
    """
    Creates a database schema if it does not exist, with optional deletion of existing schema.

    Connects to a local database, checks if a schema by the provided name already exists,
    and if so, prompts the user to either delete or retain it. If the user opts for deletion,
    the existing schema is dropped. Subsequently or if the schema didn't exist in the first place,
    the function creates a new schema and sets up a basic table structure within it.

    :param schema_name: str, The name of the schema to be created in the database.
    """

    with connect_to_localhost() as db:

        cursor = db.cursor()
        cursor.execute(f'SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = "{schema}"')

        if cursor.fetchone():
            print(f'Schema {schema} already exists.')
            while True:
                user_input = input('Do you want to delete it? (y/n): ')

                if user_input.lower() == 'y':
                    cursor.execute(f"DROP DATABASE {schema}")
                    print(f"Schema {schema} deleted successfully.")
                    break
                elif user_input.lower() == 'n':
                    return

                else:
                    print('invalid input..')

        cursor.execute(f'CREATE DATABASE {schema_name}')
        cursor.execute(f'USE {schema_name}')

        cursor.execute('''
        CREATE TABLE dataset (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student VARCHAR(5) UNIQUE
        )
        ''')

        cursor.execute('''
        CREATE TABLE exam (
            id INT AUTO_INCREMENT PRIMARY KEY,
            term VARCHAR(10)
        )    
        ''')

        cursor.execute('''
        CREATE TABLE hrv (
            id INT AUTO_INCREMENT PRIMARY KEY,
            parameter VARCHAR(15)
        )
        ''')

        cursor.execute('''
        CREATE TABLE inter_beat_interval (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT, 
            term_id INT,
            ibi_value_id INT,
            ibi_value INT,
            timestamp INT,
            FOREIGN KEY (student_id) REFERENCES dataset(id) ON DELETE CASCADE,
            FOREIGN KEY (term_id) REFERENCES exam(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE master_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            term_id INT,
            grade INT,
            nni_mean FLOAT,
            sdnn FLOAT,
            number_of_ibi INT,
            duration_in_h FLOAT,
            FOREIGN KEY (student_id) REFERENCES dataset(id) ON DELETE CASCADE,
            FOREIGN KEY (term_id) REFERENCES exam(id)                    
        )
        ''')

        cursor.execute('''
        CREATE TABLE window_values (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            term_id INT,
            window_id INT,
            timestamp INT,
            parameter_id INT,
            hrv_value FLOAT,
            number_of_ibi INT,
            FOREIGN KEY (student_id) REFERENCES dataset(id) ON DELETE CASCADE,
            FOREIGN KEY (term_id) REFERENCES exam(id),
            FOREIGN KEY (parameter_id) REFERENCES hrv(id)
        )
        ''')

        for term_type in ['mid1', 'mid2', 'final']:
            cursor.execute('INSERT INTO exam (term) VALUES (%s)', (term_type,))

        for parameter_type in ['nni_mean', 'sdnn']:
            cursor.execute('INSERT INTO hrv (parameter) VALUES (%s)', (parameter_type,))

        db.commit()


if __name__ == '__main__':
    create_schema(schema)
