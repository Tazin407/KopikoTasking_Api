from rest_framework import serializers
from .import models

class Task(serializers.ModelSerializer):
    class Meta:
        model= models.Task
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= models.CustomUser
        fields='__all__'
        

#this is to inherit later     
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class RegistrationSerializer(DynamicFieldsModelSerializer):
    confirm_password= serializers.CharField(required=True)
    class Meta:
        model= models.CustomUser
        fields= ['username', 'first_name','last_name','email', 'password','confirm_password']
        exclude= ['last_login', 'superuser_status']
        
    def validate(self, attrs):
        password= attrs.get('password')
        confirm_password= attrs.get('confirm_password')
        
        if password != confirm_password:
            raise serializers.ValidationError("Passwords don't match")
        
        return attrs
    
    def create(self, validated_data):
        user= models.CustomUser.objects.create_user(**validated_data) #** ta dictionary theke keyword nite help korbe
        user.is_active= False
        user.save()
        return user
    
    
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)