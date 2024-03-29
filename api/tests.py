from django.test import TestCase
from .models import Bucketlist
from rest_framework import status 
from rest_framework.test import APIClient
from django.urls import reverse


class ModelTestCase(TestCase):
    def setUp(self) -> None:
        self.name = "world class"
        self.bucketlist = Bucketlist(name = self.name)

    def test_model_can_create_a_bucketlist(self):

        old_count = Bucketlist.objects.count()
        self.bucketlist.save()
        new_count = Bucketlist.objects.count()
        self.assertNotEqual(old_count,new_count)

class ViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.data = {'name':'IBIZA'}
        self.response = self.client.post(reverse('create'), self.data , format="json")

    def test_api_can_create_a_bucketlist(self):
        self.assertEqual(self.response.status_code , status.HTTP_201_CREATED)
    
    def test_api_can_get_a_bucketlist(self):
        """Test the api can get a given bucketlist."""
        bucketlist = Bucketlist.objects.get()
        print(bucketlist.id)
        response = self.client.get(
            reverse('details',
            kwargs={'pk': bucketlist.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bucketlist)

    def test_api_can_update_bucketlist(self):
        """Test the api can update a given bucketlist."""
        print(self)
        change_bucketlist = {'name': 'Something new'}
        res = self.client.put(
            reverse('details', kwargs={'pk': 1}),
            change_bucketlist, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_bucketlist(self):
        """Test the api can delete a bucketlist."""
        
        bucketlist = Bucketlist.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': bucketlist.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
    