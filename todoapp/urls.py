from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todoapp import views

router = DefaultRouter()
router.register("lists", views.ListViewSet)
task_router = DefaultRouter()
task_router.register("tasks", views.TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lists/<uuid:list_id>/", include(task_router.urls)),
]
