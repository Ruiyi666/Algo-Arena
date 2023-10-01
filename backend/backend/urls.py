"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.documentation import include_docs_urls

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

class APITokenAuthView(ObtainAuthToken):

    def delete(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer' not in auth_header:
            return Response({"detail": "Authorization header is missing or invalid."}, status=status.HTTP_400_BAD_REQUEST)

        token = auth_header.split('Bearer ')[1].strip()

        try:
            token_instance = Token.objects.get(key=token)
            token_instance.delete()
            return Response({"detail": "Token deleted successfully."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token not found."}, status=status.HTTP_404_NOT_FOUND)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-token-auth/", APITokenAuthView.as_view()),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("server.urls")),
    path("docs/", include_docs_urls(title="Backend API")),
]