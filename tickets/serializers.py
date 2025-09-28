from rest_framework import serializers
from .models import Guest,Movie,Reservation,Post


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields='__all__'
        
    
class ReservationSerializers(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields='__all__'
        
        
class GusetSerializers(serializers.ModelSerializer):
    class Meta:
        model=Guest
        fields=['pk','reservation','name','mobile']
        
        
        
#uuid /  slug

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'