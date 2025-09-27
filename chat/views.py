
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import ChatSession, ChatMessage
from .utils import AdmissionBot
import uuid

def chat_view(request):
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['chat_session_id'] = session_id
        
        # Create new session
        ChatSession.objects.get_or_create(
            session_id=session_id,
            defaults={'role': 'prospect_student'}
        )
    
    # Get messages for this session
    session = ChatSession.objects.get(session_id=session_id)
    messages = ChatMessage.objects.filter(session=session)
    
    return render(request, 'chat.html', {
        'session_id': session_id,
        'messages': messages,
        'role': session.role
    })

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            session_id = data.get('session_id')
            role = data.get('role', 'prospect_student')
            
            # Validate inputs
            if not user_message or not session_id:
                return JsonResponse({'error': 'Missing message or session_id'}, status=400)
            
            # Get or create session
            session, created = ChatSession.objects.get_or_create(
                session_id=session_id,
                defaults={'role': role}
            )
            if not created:
                session.role = role
                session.save()
            
            # Save user message
            user_msg = ChatMessage.objects.create(
                session=session,
                message=user_message,
                sender='user'
            )
            
            # Generate bot response
            bot = AdmissionBot()
            bot_response = bot.get_response(user_message, role)
            
            # Save bot response
            bot_msg = ChatMessage.objects.create(
                session=session,
                message=bot_response,
                sender='bot'
            )
            
            return JsonResponse({
                'response': bot_response,
                'timestamp': bot_msg.timestamp.isoformat()
            })
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"Chat API Error: {str(e)}")  # Debug print
            return JsonResponse({'error': 'Server error'}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
# chat/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import FAQ
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def faq_dashboard(request):
    # Handle form submission
    if request.method == 'POST':
        faq_id = request.POST.get('faq_id')
        question = request.POST.get('question', '').strip()
        answer = request.POST.get('answer', '').strip()
        category = request.POST.get('category', 'general').strip()

        if not question or not answer:
            messages.error(request, 'Question and answer are required.')
            return redirect('faq_dashboard')

        if faq_id:
            # Update existing
            faq = get_object_or_404(FAQ, id=faq_id)
            faq.question = question
            faq.answer = answer
            faq.category = category
            faq.save()
            messages.success(request, 'FAQ updated successfully.')
        else:
            # Create new
            FAQ.objects.create(question=question, answer=answer, category=category)
            messages.success(request, 'FAQ added successfully.')

        return redirect('faq_dashboard')

    # GET request: show all FAQs
    faqs = FAQ.objects.all().order_by('-created_at')

    # Pre-fill form if editing (via GET param or context)
    edit_faq = None
    edit_id = request.GET.get('edit')
    if edit_id:
        edit_faq = get_object_or_404(FAQ, id=edit_id)

    return render(request, 'faq_dashboard.html', {
        'faqs': faqs,
        'edit_faq': edit_faq
    })
@staff_member_required
def delete_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    faq.delete()
    messages.success(request, 'FAQ deleted.')
    return redirect('faq_dashboard')


from django.contrib.auth import authenticate, login, logout
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:  # Only allow staff/admin users
                login(request, user)
                next_url = request.GET.get('next', '/faq-dashboard/')
                return redirect(next_url)
            else:
                messages.error(request, 'Access denied. Admins only.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def admin_logout(request):
    logout(request)

    return redirect('admin_login')
