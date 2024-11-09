#!/usr/bin/env python3
"""
Personal Data Module Tasks
"""
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the RedactingFormatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message obfuscated:

    Args:
        fields: a list of strings representing all fields
        to obfuscate

        redaction: a string representing by what the field
        will be obfuscated

        message: a string representing the log line

        separator: a string representing by which character is
        separating all fields in the log line (message)
    """
    for field in fields:
        pattern = rf'(?<={field}=)[^{separator}]+'
        message = re.sub(pattern, redaction, message)

    return message


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    streamHandler.setFormatter(formatter)

    logger.addHandler(streamHandler)

    return logger


def get_db() -> mysql.connector.connection.MYSQLConnection:
    """ Connection to MySQL environment """
    db_connect = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connect
