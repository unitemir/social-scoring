from rest_framework.test import APIClient

import pytest

from ..models import InstagramUser


@pytest.fixture
def api_client_no_auth(db):
    return APIClient()
