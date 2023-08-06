from django.db.models.manager import BaseManager
from .query import TwistedQuerySet

class TwistedManager(BaseManager.from_queryset(TwistedQuerySet)):
    pass
