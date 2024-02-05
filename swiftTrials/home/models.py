# myapp/models.py
from django.db import models

class MyData(models.Model):
    canonical_smiles = models.CharField(max_length=255)
    inchikey = models.CharField(max_length=255)
    superclass = models.CharField(max_length=255)
    class_field = models.CharField(max_length=255)
    subclass = models.CharField(max_length=255)
    molecular_framework = models.CharField(max_length=255)
    pathway = models.CharField(max_length=255, blank=True)
