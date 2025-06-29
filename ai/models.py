from django.db import models


class ChatMessage(models.Model):
    session_id = models.CharField(max_length=100)
    ROLE_CHOICES = (
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_messages"

    def __str__(self):
        return f"{self.session_id} - {self.role}: {self.content[:50]}"
