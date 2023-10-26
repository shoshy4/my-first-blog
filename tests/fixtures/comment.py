import pytest
from tests.factory.comment import CommentFactory


@pytest.fixture
def comment():
    comment = CommentFactory()
    return comment


@pytest.fixture
def comment2(user2):
    comment = CommentFactory(post_owner=user2)
    return comment


@pytest.fixture
def comments(post_1):
    comments = []
    for ix in range(4):
        comment = CommentFactory(post=post_1, approved_comment="True")
        comments.append(comment)
    return comments
