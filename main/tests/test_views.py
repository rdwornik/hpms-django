from django.test import TestCase
from unittest.mock import patch
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from main import forms, models, factories


class TestPage(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            password="adminadmin",
            email="admin@example.com"
        )
        self.client.force_login(self.user)


    def test_home_page_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'HPMS')

    def test_tags_add_page_loads_correctly(self):
        response = self.client.get(reverse("action_tag_add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tags_action.html")
        self.assertIsInstance                                                                                                                                   (
            response.context["form"], forms.TagForm
        )
    def test_tags_action_submission_works(self):
        n1 = factories.HeaderNameFactory(header_name='VISITORS_IP')
        v1 = factories.HeaderValueFactory(header_value='127.0.0.1')
        v2 = factories.HeaderValueFactory(header_value='127.0.0.2')
        v3 = factories.HeaderValueFactory(header_value='128.0.0.1')

        l1 =factories.LogsLogFactory(name=n1, value=v1)
        l2 =factories.LogsLogFactory(name=n1, value=v2)
        l3 =factories.LogsLogFactory(name=n1, value=v3)

        post_data ={
                'name_cryteria' : n1.id ,
                'value_cryteria' : '127.*' ,
                'tag' : 'localhost' ,
                'description' : 'localhost'
        }
        response = self.client.post(
                reverse("action_tag_add"), post_data
            )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            models.LogsTag.objects.filter(
                tag="localhost"
            ).exists()
        )
        self.assertEqual(
            models.LogsTagAssign.objects.count(),
            2
        )
