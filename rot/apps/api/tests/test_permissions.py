# -*- coding: utf-8 -*-
from model_mommy import mommy
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from person.models import Person


class ItemPermissionAPITestCase(APITestCase):
    fixtures = ['groups', 'test_users', 'applications']

    def setUp(self):
        self.super_user = Person.objects.get(pk=1)
        self.standard_user = Person.objects.get(pk=2)
        self.adminuser = Person.objects.get(pk=3)
        self.edit_user = Person.objects.get(pk=4)

        self.cat = mommy.make('register.Category')
        self.ba = mommy.make('register.BusinessArea')

    def _create_item(self, user):
        return mommy.make(
            'register.Item',
            categories=[self.cat],
            areas=[self.ba],
            owner=user,
            created_by=user)

    def asserUpdatePermission(self, url, data):
        resp = self.client.patch(url, data)
        self.assertEqual(resp.status_code, 200, 'Owner can update')

    def assertDeletePermission(self, url):
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 204, 'Owner can delete')

    def assertPatchNotAuthenticated(self, url, code=401):
        resp = self.client.patch(url)
        self.assertEqual(resp.status_code, code, 'Can not patch')

    def _test_user_permission(self, user, obj):
        url = reverse('item-list')

        resp = self.client.get(url)

        data = resp.json()
        data['Namme'] = 'New Name'

        url = reverse('item-detail', args=[obj.pk])

        self.assertPatchNotAuthenticated(url)

        self.client.force_authenticate(user)
        self.asserUpdatePermission(url, data)
        self.assertDeletePermission(url)
        
    def test_standard_user_has_object_permissions_on_own_item(self):
        item = self._create_item(self.standard_user)
        self._test_user_permission(self.standard_user, item)

    def test_edit_user_has_object_permissions_on_all_items(self):
        item = self._create_item(self.standard_user)
        self._test_user_permission(self.edit_user, item)

    def test_super_user_has_object_permissions_on_all_items(self):
        item = self._create_item(self.standard_user)
        self._test_user_permission(self.edit_user, item)

    def test_standard_user_has_no_permission(self):
        item = self._create_item(self.edit_user)

        url = reverse('item-list')

        resp = self.client.get(url)

        data = resp.json()
        data['Namme'] = 'New Name'

        url = reverse('item-detail', args=[item.pk])

        self.client.force_authenticate(self.standard_user)
        self.assertPatchNotAuthenticated(url, 403)



