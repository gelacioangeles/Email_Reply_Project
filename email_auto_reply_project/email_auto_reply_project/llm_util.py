import google.generativeai as genai
from .settings import GOOGLE_GEMINI_API_KEY

# Configuring the Gemini API key.
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

def generate_prompt(email_content: str):
    """
    Generates a structured prompt for Google Gemini to extract sender & receiver names,
    and inquiry questions from the provided email content.
    """
    prompt_extract_names_and_questions = f"""
    Extract the sender and receiver names, and all inquiry questions from the following email.
    
    Email Content:
    "{email_content}"
    
    Respond with exactly the following format:
    
    Sender Name: [Sender's Name]
    Receiver Name: [Receiver's Name]
    Inquiry Questions: [
        [First inquiry question]
        [Second inquiry question]
        ...
    ]
    
    Ensure:
    - The "inquiry_questions" list contains only the extracted questions.
    - If there are no questions, return an empty list: "inquiry_questions": [].
    """
    return prompt_extract_names_and_questions

def extract_sender_and_receiver_names(email_content: str):
    """
    Uses Google Gemini API to extract sender and receiver names, and inquiry questions from the email body.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        prompt = generate_prompt(email_content)

        # Calling the Gemini API.
        response = model.generate_content(prompt)

        if response and response.candidates:
            # Extracts the text content.
            response_text = response.candidates[0].content.parts[0].text.strip()
            
            # Formatting the output.
            print("\nGemini Response Content: ")
            print(response_text)

            # Spliting the response text by line breaks.
            result = response_text.split("\n")

            # Initialize default values.
            sender_name = "there"
            receiver_name = "there"
            inquiry_questions = []

            # Extracts the sender and receiver.
            if len(result) > 0:
                sender_name = result[0].split(":")[1].strip()
            if len(result) > 1:
                receiver_name = result[1].split(":")[1].strip() 

            # Extracts the inquiry questions.
            if len(result) > 2:
                questions_line = result[2].strip()
                if questions_line.startswith("Inquiry Questions:"):
                    questions_line = questions_line.replace("Inquiry Questions: [", "").replace("]", "")
                    inquiry_questions = [q.strip(' "') for q in questions_line.split("\n") if q.strip()]

            # If no questions were found, makes the list empty.
            if not inquiry_questions:
                inquiry_questions = []

            return sender_name, receiver_name, inquiry_questions

    except Exception as e:
        print(f"Error extracting names and questions from Gemini response: {e}")
    
    # Returns the default values if something goes wrong.
    return "there", "there", [] 
