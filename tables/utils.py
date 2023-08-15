from django.db import connection


def check_table_exists(table_name):
    table_names = connection.introspection.table_names()
    return table_name in table_names
