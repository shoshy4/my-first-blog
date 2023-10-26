import pytest
from tests.factory.post import PostFactory
from datetime import datetime


@pytest.fixture
def post():
    post = PostFactory()
    post.published_date = datetime.now().date()
    post.save()
    return post


@pytest.fixture
def post_1():
    post = PostFactory()
    post.id = 1
    post.save()
    return post


@pytest.fixture
def post2(user2):
    post = PostFactory(owner=user2, author=user2)
    post.published_date = datetime.now().date()
    post.save()
    return post

@pytest.fixture
def posts():
    posts = []
    for ix in range(4):
        post = PostFactory()
        post.published_date = datetime.now().date()
        post.save()
        posts.append(post)
    return posts


@pytest.fixture
def drafts():
    drafts = []
    for ix in range(4):
        drafts.append(PostFactory())
    return drafts


@pytest.fixture
def draft(user2):
    draft = PostFactory(owner=user2, author=user2)
    return draft
