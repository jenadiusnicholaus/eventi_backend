from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from eventi_group.models import EventiGroup, EventiGroupMembers, EventiGroupPlage
from eventi_group.serializers import (  CreateEventiGroupPlagesSelializers,
                                        GetMyGroupSerializers,
                                        CreateGroupSerializer, GetPlageSelializers,
                                        UpdateGroupSerializer,
                                        JoinGroupSeliazers,
                                        LeaveGroupSeliazers,
                                        GetEventiGroupMembersSerializer
                                        )
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import IntegrityError


# # Create your views here.

class GetEventiGroup(APIView):
    serializer_class = GetMyGroupSerializers
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        mygroups = EventiGroupMembers.objects.filter(members=request.user)
        serializer = self.serializer_class(mygroups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateGroup(APIView):
     serializer_class = CreateGroupSerializer

     def post(self, request):
         serializer = self.serializer_class(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response({'message': 'Group created successfully'}, status=status.HTTP_201_CREATED)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateGroup(APIView):
    serializer_class = UpdateGroupSerializer

    def patch(self, request, pk):
        try:
            group = EventiGroup.objects.get(pk=pk)
        except EventiGroup.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Group updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JoinGroupView(APIView):
    serializer_class = JoinGroupSeliazers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'A member can have only one plage per group'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetGroupMembers(APIView):
    serializer_class = GetEventiGroupMembersSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        mygroups = EventiGroupMembers.objects.filter(group=request.query_params.get('group_id'))
        serializer = self.serializer_class(mygroups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class LeaveGroup(APIView):
    serializer_class = LeaveGroupSeliazers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'A member can have only one plage per group'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class GetGroupPlages(APIView):
    serializer_class = GetPlageSelializers
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        mygroups = EventiGroupPlage.objects.filter(group=request.query_params.get('group_id'))
        serializer = self.serializer_class(mygroups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class CreateEventiGroupPlages(APIView):
    serializer_class = CreateEventiGroupPlagesSelializers
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'A member can have only one plage per group'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
