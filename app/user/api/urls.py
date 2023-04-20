from django.urls import path

# from knox import views as knox_views
from .views import UserView

urlpatterns = [
    # path('login', LoginView.as_view(), name='knox_login'),
    # path('logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    # path('logout/all', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('user', UserView.as_view(), name='user_info'),
]
