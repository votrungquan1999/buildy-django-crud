from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from todos.models import Task


class TaskAPITestCase(TestCase):
    """
    Integration tests for Task API following TDD principles.
    Tests follow red-green-refactor cycle.
    """

    def setUp(self):
        """Set up test client and initial data."""
        self.client = APIClient()
        self.list_url = '/api/tasks/'

    def test_list_empty_tasks(self):
        """
        Test listing tasks when database is empty.
        
        Validates:
        - GET /api/tasks/ returns 200
        - Response is an empty list
        """
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_create_task(self):
        """
        Test creating a new task.
        
        Validates:
        - POST /api/tasks/ with valid data returns 201
        - Response contains id, title, completed fields
        - Task is created with correct values
        - completed defaults to False
        """
        data = {
            'title': 'Test task',
            'completed': False
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertIn('id', response_data)
        self.assertEqual(response_data['title'], 'Test task')
        self.assertEqual(response_data['completed'], False)
        self.assertIn('created_at', response_data)

    def test_list_tasks_with_data(self):
        """
        Test listing tasks when database contains data.
        
        Validates:
        - GET /api/tasks/ returns all tasks
        - Response contains correct number of tasks
        """
        # Create test data
        Task.objects.create(title='Task 1', completed=False)
        Task.objects.create(title='Task 2', completed=True)
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tasks = response.json()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['title'], 'Task 1')
        self.assertEqual(tasks[1]['title'], 'Task 2')

    def test_update_task_title(self):
        """
        Test updating task title.
        
        Validates:
        - PUT /api/tasks/{id}/title/ returns 200
        - Title is updated correctly
        - Other fields remain unchanged
        """
        task = Task.objects.create(title='Original title', completed=False)
        url = f'/api/tasks/{task.id}/title/'
        data = {'title': 'Updated title'}
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated title')
        self.assertEqual(task.completed, False)

    def test_toggle_task_completion(self):
        """
        Test toggling task completion status.
        
        Validates:
        - POST /api/tasks/{id}/toggle/ returns 200
        - Completion status toggles from False to True
        - Multiple toggles work correctly (idempotency)
        """
        task = Task.objects.create(title='Test task', completed=False)
        url = f'/api/tasks/{task.id}/toggle/'
        
        # First toggle: False -> True
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.completed, True)
        
        # Second toggle: True -> False
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.completed, False)

    def test_delete_task(self):
        """
        Test deleting a task.
        
        Validates:
        - DELETE /api/tasks/{id}/ returns 204
        - Task is removed from database
        """
        task = Task.objects.create(title='Task to delete', completed=False)
        url = f'/api/tasks/{task.id}/'
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_update_title_nonexistent_task(self):
        """
        Test updating title of non-existent task.
        
        Validates:
        - PUT /api/tasks/999/title/ returns 404
        """
        url = '/api/tasks/999/title/'
        data = {'title': 'New title'}
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_toggle_nonexistent_task(self):
        """
        Test toggling non-existent task.
        
        Validates:
        - POST /api/tasks/999/toggle/ returns 404
        """
        url = '/api/tasks/999/toggle/'
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task_empty_title(self):
        """
        Test creating task with empty title.
        
        Validates:
        - POST with empty title returns 400
        - Validation error message is present
        """
        data = {'title': '', 'completed': False}
        
        response = self.client.post(self.list_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.json())
