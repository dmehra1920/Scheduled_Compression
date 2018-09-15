# -*- coding: utf-8 -*-

# Create your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class spm(models.Model):
    activity= models.CharField(max_length= 200)
    orignal_duration= models.IntegerField()
    orignal_resources= models.IntegerField()
    orignal_cost= models.IntegerField()
    additional_resources= models.IntegerField()
    additional_cost= models.IntegerField()
    crash_duration_days = models.IntegerField()
    time_saved = models.IntegerField()
    total_cost = models.IntegerField()
    def __str__(self):
        return self.activity
