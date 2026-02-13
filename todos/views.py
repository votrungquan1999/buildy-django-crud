from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task CRUD operations with custom actions.
    
    Endpoints:
    - GET /api/tasks/ - List all tasks
    - POST /api/tasks/ - Create a new task
    - PUT /api/tasks/{id}/title/ - Update task title
    - POST /api/tasks/{id}/toggle/ - Toggle completion status
    - DELETE /api/tasks/{id}/ - Delete a task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    # Disable default retrieve, update, partial_update
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']
    
    def retrieve(self, request, *args, **kwargs):
        """Disable retrieve endpoint."""
        return Response(
            {"detail": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def update(self, request, *args, **kwargs):
        """Disable generic update endpoint."""
        return Response(
            {"detail": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def partial_update(self, request, *args, **kwargs):
        """Disable generic partial update endpoint."""
        return Response(
            {"detail": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    @action(detail=True, methods=['put'], url_path='title')
    def update_title(self, request, pk=None):
        """
        Update task title only.
        
        PUT /api/tasks/{id}/title/
        Body: {"title": "New title"}
        """
        task = self.get_object()
        title = request.data.get('title')
        
        if not title:
            return Response(
                {"title": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.title = title
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='toggle')
    def toggle(self, request, pk=None):
        """
        Toggle task completion status.
        
        POST /api/tasks/{id}/toggle/
        """
        task = self.get_object()
        task.completed = not task.completed
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)
