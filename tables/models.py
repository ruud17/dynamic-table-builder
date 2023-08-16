from django.db import models, connection
from django.apps import apps
from .utils import verify_and_get_field_type
from .apps import TablesConfig

app_label = TablesConfig.name


def create_dynamic_model(table_name, fields):
    class Meta:
        db_table = table_name.lower()  # Set the lowercase table name

    attrs = {'__module__': __name__, 'Meta': Meta}

    for field_name, field_type in fields.items():
        field = verify_and_get_field_type(field_type)
        attrs[field_name] = field

    model_class = type(table_name, (models.Model,), attrs)  # generate dynamic model

    apps.register_model(app_label, model=model_class)  # Register the dynamic model

    return model_class


def update_dynamic_model(model_name, new_fields):
    model = apps.get_model(app_label, model_name)  # get model

    existing_field_names = [field.name for field in model._meta.get_fields()]

    for field_name, field_type in new_fields.items():
        field = verify_and_get_field_type(field_type)

        with connection.schema_editor() as schema_editor:
            if field_name in existing_field_names:
                old_field = model._meta.get_field(field_name)
                schema_editor.remove_field(model, old_field)  # remove existing field we want to update

            model.add_to_class(field_name, field)
            new_field = model._meta.get_field(field_name)
            schema_editor.add_field(model, new_field)  # add a field with a new type
