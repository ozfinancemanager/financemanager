from django.urls import path

from .views import AccountDetailAPIView, AccountListCreateView

urlpatterns = [
    path("accounts/", AccountListCreateView.as_view(), name="account-create"),
    path("accounts/<int:pk>/", AccountDetailAPIView.as_view(), name="account-detail"),
]
