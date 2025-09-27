# import os
# import google.generativeai as genai
# from PyPDF2 import PdfReader

# class AdmissionBot:
#     def __init__(self):
#         genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#         self.model = genai.GenerativeModel('models/gemini-2.0-flash')
#         self.pdf_context = self.load_pdf_context()

#     def load_pdf_context(self):
#         """Load admission information from PDF"""
#         try:
#             with open('admission_info.pdf', 'rb') as file:
#                 reader = PdfReader(file)
#                 text = ""
#                 for page in reader.pages:
#                     text += page.extract_text()
#                 return text
#         except FileNotFoundError:
#             return "Admission information not available"

#     def get_response(self, message, role='prospect_student'):
#         """Generate response based on role and PDF context"""
#         role_context = {
#             'prospect_student': "Answer as if explaining to a prospective student in a friendly, encouraging way.",
#             'parent': "Answer with parent's concerns in mind, focusing on safety, costs, and future prospects.",
#             'counselor': "Provide detailed administrative information, requirements, and procedures."
#         }
        
#         prompt = f"""
#         Context Information: {self.pdf_context}
#         User Role: {role_context.get(role, role_context['prospect_student'])}
#         Question: {message}
#         """
        
#         response = self.model.generate_content(prompt)
#         return response.text.strip()


# chat/utils.py
# import os
# import google.generativeai as genai
# from django.conf import settings
# from .models import FAQ, AdmissionInfo

# class AdmissionBot:
#     def __init__(self):
#         genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#         self.model = genai.GenerativeModel('models/gemini-2.0-flash')
    
#     def get_db_context(self):
#         """Retrieve context from database"""
#         faqs = FAQ.objects.all()
#         context = "\n".join([f"Q: {faq.question}\nA: {faq.answer}" for faq in faqs])
        
#         info = AdmissionInfo.objects.all()
#         context += "\n" + "\n".join([f"{item.title}: {item.content}" for item in info])
        
#         return context

#     def get_response(self, message, role='prospect_student'):
#         role_context = {
#             'prospect_student': "Answer as if explaining to a prospective student in a friendly, encouraging way.",
#             'parent': "Answer with parent's concerns in mind, focusing on safety, costs, and future prospects.",
#             'counselor': "Provide detailed administrative information, requirements, and procedures."
#         }
        
#         db_context = self.get_db_context()
#         prompt = f"""
#         Context Information: {db_context}
#         User Role: {role_context.get(role, role_context['prospect_student'])}
#         Question: {message}
#         """
        
#         try:
#             response = self.model.generate_content(prompt)
#             return response.text.strip()
#         except Exception as e:
#             print(f"AI Generation Error: {str(e)}")
#             return "I'm having trouble processing your request. Please try again."

# chat/utils.py
import os
import google.generativeai as genai
from django.conf import settings
from .models import FAQ, AdmissionInfo
import re

class AdmissionBot:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('models/gemini-2.0-flash')
    
    def get_db_context(self):
        """Retrieve context from database"""
        faqs = FAQ.objects.all()
        context = "\n".join([f"Q: {faq.question}\nA: {faq.answer}" for faq in faqs])
        
        info = AdmissionInfo.objects.all()
        context += "\n" + "\n".join([f"{item.title}: {item.content}" for item in info])
        
        return context

    def markdown_to_html(self, text):
        """Convert markdown to HTML"""
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        text = text.replace('\n', '<br>')
        return text

    def get_response(self, message, role='prospect_student'):
        role_context = {
            'prospect_student': "Answer as if explaining to a prospective student in a friendly, encouraging way. Use **bold** for important points.",
            'parent': "Answer with parent's concerns in mind, focusing on safety, costs, and future prospects. Use **bold** for important points.",
            'counselor': "Provide detailed administrative information, requirements, and procedures. Use **bold** for important points."
        }
        
        db_context = self.get_db_context()
        prompt = f"""
        Context Information: {db_context}
        User Role: {role_context.get(role, role_context['prospect_student'])}
        Question: {message}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Convert markdown to HTML
            formatted_response = self.markdown_to_html(response.text.strip())
            return formatted_response
        except Exception as e:
            print(f"AI Generation Error: {str(e)}")
            return "I'm having trouble processing your request. Please try again."