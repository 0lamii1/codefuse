from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler400 = error_400
# handler403 = error_403
# handler404 = error_404
# handler500 = error_500