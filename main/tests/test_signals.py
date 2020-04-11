from django.test import TestCase
from main import models, factories, signals

class TestSignal(TestCase):
    def setUp(self):
        self.n1 = factories.HeaderNameFactory(header_name="VISITORS_IP")
        self.n2 = factories.HeaderNameFactory(header_name="REQUEST_METHOD")

        self.v1 = factories.HeaderValueFactory(header_value="127.0.0.1")
        self.v2 = factories.HeaderValueFactory(header_value="127.0.1.2")
        self.v3 = factories.HeaderValueFactory(header_value="GET")
        
        self.l1 =factories.LogsLogFactory(name=self.n1, value=self.v1)
        self.l2 =factories.LogsLogFactory(name=self.n1, value=self.v2)
        self.l3 =factories.LogsLogFactory(name=self.n2, value=self.v3)
        
        self.tag1 = factories.LogsTagFactory(name_cryteria=self.n1,
                                            value_cryteria="127.*")
        self.tag2 = factories.LogsTagFactory(name_cryteria=self.n2,
                                            value_cryteria="POST")

    def test_tag_submited_on_add(self):
        signals.tag_submited.send(sender=models.LogsTagAssign, tag=self.tag1, edited=False)
        self.assertEqual(models.LogsTagAssign.objects.count(), 2)
        
        signals.tag_submited.send(sender=models.LogsTagAssign, tag=self.tag2, edited=False)
        self.assertEqual(models.LogsTagAssign.objects.count(), 2)
    
    def test_tag_submited_on_edit(self):
        models.LogsTag.objects.filter(pk=self.tag1.id).update(name_cryteria=self.n2,
                                                             value_cryteria=self.v3.header_value)
        signals.tag_submited.send(sender=models.LogsTagAssign,
                                  tag=models.LogsTag.objects.get(pk=self.tag1.id),
                                  edited=True)
        self.assertEqual(models.LogsTagAssign.objects.count(), 1)

        
        