from django.shortcuts import render
from django.http import HttpResponse
from . import models
# Create your views here.
def index(request):
    
    entry = models.SyncEntry.objects.create(name="test")
    
    return HttpResponse("Hello, world. You're at the kolibro index.")