#from django.contrib.auth.models import User
import graphene
from graphene_django.types import DjangoObjectType

from .models import ProfileStatus, Profile
from .models import ContactType, Contact
from .models import TaskType, TaskTypeExtra
from .models import NeedStatus, Need, NeedExtra
from .models import CapabilityStatus, Capability, CapabilityExtra
from .models import TaskStatus, Task

########################################################################
###                             Queries                              ###
########################################################################

class ProfileStatusType(DjangoObjectType):
    class Meta:
        model = ProfileStatus

#class UserType(DjangoObjectType):
#    class Meta:
#        model = User

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
    user_first_name = graphene.String()
    user_last_name = graphene.String()
    user_username = graphene.String()
    user_email = graphene.String()
    def resolve_user_first_name(parent, info):
        return parent.get_user_first_name()
    def resolve_user_last_name(parent, info):
        return parent.get_user_last_name()
    def resolve_user_username(parent, info):
        return parent.get_user_username()
    def resolve_user_email(parent, info):
        return parent.get_user_email()

####################################

class ContactTypeType(DjangoObjectType):
    class Meta:
        model = ContactType

class Contact1Type(DjangoObjectType):
    class Meta:
        model = Contact

####################################

class TaskTypeType(DjangoObjectType):
    class Meta:
        model = TaskType

class TaskTypeExtraType(DjangoObjectType):
    class Meta:
        model = TaskTypeExtra

####################################

class NeedStatusType(DjangoObjectType):
    class Meta:
        model = NeedStatus

class NeedType(DjangoObjectType):
    class Meta:
        model = Need

class NeedExtraType(DjangoObjectType):
    class Meta:
        model = NeedExtra

####################################

class CapabilityStatusType(DjangoObjectType):
    class Meta:
        model = CapabilityStatus

class CapabilityType(DjangoObjectType):
    class Meta:
        model = Capability

class CapabilityExtraType(DjangoObjectType):
    class Meta:
        model = CapabilityExtra

####################################

class TaskStatusType(DjangoObjectType):
    class Meta:
        model = TaskStatus

class Task1Type(DjangoObjectType):
    class Meta:
        model = Task


########################################################################

