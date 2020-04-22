import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from main import models, factories
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.messages import get_messages
from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

# Create your tests here.
data1 = {
   "headers":[
      {
         "name":"VISITORS_IP",
         "value":"127.0.0.1"
      },
      {
         "name":"REDIRECT_STATUS",
         "value":"403"
      }]
}
data2 = {
   "headers":[
      {
         "name":"VISITORS_IP",
         "value":"128.0.0.1"
      },
      {
         "name":"REDIRECT_STATUS",
         "value":"403"
      }]
}
class TestEndpoints(APITestCase):
   def setUp(self):
      self.user = User.objects.create_superuser(
            username="admin",
            password="adminadmin",
            email="admin@example.com"
        )
      self.client.force_authenticate(self.user)

   def test_create_object(self):
      n1 = factories.HeaderNameFactory(header_name = "VISITORS_IP")
      t1 = factories.LogsTagFactory(
         name_cryteria = n1,
         value_cryteria = "127.*"
      )
      
      response = self.client.post("/hpms/api/logslogs/",data=data1,format="json")
      self.assertEqual(response.status_code, 201)
      self.assertEqual(models.LogsLog.objects.count(),2)
      response = self.client.post("/hpms/api/logslogs/",data=data2,format="json")
      self.assertEqual(response.status_code, 201)
      self.assertEqual(models.LogsLog.objects.count(),4)
      self.assertEqual(models.LogsTagAssign.objects.count(),1)