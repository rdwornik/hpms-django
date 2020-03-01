import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from main import models
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.messages import get_messages
from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

# Create your tests here.

data = [
   {
      "name":"datetime",
      "value":"2020-02-23 15:43:55"
   },
   {
      "name":"server",
      "value":"127.0.0.1:36969"
   },
   {
      "name":"HTTP_HOST",
      "value":"www.hpd.example.com"
   },
   {
      "name":"HTTP_USER_AGENT",
      "value":"Mozilla\/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko\/20100101 Firefox\/73.0"
   },
   {
      "name":"HTTP_ACCEPT",
      "value":"text\/html,application\/xhtml+xml,application\/xml;q=0.9,image\/webp,*\/*;q=0.8"
   },
   {
      "name":"HTTP_ACCEPT_LANGUAGE",
      "value":"en-US,en;q=0.5"
   },
   {
      "name":"HTTP_ACCEPT_ENCODING",
      "value":"gzip, deflate"
   },
   {
      "name":"HTTP_CONNECTION",
      "value":"keep-alive"
   },
   {
      "name":"HTTP_UPGRADE_INSECURE_REQUESTS",
      "value":"1"
   },
   {
      "name":"HTTP_CACHE_CONTROL",
      "value":"max-age=0"
   },
   {
      "name":"PATH",
      "value":"\/local\/sbin:\/usr\/local\/bin:\/usr\/sbin:\/usr\/bin:\/sbin:\/bin:\/snap\/bin"
   },
   {
      "name":"SERVER_SIGNATURE",
      "value":"Apache\/2.4.29 (Ubuntu) Server at www.hpd.example.com Port 80<\/address>\n"
   },
   {
      "name":"SERVER_SOFTWARE",
      "value":"Apache\/2.4.29 (Ubuntu)"
   },
   {
      "name":"SERVER_NAME",
      "value":"www.hpd.example.com"
   },
   {
      "name":"SERVER_ADDR",
      "value":"127.0.1.1"
   },
   {
      "name":"SERVER_PORT",
      "value":"80"
   },
   {
      "name":"REMOTE_ADDR",
      "value":"127.0.0.1"
   },
   {
      "name":"DOCUMENT_ROOT",
      "value":"\/var\/www\/hpd"
   },
   {
      "name":"REQUEST_SCHEME",
      "value":"http"
   },
   {
      "name":"CONTEXT_PREFIX",
      "value":""
   },
   {
      "name":"CONTEXT_DOCUMENT_ROOT",
      "value":"\/var\/www\/hpd"
   },
   {
      "name":"SERVER_ADMIN",
      "value":"webmaster@localhost"
   },
   {
      "name":"SCRIPT_FILENAME",
      "value":"\/var\/www\/hpd\/errors\/403.html"
   },
   {
      "name":"REMOTE_PORT",
      "value":"35466"
   },
   {
      "name":"GATEWAY_INTERFACE",
      "value":"CGI\/1.1"
   },
   {
      "name":"SERVER_PROTOCOL",
      "value":"HTTP\/1.1"
   },
   {
      "name":"REQUEST_METHOD",
      "value":"GET"
   },
   {
      "name":"QUERY_STRING",
      "value":""
   },
   {
      "name":"REQUEST_URI",
      "value":"\/errors\/403.html"
   },
   {
      "name":"SCRIPT_NAME",
      "value":"\/errors\/403.html"
   },
   {
      "name":"PHP_SELF",
      "value":"\/errors\/403.html"
   },
   {
      "name":"REQUEST_TIME_FLOAT",
      "value":1582469035.649
   },
   {
      "name":"REQUEST_TIME",
      "value":1582469035
   }
]
data2 = {"time":"2020-03-01 10:36:00",
         "server":"127.0.0.1:36969",
         "headers":[      {
            "name":"REDIRECT_REQUEST_METHOD",
            "value":"GET"
      },
         {
            "name":"REDIRECT_STATUS",
            "value":"403"
      }]
}
class HttpTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')

    def test_create_object(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/logslog/',data=data2,format='json')
        print(response.content)
        self.assertEqual(response.status_code, 201)
      #   response = self.client.post('/api/logslog/',data=data2,format='json')
      #   self.assertEqual(response.status_code, 201)
      #  self.assertEqual(models.LogsLog.objects.all().count(),66)