class Query(object):
    profilestatus = graphene.Field(ProfileStatusType, status=graphene.String())
    all_profilestatuss = graphene.List(ProfileStatusType)
    #user = graphene.Field(UserType, id=graphene.Int())
    #all_users = graphene.List(UserType)
    profile = graphene.Field(ProfileType, id_member=graphene.Int(), user_username=graphene.String())
    all_profiles = graphene.List(ProfileType, user_username=graphene.String())

    contacttype = graphene.Field(ContactTypeType, id=graphene.Int())
    all_contacttypes = graphene.List(ContactTypeType)
    contact = graphene.Field(Contact1Type, id=graphene.Int())
    all_contacts = graphene.List(Contact1Type)

    tasktype = graphene.Field(TaskTypeType, id_member=graphene.Int())
    all_tasktypes = graphene.List(TaskTypeType)
    tasktypeextra = graphene.Field(TaskTypeExtraType, id=graphene.Int())
    all_tasktypeextras = graphene.List(TaskTypeExtraType, fldname=graphene.String())

    needstatus = graphene.Field(NeedStatusType, id=graphene.Int())
    all_needstatuss = graphene.List(NeedStatusType)
    need = graphene.Field(NeedType, id_need=graphene.Int())
    all_needs = graphene.List(NeedType, tagmajor=graphene.String(), tagminor=graphene.String())
    needextra = graphene.Field(NeedExtraType, id=graphene.Int())
    all_needextras = graphene.List(NeedExtraType)

    capabilitystatus = graphene.Field(CapabilityStatusType, id=graphene.Int())
    all_capabilitystatuss = graphene.List(CapabilityStatusType)
    capability = graphene.Field(CapabilityType, id_capability=graphene.Int())
    all_capabilitys = graphene.List(CapabilityType, tagmajor=graphene.String(), tagminor=graphene.String())
    capabilityextra = graphene.Field(CapabilityExtraType, id=graphene.Int())
    all_capabilityextras = graphene.List(CapabilityExtraType)

    taskstatus = graphene.Field(TaskStatusType, id=graphene.Int())
    all_taskstatuss = graphene.List(TaskStatusType)
    task = graphene.Field(Task1Type, id_task=graphene.Int())
    all_tasks = graphene.List(Task1Type)


    def resolve_profilestatus(self, info, **kwargs):
        status = kwargs.get('status')
        return ProfileStatus.objects.get(status=status) if status else None
    def resolve_all_profilestatuss(self, info, **kwargs):
        return ProfileStatus.objects.all()
    #def resolve_user(self, info, **kwargs):
    #    id = kwargs.get('id')
    #    return User.objects.get(pk=id) if id else None
    #def resolve_all_users(self, info, **kwargs):
    #    return User.objects.all()
    def resolve_profile(self, info, **kwargs):
        user_username = kwargs.get('user_username')
        if user_username:
            return Profile.objects.get(user__username=user_username)
        else:
            id_member = kwargs.get('id_member')
            return Profile.objects.get(id_member=id_member) if id_member else None
    def resolve_all_profiles(self, info, **kwargs):
        user_username = kwargs.get('user_username')
        if user_username:
            return Profile.objects.filter(user__username=user_username)
        else:
            return Profile.objects.all()

    ################################

    def resolve_contacttype(self, info, **kwargs):
        id = kwargs.get('id')
        return ContactType.objects.get(id=id) if id else None
    def resolve_all_contacttypes(self, info, **kwargs):
        return ContactType.objects.all()
    def resolve_contact(self, info, **kwargs):
        id = kwargs.get('id')
        return Contact.objects.get(id=id) if id else None
    def resolve_all_contacts(self, info, **kwargs):
        return Contact.objects.all()

    ################################

    def resolve_tasktype(self, info, **kwargs):
        id_member = kwargs.get('id_member')
        return TaskType.objects.get(id_member=id_member) if id_member else None
    def resolve_all_tasktypes(self, info, **kwargs):
        return TaskType.objects.all()
    def resolve_tasktypeextra(self, info, **kwargs):
        id = kwargs.get('id')
        return TaskTypeExtra.objects.get(id=id) if id else None
    def resolve_all_tasktypeextras(self, info, **kwargs):
        fldname = kwargs.get('fldname')
        return TaskTypeExtra.objects.filter(fldname=fldname) if fldname else TaskTypeExtra.objects.all()

    ################################

    def resolve_needstatus(self, info, **kwargs):
        id = kwargs.get('id')
        return NeedStatus.objects.get(id=id) if id else None
    def resolve_all_needstatuss(self, info, **kwargs):
        return NeedStatus.objects.all()
    def resolve_need(self, info, **kwargs):
        id_need = kwargs.get('id_need')
        return Need.objects.get(id_need=id_need) if id_need else None
    def resolve_all_needs(self, info, **kwargs):
        tagmajor = kwargs.get('tagmajor')
        tagminor = kwargs.get('tagminor')
        if (tagmajor or tagminor):
            kw = {}   # Workaround to the problem of filter(arg=None) != filter()
            if (tagmajor):
                kw["tasktype__tagmajor"] = tagmajor
            if (tagminor):
                kw["tasktype__tagminor"] = tagminor
            return Need.objects.filter(**kw)
        else:
            return Need.objects.all()
    def resolve_needextra(self, info, **kwargs):
        id = kwargs.get('id')
        return NeedExtra.objects.get(id=id) if id else None
    def resolve_all_needextras(self, info, **kwargs):
        return NeedExtra.objects.all()

    ################################

    def resolve_capabilitystatus(self, info, **kwargs):
        id = kwargs.get('id')
        return CapabilityStatus.objects.get(id=id) if id else None
    def resolve_all_capabilitystatuss(self, info, **kwargs):
        return CapabilityStatus.objects.all()
    def resolve_capability(self, info, **kwargs):
        id_capability = kwargs.get('id_capability')
        return Capability.objects.get(id_capability=id_capability) if id_capability else None
    def resolve_all_capabilitys(self, info, **kwargs):
        tagmajor = kwargs.get('tagmajor')
        tagminor = kwargs.get('tagminor')
        if (tagmajor or tagminor):
            kw = {}   # Workaround to the problem of filter(arg=None) != filter()
            if (tagmajor):
                kw["tasktype__tagmajor"] = tagmajor
            if (tagminor):
                kw["tasktype__tagminor"] = tagminor
            return Capability.objects.filter(**kw)
        else:
            return Capability.objects.all()
    def resolve_capabilityextra(self, info, **kwargs):
        id = kwargs.get('id')
        return CapabilityExtra.objects.get(id=id) if id else None
    def resolve_all_capabilityextras(self, info, **kwargs):
        return CapabilityExtra.objects.all()

    ################################

    def resolve_taskstatus(self, info, **kwargs):
        id = kwargs.get('id')
        return TaskStatus.objects.get(id=id) if id else None
    def resolve_all_taskstatuss(self, info, **kwargs):
        return TaskStatus.objects.all()
    def resolve_task(self, info, **kwargs):
        id_task = kwargs.get('id_task')
        return Task.objects.get(id_task=id_task) if id_task else None
    def resolve_all_tasks(self, info, **kwargs):
        return Task.objects.all()

########################################################################
###                            Mutations                             ###
########################################################################

class ProfileStatusInput(graphene.InputObjectType):
    id = graphene.ID()
    status = graphene.String()

#class ProfileInput(graphene.InputObjectType):
#    id_member = graphene.ID()
#    bio = graphene.String()
#    pstatus = 

####################################

class CreateProfileStatus(graphene.Mutation):
    class Arguments:
        input = ProfileStatusInput(required=True)

    ok = graphene.Boolean()
    profilestatus = graphene.Field(ProfileStatusType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        profilestatus_instance = ProfileStatus(status=input.status)
        profilestatus_instance.save()
        return CreateProfileStatus(ok=ok, profilestatus=profilestatus_instance)

class UpdateProfileStatus(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ProfileStatusInput(required=True)

    ok = graphene.Boolean()
    profilestatus = graphene.Field(ProfileStatusType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        profilestatus_instance = ProfileStatus.objects.get(pk=id)
        if profilestatus_instance:
            ok = True
            profilestatus_instance.name = input.name
            profilestatus_instance.save()
            return UpdateProfileStatus(ok=ok, profilestatus=profilestatus_instance)
        return UpdateProfileStatus(ok=ok, profilestatus=None)

########################################################################

class Mutation(object):
    create_profilestatus = CreateProfileStatus.Field()
    update_profilestatus = UpdateProfileStatus.Field()


# End of tagiot/schema.py
