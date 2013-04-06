from django.contrib import admin
from django.utils.translation import gettext as _
from donation import models


admin.site.register(models.Donation)