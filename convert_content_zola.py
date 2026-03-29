import os
import re
import shutil

# Directories
UPSTREAM_DOCS = 'docs'
ZOLA_CONTENT = 'content'

def convert_file(src_path, dest_path):
    with open(src_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Filter out lines containing nsfw (case-insensitive)
    filtered_lines = [line for line in lines if 'nsfw' not in line.lower()]
    
    # Strip redundant separators and "Back to Wiki Index" links at the start
    content = "".join(filtered_lines)
    # Match various patterns of the back link found in FMHY files
    content = re.sub(r'^\s*\*\*\[◄◄ Back to Wiki Index\].*?\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'◄◄ Back to Wiki Index\]\(https://www\.reddit\.com/r/FREEMEDIAHECKYEAH/wiki/index\)\*\*', '', content)
    content = re.sub(r'\[◄◄ Back to Wiki Index\].*?\n', '', content)
    
    # Remove separators again after link removal
    content = re.sub(r'^(\s*[\*-_]{3,}\s*)+', '', content, flags=re.MULTILINE)

    # Zola TOML frontmatter
    if content.startswith('---\n'):
        # Correctly split YAML frontmatter
        parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3:
            frontmatter_raw = parts[1]
            body = parts[2]
            
            toml_lines = []
            for line in frontmatter_raw.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    key = key.strip()
                    val = val.strip()
                    if val.lower() == 'true': val = 'true'
                    elif val.lower() == 'false': val = 'false'
                    # Wrap strings in quotes if they aren't already
                    elif not (val.startswith('"') or val.startswith("'") or val.replace('.','',1).isdigit()):
                        val = f'"{val}"'
                    toml_lines.append(f'{key} = {val}')
                else:
                    toml_lines.append(line)
            
            content = '+++\n' + '\n'.join(toml_lines) + '\n+++\n' + body
    elif not content.startswith('+++\n'):
        title = os.path.basename(src_path).replace('.md', '').replace('-', ' ').title()
        content = f'+++\ntitle = "{title}"\n+++\n\n' + content

    # Clean up VitePress things
    content = re.sub(r'<Post\s+[^>]*/>', '', content)
    content = re.sub(r'<script\s+setup>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r':::info\s*(.*?)\s*:::', r'{% alert(icon="info", title="Note") %}\n\1\n{% end %}', content, flags=re.DOTALL)
    content = re.sub(r':::tip\s*(.*?)\s*:::', r'{% alert(icon="lightbulb", title="Tip") %}\n\1\n{% end %}', content, flags=re.DOTALL)
    content = re.sub(r':::warning\s*(.*?)\s*:::', r'{% alert(icon="warning", title="Warning") %}\n\1\n{% end %}', content, flags=re.DOTALL)
    content = re.sub(r':::danger\s*(.*?)\s*:::', r'{% alert(icon="warning-octagon", title="Caution") %}\n\1\n{% end %}', content, flags=re.DOTALL)

    # Ensure dest dir exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Walk through upstream docs
for root, dirs, files in os.walk(UPSTREAM_DOCS):
    # Skip .vitepress folder
    if '.vitepress' in root:
        # We might want files from .vitepress/notes though
        if 'notes' in root:
             pass # process notes
        else:
            continue
            
    for file in files:
        if file.endswith('.md'):
            # Path relative to docs
            rel_path = os.path.relpath(os.path.join(root, file), UPSTREAM_DOCS)
            
            # Special case for .vitepress/notes
            if rel_path.startswith('.vitepress/notes/'):
                target_rel_path = rel_path.replace('.vitepress/notes/', 'notes/')
            else:
                target_rel_path = rel_path
            if 'nsfw' in rel_path.lower():
                continue
                
            # Colliding files check (posts.md, other.md)
            if target_rel_path in ['posts.md', 'other.md']:
                continue
                
            # Special case for index.md
            if target_rel_path == 'index.md':
                # We handle root index specially, don't overwrite our custom Home page
                continue

            src = os.path.join(root, file)
            dest = os.path.join(ZOLA_CONTENT, target_rel_path)
            
            convert_file(src, dest)

# Sync public assets
UPSTREAM_PUBLIC = os.path.join(UPSTREAM_DOCS, 'public')
ZOLA_STATIC = 'static'
if os.path.exists(UPSTREAM_PUBLIC):
    for item in os.listdir(UPSTREAM_PUBLIC):
        s = os.path.join(UPSTREAM_PUBLIC, item)
        d = os.path.join(ZOLA_STATIC, item)
        if os.path.isdir(s):
            if os.path.exists(d): shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
