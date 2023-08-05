"""Tests for api utils"""
import jwt

from open_discussions_api.utils import get_token


def test_get_token():
    """Test that get_token encodes a token decodable by the secret"""
    token = get_token('secret', 'username', ['test_role'], expires_delta=100)
    decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
    assert decoded['username'] == 'username'
    assert decoded['roles'] == ['test_role']
    assert decoded['exp'] == decoded['orig_iat'] + 100
