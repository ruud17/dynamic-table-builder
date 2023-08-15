from rest_framework import serializers


class DynamicTableModelSerializer(serializers.Serializer):
    table_name = serializers.CharField(max_length=100)
    fields = serializers.DictField()
