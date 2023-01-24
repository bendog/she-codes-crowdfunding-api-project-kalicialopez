from rest_framework.serializers import ModelSerializer

from .models import Project, Pledge

from users.serializers import CustomUserSerializer


class PledgeSerializer(ModelSerializer):
    class Meta:
        model = Pledge
        fields = ['id', 'amount', 'comment', 'anonymous', 'project', 'supporter']
        read_only_fields = ['id', 'supporter']

class ProjectSerializer(ModelSerializer):
    class Meta:
        id = ModelSerializer.ReadOnlyField()
        title = ModelSerializer.CharField(max_length=200)
        description = ModelSerializer.CharField(max_length=None)
        goal = ModelSerializer.IntegerField()
        image = ModelSerializer.URLField()
        is_open = ModelSerializer.BooleanField()
        date_created = ModelSerializer.DateTimeField()
        owner = ModelSerializer.ReadOnlyField(source='owner_id')
        total = ModelSerializer.ReadOnlyField()

        def create(self, validated_data):
            return Project.objects.create(**validated_data)
    
        def update(self, instance, validated_data):
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('description', instance.description)
            instance.goal = validated_data.get('goal', instance.goal)
            instance.image = validated_data.get('image', instance.image)
            instance.is_open = validated_data.get('is_open', instance.is_open)
            instance.data_created = validated_data.get('date_created', instance.date_created)
            instance.owner = validated_data.get('owner', instance.owner)
            instance.save()
            return instance

class ProjectDetailSerializer(ProjectSerializer):
        pledges = PledgeSerializer(many=True, read_only=True)

        liked_by = CustomUserSerializer(many=True, read_only=True)



