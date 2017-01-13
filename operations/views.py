from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers
'''
class ListEmployee(APIView):
    def get(self, request, format=None):
        employees = models.Employee.objects.all()
        serializer = serializers.EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
'';
