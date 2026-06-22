import os

url = os.environ['SUPABASE_URL'].strip()
key = os.environ['SUPABASE_ANON_KEY'].strip()

with open('index.html', 'r') as f:
    html = f.read()

html = html.replace('__SUPABASE_URL__', url)
html = html.replace('__SUPABASE_ANON_KEY__', key)

with open('index.html', 'w') as f:
    f.write(html)

print('Injection complete.')
