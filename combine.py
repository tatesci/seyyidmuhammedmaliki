# -*- coding: utf-8 -*-
"""Beş kitabı tek uygulama verisinde birleştirir."""
import json, io, os, re, unicodedata

# ---- Şevâriku'l-Envâr (mevcut, Arapça yeniden dizilebilir metin) --------
sev = json.load(io.open('app_data_v2.json', encoding='utf-8'))
four = json.load(io.open('four_data_v2.json', encoding='utf-8'))

# 4 kitap için bölüm tanımları: (baslangic_sayfa, baslik, altbaslik)
SECTIONS = {
    'Sabah': [(1, 'İstiğfâr-ı Kebîr', 'İmam Ahmed bin İdrîs'),
              (2, 'Virdü’l-Latîf', 'İmam Abdullâh bin Alevî el-Haddâd'),
              (11, 'Râtibü’l-İmâm', 'İmam Ömer bin Abdurrahmân el-Attâs'),
              (14, 'Salâtü’l-Azîmiyye', 'İmam Ahmed bin İdrîs'),
              (15, 'Bağışlama Duası', '')],
    'Ak': [(1, '', '')],  # başlık/alt başlık kullanıcı isteğiyle kaldırıldı (bkz. heroSub)
    'Kalb': [(1, 'Günlük Tesbihat Virdi', 'Kalbî Kemâlât')],
    'Kaside': [(1, 'Kasîde-i Muhammediyye', '')],  # 'İmam Bûsîrî' hero'daki sub ile tekrar ediyordu, kullanıcı isteğiyle kaldırıldı
}

META = {
    'Sabah':  dict(titleAr='وِرْدُ الصَّبَاح', accent='#C2703C',
                   sub='Sabah namazından sonra okunan evrâd'),
    'Ak':     dict(titleAr='وِرْدُ الْمَسَاء', accent='#4A5F8A',
                   sub='Akşam namazından sonra okunan evrâd'),
    'Kalb':   dict(titleAr='وِرْدُ الْكَمَالَات', accent='#5C7A4A',
                   sub='Günlük tesbihat ve zikir'),
    'Kaside': dict(titleAr='الْقَصِيدَةُ الْمُحَمَّدِيَّة', accent='#8C4A63',
                   sub='İmam Bûsîrî’nin methiyesi'),
}
ORDER = ['Sabah', 'Ak', 'Kalb', 'Kaside']

DROP = re.compile(r'^(Sabah Evrâdı|Akşam Evrâdı|Kalbî Kemâlât Virdi|'
                  r'Kasîde[‐-]i Muhammediyye)$')


def norm_search(t):
    o = []
    for ch in t:
        if 0xFB50 <= ord(ch) <= 0xFEFC:
            d = unicodedata.normalize('NFKC', ch)
            o.append(d.lstrip(' ') if len(d) > 1 else d)
        else:
            o.append(ch)
    s = ''.join(o)
    s = re.sub(r'[ً-ٰٟۖ-ۭ]', '', s)
    s = re.sub(r'[آأإٱ]', 'ا', s)
    s = s.replace('I', 'ı').replace('İ', 'i').lower()
    return re.sub(r'\s+', ' ', s).strip()


def _line_unit(blocks):
    """Bir kitapta TEK SATIRLIK Arapça kırpmanın punto yüksekliği.

    Maskelerin çoğu tek satırdır; bu yüzden hpt değerlerinin modu (2pt'lik
    kovalarda) bir satırın yüksekliğini verir. Satır sayısı buradan türetilir
    ve tüm kitaplıkta 'satır sayısı x sabit satır yüksekliği' kuralıyla
    Arapça her yerde AYNI büyüklükte gösterilir.
    """
    import collections
    hs = [b.get('hpt') for b in blocks if b.get('role') == 'arimg' and b.get('hpt')]
    if not hs:
        return 20.0
    c = collections.Counter(round(h / 2) * 2 for h in hs)
    mode = c.most_common(1)[0][0]
    lo = min(hs)
    # mod, en küçüğün 1.6 katından büyükse muhtemelen çok satırlı bloklar
    # baskın demektir; o zaman en küçüğü esas al.
    return float(lo if mode > lo * 1.6 else mode)


