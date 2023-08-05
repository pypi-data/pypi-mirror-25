"""Tests for user client API"""
import json
import pytest

from open_discussions_api.channels.client import (
    EmptyAttributesError,
    UnsupportedAttributeError,
    InvalidChannelTypeError
)


def test_create_channel(api_client):
    """test a happpy path"""
    resp = api_client.channels.create(
        title="new test channel",
        name="examplechannel",
        public_description="a good channel for all things",
        channel_type="public"
    )
    assert resp.status_code == 201
    assert json.loads(resp.request.body) == {
        "title": "new test channel",
        "name": "examplechannel",
        "public_description": "a good channel for all things",
        "channel_type": "public"
    }
    assert resp.json() == {
        "title": "new test channel",
        "name": "examplechannel",
        "public_description": "a good channel for all things",
        "channel_type": "public"
    }


def test_create_private_channel(api_client):
    """test a different happy path"""
    resp = api_client.channels.create(
        title="new private channel",
        name="privatechannel",
        public_description="a good channel for all things",
        channel_type="private"
    )
    assert resp.status_code == 201
    assert json.loads(resp.request.body) == {
        "title": "new private channel",
        "name": "privatechannel",
        "public_description": "a good channel for all things",
        "channel_type": "private"
    }
    assert resp.json() == {
        "title": "new private channel",
        "name": "privatechannel",
        "public_description": "a good channel for all things",
        "channel_type": "private"
    }


def test_create_channel_with_no_arguments(api_client):
    """should raise when provided nothing"""
    with pytest.raises(EmptyAttributesError):
        api_client.channels.create()


def test_create_channel_with_unsupported_args(api_client):
    """should raise if you pass a bad param"""
    with pytest.raises(UnsupportedAttributeError) as err:
        api_client.channels.create(bad="wrong")
    assert str(err.value) == "Argument 'bad' is not a supported field"


def test_create_channel_with_bad_channel_type(api_client):
    """should raise if you pass something unsupported"""
    with pytest.raises(InvalidChannelTypeError) as err:
        api_client.channels.create(
            title="new private channel",
            name="privatechannel",
            public_description="a good channel for all things",
            channel_type="fun"
        )
    assert str(err.value) == "Channel type 'fun' is not a valid option"
