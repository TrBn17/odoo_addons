# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request

class GeminiChatController(http.Controller):
    
    @http.route('/gemini_chat/send_message', type='json', auth='user')
    def send_message(self, chat_id, message):
        """Send message and get AI response"""
        chat = request.env['gemini.chat'].browse(chat_id)
        if not chat.exists():
            return {'error': 'Chat not found'}
        
        try:
            response = chat.send_message(message)
            # Reload messages
            messages = []
            for msg in chat.message_ids:
                messages.append({
                    'id': msg.id,
                    'type': msg.message_type,
                    'content': msg.content,
                    'create_date': msg.create_date.strftime('%Y-%m-%d %H:%M:%S') if msg.create_date else '',
                })
            
            return {
                'success': True,
                'messages': messages,
                'response': response
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @http.route('/gemini_chat/get_messages', type='json', auth='user')
    def get_messages(self, chat_id):
        """Get all messages for a chat"""
        chat = request.env['gemini.chat'].browse(chat_id)
        if not chat.exists():
            return {'error': 'Chat not found'}
        
        messages = []
        for msg in chat.message_ids:
            messages.append({
                'id': msg.id,
                'type': msg.message_type,
                'content': msg.content,
                'create_date': msg.create_date.strftime('%Y-%m-%d %H:%M:%S') if msg.create_date else '',
            })
        
        return {'messages': messages}
