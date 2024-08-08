from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Project,
    Milestone,
    Category,
    Tag,
    Todo,
    Comment,
    Attachment,
    RecurringTask,
    ActivityLog,
)
from .serializers import (
    ProjectSerializer,
    MilestoneSerializer,
    CategorySerializer,
    TagSerializer,
    TodoSerializer,
    CommentSerializer,
    AttachmentSerializer,
    RecurringTaskSerializer,
    ActivityLogSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsProjectMemberOrReadOnly


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "projects": reverse("project-list", request=request, format=format),
            "milestones": reverse("milestone-list", request=request, format=format),
            "categories": reverse("category-list", request=request, format=format),
            "tags": reverse("tag-list", request=request, format=format),
            "todos": reverse("todo-list", request=request, format=format),
            "comments": reverse("comment-list", request=request, format=format),
            "attachments": reverse("attachment-list", request=request, format=format),
            "recurring-tasks": reverse(
                "recurringtask-list", request=request, format=format
            ),
            "activity-logs": reverse(
                "activitylog-list", request=request, format=format
            ),
        }
    )


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["owner", "members"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsProjectMemberOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["project"]
    ordering_fields = ["due_date"]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsProjectMemberOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["project"]
    search_fields = ["name"]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsProjectMemberOrReadOnly,
    ]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "user",
        "project",
        "category",
        "milestone",
        "completed",
        "priority",
    ]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "created_at", "updated_at"]

    @action(detail=True, methods=["post"])
    def add_comment(self, request, pk=None):
        todo = self.get_object()
        serializer = CommentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(todo=todo, user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["post"])
    def add_attachment(self, request, pk=None):
        todo = self.get_object()
        serializer = AttachmentSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(todo=todo, uploaded_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsProjectMemberOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["todo", "user"]
    ordering_fields = ["created_at"]


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsProjectMemberOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["todo", "uploaded_by"]
    ordering_fields = ["uploaded_at"]


class RecurringTaskViewSet(viewsets.ModelViewSet):
    queryset = RecurringTask.objects.all()
    serializer_class = RecurringTaskSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsProjectMemberOrReadOnly,
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["todo", "frequency"]


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["user", "action"]
    ordering_fields = ["timestamp"]
