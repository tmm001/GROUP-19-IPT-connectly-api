from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .models import Post, Comment
from .permissions import IsPostAuthor
from .factories.post_factory import PostFactory  # Import the factory
from .singletons.logger_singleton import LoggerSingleton  # Import the logger

logger = LoggerSingleton().get_logger()  # Get the logger instance


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """
    Creates a new user. Uses Django's create_user method for password hashing.
    """
    logger.info(f"Attempting to create user: {request.data.get('username')}")  # Log user creation attempt
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            logger.info(f"User created successfully: {user.username} (ID: {user.id})")  # Log success
            return Response({'id': user.id, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        logger.warning(f"Invalid user creation attempt: {serializer.errors}")  # Log validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        Retrieves a list of all users. Only accessible to admin users.
        """
        logger.info("Retrieving user list (admin only)")  # Log user list retrieval
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserUpdate(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, id):
        """
        Updates an existing user. Only accessible to admin users.
        Uses set_password for password updates.
        """
        logger.info(f"Attempting to update user with ID: {id}")  # Log user update attempt
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            logger.warning(f"User update attempt failed: User with ID {id} not found")  # Log user not found
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if 'email' in serializer.validated_data:
                user.email = serializer.validated_data['email']
            if 'password' in serializer.validated_data:
                user.set_password(serializer.validated_data['password'])
            user.save()
            logger.info(f"User updated successfully: {user.username} (ID: {user.id})")  # Log success
            return Response({'message': 'User updated successfully'})
        logger.warning(f"Invalid user update attempt: {serializer.errors}")  # Log validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDelete(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        """
        Deletes a user. Only accessible to admin users.
        """
        logger.info(f"Attempting to delete user with ID: {id}")  # Log user deletion attempt
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            logger.warning(f"User deletion attempt failed: User with ID {id} not found")  # Log user not found
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        logger.info(f"User deleted successfully: {user.username} (ID: {user.id})")  # Log success
        return Response({'message': 'User deleted successfully'})


class PostListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"Retrieving all posts for user: {request.user.username}") # Log
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = PostFactory.create_post(
                author=request.user,
                content=serializer.validated_data['content'],
                post_type=serializer.validated_data.get('post_type', 'text') # Get post_type
            )
            logger.info(f"Post created by {request.user.username} with id {post.id}")  # Log post creation
            return_serializer = PostSerializer(post)
            return Response(return_serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Invalid post creation attempt: {serializer.errors}")  # Log validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self, request, post)
            return post
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        logger.info(f"Retrieving post with ID: {pk} for user {request.user.username}")
        post = self.get_object(pk)
        if post is None:
            logger.warning(f"Post retrieval failed. Post with id {pk} not found, or unauthorized access.")
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        logger.info(f"Attempting to update post with ID: {pk} by user {request.user.username}")
        post = self.get_object(pk)
        if post is None:
            logger.warning(f"Post update failed. Post with id {pk} not found, or unauthorized access.")
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Post with ID: {pk} updated successfully by user {request.user.username}")
            return Response(serializer.data)
        logger.warning(f"Invalid post update attempt: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        logger.info(f"Attempting to delete post with ID: {pk} by user {request.user.username}")
        post = self.get_object(pk)
        if post is None:
            logger.warning(f"Post deletion failed. Post with id {pk} not found, or unauthorized access.")
            return Response(status=status.HTTP_404_NOT_FOUND)
        post.delete()
        logger.info(f"Post with ID: {pk} deleted successfully by user {request.user.username}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"Retrieving all comments for user: {request.user.username}")
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            logger.info(f"Comment created by {request.user.username} on post {serializer.validated_data['post']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(f"Invalid comment creation attempt: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)