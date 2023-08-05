"""Tests for user client API"""
# pylint: disable=unused-argument
import json

import pytest


def test_list_users(api_client):
    """Test list users for correct request"""
    resp = api_client.users.list()
    assert resp.status_code == 200
    assert resp.json() == [{
        "id": 39,
        "username": "01BQRHXRDP1J63DF8QQB6B8TKA",
        "profile": {
            "name": "name",
            "image": "test1.jpg",
            "image_small": "test2.jpg",
            "image_medium": "test3.jpg"
        }
    }]


def test_create_user(api_client):
    """Test create user"""
    resp = api_client.users.create(
        name="my name",
        image="image1.jpg",
        image_small="image2.jpg",
        image_medium="image3.jpg"
    )
    assert json.loads(resp.request.body) == {
        "profile": {
            "name": "my name",
            "image": "image1.jpg",
            "image_small": "image2.jpg",
            "image_medium": "image3.jpg",
        }
    }
    assert resp.status_code == 201
    assert resp.json() == {
        "id": 41,
        "username": "01BRMT958T3DW02ZAYDG7N6QCB",
        "profile": {
            "name": "my name",
            "image": "image1.jpg",
            "image_small": "image2.jpg",
            "image_medium": "image3.jpg"
        }
    }


def test_create_user_no_profile_props(api_client):
    """Updating with no args raises error"""
    with pytest.raises(AttributeError) as err:
        api_client.users.create()
    assert str(err.value) == "No fields provided to create"


def test_create_user_invalid_profile_props(api_client):
    """Updating with invalid arg raises error"""
    with pytest.raises(AttributeError) as err:
        api_client.users.create(bad_arg=2)
    assert str(err.value) == "Argument bad_arg is not supported"


def test_get_user(api_client, use_betamax):
    """Test get user"""
    resp = api_client.users.get("01BRMT958T3DW02ZAYDG7N6QCB")
    assert resp.status_code == 200
    assert resp.json() == {
        "id": 41,
        "username": "01BRMT958T3DW02ZAYDG7N6QCB",
        "profile": {
            "name": "my name",
            "image": "image1.jpg",
            "image_small": "image4.jpg",
            "image_medium": "image3.jpg"
        }
    }


def test_update_user(api_client):
    """Test patch user"""
    resp = api_client.users.update("01BRMT958T3DW02ZAYDG7N6QCB", image_small="image4.jpg")
    assert json.loads(resp.request.body) == {
        "profile": {
            "image_small": "image4.jpg",
        }
    }
    assert resp.status_code == 200
    assert resp.json() == {
        "id": 41,
        "username": "01BRMT958T3DW02ZAYDG7N6QCB",
        "profile": {
            "name": "my name",
            "image": "image1.jpg",
            "image_small": "image4.jpg",
            "image_medium": "image3.jpg"
        }
    }


def test_update_user_no_profile_props(api_client):
    """Updating with no args raises error"""
    with pytest.raises(AttributeError) as err:
        api_client.users.update("01BRMT958T3DW02ZAYDG7N6QCB")
    assert str(err.value) == "No fields provided to update"


def test_update_user_invalid_profile_props(api_client):
    """Updating with invalid arg raises error"""
    with pytest.raises(AttributeError) as err:
        api_client.users.update("01BRMT958T3DW02ZAYDG7N6QCB", bad_arg=2)
    assert str(err.value) == "Argument bad_arg is not supported"
