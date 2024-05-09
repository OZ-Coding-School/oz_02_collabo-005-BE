from rest_framework import serializers
from .models import Menu

class MenuStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "name", "status"]