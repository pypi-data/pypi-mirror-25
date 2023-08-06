from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from parameterized import parameterized
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class SubscribeTestCase(TestCase):
    fixtures = ['lp_stripe_users']

    def setUp(self):
        self.client = APIClient()

    def authenticate(self, user=None):
        self.client.credentials()
        if user:
            token, created = Token.objects.get_or_create(user=user)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    @staticmethod
    def modify_data(data={}, exclude=[], injections={}):
        data = {**data, **injections}
        for field in exclude:
            data.pop(field, None)

        return data

    @staticmethod
    def get_default_user():
        return User.objects.get(username='derek.jeter')

    @staticmethod
    def get_admin_user():
        return User.objects.get(username='ken.griffey')

    def subscribe(self, **kwargs):
        return self.client.post(
            reverse('lp_stripe_subscriptioncreate'),
            format='json',
            **kwargs
        )

    def retrieve(self, **kwargs):
        return self.client.get(
            reverse('lp_stripe_subscriptionretrieve'),
            format='json',
            **kwargs
        )


@override_settings(STRIPE_TEST_API_KEY='sk_test_Eo1tQw3uuPrl8uG6kUZ8rjcl')
class SubscribeTestCase(SubscribeTestCase):
    PERMISSIONS = [
        ('Anonymous User', None, status.HTTP_401_UNAUTHORIZED),
        ('Authenticated User', SubscribeTestCase.get_default_user(), status.HTTP_201_CREATED),
        ('Authenticated Admin User', SubscribeTestCase.get_admin_user(), status.HTTP_201_CREATED)
    ]
    REQUIRED_FIELDS = [
        ('source', 'source'),
        ('plan', 'plan')
    ]

    def setUp(self):
        super(SubscribeTestCase, self).setUp()
        self.user = self.get_default_user()
        self.data = {
            'source': 'tok_amex',
            'plan': 'gold'
        }

    @parameterized.expand(PERMISSIONS)
    def test_permission(self, _, user, expected):
        self.authenticate(user=user)
        response = self.subscribe(data=self.data)
        self.assertEqual(response.status_code, expected)

    @parameterized.expand(REQUIRED_FIELDS)
    def test_required_field(self, _, field):
        self.authenticate(user=self.get_default_user())
        data = self.modify_data(self.data, exclude=[field])
        response = self.subscribe(data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_subscribe(self):
        self.authenticate(user=self.user)
        response = self.subscribe(data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    @override_settings(STRIPE_TEST_API_KEY=None)
    def test_missing_api_configuration(self):
        self.authenticate(user=self.user)
        response = self.subscribe(data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_retrieve_subscription(self):
        self.authenticate(user=self.user)
        self.subscribe(data=self.data)
        response = self.retrieve()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
