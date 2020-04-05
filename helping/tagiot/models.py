from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import format_html

from common.utils import ChoiceEnum

########################################################################
####                             Models                             ####
########################################################################

####################################
#      Extra user information      #
####################################

class ProfileStatus(models.Model):
    status = models.CharField("status", max_length=32, unique=True)
    PS_FREE = "free"
    PS_BUSY = "busy"

    @classmethod
    def get_PS(cls, status):
        """PS = ProfileStatus"""
        pss = ProfileStatus.objects.filter(status=status)
        if (len(pss) > 0):
            if (len(pss) > 1):
                import logging
                logger = logging.getLogger(__name__)
                logger.error("More than one ProfileStatus record with status=%(status)s", {"status": status})
            ps = pss[0]
        else:
            ps = ProfileStatus(status=status)
            ps.save()
        return ps

    def __str__(self):
        return self.status

    ##### ProfileStatus.Meta #########
    class Meta:
        indexes = [
            models.Index(fields=['status']),
            ]


class Profile(models.Model):
    id_member = models.AutoField("member id", primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField("language", max_length=5, default="en")
    bio = models.TextField(max_length=500, blank=True)
    pstatus = models.ForeignKey(ProfileStatus, on_delete=models.CASCADE)
    # Contact      # 1:N relation to contact information
    # Need         # 1:N relation to help requests
    # Capabilities # 1:N relation to help offers

    def __str__(self):
        uname = self.user.first_name + " " + self.user.last_name
        return uname if uname.strip != "" else self.profile.user.username

    # Auxiliary functions for use by ProfileAdmin
    def get_user_first_name(self):
        return self.user.first_name
    def get_user_last_name(self):
        return self.user.last_name
    def get_user_username(self):
        return self.user.username
    def get_user_email(self):
        return self.user.email
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,pstatus=ProfileStatus.get_PS(ProfileStatus.PS_FREE))
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("Created user profile for %(username).", {"username": instance.username})

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    import logging
    logger = logging.getLogger(__name__)
    logger.debug("Updated user profile for %(username)s.", {"username": instance.username})

####################################
#       Contact information        #
####################################
# Note: was lifted from my Hamakor membership application from
#       almost 2 years ago

class ContactType(models.Model):
    ct_name = models.CharField("contact type", max_length=32, unique=True)
    CT_MOBILE = "mobile"
    CT_EMAIL = "email"
    CT_ADDRESS = "address"
    CT_URL_LINKEDIN = "linkedin"
    CT_URL_FACEBOOK = "facebook"
    CT_URL_WEBSITE = "website"

    @classmethod
    def get_CT(cls, ct_name):
        cts = ContactType.objects.filter(ct_name=ct_name)
        if (len(cts) > 0):
            if (len(cts) > 1):
                import logging
                logger = logging.getLogger(__name__)
                logger.error("More than one ContactType record with name=%(name)s", {"name": ct_name})
            ct = cts[0]
        else:
            ct = ContactType(ct_name=ct_name)
            ct.save()
        return ct

    def __str__(self):
        return self.ct_name

    ##### ContactType.Meta #########
    class Meta:
        indexes = [
            models.Index(fields=['ct_name']),
            ]

####################################
# Contact
####################################

