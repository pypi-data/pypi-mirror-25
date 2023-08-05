from django.conf import settings
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.utils import timezone
from rest_framework.test import APIClient
from ohm2_handlers_light import utils as h_utils

try:
	import simplejson as json
except Exception:
	import json




class TestCase(TestCase):

	def setUp(self):
		pass

	def test_cleaned_ohm2_address_light(self):


		params = {
			"address": {
				"country": {
					"alpha_2": "CL"
				},
				"first_level": "asdasd",
			}
		}

		try:
			p = h_utils.cleaned(params, (
				("ohm2_address_light", "address", None),
			))
			print(p)
		except Exception as e:
			print(e)
			error = True
		else:
			error = False	
		
		
		self.assertEqual(error, False)