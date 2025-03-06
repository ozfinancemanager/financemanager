from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view  # type: ignore
from rest_framework import permissions
from finance.views import TransactionHistoryListCreate, TransactionHistoryDetail #추가

from .base import urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title="Finance Manager API",
        default_version="v1",
        description="API 문서입니다.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    re_path('api/transactions/', TransactionHistoryListCreate.as_view(), name='transaction-list-create'), #url 추가
    re_path('api/transactions/<int:pk>/', TransactionHistoryDetail.as_view(), name='transaction-detail'), #url 추가
]
