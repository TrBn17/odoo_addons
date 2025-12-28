#!/usr/bin/env python3
import xmlrpc.client

# Odoo connection info
url = "http://localhost:8069"
db = "odoo"
username = "trbaongoc17@gmail.com"
password = input("Enter your Odoo password: ")

# Authenticate
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    print(f"✅ Authenticated as user ID: {uid}")
    
    # Update module list
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    models.execute_kw(db, uid, password, 'ir.module.module', 'update_list', [])
    
    print("✅ Module list updated!")
    
    # Search for hr_gemini_assistant module
    module_ids = models.execute_kw(db, uid, password, 'ir.module.module', 'search', 
                                    [[('name', '=', 'hr_gemini_assistant')]])
    
    if module_ids:
        print(f"✅ Found hr_gemini_assistant module (ID: {module_ids[0]})")
        
        # Install the module
        models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_install', [module_ids])
        print("✅ Module hr_gemini_assistant installed successfully!")
    else:
        print("❌ Module hr_gemini_assistant not found")
else:
    print("❌ Authentication failed")
