from django.db import models
import uuid

# Create your models here.


class EventiGroup(models.Model):
    name = models.CharField(max_length=100, unique=True )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    admin = models.ForeignKey('authentication.User', related_name='admin', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='eventi_group/profile_pictures', null=True, blank=True)
    cover_picture = models.ImageField(upload_to='eventi_group/cover_pictures', null=True, blank=True)
    is_private = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_sponsored = models.BooleanField(default=False)
    is_promoted = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    is_following = models.BooleanField(default=False)
    is_favourite = models.BooleanField(default=False)
    sharing_link = models.CharField(max_length=100, null=True, blank=True)
    invite_link = models.CharField(max_length=100, null=True, blank=True)
    invite_code = models.CharField(max_length=100, null=True, blank=True)
    invite_expiry = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    timezone = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Eventi Group'
        verbose_name_plural = 'Eventi Groups'
        db_table = 'EVT_group'



    def __str__(self):
        return self.name
    
    @property
    def get_members(self):
        return self.members.all()
    
class EventiGroupMembers(models.Model):
    group = models.ForeignKey(EventiGroup, on_delete=models.CASCADE, related_name='group')
    members = models.ManyToManyField('authentication.User', related_name='members')

    class Meta:
        verbose_name = 'Eventi Group Members'
        verbose_name_plural = 'Eventi Group Members'
        db_table = 'EVT_group_members'


class EventiGroupPlage(models.Model):
    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(EventiGroup, on_delete=models.CASCADE, related_name='group_plage', null=True, blank=True)
    plaged_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='plaged_by', null=True, blank=True  )
    plaging_date = models.DateTimeField(auto_now_add=True)
    plaged_amount = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    plage_paid_amount = models.IntegerField(default=0)
    plaging_expiry = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Eventi Group Plages'
        verbose_name_plural = 'Eventi Group Plages'
        db_table = 'EVT_group_plages'  


    def __str__(self):
        return str(self.plaged_amount)
    

# class MemberShip(models.Model):
#     uid = models.UUIDField(
#         primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True, blank=True, related_name='group_member')
#     plage = models.OneToOneField(EventiGroupPlage, on_delete=models.CASCADE, related_name='member_plage', null=True, blank=True)
#     is_admin = models.BooleanField(default=False)
#     is_moderator = models.BooleanField(default=False)
#     is_member = models.BooleanField(default=False)
#     is_blocked = models.BooleanField(default=False)
#     is_reported = models.BooleanField(default=False)
#     is_banned = models.BooleanField(default=False)
#     is_hidden = models.BooleanField(default=False)
#     is_featured = models.BooleanField(default=False)

#     class Meta:
#         verbose_name = 'Eventi Group Membership'
#         verbose_name_plural = 'Eventi Group Membership'
#         db_table = 'EVT_group_membership'  
        



    





    

    







   