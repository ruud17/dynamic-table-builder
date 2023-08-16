from django.db import models, migrations, connection
from django.apps import apps
from django.core.management import call_command

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
            field = models.BooleanField(default=False)
        else:
            raise ValueError(f"Unsupported field type: {field_type}")

        attrs[field_name] = field

    model_class = type(table_name, (models.Model,), attrs)

    # Register the dynamic model with the app label
    apps.register_model(app_label='tables', model=model_class)
    # apps.all_models[app_label][model_name] = dynamic_model

    return model_class



def update_dynamic_model(model_name, new_fields):
    # get model
    app_label = "tables"
    model = apps.get_model(app_label, model_name)

    existing_field_names = [field.name for field in model._meta.get_fields()]

    for field_name, field_type in new_fields.items():
        if field_type == 'string':
            field = models.CharField(max_length=255)
        elif field_type == 'number':
            field = models.IntegerField()
        elif field_type == 'boolean':
            field = models.BooleanField()
        else:
            raise ValueError(f"Unsupported field type: {field_type}")

        with connection.schema_editor() as schema_editor:
            if field_name in existing_field_names:
                old_field = model._meta.get_field(field_name)
                schema_editor.remove_field(model, old_field)

            model.add_to_class(field_name, field)
            new_field = model._meta.get_field(field_name)
            schema_editor.add_field(model, new_field)
