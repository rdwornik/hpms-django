from decimal import Decimal
from django.urls import reverse


from django.contrib.staticfiles.testing import (
StaticLiveServerTestCase
)
from django.contrib.auth.models import User

from main import models, factories
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.wait import WebDriverWait

class FrontendTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.timeout = 2
        options = Options()
        options.headless = True
        # cls.selenium = webdriver.Firefox(options=options)
        binary = FirefoxBinary('/opt/firefox/firefox')
        cls.selenium = webdriver.Firefox(options=options,firefox_binary=binary)
        cls.selenium.implicitly_wait(10)
        cls.user = User.objects.create_superuser(
            username="admin",
           password="adminadmin",
            email="admin@example.com"
        )
        cls.user.save()
        cls.n1 = factories.HeaderNameFactory(header_name="VISITORS_IP")
        cls.v1 = factories.HeaderValueFactory(header_value="127.0.0.1")
        cls.v2 = factories.HeaderValueFactory(header_value="127.0.1.2")
        cls.v3 = factories.HeaderValueFactory(header_value="128.0.0.1")
        cls.t1=factories.TransactionFactory()
        cls.t2=factories.TransactionFactory()
        cls.t3=factories.TransactionFactory()

        cls.l1 =factories.LogsLogFactory(name=cls.n1,transaction=cls.t1, value=cls.v1)
        cls.l2 =factories.LogsLogFactory(name=cls.n1,transaction=cls.t2,value=cls.v2)
        cls.l3 =factories.LogsLogFactory(name=cls.n1,transaction=cls.t3, value=cls.v3)
    
    def login(self):
        self.selenium.get('%s%s' % (self.live_server_url, reverse("login")))
        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('adminadmin')
        self.selenium.find_element_by_id('login-button').click()
        WebDriverWait(self.selenium, self.timeout).until(
        lambda driver: driver.find_element_by_tag_name('body'))
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def test_transaction_detail_loaded(self):
        # self.selenium.find_element_by_css_selector("tbody > tr > td > a").click()
        self.login()
        self.selenium.get('%s%s' % (self.live_server_url, reverse("transactions")))
        print(self.selenium.current_url)
    def test_visitor_link_loaded(self):
        self.login()
        self.selenium.get('%s%s' % (self.live_server_url, reverse("visitors")))
        self.selenium.find_element_by_css_selector("tbody > tr > td > a").click()
        WebDriverWait(self.selenium, self.timeout).until(
        lambda driver: driver.find_element_by_tag_name('body'))
        transaction_url = "{}{}?ip=1".format(self.live_server_url, reverse("transactions"))
        self.assertEqual(transaction_url,self.selenium.current_url)
