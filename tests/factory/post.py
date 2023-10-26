import factory
import factory.fuzzy
from blog.models import Post, Comment
from datetime import datetime
from .user import UserFactory

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.fuzzy.FuzzyText()
    text = factory.fuzzy.FuzzyText()
    created_date = factory.fuzzy.FuzzyDate(datetime.now().date())
    owner = factory.SubFactory(UserFactory)
