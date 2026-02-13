from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model with comprehensive validation.
    
    Validation rules:
    - title: Required, min 1 character, max 255, no whitespace-only strings
    - completed: Optional boolean (default False)
    """
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'title': {'trim_whitespace': True}
        }
    
    def validate_title(self, value):
        """
        Validate that title is not empty or whitespace-only.
        
        Args:
            value: The title string to validate
            
        Returns:
            str: The validated title
            
        Raises:
            ValidationError: If title is empty or whitespace-only
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty or whitespace only")
        return value.strip()
