#!/usr/bin/env python3
"""Regex-ing"""

import re
from typing import List
import logging
import mysql.connector
import os
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str] = PII_FIELDS):
        """init method"""
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format method"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.+?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter())
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    connector = mysql.connector.connect(
        user=os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.environ.get('PERSONAL_DATA_DB_NAME'))
    return connector


def main():
    """takes no arguments and returns nothing"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        message = f"name={row[0]}; " + \
                  f"email={row[1]}; " + \
                  f"phone={row[2]}; " + \
                  f"ssn={row[3]}; " + \
                  f"password={row[4]}; " + \
                  f"ip={row[5]}; " + \
                  f"last_login={row[6]}; " + \
                  f"user_agent={row[7]};"
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
