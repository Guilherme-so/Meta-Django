from rest_framework import serializers 
from .models import Rating
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )
    
    class Meta:
        model = Rating
        fields = ['user','menu_item_id','rating']
        
        validators = [
            UniqueTogetherValidator(
                queryset = Rating.objects.all(),
                fields = ['user','menu_item_id']
            )
        ]
        
        extra_kwargs = {
            'rating': {
                'max_value': 5,
                'min_value':0,
                },
        }