books = []

# 1) Şevâriku'l-Envâr
books.append({
    'id': 'sev', 'title': "Şevâriku'l-Envâr", 'titleAr': 'شَوَارِقُ الأَنْوَار',
    'sub': "Min ed'iyeti's-sâdeti'l-ahyâr",
    'by': 'es-Seyyid Muhammed bin Alevî el-Mâlikî el-Hasenî',
    'accent': '#B08A34', 'reflow': True,
    'sections': [{'title': s['title'], 'titleAr': s['titleAr'], 'sub': s['sub'],
                  'blocks': s['blocks'], 'search': s['search']}
                 for s in sev['sections']],
})

# 2-5) diğer dört kitap
for key in ORDER:
    src = four[key]
    m = META[key]
    defs = SECTIONS[key]
    unit = _line_unit(src['blocks'])
    secs = []
    for i, (start, title, sub) in enumerate(defs):
        end = defs[i + 1][0] if i + 1 < len(defs) else 10 ** 6
        blocks = []
        for b in src['blocks']:
            if not (start <= b['p'] < end):
                continue
            if b['role'] == 'arimg':
                nl = max(1, min(24, round((b.get('hpt') or unit) / unit)))
                blocks.append({'k': 'arimg', 'img': b['img'], 'w': b['w'],
                               'h': b['h'], 'nl': nl})
                continue
            t = (b.get('text') or '').strip()
            if not t or DROP.match(t):
                continue
            k = {'translit': 'translit', 'turkish': 'turkish',
                 'note': 'note', 'cap': 'cap', 'head': 'head',
                 'arabic': 'arabic', 'title_ar': 'title_ar'}.get(b['role'], 'turkish')
            blocks.append({'k': k, 't': t})
        txt = ' '.join(b.get('t', '') for b in blocks)
        secs.append({'title': title, 'titleAr': '', 'sub': sub, 'blocks': blocks,
                     'search': norm_search(title + ' ' + sub + ' ' + txt)})
    books.append({'id': key.lower(), 'title': src['title'], 'titleAr': m['titleAr'],
                  'sub': m['sub'], 'by': '', 'accent': m['accent'],
                  'reflow': key in ('Sabah', 'Ak', 'Kaside', 'Kalb'), 'sections': secs,
                  # Akşam Evrâdı: hero'daki "Akşam Evrâdı" (lat) tekrarı ve alt
                  # yazı, kullanıcı isteğiyle kaldırıldı (bölüm başlığıyla
                  # gereksiz tekrar oluşturuyordu). Diğer kitaplar etkilenmez.
                  **({'heroSub': False} if key == 'Ak' else {})})

# 6) Muhammed el-Mâlikî hayatı/tez PDF'inden çıkarılan düz metin (taslak -
#    okunuşlu/mealli evrâd yapısında DEĞİL, sade Türkçe akademik metin;
#    extract_thesis1.py ile üretildi, kullanıcıyla birlikte kademeli
#    biçimlendirilecek).
try:
    books.append(json.load(io.open('thesis1_data.json', encoding='utf-8')))
except FileNotFoundError:
    pass

data = {'books': books}
io.open('library.json', 'w', encoding='utf-8').write(
    json.dumps(data, ensure_ascii=False, separators=(',', ':')))
print('library.json  %.2f MB' % (os.path.getsize('library.json') / 1048576))
for b in books:
    nb = sum(len(s['blocks']) for s in b['sections'])
    ni = sum(1 for s in b['sections'] for x in s['blocks'] if x.get('k') == 'arimg')
    nls = sorted(x['nl'] for s in b['sections'] for x in s['blocks'] if x.get('k') == 'arimg')
    print('  %-24s bolum=%-3d blok=%-5d arapca_gorsel=%-3d satir: %s' %
          (b['title'], len(b['sections']), nb, ni,
           ('%d..%d' % (nls[0], nls[-1])) if nls else '-'))
