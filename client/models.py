from django.db import models
from morango.models import SyncableModel
from morango.models import Certificate



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
    


    class ScopeDefinitions(object):
        """
        Class contains morango scope definition constants for certificates.
        """

        SERVER = "server"
        CLIENT = "client"
        
    def calculate_source_id(self):
        # if we don't already have a source ID, get one by generating a new root certificate, and using its ID
        if not self._morango_source_id:
            self._morango_source_id = Certificate.generate_root_certificate(
                SyncEntry.ScopeDefinitions.SERVER
            ).id
        return self._morango_source_id