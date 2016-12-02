from rest_framework import serializers
from . import models

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'first_name': {'write_only': True}
        }
        fields = (
            'first_name',
            'last_name',
            'start_date',
            'end_date',
        )
        model = models.Employee
