#!/usr/bin/env python3
"""
Regex-ing
"""
import re


def filter_datum(fields, redaction, message, separator):
    """Returns the log message obfuscated:"""
    for field in fields:
        message = re.sub(rf'(?<={field}=)[^{separator}]+', redaction, message)
    return message
