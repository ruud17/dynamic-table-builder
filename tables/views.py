from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.db import connection
from django.apps import apps
from .apps import TablesConfig
from .models import create_dynamic_model, update_dynamic_model
from .serializers import DynamicCreateTableModelSerializer, DynamicUpdateTableModelSerializer, GeneralSerializer
from .utils import check_table_exists, create_dynamic_table_migration


class CreateDynamicTableModel(APIView):
    def post(self, request):
        serializer = DynamicCreateTableModelSerializer(data=request.data)

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

                create_dynamic_table_migration(app_label, table_name)  # generate migration

                return Response({"message": f"Table {table_name.lower()} generated successfully."},
                                status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateDynamicTableModel(APIView):
    def put(self, request, id):
        serializer = DynamicUpdateTableModelSerializer(data=request.data)
        table_name = id

        if serializer.is_valid():
            fields = serializer.validated_data['fields']

            if not check_table_exists(table_name):
                return Response({"error": "Table does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                update_dynamic_model(table_name, fields)

                return Response({"message": f"Table {id.lower()} updated successfully."},
                                status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllRows(ModelViewSet):
    @property
    def model(self):
        return apps.get_model(app_label=TablesConfig.name, model_name=str(self.kwargs['id']), require_ready=False)

    def get_queryset(self):
        model = self.model
        return model.objects.all()

    def get_serializer_class(self):
        GeneralSerializer.Meta.model = self.model
        return GeneralSerializer


