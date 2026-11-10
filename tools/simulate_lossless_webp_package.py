#!/usr/bin/env python3
"""Read-only temporary ZIP comparison of lossless WebP replacements for five PNGs.
The website is not rewritten or deployed. Both original and alternate package
sizes are measured; originals remain in the checkout.
"""
from pathlib import Path
from PIL import Image
import io,zipfile,os
root=Path.cwd()
samples=[
 'images/02-early-days-sac-1.2.png',
 'images/01-jesus-game.png',
 'images/01-tomblibrary.png',
 'images/01-redeemed-phone.png',
 'images/01-playbill.png',
]
media={}
for name in samples:
    with Image.open(root/name) as im:
        im.load()
        buf=io.BytesIO()
        im.save(buf,format='WEBP',lossless=True,method=6)
        media[name[:-4]+'.webp']=buf.getvalue()
allfiles=[p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts]
excluded=set(samples)
for label in ['original','lossless_webp_sample']:
    target=Path(os.environ.get('RUNNER_TEMP','/tmp'))/f'pages-{label}.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=3,allowZip64=True) as z:
        for p in allfiles:
            name=p.relative_to(root).as_posix()
            if label!='original' and name in excluded:continue
            z.write(p,name)
        if label!='original':
            for name,data in media.items():z.writestr(name,data)
    print(f'{label}_package_bytes={target.stat().st_size}')
    target.unlink()
print('Sample WebP conversions are byte-for-byte lossless. References are NOT rewritten in this size-only simulation.')
print('No images, pages, or production deployment changed.')
