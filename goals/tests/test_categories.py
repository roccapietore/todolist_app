from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from core.models import User
from goals.models import GoalCategory, Board, BoardParticipant


class TestCategories(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='User', password='po324ure11')
        self.board = Board.objects.create(title='Title')
        self.category = GoalCategory.objects.create(title='Category', user=self.user, board=self.board)
        self.new_participant = BoardParticipant.objects.create(board=self.board, user=self.user, role=1)

    def tearDown(self):
        self.client.logout()
        BoardParticipant.objects.all().delete()
        GoalCategory.objects.all().delete()
        Board.objects.all().delete()
        User.objects.all().delete()

    # def test_auth_req_category(self):
    #     response = self.client.put(reverse(viewname='category_id', kwargs={'pk': self.category.pk}), {})
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('category_create'),
                                    {'title': 'category',
                                     'board': self.board.pk}
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_json = response.json()
        self.assertEqual(resp_json['title'], 'category')

    def test_category_list(self):
        url = reverse('category_list')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data is not None)

    def test_get_category_by_id(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(viewname='category_id', kwargs={'pk': self.category.pk}))
        resp_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_json['title'], 'Category')

    def test_get_404_category_by_id(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(viewname='category_id', kwargs={'pk': 100000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_category(self):
        self.client.force_login(self.user)
        response = self.client.put(reverse(viewname='category_id', kwargs={'pk': self.category.pk}),
                                   {'title': 'New_Category',  'board': self.board.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_json = response.json()
        self.assertEqual(resp_json['title'], 'New_Category')

    def test_partially_update_category(self):
        self.client.force_login(self.user)
        response = self.client.patch(reverse(viewname='category_id', kwargs={'pk': self.category.pk}),
                                     {'title': 'New_Category'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_json = response.json()
        self.assertEqual(resp_json['title'], 'New_Category')

    def test_delete_category(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse(viewname='category_id', kwargs={'pk': self.category.pk}))
        self.assertEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
