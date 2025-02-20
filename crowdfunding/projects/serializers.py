# from rest_framework.serializers import ModelSerializer
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
        if obj.anonymous: #i.e. if anonymous = true
            return None
        else:
            return obj.supporter.username
    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:

        # total = serializers.DecimalField(decimal_places = 2, max_digits = 9)

        model = Project
        fields = ['id', 'title', 'description', 'goal', 'image', 'is_open', 'date_created', 'owner', 'total', 'liked_by', 'pledges']
        read_only_fields = ['id', 'owner', 'date_created', 'total', 'liked_by', 'pledges']
    

        def create(self, validated_data):
            return Project.objects.create(**validated_data)
    

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    liked_by = CustomUserSerializer(many=True, read_only=True)



