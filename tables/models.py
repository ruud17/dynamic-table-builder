from django.db import models

"""
{
    "table_name": "DynamicTable",
    "fields": {
        "name": "string",
        "age": "number",
        "is_active": "boolean"
    }
}
"""


def create_dynamic_model(table_name, fields):
    class Meta:
        db_table = table_name.lower()  # Set the lowercase table name

    attrs = {'__module__': __name__, 'Meta': Meta}

    for field_name, field_type in fields.items():
        if field_type == 'string':
            field = models.CharField(max_length=255)
        elif field_type == 'number':
            field = models.IntegerField()
        elif field_type == 'boolean':
            field = models.BooleanField()
        else:
            raise ValueError(f"Unsupported field type: {field_type}")

        attrs[field_name] = field

    model_class = type(table_name, (models.Model,), attrs)

    return model_class
