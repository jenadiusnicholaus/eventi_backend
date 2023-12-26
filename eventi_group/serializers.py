
from django.db import IntegrityError
from rest_framework import serializers
from authentication.serializers import GetUserSerializer
from eventi_group.models import EventiGroup, EventiGroupMembers, EventiGroupPlage
from authentication.serializers import GetUserSerializer


class GetEventiGroupSerializer(serializers.ModelSerializer):
    admin = GetUserSerializer()
  
    class Meta:
        model = EventiGroup
        fields = ['pk', 'name',  'description', 'admin', "latitude", "longitude", "address", "city", "country", "start_date", "end_date", "category", "profile_picture", "cover_picture", 'is_private']
        extra_kwargs = {
            'members': {'required': True},
            'admin': {'required': True},
            'latitude': {'required': True},
            'longitude': {'required': True},
            'address': {'required': True},
            'city': {'required': True},
            'country': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'category': {'required': True},
            'profile_picture': {'required': False},
            'cover_picture': {'required': False},
            'is_private': {'required': False},
            
        }


class GetMyGroupSerializers(serializers.ModelSerializer):
    group = GetEventiGroupSerializer(read_only=True)
    members = GetUserSerializer(read_only=True, many=True)
    class Meta:
        model = EventiGroupMembers
        fields = ['pk', 'group', 'members']

        

class GetEventiGroupMembersSerializer(serializers.ModelSerializer):
    members = GetUserSerializer(many=True, read_only=True)
    class Meta:
        model = EventiGroupMembers
        fields = ['pk', 'group', 'members']
       
       


class CreateGroupSerializer(serializers.ModelSerializer):
    members = serializers.ListField(child=serializers.CharField(max_length=100))
    class Meta:
        model = EventiGroup
        fields = ['name','members', 'description', 'admin', "latitude", "longitude", "address", "city", "country", "start_date", "end_date", "category", "profile_picture", "cover_picture"]
        extra_kwargs = {
            'members': {'required': True},
            'admin': {'required': True},
            'latitude': {'required': True},
            'longitude': {'required': True},
            'address': {'required': True},
            'city': {'required': True},
            'country': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'category': {'required': True},
            'profile_picture': {'required': False},
            'cover_picture': {'required': False},
            
        }

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        group, created = EventiGroup.objects.get_or_create(**validated_data)
        group_members = EventiGroupMembers.objects.create(group_id=group.id, )
        for member_data in members_data:
            group_members.members.add(member_data)
        return group

  
    
class UpdateGroupSerializer(serializers.ModelSerializer):
    members = serializers.ListField(child=serializers.CharField(max_length=100))

    class Meta:
        model = EventiGroup
        fields = ['name', 'members', 'description',  'admin', "latitude", "longitude", "address", "city", "country", "start_date", "end_date", "category", "profile_picture", "cover_picture", 'is_private']
        extra_kwargs = {
            'members': {'required': True},
            'admin': {'required': True},
            'latitude': {'required': True},
            'longitude': {'required': True},
            'address': {'required': True},
            'city': {'required': True},
            'country': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'category': {'required': True},
            'profile_picture': {'required': False},
            'cover_picture': {'required': False},
            'is_private': {'required': False},
            
        }
        

    def patch(self, instance, validated_data):
        members_data = validated_data.pop('members')
        group, created = EventiGroup.objects.get_or_create(**validated_data)
        group_members = EventiGroupMembers.objects.create(group_id=group.id, )
        for member_data in members_data:
            group_members.members.add(member_data)
        return group
    

class DeleteGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventiGroup
        fields = ['pk']

    def delete(self, instance, validated_data):
        group = EventiGroup.objects.get(pk=validated_data['pk'])
        group.delete()


        return group
    
class JoinGroupSeliazers(serializers.ModelSerializer):

    class Meta:
        model = EventiGroupMembers
        fields = ['group', 'members']
        extra_kwargs = {
            'group': {'required': True},
            'members': {'required': True},
        }
        
    def create(self, validated_data):
        group = validated_data.pop('group')
        members_data = validated_data.pop('members')
        group= EventiGroup.objects.get(id=group.id)
        print(group)
        group_members = EventiGroupMembers.objects.filter(group_id=group.id).first()
        print(group_members)
        for member_data in members_data:
            is_member = EventiGroupMembers.objects.filter(group_id=group.id, members=member_data).exists()
          
            if (is_member):
                raise serializers.ValidationError("You are already a members of this group")
            else:
                group_members.members.add(member_data)
        group_members.save()    
        return group_members
    


    
class LeaveGroupSeliazers(serializers.ModelSerializer):
    
        class Meta:
            model = EventiGroupMembers
            fields = ['group', 'members']
            extra_kwargs = {
                'group': {'required': True},
                'members': {'required': True},
            }
            
        def create(self, validated_data):
            group = validated_data.pop('group')
            members_data = validated_data.pop('members')
            group= EventiGroup.objects.get(id=group.id)
            print(group)
            group_members = EventiGroupMembers.objects.filter(group_id=group.id).first()
            print(group_members)
            for member_data in members_data:
                is_member = EventiGroupMembers.objects.filter(group_id=group.id, members=member_data).exists()
            
                if (is_member):
                    group_members.members.remove(member_data)
                else:
                    raise serializers.ValidationError("You are not a members of this group")
            group_members.save()    
            return group_members
        


class GetPlageSelializers(serializers.ModelSerializer):

    class Meta:
        model = EventiGroupPlage
        fields = ['group','plaged_amount', 'paid', 'plage_paid_amount', 'plaging_expiry', 'plaged_by']
    
class CreateEventiGroupPlagesSelializers(serializers.ModelSerializer):
    class Meta:
        model = EventiGroupPlage
        fields = ['group','plaged_amount', 'paid', 'plage_paid_amount', 'plaging_expiry', 'plaged_by']
        extra_kwargs = {
            'group': {'required': True},
            'plaged_amount': {'required': True},
            'paid': {'required': False},
            'plage_paid_amount': {'required': False},
            'plaging_expiry': {'required': False},
            'plaged_by': {'required': True},
        }

    def create(self, validated_data):
        group = validated_data.pop('group')
        plaged_by = validated_data.pop('plaged_by')
        group= EventiGroup.objects.get(id=group.id)
        print(group)
        group_members = EventiGroupMembers.objects.filter(group_id=group.id).first()
        print(group_members)
        is_member = EventiGroupMembers.objects.filter(group_id=group.id, members=plaged_by).exists()
        if (is_member):
            try:
                if not EventiGroupPlage.objects.filter(group_id=group.id, plaged_by=plaged_by).exists():
                    group_plage = EventiGroupPlage.objects.create(group_id=group.id, plaged_by=plaged_by, **validated_data)
                    return group_plage
                else:
                    raise serializers.ValidationError("You have already created a plage for this group")
            except IntegrityError:
                raise serializers.ValidationError("AN error occured while creating the plage")
        else:
            raise serializers.ValidationError("You are not a members of this group")


        
