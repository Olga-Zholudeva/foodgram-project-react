from django.db.models import EmailField
from django_case_insensitive_field import CaseInsensitiveFieldMixin


class LowerEmailField(CaseInsensitiveFieldMixin, EmailField):

    def __init__(self, *args, **kwargs):

        super(CaseInsensitiveFieldMixin, self).__init__(*args, **kwargs)
