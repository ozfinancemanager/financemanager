from django.urls import path

from .views import AccountDeleteView, AccountDetailAPIView, AccountListCreateView

urlpatterns = [
    path("accounts/", AccountListCreateView.as_view(), name="account-create"),
    path("accounts/<int:pk>/", AccountDetailAPIView.as_view(), name="account-detail"),
    path("accounts/<int:account_id>/delete/", AccountDeleteView.as_view(), name="account-delete"),
]
