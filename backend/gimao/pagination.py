from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class OptionalPageNumberPagination(PageNumberPagination):
    """
    Active la pagination uniquement quand `page` est fourni.

    Cela permet de migrer progressivement le frontend sans casser les
    consommateurs historiques qui attendent encore un tableau brut.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        if self.page_query_param not in request.query_params:
            # Pas de parametre `page` : on conserve le contrat historique
            # des endpoints qui renvoient encore un tableau brut.
            return None
        return super().paginate_queryset(queryset, request, view=view)


class StandardOptionalPagination(OptionalPageNumberPagination):
    page_size = 10


class LargeOptionalPagination(OptionalPageNumberPagination):
    page_size = 25


class OptionalPaginationViewSetMixin:
    """
    Fournit une réponse paginée pour les actions custom tout en conservant
    le format tableau brut quand `page` n'est pas demandé.
    """

    def get_paginated_or_full_response(
        self,
        queryset,
        *,
        serializer_class=None,
        extra=None,
        many=True,
    ):
        page = self.paginate_queryset(queryset)

        if serializer_class is None:
            serializer_factory = lambda items: self.get_serializer(items, many=many)
        else:
            serializer_factory = lambda items: serializer_class(
                items,
                many=many,
                context=self.get_serializer_context(),
            )

        if page is not None:
            serializer = serializer_factory(page)

            if not extra:
                return self.get_paginated_response(serializer.data)

            return Response(
                {
                    "count": self.paginator.page.paginator.count,
                    "next": self.paginator.get_next_link(),
                    "previous": self.paginator.get_previous_link(),
                    "results": serializer.data,
                    **extra,
                }
            )

        serializer = serializer_factory(queryset)
        return Response(serializer.data)
