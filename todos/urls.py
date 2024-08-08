from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from .auth_views import (
    RegisterView,
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
)

from .views import (
    api_root,
    ProjectViewSet,
    MilestoneViewSet,
    CategoryViewSet,
    TagViewSet,
    TodoViewSet,
    CommentViewSet,
    AttachmentViewSet,
    RecurringTaskViewSet,
    ActivityLogViewSet,
)

router = DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"milestones", MilestoneViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"tags", TagViewSet)
router.register(r"todos", TodoViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"attachments", AttachmentViewSet)
router.register(r"recurring-tasks", RecurringTaskViewSet)
router.register(r"activity-logs", ActivityLogViewSet)

urlpatterns = [
    path("", api_root),
    path("", include(router.urls)),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path(
        "auth/password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]
