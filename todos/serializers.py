from rest_framework import serializers
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


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    milestones = serializers.HyperlinkedRelatedField(
        many=True, view_name="milestone-detail", read_only=True
    )
    todos = serializers.HyperlinkedRelatedField(
        many=True, view_name="todo-detail", read_only=True
    )

    class Meta:
        model = Project
        fields = [
            "url",
            "id",
            "name",
            "description",
            "owner",
            "members",
            "created_at",
            "updated_at",
            "milestones",
            "todos",
        ]
        extra_kwargs = {
            "url": {"view_name": "project-detail"},
            "owner": {"view_name": "user-detail"},
            "members": {"view_name": "user-detail", "many": True},
        }


class MilestoneSerializer(serializers.HyperlinkedModelSerializer):
    todos = serializers.HyperlinkedRelatedField(
        many=True, view_name="todo-detail", read_only=True
    )

    class Meta:
        model = Milestone
        fields = ["url", "id", "project", "name", "due_date", "todos"]
        extra_kwargs = {
            "url": {"view_name": "milestone-detail"},
            "project": {"view_name": "project-detail"},
        }


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    todos = serializers.HyperlinkedRelatedField(
        many=True, view_name="todo-detail", read_only=True
    )

    class Meta:
        model = Category
        fields = ["url", "id", "name", "project", "todos"]
        extra_kwargs = {
            "url": {"view_name": "category-detail"},
            "project": {"view_name": "project-detail"},
        }


class TagSerializer(serializers.HyperlinkedModelSerializer):
    todos = serializers.HyperlinkedRelatedField(
        many=True, view_name="todo-detail", read_only=True
    )

    class Meta:
        model = Tag
        fields = ["url", "id", "name", "todos"]
        extra_kwargs = {
            "url": {"view_name": "tag-detail"},
        }


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ["url", "id", "todo", "user", "content", "created_at"]
        extra_kwargs = {
            "url": {"view_name": "comment-detail"},
            "todo": {"view_name": "todo-detail"},
            "user": {"view_name": "user-detail"},
        }


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attachment
        fields = ["url", "id", "todo", "file", "uploaded_by", "uploaded_at"]
        extra_kwargs = {
            "url": {"view_name": "attachment-detail"},
            "todo": {"view_name": "todo-detail"},
            "uploaded_by": {"view_name": "user-detail"},
        }


class RecurringTaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecurringTask
        fields = ["url", "id", "todo", "frequency", "start_date", "end_date"]
        extra_kwargs = {
            "url": {"view_name": "recurringtask-detail"},
            "todo": {"view_name": "todo-detail"},
        }


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    recurring_task = RecurringTaskSerializer(read_only=True)
    subtasks = serializers.HyperlinkedRelatedField(
        many=True, view_name="todo-detail", read_only=True
    )

    class Meta:
        model = Todo
        fields = [
            "url",
            "id",
            "title",
            "description",
            "completed",
            "user",
            "project",
            "category",
            "milestone",
            "tags",
            "priority",
            "due_date",
            "estimated_time",
            "actual_time",
            "parent_task",
            "subtasks",
            "created_at",
            "updated_at",
            "comments",
            "attachments",
            "recurring_task",
        ]
        extra_kwargs = {
            "url": {"view_name": "todo-detail"},
            "user": {"view_name": "user-detail"},
            "project": {"view_name": "project-detail"},
            "category": {"view_name": "category-detail"},
            "milestone": {"view_name": "milestone-detail"},
            "tags": {"view_name": "tag-detail", "many": True},
            "parent_task": {"view_name": "todo-detail"},
        }


class ActivityLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ["url", "id", "user", "action", "target", "timestamp"]
        extra_kwargs = {
            "url": {"view_name": "activitylog-detail"},
            "user": {"view_name": "user-detail"},
        }
