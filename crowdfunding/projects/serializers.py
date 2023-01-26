from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Project, Pledge

from users.serializers import CustomUserSerializer


class PledgeSerializer(serializers.ModelSerializer):
    # For serializer method field
    supporter = serializers.SerializerMethodField()
    
    class Meta:
        model = Pledge
        fields = ['id', 'pledge_amount', 'comment', 'anonymous', 'project', 'supporter']
        read_only_fields = ['id', 'supporter']

    def get_supporter(self, obj):
        if obj.anonymous:
            return None
        else:
            return obj.supporter


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:

        # total = serializers.DecimalField(decimal_places = 2, max_digits = 9)

        model = Project
        fields = ['id', 'title', 'description', 'goal', 'image', 'is_open', 'date_created', 'owner', 'total', 'liked_by', 'pledges']
        read_only_fields = ['id', 'owner', 'date_created', 'total', 'liked_by', 'pledges']
    

        # def create(self, validated_data):
        #     return Project.objects.create(**validated_data)
    
        # def update(self, instance, validated_data):
        #     instance.title = validated_data.get('title', instance.title)
        #     instance.description = validated_data.get('description', instance.description)
        #     instance.goal = validated_data.get('goal', instance.goal)
        #     instance.image = validated_data.get('image', instance.image)
        #     instance.is_open = validated_data.get('is_open', instance.is_open)
        #     instance.data_created = validated_data.get('date_created', instance.date_created)
        #     instance.owner = validated_data.get('owner', instance.owner)
        #     instance.total = validated_data.get('total', instance.total)
        #     instance.liked_by = validated_data.get('liked_by', instance.liked_by)
        #     instance.save()
        #     return instance

class ProjectDetailSerializer(ProjectSerializer):
        pledges = PledgeSerializer(many=True, read_only=True)

        liked_by = CustomUserSerializer(many=True, read_only=True)



