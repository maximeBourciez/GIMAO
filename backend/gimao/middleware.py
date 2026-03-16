import hashlib
from django.http import JsonResponse
from security.models import ApiToken


class ApiTokenMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith("/api/"):

            if request.path in ["/api/utilisateurs/login/", "/api/utilisateurs/definir-mot-de-passe/", "/api/utilisateurs/exists/"]:
                return self.get_response(request)

            auth = request.headers.get("Authorization")

            if not auth or not auth.startswith("Bearer "):
                return JsonResponse({"error": "Token manquant"}, status=401)

            token = auth.split(" ")[1]

            token_hash = hashlib.sha256(token.encode()).hexdigest()

            try:
                api_token = ApiToken.objects.get(token_hash=token_hash)

                if not api_token.is_valid():
                    return JsonResponse({"error": "Token expiré ou révoqué"}, status=401)

                request.api_user = api_token.user

            except ApiToken.DoesNotExist:
                return JsonResponse({"error": "Token invalide"}, status=401)

        return self.get_response(request)