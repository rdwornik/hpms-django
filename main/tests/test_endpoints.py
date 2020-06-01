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
         "name":"VISITOR_IP",
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
         "name":"VISITOR_IP",
         "value":"128.0.0.1"
      },
      {
         "name":"REDIRECT_STATUS",
         "value":"403"
      }]
}

data3 = {
  "headers": [{
      "name": "REQUEST_TIME",
      "value": 1588863521
    },
    {
      "name": "[GET]",
      "value": "key: name value: John"
    },
    {
      "name": "[GET]",
      "value": "key: name value: Matt"
    },
    {
      "name": "[GET]",
      "value": "key: second_name value: Tom"
    }
  ]
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
      n1 = factories.HeaderNameFactory(header_name = "VISITOR_IP")
      n2 = factories.HeaderNameFactory(header_name = "REDIRECT_STATUS")
      c1 = factories.TagCryteriaFactory(
         name_cryteria = n1,
         value_cryteria = "127\.*"
      )
      c2 = factories.TagCryteriaFactory(
         name_cryteria = n2,
         value_cryteria = "403"
      )
      t1 = factories.LogsTagFactory(tag_name="test")
      t1.cryterias.add(c1,c2)
      response = self.client.post("/hpms/api/logslogs/",data=data1,format="json")
      self.assertEqual(response.status_code, 201)
      self.assertEqual(models.LogsLog.objects.count(),2)
      
      response = self.client.post("/hpms/api/logslogs/",data=data2,format="json")
      self.assertEqual(response.status_code, 201)
      self.assertEqual(models.LogsLog.objects.count(),4)
      
      self.assertEqual(models.LogsTagAssign.objects.count(),1)
      
   def test_create_object2(self):
      response = self.client.post("/hpms/api/logslogs/",data=data3,format="json")
      self.assertEqual(response.status_code, 201)
      self.assertEqual(models.LogsLog.objects.count(),4)