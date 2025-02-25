import speech_recognition as sr
import os, subprocess
from transformers import pipeline
nlp_model = pipeline("question-answering")
def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio).lower()
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        return ""
    except sr.RequestError:
        print("Speech service unavailable.")
        return ""

def find_and_open_app(app_name, search_path="C:\\Program Files"):
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file.lower().startswith(app_name.lower()) and file.endswith(".exe"):
                app_path = os.path.join(root, file)
                print(f"Opening {app_name} from: {app_path}")
                os.startfile(app_path)
                return True
    print(f"Application '{app_name}' not found.")
    return False

def find_and_open_document(doc_name, search_path="C:\\Users"):
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file.lower().startswith(doc_name.lower()): 
                doc_path = os.path.join(root, file)
                print(f"Opening {doc_name} from: {doc_path}")

                try:
                    if os.name == "nt":  # Windows
                        os.startfile(doc_path)
                except Exception as e:
                    print(f"Error opening document: {e}")
                return True

    print(f"Document '{doc_name}' not found.")
    return False



from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

model_name = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

def ai_assistant(user_input):
    if user_input:
        print(f"You: {user_input}")
        inputs = tokenizer(user_input, return_tensors="pt")
        reply_ids = model.generate(**inputs, max_length=100)
        response = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
        print(f"Assistant: {response}")
        return response
