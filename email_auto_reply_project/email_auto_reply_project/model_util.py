from .models import InquiryQuestion

def retrieve_all_inquiry_questions():
    all_inquiry_questions = InquiryQuestion.objects.all()
    print(f"### Retrieved Inquiry Questions: {all_inquiry_questions}")
    return all_inquiry_questions
