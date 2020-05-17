from django.test import TestCase
from main import forms, models

class TestForm(TestCase):
    def test_valid_tags_form_submit_tag(self):
        form = forms.TagForm({
                "name_cryteria" : models.HeaderName.objects.create(header_name="VISITORS_IP"),
                "value_cryteria" : "127.*" ,
                "tag" : "localhost" ,
                "description" : "localhost"
            }
        )
        self.assertTrue(form.is_valid())
        tag = form.save()
        self.assertEquals(models.LogsTag.objects.all().count(),1)
    
    def test_invalid_tags_form_missing_field(self):
        form = forms.TagForm({
                "name_cryteria" : models.HeaderName.objects.create(header_name="VISITORS_IP"),
                "description" : "none"
        })
        self.assertFalse(form.is_valid())
    def test_invalid_tags_form_regex(self):
        form = forms.TagForm({
                "name_cryteria" : models.HeaderName.objects.create(header_name="VISITORS_IP"),
                "value_cryteria" : "*" ,
                "tag" : "localhost" ,
                "description" : "localhost"
            }
        )
        self.assertFalse(form.is_valid())
