# -*- coding: utf-8 -*-
"""lib.html (Artifact-icin, dogtype/head/body OLMADAN hazirlanmis) dosyasini
gercek bir web sitesinde index.html olarak calisacak TAM/GECERLI bir HTML5
belgesine sarar. Icerik/mantik/veri OLDUGU GIBI kalir - yalnizca standart
<!DOCTYPE html><html><head>...</head><body>...</body></html> iskeleti
eklenir (Claude'un Artifact onizlemesinin otomatik yaptigi sarmalama,
gercek bir hosting'te elle yapilmasi gerekir)."""
import io, os

content = io.open('lib.html', encoding='utf-8').read()

# lib.html su sirada: <title>...</title> + font <link>'ler + <style>...</style>
# + <div id="app"></div> + <script id="kitap">...</script> + <script>...</script>
# Bunlari HEAD'e (title+link+style) ve BODY'ye (div+script'ler) ayiralim.
style_end = content.index('</style>') + len('</style>')
head_part = content[:style_end]
body_part = content[style_end:]

doc = (
    '<!DOCTYPE html>\n'
    '<html lang="tr">\n'
    '<head>\n'
    '<meta charset="UTF-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    + head_part + '\n'
    '</head>\n'
    '<body>\n'
    + body_part + '\n'
    '</body>\n'
    '</html>\n'
)

io.open('index.html', 'w', encoding='utf-8').write(doc)
print('index.html  %.2f MB' % (os.path.getsize('index.html') / 1048576))
