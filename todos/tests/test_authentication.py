from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from todos.models import Task


# Valid credentials
API_KEY = "buildy-api-key-2026"
API_SECRET = "buildy-secret-2026"


class AuthenticationTestCase(TestCase):
    """
    Comprehensive test suite for API key authentication.
    
    Tests cover:
    - Missing credentials scenarios
    - Invalid credentials scenarios
    - Valid credentials scenario
    - Per-endpoint authentication requirements
    """
    
    def setUp(self):
        self.client = APIClient()
        self.task = Task.objects.create(title="Test task", completed=False)
        
    # Missing Credentials Tests
    
    def test_missing_both_headers(self):
        """Test that requests without any auth headers return 401."""
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_missing_api_key_header(self):
        """Test that requests without X-API-Key header return 401."""
        response = self.client.get(
            '/api/tasks/',
            HTTP_X_API_SECRET=API_SECRET
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('X-API-Key', response.data['detail'])
    
    def test_missing_api_secret_header(self):
        """Test that requests without X-API-Secret header return 401."""
        response = self.client.get(
            '/api/tasks/',
            HTTP_X_API_KEY=API_KEY
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('X-API-Secret', response.data['detail'])
    
    # Invalid Credentials Tests
    
    def test_invalid_api_key(self):
        """Test that requests with wrong API key return 401."""
        response = self.client.get(
            '/api/tasks/',
            HTTP_X_API_KEY='wrong-key',
            HTTP_X_API_SECRET=API_SECRET
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Invalid API key', response.data['detail'])
    
    def test_invalid_api_secret(self):
        """Test that requests with wrong API secret return 401."""
        response = self.client.get(
            '/api/tasks/',
            HTTP_X_API_KEY=API_KEY,
            HTTP_X_API_SECRET='wrong-secret'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Invalid API secret', response.data['detail'])
    
    def test_invalid_both_credentials(self):
        """Test that requests with both credentials wrong return 401."""
        response = self.client.get(
            '/api/tasks/',
            HTTP_X_API_KEY='wrong-key',
            HTTP_X_API_SECRET='wrong-secret'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # Valid Credentials Test
    
    def test_valid_credentials(self):
        """Test that requests with valid credentials return 200."""
        response = self.client.get(
            '/api/tasks/',
            HTTP_X_API_KEY=API_KEY,
            HTTP_X_API_SECRET=API_SECRET
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Per-Endpoint Authentication Tests
    
    def test_list_tasks_requires_auth(self):
        """Test that GET /api/tasks/ requires authentication."""
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_task_requires_auth(self):
        """Test that POST /api/tasks/ requires authentication."""
        response = self.client.post(
            '/api/tasks/',
            {'title': 'New task', 'completed': False},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_title_requires_auth(self):
        """Test that PUT /api/tasks/{id}/title/ requires authentication."""
        response = self.client.put(
            f'/api/tasks/{self.task.id}/title/',
            {'title': 'Updated title'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_toggle_requires_auth(self):
        """Test that POST /api/tasks/{id}/toggle/ requires authentication."""
        response = self.client.post(f'/api/tasks/{self.task.id}/toggle/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_task_requires_auth(self):
        """Test that DELETE /api/tasks/{id}/ requires authentication."""
        response = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
