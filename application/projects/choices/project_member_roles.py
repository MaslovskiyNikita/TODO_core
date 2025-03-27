from django.db import models


class Roles(models.TextChoices):

    REDACTOR = "redactor", "redactor"
    VIEWER = "viewer", "viewer"
