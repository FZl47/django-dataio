from django.db import models
from django.contrib.contenttypes.models import ContentType


class ModelField(models.Model):
    """
    Represents a field configuration for a specific Django model.

    Stores field name, related model (via ContentType),
    and its X position for ordering or layout purposes.
    """

    name = models.CharField(max_length=256)
    model = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    xp = models.PositiveBigIntegerField()  # X Position

    def __str__(self) -> str:
        """
        Return human-readable representation of the model field.
        """
        return f"{self.model} | {self.name}"
