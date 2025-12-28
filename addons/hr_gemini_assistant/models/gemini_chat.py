# -*- coding: utf-8 -*-
import os
import json
import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
except ImportError:
    _logger.warning("google-generativeai library not installed. Please install it using: pip install google-generativeai")
    genai = None


class GeminiChat(models.Model):
    _name = 'gemini.chat'
    _description = 'Gemini AI Chat for HR Queries'
    _order = 'create_date desc'

    name = fields.Char(string='Chat Title', required=True, default='New Chat')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly=True)
    message_ids = fields.One2many('gemini.chat.message', 'chat_id', string='Messages')
    message_input = fields.Text(string='Message Input')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed')
    ], default='draft', string='Status')
    
    def action_send_message(self):
        """Send message from form"""
        _logger.info(f"Message input value: {self.message_input}")
        
        if not self.message_input or not self.message_input.strip():
            raise UserError('Vui lòng nhập tin nhắn trước khi gửi!')
        
        message_text = self.message_input.strip()
        self.send_message(message_text)
        
        # Clear the input field after sending
        self.message_input = ''
        
        # Return action to reload form and show new messages
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'gemini.chat',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def send_message(self, user_message):
        """Send message and get AI response with streaming"""
        if not genai:
            raise UserError('Google Generative AI library is not installed.')
        
        # Get API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise UserError('GEMINI_API_KEY not configured.')
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Create user message
        user_msg = self.env['gemini.chat.message'].create({
            'chat_id': self.id,
            'message_type': 'user',
            'content': user_message,
        })
        
        # Get employee context
        employee_data = self._get_employee_context()
        system_prompt = self._create_system_prompt(employee_data)
        
        # Call Gemini API - using the latest available model
        model = genai.GenerativeModel('gemini-2.5-flash')
        full_prompt = f"{system_prompt}\n\nUser Question: {user_message}"
        
        response = model.generate_content(full_prompt, stream=False)
        
        if response and response.text:
            ai_response = response.text
            
            # Extract employee IDs
            employee_ids = []
            for emp_data in employee_data:
                if str(emp_data['id']) in ai_response or emp_data['name'] in ai_response:
                    employee_ids.append(emp_data['id'])
            
            # Create AI message
            ai_msg = self.env['gemini.chat.message'].create({
                'chat_id': self.id,
                'message_type': 'assistant',
                'content': ai_response,
                'employee_ids': [(6, 0, employee_ids)] if employee_ids else False,
            })
            
            # Update chat state and name
            if self.state == 'draft':
                self.state = 'active'
            if self.name == 'New Chat':
                self.name = user_message[:50] + ('...' if len(user_message) > 50 else '')
            
            return ai_response
        
        raise UserError('No response from AI.')
    
    def _get_employee_context(self):
        """Get employee data"""
        employees = self.env['hr.employee'].search([])
        employee_data = []
        
        for emp in employees:
            emp_info = {
                'id': emp.id,
                'name': emp.name,
                'job_title': emp.job_title or 'N/A',
                'department': emp.department_id.name if emp.department_id else 'N/A',
                'work_email': emp.work_email or 'N/A',
                'work_phone': emp.work_phone or 'N/A',
                'manager': emp.parent_id.name if emp.parent_id else 'N/A',
                'company': emp.company_id.name if emp.company_id else 'N/A',
            }
            employee_data.append(emp_info)
        
        return employee_data
    
    def _create_system_prompt(self, employee_data):
        """Create system prompt"""
        prompt = """You are an AI assistant for HR queries. Employee data:

"""
        prompt += json.dumps(employee_data, indent=2, ensure_ascii=False)
        prompt += """

Answer questions professionally and concisely. Include employee IDs when relevant.
"""
        return prompt


class GeminiChatMessage(models.Model):
    _name = 'gemini.chat.message'
    _description = 'Gemini Chat Message'
    _order = 'create_date asc'

    chat_id = fields.Many2one('gemini.chat', string='Chat', required=True, ondelete='cascade')
    message_type = fields.Selection([
        ('user', 'User'),
        ('assistant', 'AI Assistant')
    ], required=True, string='Type')
    content = fields.Text(string='Message', required=True)
    employee_ids = fields.Many2many('hr.employee', string='Related Employees')

