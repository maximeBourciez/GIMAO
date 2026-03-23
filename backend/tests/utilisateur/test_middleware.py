from types import SimpleNamespace

import pytest

from utilisateur.middleware import (
    CurrentUserMiddleware,
    get_current_request,
    get_current_user,
    get_thread_log_group,
    get_thread_user,
    set_thread_user,
)


@pytest.fixture(autouse=True)
def clear_thread_user_fixture():
    set_thread_user(None)
    yield
    set_thread_user(None)


def test_set_and_get_thread_user_roundtrip():
    user_obj = SimpleNamespace(id=123)

    set_thread_user(user_obj)

    assert get_thread_user() is user_obj


@pytest.mark.django_db
def test_current_user_middleware_sets_and_cleans_thread_context():
    captured = {}

    def get_response(request):
        captured["request_inside"] = get_current_request()
        captured["user_inside"] = get_current_user()
        captured["log_group_inside"] = get_thread_log_group()
        return SimpleNamespace(status_code=200)

    middleware = CurrentUserMiddleware(get_response)
    request = SimpleNamespace(user=SimpleNamespace(username="dummy", is_authenticated=True))

    response = middleware(request)

    assert response.status_code == 200
    assert captured["request_inside"] is request
    assert captured["user_inside"] is request.user
    assert captured["log_group_inside"] is not None

    assert get_current_request() is None
    assert get_current_user() is None
    assert get_thread_log_group() is None


def test_get_current_user_returns_none_when_no_request_context():
    assert get_current_request() is None
    assert get_current_user() is None
