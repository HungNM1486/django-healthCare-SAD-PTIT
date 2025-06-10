# chatbot/bot.py
from .models import Intent, TrainingPhrase, Response, Message, ChatSession
from .nlp import NLPProcessor
import random
import re

class ChatBot:
    def __init__(self):
        self.nlp = NLPProcessor()
        self.fallback_responses = [
            "Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể hỏi về các bệnh như: cảm cúm, sốt xuất huyết, tiêu chảy, viêm phổi, tay chân miệng, thủy đậu, sởi, viêm gan B, lao phổi, tiểu đường.",
            "Tôi không chắc mình hiểu đúng ý bạn. Hãy thử hỏi cụ thể về triệu chứng, điều trị hoặc cách phòng ngừa của một bệnh cụ thể.",
            "Có vẻ câu hỏi này nằm ngoài kiến thức của tôi. Tôi có thể tư vấn tốt nhất về 10 bệnh phổ biến tại Việt Nam."
        ]
        
        self.greeting_patterns = [
            r'\b(xin chào|chào|hello|hi)\b',
            r'\b(chào buổi sáng|chào buổi chiều|chào buổi tối)\b'
        ]
        
        self.disease_keywords = {
            'cảm_cúm': ['cảm', 'cúm', 'sốt', 'ho', 'sổ mũi', 'đau đầu'],
            'sốt_xuất_huyết': ['sốt xuất huyết', 'muỗi vằn', 'chảy máu', 'tiểu cầu'],
            'tiêu_chảy': ['tiêu chảy', 'đi ngoài', 'đau bụng', 'oresol'],
            'viêm_phổi': ['viêm phổi', 'ho đờm', 'khó thở', 'đau ngực'],
            'tay_chân_miệng': ['tay chân miệng', 'nốt phỏng', 'loét miệng'],
            'thủy_đậu': ['thủy đậu', 'mụn nước', 'ngứa'],
            'sởi': ['sởi', 'phát ban', 'koplik'],
            'viêm_gan_B': ['viêm gan', 'gan b', 'vàng da', 'hbsag'],
            'lao_phổi': ['lao', 'ho máu', 'ho kéo dài', 'bcg'],
            'tiểu_đường': ['tiểu đường', 'đường huyết', 'đái tháo đường']
        }
    
    def train_from_database(self):
        # Get all intents and training phrases from database
        intents = Intent.objects.all()
        training_phrases = []
        intent_names = []
        
        for intent in intents:
            phrases = TrainingPhrase.objects.filter(intent=intent)
            for phrase in phrases:
                training_phrases.append(phrase.text)
                intent_names.append(intent.name)
        
        # Train NLP model if we have data
        if training_phrases and intent_names:
            self.nlp.train_model(training_phrases, intent_names)
    
    def detect_disease_context(self, message_text):
        """Detect which disease the user might be asking about"""
        message_lower = message_text.lower()
        
        for disease, keywords in self.disease_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return disease
        
        return None
    
    def is_greeting(self, message_text):
        """Check if message is a greeting"""
        message_lower = message_text.lower()
        for pattern in self.greeting_patterns:
            if re.search(pattern, message_lower):
                return True
        return False
    
    def process_message(self, session, message_text):
        # Check for empty database
        if Intent.objects.count() == 0:
            return self._create_error_response(session, message_text, 
                "Hệ thống đang được cập nhật. Vui lòng thử lại sau.")
        
        # Check for greeting
        if self.is_greeting(message_text):
            intent_name = 'chào_hỏi'
        else:
            # Try to detect disease context first
            disease_context = self.detect_disease_context(message_text)
            
            # Predict intent using NLP
            intent_name, confidence = self.nlp.predict_intent(message_text)
            
            # If NLP confidence is low but we detected disease context, use that
            if confidence < 0.3 and disease_context:
                intent_name = disease_context
                confidence = 0.5
        
        # Get response based on intent
        if intent_name:
            try:
                intent = Intent.objects.get(name=intent_name)
                responses = Response.objects.filter(intent=intent).order_by('-priority')
                
                if responses:
                    # For disease queries, try to match specific aspect (symptoms, treatment, prevention)
                    message_lower = message_text.lower()
                    
                    if any(word in message_lower for word in ['phòng', 'ngừa', 'tránh', 'vaccine']):
                        # Look for prevention responses
                        prevention_responses = [r for r in responses if 'phòng ngừa' in r.text.lower() or '🛡️' in r.text]
                        if prevention_responses:
                            response_text = prevention_responses[0].text
                        else:
                            response_text = responses[0].text
                    elif any(word in message_lower for word in ['triệu chứng', 'dấu hiệu', 'biểu hiện']):
                        # Look for symptom responses
                        symptom_responses = [r for r in responses if 'triệu chứng' in r.text.lower() or '🔴' in r.text]
                        if symptom_responses:
                            response_text = symptom_responses[0].text
                        else:
                            response_text = responses[0].text
                    else:
                        # Return most relevant response
                        response_text = responses[0].text
                else:
                    response_text = f"Tôi hiểu bạn đang hỏi về {intent_name.replace('_', ' ')}, nhưng tôi cần thêm thông tin cụ thể. Bạn muốn biết về triệu chứng, cách điều trị hay phòng ngừa?"
            except Intent.DoesNotExist:
                response_text = random.choice(self.fallback_responses)
        else:
            response_text = random.choice(self.fallback_responses)
        
        # Save messages
        Message.objects.create(
            session=session,
            sender='user',
            content=message_text
        )
        
        bot_message = Message.objects.create(
            session=session,
            sender='bot',
            content=response_text
        )
        
        return bot_message
    
    def _create_error_response(self, session, message_text, error_message):
        """Create error response and save to database"""
        Message.objects.create(
            session=session,
            sender='user',
            content=message_text
        )
        
        bot_message = Message.objects.create(
            session=session,
            sender='bot',
            content=error_message
        )
        
        return bot_message