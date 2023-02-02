# from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import Pledge, Project

User = get_user_model()


class PledgeSerializer(serializers.ModelSerializer):
    # For serializer method field
    supporter = serializers.SerializerMethodField()

    class Meta:
        model = Pledge
        fields = ["id", "pledge_amount", "comment", "anonymous", "project", "supporter"]
        read_only_fields = ["id", "supporter"]

    def get_supporter(self, obj):
        if obj.anonymous:  # i.e. if anonymous = true
            return None
        else:
            return obj.supporter.username

    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        # total = serializers.DecimalField(decimal_places = 2, max_digits = 9)

        model = Project
        fields = [
            "id",
            "title",
            "description",
            "goal",
            "image",
            "is_open",
            "date_created",
            "owner",
            "total",
            "liked_by",
            "pledges",
        ]
        read_only_fields = ["id", "owner", "date_created", "total", "liked_by", "pledges"]

        def create(self, validated_data):
            return Project.objects.create(**validated_data)


class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    liked_by = CustomUserSerializer(many=True, read_only=True)


# class GlobalSearchSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = [
#             "first_name",
#             "last_name",
#             "bio",
#             "country_of_residence",
#             "highest_level_of_education",
#         ]
#
#     def to_internal_value(self, obj):
#         if isinstance(obj, Project):
#             serializer = ProjectSerializer(obj)
#         elif isinstance(obj, CustomUser):
#             serializer = CustomUserSerializer(obj)
#         else:
#             raise Exception("Neither a project nor user instance!")
#         return serializer.data


class MultiObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Project):
            serializer = ProjectSerializer(value)
        elif isinstance(value, User):
            serializer = CustomUserSerializer(value)
        else:
            raise TypeError("Unexpected type of tagged object")
        return serializer.data


class MultiObjectHyperlinkedField(serializers.HyperlinkedRelatedField):
    view_name = ""

    def to_representation(self, value):
        """convert the model item into a hyperlink related field"""
        # This stuff is here to replicate the process that happens in the parent class
        request = self.context["request"]
        format = self.context.get("format")
        if format and self.format and self.format != format:
            format = self.format
        # this is where the actual work happens.
        if isinstance(value, Project):
            field = self.get_url(value, "project-detail", request=request, format=format)
        elif isinstance(value, User):
            field = self.get_url(value, "customuser-detail", request=request, format=format)
        else:
            raise TypeError("Unexpected type of tagged object")
        return field


class GlobalSearchSerializer(serializers.Serializer):
    type = serializers.CharField(read_only=True)
    link = MultiObjectHyperlinkedField(read_only=True, source="item")
    item = MultiObjectRelatedField(read_only=True)

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError
