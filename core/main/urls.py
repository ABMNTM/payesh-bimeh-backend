from rest_framework.routers import DefaultRouter

from main.api.views.enrollment import EnrollmentViewSet

router = DefaultRouter()

router.register(r"enrollment", EnrollmentViewSet, basename="enrollment")

urlpatterns = router.urls
