import factory
import factory.fuzzy
from blog.models import Post, Comment
from django.contrib import auth
from datetime import datetime


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = auth.get_user_model()

    username = factory.faker.Faker('name')
    password = "test"


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.fuzzy.FuzzyText()
    text = factory.fuzzy.FuzzyText()
    created_date = factory.fuzzy.FuzzyDate(datetime.now().date())
    published_date = factory.fuzzy.FuzzyDate(datetime.now().date())
    owner = factory.SubFactory(UserFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    text = factory.fuzzy.FuzzyText()
    created_date = factory.fuzzy.FuzzyDate(datetime.now().date())
    approved_comment = factory.faker.Faker('boolean')
    post_owner = factory.SubFactory(UserFactory)

