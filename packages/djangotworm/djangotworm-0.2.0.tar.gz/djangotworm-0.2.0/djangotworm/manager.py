from django.db.models.manager import BaseManager
from twango.query import TwistedQuerySet

class TwistedManager(BaseManager.from_queryset(TwistedQuerySet)):
    pass
