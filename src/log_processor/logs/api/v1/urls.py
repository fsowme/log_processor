from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('nginx', views.NginxLogViewSet)

urlpatterns = router.urls
