from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser  # Import permissions
from rest_framework.views import APIView
from .serializers import UserSerializer, PostSerializer, CommentSerializer  # Import all serializers
from .models import Post, Comment  # Import Post and Comment models
from .permissions import IsPostAuthor  # Import custom permission


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow anyone to create a user initially
def create_user(request):
    """
    Creates a new user.  Uses Django's create_user method for password hashing.
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Use create_user to handle password hashing
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']  # Pass the password
            )
            return Response({'id': user.id, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    permission_classes = [IsAdminUser]  # Only admins can list users

    def get(self, request):
        """
        Retrieves a list of all users.  Only accessible to admin users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserUpdate(APIView):
    permission_classes = [IsAdminUser]  # Only admins can update users

    def put(self, request, id):
        """
        Updates an existing user.  Only accessible to admin users.
        Uses set_password for password updates.
        """
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            # Update email if provided
            if 'email' in serializer.validated_data:
                user.email = serializer.validated_data['email']

            # Update password if provided. Use set_password()
            if 'password' in serializer.validated_data:
                user.set_password(serializer.validated_data['password'])

            user.save()
            return Response({'message': 'User updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDelete(APIView):
    permission_classes = [IsAdminUser]  # Only admins can delete users

    def delete(self, request, id):
        """
        Deletes a user. Only accessible to admin users.
        """
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'message': 'User deleted successfully'})

class PostListCreate(APIView):
    permission_classes = [IsAuthenticated] # Only authenticated users to view/create

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # Associate the post with the currently logged-in user
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor] # Check authentication and ownership

    def get_object(self, pk): # Helper function to get a Post, and check permissions
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self, request, post) #DRF built-in function
            return post
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_object(pk)
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListCreate(APIView):
    permission_classes = [IsAuthenticated] # Only authenticated users to comment
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # Associate the comment with the currently logged-in user
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)