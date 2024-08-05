from rest_framework import serializers
from .models import Book, UserInteraction

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = '__all__'

    def validate_book(self, value):
        """
        Ensure the book entry exists.
        """
        if not Book.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Book entry does not exist.")
        return value
