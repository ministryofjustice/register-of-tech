from model_mommy import mommy
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class BusinessAreaViewSetAPITestCase(APITestCase):
    def setUp(self):
        self.fixture = mommy.make('register.BusinessArea')

    def test_detail(self):
        response = self.client.get(reverse('area-detail', (self.fixture.id,)))
        self.assertEqual(set('id name description parent_id'.split()), response.data.keys())

    def test_list(self):
        response = self.client.get(reverse('area-list'))
        self.assertEqual(set('id name description parent_id'.split()), response.data['results'][0].keys())


class CategoryViewSetAPITestCase(APITestCase):
    def setUp(self):
        self.fixture = mommy.make('register.Category')

    def test_detail(self):
        response = self.client.get(reverse('category-detail', (self.fixture.id,)))
        self.assertEqual(set('id name parent_id'.split()), response.data.keys())

    def test_list(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(set('id name parent_id'.split()), response.data['results'][0].keys())


class PeopleViewSetAPITestCase(APITestCase):
    def setUp(self):
        self.fixture = mommy.make('person.Person')

    def test_detail(self):
        response = self.client.get(reverse('people-detail', (self.fixture.id,)))
        self.assertEqual(set('id first_name last_name email role peoplefinder'.split()), response.data.keys())

    def test_list(self):
        response = self.client.get(reverse('people-list'))
        self.assertEqual(set('id first_name last_name email role peoplefinder'.split()),
                         response.data['results'][0].keys())


class ItemViewSetAPITestCase(APITestCase):
    def setUp(self):
        self.fixture = mommy.make('register.Item')

    def test_detail(self):
        response = self.client.get(reverse('item-detail', (self.fixture.id,)))
        self.assertEqual(set('id name description categories areas owner'.split()), response.data.keys())

    def test_list(self):
        response = self.client.get(reverse('item-list'))
        self.assertEqual(set('id name description categories areas owner'.split()),
                         response.data['results'][0].keys())
