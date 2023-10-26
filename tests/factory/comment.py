import factory
import factory.fuzzy
from blog.models import Comment
from django.contrib import auth
from datetime import datetime
from .user import UserFactory
from .post import PostFactory

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.faker.Faker('name')
    text = factory.fuzzy.FuzzyText()
    created_date = factory.fuzzy.FuzzyDate(datetime.now().date())
    approved_comment = False
    post_owner = factory.SubFactory(UserFactory)
