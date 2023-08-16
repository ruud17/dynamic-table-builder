from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.core.management import call_command
from django.db import connection
from django.apps import apps
from .models import create_dynamic_model
from .serializers import DynamicTableModelSerializer, GeneralSerializer
from .utils import check_table_exists


class CreateDynamicTableModel(APIView):
    def post(self, request, format=None):
        serializer = DynamicTableModelSerializer(data=request.data)

        if serializer.is_valid():
            table_name = serializer.validated_data['table_name'].lower()
            fields = serializer.validated_data['fields']

            if check_table_exists(table_name):
                return Response({"error": "Table already exists."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                model_class = create_dynamic_model(table_name, fields)
                app_label = model_class._meta.app_label

                # Create the database table using SchemaEditor
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(model_class)

                # Prepare the arguments and options for the call_command function
                args = [app_label]
                options = {'name': f'create_dynamic_table_{table_name}', 'no_input': True}
                # Call the makemigrations command with the provided arguments and options
                call_command('makemigrations', *args, **options)

                return Response({"message": f"Table {table_name.lower()} generated successfully."},
                                status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllRows(ModelViewSet):
    @property
    def model(self):
        return apps.get_model(app_label=str('tables'), model_name=str(self.kwargs['id']), require_ready=False)

    def get_queryset(self):
        model = self.model
        return model.objects.all()

    def get_serializer_class(self):
        GeneralSerializer.Meta.model = self.model
        return GeneralSerializer


