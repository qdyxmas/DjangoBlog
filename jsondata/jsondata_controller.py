from rest_framework import serializers

from jsondata.models import JsonData


class JsonDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonData
        fields = '__all__'