class Contact(models.Model):
    """Contact information item"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    contact_type = models.ForeignKey(ContactType, on_delete=models.CASCADE)
    contact_data = models.CharField("contact data", max_length=64)
    use_voice = models.BooleanField("use voice", default=True)
    use_sms = models.BooleanField("use SMS", default=True)

    def __str__(self):
        return F"{self.profile}: {self.contact_type} {self.contact_data}"

    DEFAULT_USES = {
        ContactType.CT_MOBILE :      { "use_voice" : True,  "use_sms" : True   },
        ContactType.CT_EMAIL :       { "use_voice" : False, "use_sms" : False  },
        ContactType.CT_ADDRESS :     { "use_voice" : False, "use_sms" : False  },
        ContactType.CT_URL_FACEBOOK: { "use_voice" : False, "use_sms" : False  },
        ContactType.CT_URL_LINKEDIN: { "use_voice" : False, "use_sms" : False  },
        ContactType.CT_URL_WEBSITE:  { "use_voice" : False, "use_sms" : False  },
        }

    ##### Contact.Meta #################################################
    class Meta:
        ordering = ['profile', 'contact_type']
        indexes = [
            models.Index(fields=['profile', 'contact_type']),
            ]

####################################
#          Tags for tasks          #
####################################

class TaskType(models.Model):
    id_member = models.AutoField("task type id", primary_key=True)
    tagmajor = models.CharField("main type", max_length=32)
    tagminor = models.CharField("subtype", max_length=32)
    description = models.TextField(max_length=500, blank=True)
    # TaskTypeExtra # 1:N relation to extra fields definition

    def __str__(self):
        return F"{self.tagmajor}/{self.tagminor}"

    class Meta:
        ordering = ['tagmajor', 'tagminor']
        indexes = [
            models.Index(fields=['tagmajor', 'tagminor']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['tagmajor', 'tagminor'], name='unique_task_type'),
        ]

class TaskTypeExtra(models.Model):
    # Fields specifying additional information about the task
    tasktype = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    fldname = models.CharField("field name", max_length=32)
    mandatory = models.BooleanField("mandatory", default=False)

    def __str__(self):
        return F"{self.tasktype}:{self.fldname}"

    class Meta:
        ordering = ['fldname']
        indexes = [
            models.Index(fields=['tasktype', 'fldname']),
        ]
        #constraints = [
        #    models.UniqueConstraint(fields=['tasktype', 'fldname'], name='unique_field_for_task'),
        # Decision: not to force uniqueness of fieldname per task type,
        # because some fields, such as 'language' can have multiple values.
        #]

####################################
#           Help Needed            #
####################################

class NeedStatus(models.Model):
    status = models.CharField("status", max_length=32, unique=True)
    N_FOUND = "found"
    N_OPEN = "open"   # not found

    @classmethod
    def get_N(cls, status):
        ns = NeedStatus.objects.filter(status=status)
        if (len(ns) > 0):
            if (len(ns) > 1):
                import logging
                logger = logging.getLogger(__name__)
                logger.error("More than one NeedStatus record with status=%(status)s", {"status": status})
            n = ns[0]
        else:
            n = NeedStatus(status=status)
            n.save()
        return n

    def __str__(self):
        return self.status

    ##### ProfileStatus.Meta #########
    class Meta:
        indexes = [
            models.Index(fields=['status']),
            ]


class Need(models.Model):
    id_need = models.AutoField("need id", primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tasktype = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    details = models.TextField(max_length=500, blank=True)
    nstatus = models.ForeignKey(NeedStatus, on_delete=models.CASCADE)
    # NeedExtra   # 1:N relation to information in fields defined in NeedExtra

    def __str__(self):
        return F"{self.profile} need {self.tasktype} status {self.nstatus}"

    class Meta:
        ordering = ['profile', 'tasktype']
        indexes = [
            models.Index(fields=['profile', 'tasktype', 'nstatus']),
        ]

class NeedExtra(models.Model):
    need = models.ForeignKey(Need, on_delete=models.CASCADE)
    fldname = models.CharField("field name", max_length=32)
    fldvalue = models.CharField("field value", max_length=32)

    def __str__(self):
        return F"{self.fldname}={self.fldvalue}"

    class Meta:
        ordering = ['fldname']
        indexes = [
            models.Index(fields=['need', 'fldname', 'fldvalue']),
        ]


####################################
#           Help Offered           #
####################################

class CapabilityStatus(models.Model):
    status = models.CharField("status", max_length=32, unique=True)
    CS_FREE = "free"
    CS_BUSY = "busy"

    @classmethod
    def get_CS(cls, status):
        """CS = CapabilityStatus"""
        css = CapabilityStatus.objects.filter(status=status)
        if (len(css) > 0):
            if (len(css) > 1):
                import logging
                logger = logging.getLogger(__name__)
                logger.error("More than one CapabilityStatus record with status=%(status)s", {"status": status})
            cs = css[0]
        else:
            cs = CapabilityStatus(status=status)
            cs.save()
        return cs

    def __str__(self):
        return self.status

    ##### CapabilityStatus.Meta #########
    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]


class Capability(models.Model):
    id_capability = models.AutoField("capability id", primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tasktype = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    details = models.TextField(max_length=500, blank=True)
    cstatus = models.ForeignKey(CapabilityStatus, on_delete=models.CASCADE)
    # CapabilityExtra # 1:N relation to information in fields defined in CapabilityExtra

    class Meta:
        ordering = ['id_capability', 'tasktype']
        indexes = [
            models.Index(fields=['id_capability', 'profile', 'tasktype']),
        ]

class CapabilityExtra(models.Model):
    capability = models.ForeignKey(Capability, on_delete=models.CASCADE)
    fldname = models.CharField("field name", max_length=32)
    fldvalue = models.CharField("field value", max_length=32)

    def __str__(self):
        return F"{self.fldname}={self.fldvalue}"

    class Meta:
        ordering = ['fldname']
        indexes = [
            models.Index(fields=['capability', 'fldname', 'fldvalue']),
        ]

####################################
#           Active Tasks           #
####################################

class TaskStatus(models.Model):
    status = models.CharField("status", max_length=32, unique=True)
    # Transitions:
    # Start with T_C_FLASHED or T_N_FLASHED depending upon who flashed.
    # Once both confirm, the task is T_MATCHED and presumably being executed.
    # When it is done (or terminated), the task goes to T_FINISHED state.
    T_C_FLASHED  = "capableflashed"
    T_N_FLASHED  = "needyflashed"
    T_MATCHED    = "matched"       # Now the task is being executed (maybe waiting for them to actually work on it; details will be in 'feedback')
    T_FINISHED   = "finished"      # The task could be terminated (details will be in 'feedback')

    @classmethod
    def get_T(cls, status):
        """T = TaskStatus"""
        tss = TaskStatus.objects.filter(status=status)
        if (len(tss) > 0):
            if (len(tss) > 1):
                import logging
                logger = logging.getLogger(__name__)
                logger.error("More than one TaskStatus record with status=%(status)s", {"status": status})
            ts = tss[0]
        else:
            ts = TaskStatus(status=status)
            ts.save()
        return ts

    def __str__(self):
        return self.status

    ##### TaskStatus.Meta #########
    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]

class Task(models.Model):
    id_task = models.AutoField("task id", primary_key=True)
    need = models.ForeignKey(Need, on_delete=models.CASCADE)
    capable = models.ForeignKey(Capability, on_delete=models.CASCADE)
    tstatus = models.ForeignKey(TaskStatus, on_delete=models.CASCADE)
    feedback = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return F"{self.need.profile.user.username}:{self.capability.profile.user.username}---{self.capability.tasktype}"

    class Meta:
        ordering = ['id_task', 'tstatus',]
        indexes = [
            models.Index(fields=['id_task', 'need', 'capable', 'tstatus',]),
        ]

########################################################################
# End of tagiot/models.py
