from ..models import Post  # Use relative import

class PostFactory:
    @staticmethod
    def create_post(author, content, post_type="text"):
        """
        Creates a Post instance.

        Args:
            author: The User instance who is the author of the post.
            content: The text content of the post.
            post_type: The type of post ('text' by default). Could be expanded.

        Returns:
            A newly created Post instance.
        """
        post = Post.objects.create(author=author, content=content, post_type=post_type)
        return post