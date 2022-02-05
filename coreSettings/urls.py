from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["https", "http"]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Online API",
        default_version='v1',
        description="Online API for Product IT",
        terms_of_service="#",
        contact=openapi.Contact(email="email@email.com"),
    ),
    generator_class=BothHttpAndHttpsSchemaGenerator,
    public=False,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,)
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

                  path('Token/get/', TokenObtainPairView.as_view(), name='token_obtain_access_refresh'),
                  path('Token/renew/', TokenRefreshView.as_view(), name='token_renew_access_with_refresh'),

                  path('api/', include('rest_framework.urls')),
                  path('accounts/', include('allauth.urls')),
                  path('__debug__/', include('debug_toolbar.urls')),
                  path(r'^api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
