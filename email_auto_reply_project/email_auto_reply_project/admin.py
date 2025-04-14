from django.contrib import admin
from .models import InquiryUser, EmailInquiry, InquiryQuestion

admin.site.register(InquiryUser)
admin.site.register(EmailInquiry)
admin.site.register(InquiryQuestion)
