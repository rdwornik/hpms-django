from django.test import TestCase
from unittest.mock import patch
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from main import forms, models, factories
from django.test import Client
from django.db.models import Q

class TestPage(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="admin",
            password="adminadmin",
            email="admin@example.com"
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.n1 = factories.HeaderNameFactory(header_name="VISITOR_IP")
        self.n2 = factories.HeaderNameFactory(header_name = "REDIRECT_STATUS")
        self.v1 = factories.HeaderValueFactory(header_value="127.0.0.1")
        self.v2 = factories.HeaderValueFactory(header_value="127.0.1.2")
        self.v3 = factories.HeaderValueFactory(header_value="128.0.0.1")
        self.v4 = factories.HeaderValueFactory(header_value="403")
        self.t1=factories.TransactionFactory()
        self.t2=factories.TransactionFactory()
        self.t3=factories.TransactionFactory()

        self.l1 =factories.LogsLogFactory(name=self.n1,transaction=self.t1, value=self.v1)
        self.l2 =factories.LogsLogFactory(name=self.n2,transaction=self.t1,value=self.v4)
        
        self.l4 =factories.LogsLogFactory(name=self.n1,transaction=self.t2,value=self.v2)
        self.l5 =factories.LogsLogFactory(name=self.n1,transaction=self.t3, value=self.v3)
        
    def test_transactions_page_works(self):
        response = self.client.get(reverse("transactions"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transactions.html")
        self.assertContains(response, "Transactions")
      
    def test_transactions_detail_page_works(self):
        response = self.client.get(reverse("transactions_detail",args=[self.t1.logslog_set.get(Q(name=self.n1)).value_id,self.t1.transaction]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "transactions_detail.html")
        self.assertContains(response, "Transaction {}".format(self.l1.transaction_id))
    
    def test_tags_page_works(self):
        response = self.client.get(reverse("tags"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tags.html")
        self.assertContains(response, "Tags")

    def test_tag_add_form_page_works(self):
        response = self.client.get(reverse("tags_add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tags_form.html")
        self.assertIsInstance(
            response.context["form"], forms.LogsTagForm
        )
        self.assertIsInstance(
            response.context["formset"], forms.TagCryteriaFormSet
        )
    
    def test_tag_edit_form_page_works(self):
        c1 = factories.TagCryteriaFactory(
            name_cryteria = self.n1,
            value_cryteria = "127\.*"
        )
        tag = factories.LogsTagFactory(tag_name="test")
        tag.cryterias.add(c1)
        response = self.client.get(reverse("tags_edit",args=[tag.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tags_form.html")
        self.assertIsInstance(
            response.context["form"], forms.LogsTagForm
        )
        self.assertIsInstance(
            response.context["formset"], forms.TagCryteriaFormSet
        )

    def test_visitors_page_works(self):
        response = self.client.get(reverse("visitors"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "visitors.html")
        self.assertContains(response, "Visitors")
    
    def test_search_page_works(self):
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search.html")
        self.assertContains(response, "Search")
        
    def test_logout_page_works(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "logout.html")
        self.assertContains(response, "You have been logout")
    
    def test_all_notes_page_works(self):
        response = self.client.get(reverse("all_notes"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "all_notes.html")
        self.assertContains(response, "All notes")
    
    def test_activity_page_works(self):
        response = self.client.get(reverse("activity"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "activity.html")
        self.assertContains(response, "Activity")
    
    def test_tag_add_works(self):
        post_data ={
                'form-0-name_cryteria' : self.n1.id,
                "form-0-value_cryteria" : "127\.*",
                "tag_name" : "localhost" ,
                "description" : "localhost",
                'form-TOTAL_FORMS': 1, 
                'form-INITIAL_FORMS': 0 
        }
        response = self.client.post(
                reverse("tags_add"), post_data
            )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            models.LogsTag.objects.filter(
                tag_name="localhost"
            ).exists()
        )

    def test_tag_delete_works(self):
        c1 = factories.TagCryteriaFactory(
            name_cryteria = self.n1,
            value_cryteria = "127\.*"
        )
        tag = factories.LogsTagFactory(tag_name="test")
        tag.cryterias.add(c1)
        
        post_data = {
                "select" : "delete_selected",
                "selected_tags":[tag.id]
        }
        response = self.client.post(
            reverse("tags"), post_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            models.LogsTag.objects.count(),
            0
        )
        
    def test_tag_edit_works(self):
        c1 = factories.TagCryteriaFactory(
            name_cryteria = self.n1,
            value_cryteria = "127\.*"
        )
        tag = factories.LogsTagFactory(tag_name="test")
        tag.cryterias.add(c1)
        
        post_data ={
                'form-0-name_cryteria' : self.n1.id,
                "form-0-value_cryteria" : c1.value_cryteria ,
                "tag_name" : "localhost" ,
                "description" : "localhost",
                'form-TOTAL_FORMS': 1, 
                'form-INITIAL_FORMS': 0 
        }     
        response = self.client.post(
                reverse("tags_edit", 
                        args=[tag.id]
                        ),
                post_data
        )
        self.assertEquals(response.status_code,302)
        self.assertEqual(models.LogsTag.objects.get(pk=tag.id).tag_name, "localhost")
        self.assertEqual(
            models.LogsTag.objects.count(),
            1
        )