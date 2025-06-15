from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class MyPlanningApiTestCase(APITestCase):
    def test_get_sprints(self):
        url = reverse('sprints')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0, msg="No items in project list")

        first_item = data[0]

        expected_keys = {'id', 'state', 'name', 'goal', 'createdDate'}
        self.assertTrue(expected_keys.issubset(first_item.keys()))

        # current sprint is active
        self.assertEqual(first_item['state'], 'active')

    def test_get_issue(self):
        url = reverse('issue', kwargs={'id': 35231})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('fields', response.data)

        self.assertIn('sprint', response.data.get('fields'))

        self.assertEqual(519, response.data.get('fields').get('sprint').get('id'))

    def test_get_issues_by_user(self):
        url = reverse('issues-by-users')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0, msg="No items in project list")

        first_item = data[0]

        expected_keys = {'id', 'name', 'issues'}
        self.assertTrue(expected_keys.issubset(first_item.keys()))

        expected_issues_keys = {'id', 'title', 'description', 'epic'}
        self.assertTrue(expected_issues_keys.issubset(first_item.get('issues')[0]))
