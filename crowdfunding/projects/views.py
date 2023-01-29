from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status, generics, permissions, filters

from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer 
from .serializers import CustomUserSerializer
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class ProjectList(generics.ListCreateAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["is_open", "owner", "date_created"]
    search_fields = ["title", "description"]
    # can't have the same search fields and filter fields.

    def perform_create(self, serializer):
        serializer.save(supporter=self.request.user)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request):
#         projects = Project.objects.all()
#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProjectDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = ProjectDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # https://www.youtube.com/watch?v=b680A5fteEo
    def delete(self, request, pk):
        project = self.get_object(pk=pk)
        project.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)


class PledgeList(generics.ListCreateAPIView):

    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("supporter",)

    def perform_create(self, serializer):
        serializer.save(supporter=self.request.user)
    

    # Not needed for the filter to work
    # def get(self, request):
    #     pledges = self.filter_queryset(self.get_queryset)
    #     serializer = self.get_serializer(pledges, many = True)
    #     return Response(serializer.data)

class PledgeDetail(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsSupporterOrReadOnly
    ]

    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
