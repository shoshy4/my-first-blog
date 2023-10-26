from django.urls import reverse
import pytest
from datetime import datetime, timedelta


# @pytest.mark.django_db
# def test_post_model(post_1):
#     print(post_1.id)
#     print(post_1.author)
#     print(post_1.published_date)

@pytest.mark.django_db
def test_comment_model(comments):
    for comment in comments:
        print(comment.post.id)
        print(comment.post.author)
        print(comment.author)
        print(comment.text)
        print(comment.approved_comment)



# @pytest.mark.django_db
# def test_post_model_draft(draft):
#     print(draft.title)
#     print(draft.author)
#     print(draft.published_date)


@pytest.mark.django_db
def test_post_list(api_client_auth, posts):
    url = reverse('post_list_create_api')
    client, _ = api_client_auth
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['count'] == 4


@pytest.mark.django_db
def test_post_create(api_client_auth):
    url = reverse('post_list_create_api')
    client, _ = api_client_auth
    payload = {"author": 1,
            "owner": "apple",
            "title": "Temporary post",
            "text": "This is a temporary post"
            }
    response = client.post(url, payload, format='json')
    assert response.status_code == 201
    assert "author" in response.data


@pytest.mark.django_db
def test_draft_list(api_client_auth, drafts):
    url = reverse('draft_list_api')
    client, _ = api_client_auth
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_detail(api_client_auth, post):
    url = reverse('post_update_detail_remove_api', kwargs={'pk': '1'})
    client, _ = api_client_auth
    response = client.get(url)
    assert response.status_code == 200
    assert "owner" in response.data


@pytest.mark.django_db
def test_post_update(api_client_auth,post2):
    url = reverse('post_update_detail_remove_api', kwargs={'pk': post2.id})
    client, _ = api_client_auth
    response = client.patch(url, {
        "title": "Temporary post",
        "text": "This is a temporary post" }, format='json')
    assert response.status_code == 200
    assert response.data["title"] == "Temporary post"


@pytest.mark.django_db
def test_post_delete(api_client_auth,post2):
    url = reverse('post_update_detail_remove_api', kwargs={'pk': post2.id})
    client, _ = api_client_auth
    response = client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_post_publish(api_client_auth, draft):
    url = reverse('post_publish_api', kwargs={'pk': draft.id})
    client, _ = api_client_auth
    published_date = (draft.created_date + timedelta(days=2))
    response = client.patch(url, {"published_date": published_date}, format='json')
    assert response.status_code == 200
    assert datetime.strptime(response.data["published_date"][:10],'%Y-%m-%d').date() == published_date


@pytest.mark.django_db
def test_post_publish_date_not_specified(api_client_auth, draft):
    url = reverse('post_publish_api', kwargs={'pk': draft.id})
    client, _ = api_client_auth
    response = client.patch(url)
    assert response.status_code == 200
    assert datetime.strptime(response.data["published_date"][:10],'%Y-%m-%d').date() == datetime.now().date()



@pytest.mark.django_db
def test_comment_create(api_client_auth, post):
    url = reverse('comment_list_create_api', kwargs={'post_pk':'1'})
    client, _ = api_client_auth
    payload = {
        "post": "1",
        "author": "Berry",
        "text": "Is that really a new comment?",
        "post_owner": "apple"
            }
    response = client.post(url, payload, format='json')
    assert response.status_code == 201
    assert "post" in response.data


@pytest.mark.django_db
def test_comment_list(api_client_auth, post_1, comments):
    url = reverse('comment_list_create_api', kwargs={'post_pk':post_1.id})
    client, _ = api_client_auth
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['count'] == 4


@pytest.mark.django_db
def test_comment_update(api_client_auth,  comment2, post2):
    url = reverse('comment_update_remove_detail_api', kwargs={'pk': comment2.id, 'post_pk':post2.id})
    client, _ = api_client_auth
    response = client.patch(url, {
        "text": "Trying to change comment's text" }, format='json')
    assert response.status_code == 200
    assert "post" in response.data


@pytest.mark.django_db
def test_comment_detail(api_client_auth, comment2, post2):
    url = reverse('comment_update_remove_detail_api', kwargs={'pk': comment2.id, 'post_pk':post2.id} )
    client, _ = api_client_auth
    response = client.get(url)
    assert response.status_code == 200
    assert "post_owner" in response.data


@pytest.mark.django_db
def test_comment_delete(api_client_auth, comment2, post2):
    url = reverse('comment_update_remove_detail_api', kwargs={'pk': comment2.id, 'post_pk':post2.id})
    client, _ = api_client_auth
    response = client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_comment_approve(api_client_auth, post2, comment2):
    url = reverse('comment_update_remove_detail_api', kwargs={'pk': comment2.id, 'post_pk':post2.id})
    client, _ = api_client_auth
    response = client.patch(url)
    assert response.status_code == 200
    assert "post" in response.data

#url, {"approved_comment": "True" }, format='json'