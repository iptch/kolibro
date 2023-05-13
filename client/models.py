from django.db import models
from morango.models import SyncableModel

# Create your models here.
class SyncEntry(SyncableModel):
    
    name = models.CharField(max_length=100)
    
    # SyncEntry model must define a morange_model_name attribute <- SnycableModel
    morango_model_name = "sync_entry"
    
    # You must define a 'calculate_source_id' method on models that inherit from SyncableModel
    def calculate_source_id(self):
        return self.name
    
    # You must define a 'calculate_partition' method on models that inherit from SyncableModel
    def calculate_partition(self):
        return "default"
    
    def __str__(self):
        return self.name
