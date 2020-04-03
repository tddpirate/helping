# Common utilities for the membership application

from enum import Enum

# Inspired by: http://blog.richard.do/index.php/2014/02/how-to-use-enums-for-django-field-choices/
class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((fld.value, cls.labels()[fld]) for fld in cls)

    @classmethod
    def values(cls):
        return set((fld.value for fld in cls))

    def __int__(self):
        return int(self.value)

# End of utils.py
