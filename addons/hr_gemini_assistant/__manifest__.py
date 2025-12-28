# -*- coding: utf-8 -*-
{
    'name': 'HR Gemini AI Assistant',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'AI-powered assistant for HR employee information queries using Google Gemini',
    'description': """
        HR Gemini AI Assistant
        =======================
        This module integrates Google Gemini AI to help users query employee information
        in natural language. Features include:
        
        * Natural language queries about employees
        * Smart search and information retrieval
        * Chat history tracking
        * Integration with Odoo HR module
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/gemini_chat_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hr_gemini_assistant/static/src/css/gemini_chat.css',
        ],
    },
    'external_dependencies': {
        'python': ['google.generativeai'],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
