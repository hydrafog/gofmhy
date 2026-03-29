import os
import re
import shutil

# Directories
UPSTREAM_DOCS = 'docs'
ZOLA_CONTENT = 'content'

def convert_file(src_path, dest_path):
    with open(src_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    # Filter out nsfw lines first globally
    lines = raw_content.splitlines()
    lines = [line for line in lines if 'nsfw' not in line.lower()]
    content = "\n".join(lines)

    frontmatter = {}
    body = content

    # 1. Extract Frontmatter
    if content.startswith('---'):
        parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3:
            yaml_fm = parts[1]
            body = parts[2]
            
            # Simple YAML to dict conversion
            for line in yaml_fm.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    key = key.strip()
                    val = val.strip()
                    if val.lower() == 'true': val = True
                    elif val.lower() == 'false': val = False
                    elif val.replace('.','',1).isdigit():
                        if '.' in val: val = float(val)
                        else: val = int(val)
                    else:
                        # Strip quotes if present
                        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                            val = val[1:-1]
                    frontmatter[key] = val

    # 2. Clean up Body
    # Remove "Back to Wiki Index" links
    body = re.sub(r'^\s*\*\*\[◄◄ Back to Wiki Index\].*?\n', '', body, flags=re.MULTILINE)
    body = re.sub(r'◄◄ Back to Wiki Index\]\(https://www\.reddit\.com/r/FREEMEDIAHECKYEAH/wiki/index\)\*\*', '', body)
    body = re.sub(r'\[◄◄ Back to Wiki Index\].*?\n', '', body)
    
    # Remove redundant separators at the top of the body
    body = body.strip()
    body = re.sub(r'^([\*-_]{3,}\s*)+', '', body)
    body = body.strip()

    # Clean up VitePress things
    body = re.sub(r'<Post\s+[^>]*/>', '', body)
    body = re.sub(r'<script\s+setup>.*?</script>', '', body, flags=re.DOTALL)
    body = re.sub(r':::info\s*(.*?)\s*:::', r'{% alert(icon="info", title="Note") %}\n\1\n{% end %}', body, flags=re.DOTALL)
    body = re.sub(r':::tip\s*(.*?)\s*:::', r'{% alert(icon="lightbulb", title="Tip") %}\n\1\n{% end %}', body, flags=re.DOTALL)
    body = re.sub(r':::warning\s*(.*?)\s*:::', r'{% alert(icon="warning", title="Warning") %}\n\1\n{% end %}', body, flags=re.DOTALL)
    body = re.sub(r':::danger\s*(.*?)\s*:::', r'{% alert(icon="warning-octagon", title="Caution") %}\n\1\n{% end %}', body, flags=re.DOTALL)

    # 3. Construct Zola File
    if not frontmatter:
        title = os.path.basename(src_path).replace('.md', '').replace('-', ' ').title()
        frontmatter['title'] = title

    # Ensure date is a string for TOML if it exists
    toml_fm = "+++\n"
    for k, v in frontmatter.items():
        if isinstance(v, bool):
            toml_fm += f'{k} = {str(v).lower()}\n'
        elif isinstance(v, (int, float)):
            toml_fm += f'{k} = {v}\n'
        else:
            # Escape backslashes and quotes
            v_escaped = str(v).replace('\\', '\\\\').replace('"', '\\"')
            toml_fm += f'{k} = "{v_escaped}"\n'
    toml_fm += "+++\n"

    # Ensure dest dir exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(toml_fm + "\n" + body)

# Walk through upstream docs
if os.path.exists(UPSTREAM_DOCS):
    for root, dirs, files in os.walk(UPSTREAM_DOCS):
        if '.vitepress' in root:
            if 'notes' in root: pass
            else: continue
                
        for file in files:
            if file.endswith('.md'):
                rel_path = os.path.relpath(os.path.join(root, file), UPSTREAM_DOCS)
                if rel_path.startswith('.vitepress/notes/'):
                    target_rel_path = rel_path.replace('.vitepress/notes/', 'notes/')
                else:
                    target_rel_path = rel_path
                    
                if 'nsfw' in rel_path.lower() or target_rel_path in ['posts.md', 'other.md', 'index.md']:
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
