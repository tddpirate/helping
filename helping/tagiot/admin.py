from django.contrib import admin
from django.db import models

from .models import ProfileStatus, Profile
from .models import ContactType, Contact
from .models import TaskType, TaskTypeExtra
from .models import NeedStatus, Need, NeedExtra
from .models import CapabilityStatus, Capability
# !!! Import also CapabilityExtra, Task !!! Once they are implemented.

########################################################################
####                      Models Administration                     ####
########################################################################

#######################################
#          Enumeration models         #
#######################################

class EnumAdmin(admin.ModelAdmin):
    pass

#######################################
# Subordinate models which are inline #
#######################################

class ContactInline(admin.TabularInline):
    model = Contact
    extra = 4

class TaskTypeExtraInline(admin.TabularInline):
    model = TaskTypeExtra
    extra = 4

class NeedExtraInline(admin.TabularInline):
    model = NeedExtra
    extra = 4

#######################################
#        "Actual Work" models         #
#######################################

class ProfileAdmin(admin.ModelAdmin):
    list_display = [ 'id_member',
                     'get_user_first_name', 'get_user_last_name', 'get_user_username', 'get_user_email',
                     'bio',
    ]
    readonly_fields=('id_member',
                     'get_user_first_name', 'get_user_last_name', 'get_user_username', 'get_user_email',
    )
    list_display_links = [ 'get_user_username',
    ]
    fieldsets = [
        ('User', {'fields': ['get_user_first_name', 'get_user_last_name', 'get_user_username', 'get_user_email',]}),
        ('Profile', {'fields': ['bio',]}),
    ]
    inlines = [ContactInline,]
    search_fields = ['=id_member',
                     '^get_user_first_name', '^get_user_last_name', '^get_user_username', '^get_user_email',
    ]

class TaskTypeAdmin(admin.ModelAdmin):
    list_display = [ 'id_member',
                     'tagmajor', 'tagminor', 'description'
    ]
    readonly_fields=('id_member',)
    list_display_links = ['id_member', 'tagmajor', 'tagminor',]
    inlines = [TaskTypeExtraInline,]
    search_fields = ['=id_member', '^tagmajor', '^tagminor',]

class NeedAdmin(admin.ModelAdmin):
    list_display = [ 'id_need',
                     'profile', 'tasktype', 'details',
                     'nstatus',
    ]
    readonly_fields=('id_need',)
    list_display_links = ['id_need', 'profile', 'tasktype',]
    inlines = [NeedExtraInline,]
    search_fields = ['=id_need', '^profile', '^tasktype',]


#!!!!!!! Modules needing Admin:  Capability



########################################################################
####                           Registrations                        ####
########################################################################


for (model, model_admin) in [
        (ProfileStatus, EnumAdmin),
        (ContactType, EnumAdmin),
        (NeedStatus, EnumAdmin),
        (CapabilityStatus, EnumAdmin),
        (Profile, ProfileAdmin),
        (TaskType, TaskTypeAdmin),
        (Need, NeedAdmin),
        ]:
    admin.site.register(model, model_admin)

# End of tagiot/admin.py
