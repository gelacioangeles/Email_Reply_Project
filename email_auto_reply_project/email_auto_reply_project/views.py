import json
import re
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .llm_util import extract_sender_and_receiver_names
from .models import InquiryQuestion, EmailInquiry, InquiryUser

def home(request):
    all_inquiry_questions = InquiryQuestion.objects.select_related('email_inquiry__user').all()
    return render(request, 'home.html', {'inquiry_questions': all_inquiry_questions})

@csrf_exempt
def auto_reply_email(request):

    if request.method == "POST":
        try:
            # Parses the incoming JSON request.
            data = json.loads(request.body)
            email_content = data.get("content", "").strip()

            # Extracts the sender, receiver, and inquiry-related information.
            sender, receiver, inquiry_questions = extract_sender_and_receiver_names(email_content)

            # Extracts the first and last name from the sender's name.
            sender_name_parts = sender.split()
            first_name = sender_name_parts[0] if sender_name_parts else "Unknown"
            last_name = sender_name_parts[-1] if len(sender_name_parts) > 1 else ""

            # Extracts the email address from the content if there is one.
            sender_email = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email_content)
            sender_email = sender_email.group(0) if sender_email else f"{first_name.lower()}.{last_name.lower()}@example.com"

            # Creates or retrieve user based on extracted email.
            user, created = InquiryUser.objects.get_or_create(
                email=sender_email, 
                defaults={'first_name': first_name, 'last_name': last_name}
            )

            # Saves the email inquiry in the database.
            email_inquiry = EmailInquiry.objects.create(
                user=user, 
                email_content=email_content
            )

            # Regular expression to identify questions in the email content.
            question_regex = r"\b(?:Who|What|When|Where|Why|How|Is|Are|Do|Does|Can|Could|Would|Should)\b[^.?]*[.?\n]"
            extracted_questions = [q.strip() for q in re.findall(question_regex, email_content, re.IGNORECASE)]

            # If no explicit questions are found, this looks for potential inquiry-related phrases.
            if not extracted_questions:
                potential_questions = re.findall(
                    r"[^.!?]*\b(meeting|schedule|update|status|details|confirm|follow up|help|assistance)\b[^.!?]*[.!?]", 
                    email_content, re.IGNORECASE
                )
                extracted_questions.extend([q.strip() for q in potential_questions])

            # Ensures the extracted questions end with a question mark.
            formatted_questions = [q.rstrip('.') + '?' if not q.endswith("?") else q for q in extracted_questions]

            # Saves the extracted questions to the database.
            for question_text in formatted_questions:
                InquiryQuestion.objects.create(
                    email_inquiry=email_inquiry,
                    question=question_text,
                    answer=""
                )

            # Generates an automatic reply message.
            reply_message = f"Hi {first_name}, thanks for your email. I will get back to you soon. Best, {receiver}."

            # Returns a JSON response with extracted data and auto-reply.
            return JsonResponse({
                "reply": reply_message,
                "status": "success",
                "sender": sender,
                "receiver": receiver,
                "extracted_questions": formatted_questions,
                "user_info": {
                    "id": user.id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": sender_email
                }
            })

        except json.JSONDecodeError:
            # Handle cases where the request body is not valid JSON.
            return JsonResponse({"error": "Invalid JSON format", "status": "failure"}, status=400)

    # Handle requests that are not POST.
    return JsonResponse({"error": "Only POST requests are allowed", "status": "failure"}, status=405)