from rest_framework import serializers
from .models import User, Post, Comment  # Import all models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'date_joined']  # Use 'date_joined'
        extra_kwargs = {'password': {'write_only': True},
                        'date_joined': {'read_only': True}} # Make date_joined read-only

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.StringRelatedField(many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True) # Read-only author

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'created_at', 'comments']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)  # Read-only author
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all()) #Ensure post exists

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']

    def validate_post(self, value):
        """
        Check that the post exists.
        """
        if not Post.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Post not found.")
        return value