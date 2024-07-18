from django.urls import path
from .views import ConsultaDividaView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('consulta-divida/', ConsultaDividaView.as_view(), name='consulta_divida'),
]