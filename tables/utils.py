from django.db import connection, models
from django.core.management import call_command


def check_table_exists(table_name):
    table_names = connection.introspection.table_names()
    return table_name in table_names


def verify_and_get_field_type(field_type):
    if field_type == 'string':
        field = models.CharField(max_length=255)
    elif field_type == 'number':
        field = models.IntegerField()
    elif field_type == 'boolean':
        field = models.BooleanField(default=False)
    else:
        raise ValueError(f"Unsupported field type: {field_type}")

    return field


def create_dynamic_table_migration(app_label, table_name):
    args = [app_label]
    options = {'name': f'create_dynamic_table_{table_name}', 'no_input': True}

    call_command('makemigrations', *args, **options)
