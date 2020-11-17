from django.urls import path
from .views import me_account, me_membership, me_settings

urlpatterns = [
    path('', me_account, name='me-account'),
    path('membership/', me_membership, name='me-membership'),
    path('settings/', me_settings, name='me-settings'),
]