from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import ChatSession, Message
from .bot import ChatBot

# Initialize the chatbot
chatbot = None

def get_chatbot():
    global chatbot
    if chatbot is None:
        chatbot = ChatBot()
        # Chỉ train sau khi đã tạo bảng
        try:
            chatbot.train_from_database()
        except:
            pass
    return chatbot

@login_required
def chat_view(request):
    # Get or create active chat session
    session, created = ChatSession.objects.get_or_create(
        user=request.user,
        is_active=True
    )
    
    # Get chat history
    messages = Message.objects.filter(session=session)
    
    context = {
        'session': session,
        'messages': messages
    }
    
    return render(request, 'chatbot/chat.html', context)

@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message_text = data.get('message', '')
        
        # Get active session
        session = get_object_or_404(ChatSession, user=request.user, is_active=True)
        
        # Process message and get response
        bot = get_chatbot()
        bot_message = bot.process_message(session, message_text)
        
        return JsonResponse({
            'response': bot_message.content,
            'timestamp': bot_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def new_session(request):
    # Set all current sessions to inactive
    ChatSession.objects.filter(user=request.user, is_active=True).update(is_active=False)
    
    # Create new session
    ChatSession.objects.create(user=request.user, is_active=True)
    
    return redirect('chat_view')