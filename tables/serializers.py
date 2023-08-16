from rest_framework import serializers


class DynamicCreateTableModelSerializer(serializers.Serializer):
    table_name = serializers.CharField(max_length=100)
    fields = serializers.DictField()

class DynamicUpdateTableModelSerializer(serializers.Serializer):
    fields = serializers.DictField()

class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'
