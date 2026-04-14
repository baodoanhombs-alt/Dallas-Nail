import os

def update_file(f_name):
    with open(f_name, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = content.replace("'/api/", "'https://dallas-nail.onrender.com/api/")
    content = content.replace("`/api/", "`https://dallas-nail.onrender.com/api/")
    content = content.replace('"/api/', '"https://dallas-nail.onrender.com/api/')
    
    with open(f_name, 'w', encoding='utf-8') as f:
        f.write(content)

update_file("index.html")
update_file("admin.html")
print("Done updating API links")
