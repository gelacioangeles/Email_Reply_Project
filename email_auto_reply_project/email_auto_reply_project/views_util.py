from .model_util import save_inquiry_question
from .llm_util import extract_sender_and_receiver_names

def extract_receiver_and_sender_names(email_content: str):
    # Extract names using llm_util (assumed to be a function that returns names and questions)
    sender_name, receiver_name, inquiry_questions = extract_sender_and_receiver_names(email_content)
    
    # Save extracted questions to the database
    save_inquiry_question(inquiry_questions, email_content)

    # Return the extracted names and questions
    return sender_name, receiver_name, inquiry_questions
