from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    create_time = models.DateTimeField(
        verbose_name=_('Create Time'), auto_now_add=True)
    modify_time = models.DateTimeField(
        verbose_name=_('Modify Time'), auto_now=True)

    auto_cols = ['create_time', 'modify_time']

    class Meta:
        abstract = True
        ordering = ('-create_time',)
        get_latest_by = ('create_time',)
