import os
import re

def add_csrf_to_forms(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Regex to find <form ... method="POST"> and insert the csrf token just after the tag
                new_content = re.sub(
                    r'(<form[^>]*method=[\'"]?post[\'"]?[^>]*>)', 
                    r'\1\n    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>', 
                    content, 
                    flags=re.IGNORECASE
                )
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Added CSRF to {filepath}')

add_csrf_to_forms('templates')
