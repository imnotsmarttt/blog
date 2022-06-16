
from .models import PostLike, BlogPost


def is_fan(obj, user) -> bool:
    """Проверяет, лайкнул ли `user` `obj`.
    """
    if not user.is_authenticated:
        return False
    likes = PostLike.objects.filter(
        user=user, post=obj)
    return likes.exists()