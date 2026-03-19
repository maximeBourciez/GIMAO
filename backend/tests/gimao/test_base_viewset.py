import pytest
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from gimao.viewsets import GimaoModelViewSet
from tests.factories import RoleFactory, UtilisateurFactory
from utilisateur.middleware import get_thread_user, set_thread_user
from utilisateur.models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "nomRole")


class DummyBaseViewSet(GimaoModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


@pytest.fixture(autouse=True)
def clear_thread_user():
    set_thread_user(None)
    yield
    set_thread_user(None)


def _build_view_and_request(method="post", data=None, user=None):
    factory = APIRequestFactory()
    if method == "post":
        request = factory.post("/dummy/", data=data or {}, format="json")
    else:
        request = factory.get("/dummy/")

    if user is not None:
        force_authenticate(request, user=user)

    view = DummyBaseViewSet()
    if method == "post":
        view.action_map = {"post": "create"}
    else:
        view.action_map = {"get": "list"}
    view.headers = view.default_response_headers
    drf_request = view.initialize_request(request)
    view.request = drf_request
    view.args = ()
    view.kwargs = {}
    return view, drf_request


def _run_initial_and_finalize(view, drf_request):
    view.initial(drf_request)
    assert isinstance(drf_request, Request)
    view.finalize_response(drf_request, Response({"ok": True}))


@pytest.mark.django_db
def test_initial_sets_thread_user_from_payload_user_key():
    app_user = UtilisateurFactory()
    view, drf_request = _build_view_and_request(data={"user": app_user.pk})

    view.initial(drf_request)

    assert get_thread_user().pk == app_user.pk

    view.finalize_response(drf_request, Response({"ok": True}))
    assert get_thread_user() is None


@pytest.mark.django_db
def test_initial_sets_thread_user_from_payload_utilisateur_dict():
    app_user = UtilisateurFactory()
    view, drf_request = _build_view_and_request(data={"utilisateur": {"id": app_user.pk}})

    _run_initial_and_finalize(view, drf_request)

    assert get_thread_user() is None


@pytest.mark.django_db
def test_initial_sets_thread_user_from_payload_utilisateur_id_key():
    app_user = UtilisateurFactory()
    view, drf_request = _build_view_and_request(data={"utilisateur_id": app_user.pk})

    view.initial(drf_request)

    assert get_thread_user().pk == app_user.pk


@pytest.mark.django_db
def test_initial_keeps_thread_user_none_when_payload_id_invalid():
    view, drf_request = _build_view_and_request(data={"user": "not-an-int"})

    _run_initial_and_finalize(view, drf_request)

    assert get_thread_user() is None


@pytest.mark.django_db
def test_initial_uses_request_user_utilisateur_when_authenticated():
    app_user = UtilisateurFactory()
    django_user = User.objects.create_user(username="dj_user", password="secret")
    django_user.utilisateur = app_user

    view, drf_request = _build_view_and_request(data={}, user=django_user)

    view.initial(drf_request)

    assert get_thread_user().pk == app_user.pk


@pytest.mark.django_db
def test_initial_uses_username_mapping_when_no_utilisateur_attr():
    app_user = UtilisateurFactory(nomUtilisateur="mapped_user")
    django_user = User.objects.create_user(username="mapped_user", password="secret")

    view, drf_request = _build_view_and_request(data={}, user=django_user)

    view.initial(drf_request)

    assert get_thread_user().pk == app_user.pk


@pytest.mark.django_db
def test_finalize_response_always_clears_thread_user():
    app_user = UtilisateurFactory()
    view, drf_request = _build_view_and_request(data={"user": app_user.pk})

    view.initial(drf_request)
    assert get_thread_user() is not None

    response = view.finalize_response(drf_request, Response({"ok": True}))

    assert response.status_code == 200
    assert get_thread_user() is None
