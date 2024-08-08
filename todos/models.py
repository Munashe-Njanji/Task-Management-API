from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User, related_name="owned_projects", on_delete=models.CASCADE
    )
    members = models.ManyToManyField(User, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Milestone(models.Model):
    project = models.ForeignKey(
        Project, related_name="milestones", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(
        Project, related_name="categories", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Todo(models.Model):
    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("URGENT", "Urgent"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name="todos", on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="todos", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name="todos", on_delete=models.SET_NULL, null=True
    )
    milestone = models.ForeignKey(
        Milestone, related_name="todos", on_delete=models.SET_NULL, null=True
    )
    tags = models.ManyToManyField(Tag, related_name="todos")
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="MEDIUM"
    )
    due_date = models.DateTimeField(null=True, blank=True)
    estimated_time = models.DurationField(null=True, blank=True)
    actual_time = models.DurationField(null=True, blank=True)
    parent_task = models.ForeignKey(
        "self", null=True, blank=True, related_name="subtasks", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    todo = models.ForeignKey(Todo, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.todo.title}"


class Attachment(models.Model):
    todo = models.ForeignKey(Todo, related_name="attachments", on_delete=models.CASCADE)
    file = models.FileField(upload_to="attachments/")
    uploaded_by = models.ForeignKey(
        User, related_name="attachments", on_delete=models.CASCADE
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.todo.title}"


class RecurringTask(models.Model):
    FREQUENCY_CHOICES = [
        ("DAILY", "Daily"),
        ("WEEKLY", "Weekly"),
        ("MONTHLY", "Monthly"),
        ("YEARLY", "Yearly"),
    ]

    todo = models.OneToOneField(Todo, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Recurring {self.todo.title}"


class ActivityLog(models.Model):
    user = models.ForeignKey(User, related_name="activities", on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.action} {self.target}"
