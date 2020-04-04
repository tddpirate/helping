from django.contrib.auth.models import User
import graphene
from graphene_django.types import DjangoObjectType

from .models import ProfileStatus, Profile
from .models import ContactType, Contact
from .models import TaskType, TaskTypeExtra
from .models import NeedStatus, Need, NeedExtra
from .models import CapabilityStatus, Capability
# !!! Import also CapabilityExtra, Task !!! Once they are implemented.

########################################################################

class ProfileStatusType(DjangoObjectType):
    class Meta:
        model = ProfileStatus

class UserType(DjangoObjectType):
    class Meta:
        model = User

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile

class ContactTypeType(DjangoObjectType):
    class Meta:
        model = ContactType

class Contact1Type(DjangoObjectType):
    class Meta:
        model = Contact

class TaskTypeType(DjangoObjectType):
    class Meta:
        model = TaskType

class TaskTypeExtraType(DjangoObjectType):
    class Meta:
        model = TaskTypeExtra

class NeedStatusType(DjangoObjectType):
    class Meta:
        model = NeedStatus

class NeedType(DjangoObjectType):
    class Meta:
        model = Need

class NeedExtraType(DjangoObjectType):
    class Meta:
        model = NeedExtra

class CapabilityStatusType(DjangoObjectType):
    class Meta:
        model = CapabilityStatus

class CapabilityType(DjangoObjectType):
    class Meta:
        model = Capability


########################################################################

class Query(object):
    all_profilestatuss = graphene.List(ProfileStatusType)
    all_users = graphene.List(UserType)
    all_profiles = graphene.List(ProfileType)

    def resolve_all_profilestatuss(self, info, **kwargs):
        return ProfileStatus.objects.all()
    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()
    def resolve_all_profiles(self, info, **kwargs):
        return Profile.objects.all()

# End of tagiot/schema.py
