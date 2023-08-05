from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import ugettext as _
from ohm2_handlers_light.models import GeoBaseModel
from ohm2_countries_light.models import Country
from . import managers
from . import settings




class Address(GeoBaseModel):
	country = models.ForeignKey(Country, on_delete = models.CASCADE)

	first_level = models.CharField(max_length = settings.STRING_NORMAL, null = True, blank = True, default = "")
	second_level = models.CharField(max_length = settings.STRING_NORMAL, null = True, blank = True, default = "")
	third_level = models.CharField(max_length = settings.STRING_NORMAL, null = True, blank = True, default = "")
	fourth_level = models.CharField(max_length = settings.STRING_NORMAL, null = True, blank = True, default = "")

	street = models.CharField(max_length = settings.STRING_NORMAL)
	number = models.CharField(max_length = settings.STRING_NORMAL)

	floor = models.CharField(max_length = settings.STRING_NORMAL, null = True, blank = True, default = "")
	tower = models.CharField(max_length = settings.STRING_NORMAL, null = True, blank = True, default = "")
	block = models.CharField(max_length = settings.STRING_NORMAL, null = True, blank = True, default = "")

	coordinates = models.PointField(srid = settings.SRID, null = True, blank = True, default = None)

	