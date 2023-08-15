from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection, models
from .models import create_dynamic_model
from .serializers import DynamicTableModelSerializer

class DynamicTableGenerationView(APIView):
    def post(self, request, format=None):
        serializer = DynamicTableModelSerializer(data=request.data)

        if serializer.is_valid():
            table_name = serializer.validated_data['table_name']
            fields = serializer.validated_data['fields']

            try:
                model_class = create_dynamic_model(table_name, fields)

                # Create the database table using SchemaEditor
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(model_class)

                return Response({"message": f"Table {table_name} generated successfully."}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

