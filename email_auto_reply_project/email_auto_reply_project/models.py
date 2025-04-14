from django.db import models

class InquiryUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class EmailInquiry(models.Model):
    user = models.ForeignKey(
        InquiryUser, on_delete=models.CASCADE, related_name="inquiries", null=True, blank=True, default=None
    )
    email_content = models.TextField()
    inquiry_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.user.email if self.user else 'Unknown'} at {self.inquiry_timestamp}"

class InquiryQuestion(models.Model):
    email_inquiry = models.ForeignKey(
        EmailInquiry, on_delete=models.CASCADE, related_name="questions", null=True, blank=True, default=None
    )
    question = models.TextField()
    answer = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.question
