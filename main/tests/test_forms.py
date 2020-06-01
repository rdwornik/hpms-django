from django.test import TestCase
from main import forms, models
from main import models, factories

class TestForm(TestCase):
    def test_valid_tags_form_submit_tag(self):
        form = forms.LogsTagForm({
                "tag_name" : "localhost" ,
                "description" : "localhost"
            }
        )
        self.assertTrue(form.is_valid())
        tag = form.save()
        self.assertEquals(models.LogsTag.objects.all().count(),1)
    
    def test_invalid_tags_form_missing_field(self):
        n1 = factories.HeaderNameFactory(header_name = "VISITOR_IP")
        data = {
            'form-0-name_cryteria' : n1,
            "tag_name" : "localhost" ,
            "description" : "localhost",
            'form-TOTAL_FORMS': 1, 
            'form-INITIAL_FORMS': 0 }
        form = forms.TagCryteriaFormSet(data)
        self.assertFalse(form.is_valid())
    def test_invalid_tags_form_regex(self):
        n1 = factories.HeaderNameFactory(header_name = "VISITOR_IP")
        data = {
                'form-0-name_cryteria' : n1,
                "form-0-value_cryteria" : "*",
                "tag_name" : "localhost" ,
                "description" : "localhost",
                'form-TOTAL_FORMS': 1, 
                'form-INITIAL_FORMS': 0 }
        form = forms.TagCryteriaFormSet(data)
        self.assertFalse(form.is_valid())
