from django.db import models
from uuid import uuid4
import api.utils.gets as g

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    participants = models.ManyToManyField("CustomUser", related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self):
        participants = self.participants.all()
        match = g.get_match(participants[0], participants[1])
        if match:
            match.delete()

        super().delete()

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, default=None, on_delete=models.CASCADE
    )
    sender = models.ForeignKey("CustomUser", default=None, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def get_sent_time(self):
        return self.sent_at.strftime("%I:%M %p")