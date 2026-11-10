#!/usr/bin/env python3
"""Read-only deterministic asset reference inventory.
Only actual web source (.html, .css, .js) counts; documentation, logs and audit
scripts never affect the classification. Conservative, not a deletion list.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
from collections import defaultdict
import json,re
root=Path.cwd()
media_ext={'.png','.jpg','.jpeg','.gif','.webp','.svg','.mp4'}
web_ext={'.html','.css','.js'}
media={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in media_ext and '.git' not in p.parts}
refs=defaultdict(list)
for page in root.rglob('*'):
    if not page.is_file() or page.suffix.lower() not in web_ext or '.git' in page.parts: continue
    try: body=unquote(page.read_text(encoding='utf-8'))
    except (UnicodeError,OSError): continue
    pagepath=page.relative_to(root).as_posix()
    # Match quoted path-like tokens, including src/href and CSS url() strings.
    candidates=re.findall(r"""['"\(]\s*([^'"\)\s<>]+\.(?:png|jpg|jpeg|gif|webp|svg|mp4)(?:\?[^'"\)\s<>]*)?)""",body,re.I)
    for token in candidates:
        url=urlsplit(token)
        if url.scheme or url.netloc or token.startswith('//'): continue
        path=unquote(url.path).lstrip('/')
        options=[path,(page.parent/path).resolve().relative_to(root.resolve()).as_posix()] if not token.startswith('/') else [path]
        for candidate in options:
            if candidate in media:
                refs[candidate].append(pagepath)
                break
unused=[(name,p.stat().st_size) for name,p in media.items() if name not in refs]
report={
 'method':'Deterministic web-source quoted asset URL scan; no docs or audit text included. Does not detect dynamically computed URLs, external deep links, or public bookmarks.',
 'media_count':len(media),
 'referenced_media_count':len(refs),
 'unmatched_media_count':len(unused),
 'unmatched_media_bytes':sum(size for _,size in unused),
 'referenced_media_bytes':sum(media[n].stat().st_size for n in refs),
 'largest_unmatched':[{'path':n,'bytes':size} for n,size in sorted(unused,key=lambda x:-x[1])[:25]],
}
print('DETERMINISTIC_ASSET_AUDIT_START')
print(json.dumps(report,indent=2))
print('DETERMINISTIC_ASSET_AUDIT_END')
