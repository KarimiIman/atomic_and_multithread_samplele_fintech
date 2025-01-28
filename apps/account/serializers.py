from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=256, required=True, )
    password = serializers.CharField(max_length=512, required=True, )

