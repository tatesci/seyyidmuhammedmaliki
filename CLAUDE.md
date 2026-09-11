# Evrâd Kitaplığı — Proje Bilgileri (CLAUDE.md)

## Proje Nedir

6 kitaplık bir **dinî metin okuma web sitesi**: Şevâriku'l-Envâr, Sabah Evrâdı,
Akşam Evrâdı, Kalbî Kemâlât Virdi, Kasîde-i Muhammediyye, Muhammed el-Mâlikî'nin
Hayatı-Eserleri-Tasavvufî Görüşleri (doktora tezi, düz metin). Tek sayfalık
statik bir HTML/CSS/JavaScript uygulaması — backend yok, tüm veri tek bir
`<script type="application/json">` içine gömülü.

**Bu proje NetPlus muhasebe yazılımıyla TAMAMEN İLGİSİZDİR** — aynı fiziksel
makinede çalışan ayrı, bağımsız bir iştir. Bu klasörü (`C:\Claude\sseyyidmuhammedmaliki`)
başka hiçbir projenin dosyalarıyla karıştırma.

## Canlı Site

**https://seyyidmuhammedmaliki.com/**

Kalbî Kemâlât Virdi kitabı şifreyle korunur (`102030`, `lib_template.html`
içindeki `LOCKED` sabiti). Bu meraklı gözlere karşı bir önlemdir, **teknik bir
şifreleme değildir** — içerik yine sayfanın ham kaynağında düz metin olarak
durur.

## 🚀 Dağıtım Modeli — GÜNCEL (2026-09-11'den itibaren)

**Vercel (serverless) + GitHub entegrasyonu.** Artık cPanel/FTP'ye elle dosya
yükleme YOK.

- GitHub deposu: **https://github.com/tatesci/seyyidmuhammedmaliki**
- `güncelle.bat` (bu klasörde, çift tıkla çalışır): `git add .` → commit mesajı
  sorar → `git commit` → `git push origin main`.
- Vercel bu GitHub deposuna bağlı (kullanıcı tarafından kuruldu) — `main`
  dalına yapılan her push otomatik olarak canlı siteye yansır.
- **Eski model (ARTIK KULLANILMIYOR, yalnızca tarihsel referans için):**
  Önceden paylaşımlı cPanel/FTP hosting kullanılıyordu, SSH erişimi yoktu, her
  güncelleme kullanıcı tarafından elle cPanel Dosya Yöneticisi'ne
  yükleniyordu. Bu artık geçerli değil — sil baştan bu bilgiyi kullanma.
- **⚠️ Claude'un `git push` atması hakkında:** Kod/içerik değişikliklerini
  `origin/main`'e push etmeden önce, aksi açıkça ve kalıcı olarak
  yetkilendirilmedikçe **kullanıcıya sor**. Bir push, canlı siteyi (Vercel
  otomatik dağıtımıyla) hemen günceller — bu "paylaşılan/genel durumu
  etkileyen" bir eylemdir. `git add`/`git commit` (henüz push edilmemiş,
  yerel) yapmakta sakınca yok, ama `git push`'tan önce onay iste (kullanıcı
  ileride "artık sormadan push'la" derse bu notu güncelle).

## 📁 Dosya Envanteri (bu klasörde)

| Dosya | Ne işe yarar |
|---|---|
| `app_data_v2.json` | Şevâriku'l-Envâr verisi. Blok anahtarları: `k` (rol) / `t` (metin). `sections[].blocks[]` yapısı. |
| `four_data_v2.json` | Sabah/Akşam/Kalbî Kemâlât/Kasîde verisi. Kitap anahtarları: `Sabah`/`Ak`/`Kalb`/`Kaside`. Blok anahtarları: `role`/`text`, düz `blocks[]` listesi (bölümsüz). |
| `thesis1_data.json` | Muhammed el-Mâlikî tezi — düz metin, TÜM bloklar `role:"turkish"` (Arapça/okunuş katmanı yok). |
| `lib_template.html` | Sitenin CSS + JavaScript'i. `__DATA__` yer tutucusu içerir. |
| `combine.py` | Üç veri dosyasını birleştirip `library.json` üretir. |
| `mklib.py` | `lib_template.html` + `library.json` → `lib.html` (Claude **Artifact** için — doctype/html/head/body YOK, Artifact yayınlama mekanizması otomatik sarar). |
| `make_standalone.py` | `lib.html`'i gerçek bir web sitesi için TAM/geçerli bir HTML5 belgesine sarar (`<!DOCTYPE html>` dahil) → `index.html`. |
| `index.html` | **Git'e push edilen / sitede canlı olan nihai dosya.** |
| `library.json` | Ara ürün (combine.py çıktısı, mklib.py girdisi). |
| `güncelle.bat` | Çift tıkla git add+commit+push yapan script. |

## 🔁 Yeniden Derleme Sırası (BİR İÇERİK DEĞİŞİKLİĞİ YAPTIKTAN SONRA HER ZAMAN)

```bash
python combine.py
python mklib.py
python make_standalone.py
```

Bu üç komut `app_data_v2.json` / `four_data_v2.json` / `thesis1_data.json` /
`lib_template.html`'den `index.html`'i (ve ara `library.json`/`lib.html`'i)
sıfırdan yeniden üretir. Üçünü sırayla çalıştırmak, elle hiçbir şey
düzenlemeseniz bile mevcut `index.html` ile birebir aynı sonucu üretir (bu
doğrulandı — bkz. ROADMAP.md).

## 🔒 KRİTİK KURALLAR — ASLA BOZMA

1. **Arapça metne (`role`/`k` == `"arabic"`) ASLA dokunma** — kullanıcı açıkça
   ve özellikle istemedikçe. Dört kitabın Arapça karakter sayısı/dizilimi
   orijinaline birebir sadık kalmalı.

2. **"Mavi" = Okunuş/translit, "Yeşil" = Meâl/turkish, "Altın" = Arapça.**
   Kullanıcı "mavi yazılı okunuşları düzelt" derse **SADECE** `role`/`k` alanı
   `"translit"` olan blokları değiştir. Alan adı `four_data_v2.json`'da
   `role`/`text`, `app_data_v2.json`'da `k`/`t`'dir. Aynı kalıp (ör. "(3 defa)")
   `"turkish"` (yeşil/mana) blokta da geçebilir — **kesinlikle dokunma**,
   kullanıcı özellikle o rolü de kapsıyorsa açıkça belirtir.

3. **Metin arama/değiştirme regex'leri MUTLAKA `re.IGNORECASE` (büyük/küçük
   harf duyarsız) olmalı.** 2026-09-10/11'de gerçek bir hata yaşandı:
   "(3 defa)" için yazılan **case-sensitive** bir regex, "(3 Defa)" (büyük D
   ile yazılmış) ONLARCA kaydı — özellikle Sabah Evrâdı'nda — sessizce
   atladı. Kullanıcı "sabah evradında hâlâ birçok yerde var" diye ısrarla
   tekrar sorana kadar bu fark edilmedi. **Bir daha ASLA case-sensitive bir
   metin taraması/düzeltmesi yapma** — regex'e her zaman `re.IGNORECASE`
   ekle, sonuçları TÜM kitaplıkta (yalnızca bahsedilen kitapta değil,
   tarayıcıda `DATA.books.forEach(...)` ile TÜM kitaplar+bölümler+bloklar
   üzerinde) çapraz kontrol et.

4. **ÖNCE TARA (scan), SONRA UYGULA (fix) — iki ayrı adım, asla tek adımda
   kör toplu değiştirme yapma.** Önce bulunan TÜM eşleşmeleri (rol +
   kitap + tam metin) kullanıcıya göster/say, kapsamı doğrula, SONRA
   değiştir. Kullanıcının verdiği eşleştirme tablosuna (ör. "(3 defa)" →
   "(Salâse)") **UYMAYAN** bir varyant kalıp bulunursa (ör. "(selasen)",
   "(1 defa)", "(10 defa)", "(40 veya 100 defa)" gibi bileşik/farklı sayı
   ifadeleri) — **KULLANICIYA SOR, kendi tahmininle Arapça terim
   uydurma.** Dinî bir metinde yanlış bir transliterasyon terimi ciddi bir
   hatadır.

5. **Her düzeltmeden sonra sıralı doğrulama zinciri:**
   (a) rebuild (yukarıdaki 3 komut),
   (b) yerel tarayıcıda görsel/JS ile doğrula (`python -m http.server <boş
       port>`, sonra `mcp__Claude_Browser__*` araçlarıyla — HEM mavi metinde
       düzeltmenin göründüğünü HEM yeşil metnin DEĞİŞMEDİĞİNİ kontrol et),
   (c) Claude Artifact'ı güncelle (aşağıya bak),
   (d) `index.html`'i kullanıcıya gönder (SendUserFile) VEYA — kullanıcı
       onayıyla — `güncelle.bat` mantığını uygulayıp `git push` yap.

6. **Yerel doğrulama sunucusu için HER ZAMAN boş/kullanılmayan bir port
   seç** (8099, 8131, 8171, 8172, 8173 gibi rastgele yüksek portlar — bu
   proje aynı makinede/oturumda başka projelerle [ör. NetPlus] paralel
   çalışabildiğinden port çakışması olabilir). `curl -s -o /dev/null -w
   "%{http_code}"` ile portun cevap verdiğini doğrula; işin bitince
   `pkill -f "http.server <port>"` ile KAPAT.

7. **Heredoc/inline Bash `-c` ile Türkçe/Arapça karakter içeren Python kodu
   YAZMA — mutlaka `Write` tool ile ayrı bir `.py` dosyası oluştur.** Bash
   `-c` inline string'ler Unicode karakterleri bozar (tekrarlanan bir
   sorun).

8. **Dosya adı Unicode NFC/NFD uyuşmazlığına dikkat** — Türkçe İ/â/ı gibi
   karakterler içeren bir dosya yolunu ELLE yazıp `fitz.open()`/`open()` gibi
   fonksiyonlara vermek `FileNotFoundError` verebilir (dosya sisteminde
   ayrıştırılmış/decomposed Unicode kullanılıyor olabilir). Emin değilsen
   `os.listdir()` ile gerçek dosya adını programatik olarak bul.

## 🎨 Claude Artifact (paralel önizleme, canlı siteden BAĞIMSIZ)

**https://claude.ai/code/artifact/23a5fc05-b165-4c16-9955-069cd184aa23**

Her içerik değişikliğinden sonra `lib.html`'i (`mklib.py`'nin çıktısı) bu
URL'e `Artifact` action=`"publish"` ile **yeniden yayınla** — bu, canlı site
ile senkron kalmak için AYRI/manuel bir adımdır, otomatik değildir. `favicon`
parametresini yeniden yayınlarken **verme** (artifact zaten sahip, kural
gereği aynı favicon korunmalı).

## 🔓 Kilitli Kitap

Kalbî Kemâlât Virdi şifreyle korunur (`LOCKED = {'kalb':'102030'}`,
`lib_template.html`). Yerel testte hızlıca "kilidi açmak" gerekirse tarayıcı
konsolunda `sessionStorage.setItem('unlock.kalb','1')` + sayfayı yenile
yeterlidir (şifre formunu elle doldurmaya gerek yok).

## ⚠️ Bilinen Açık/Bekleyen Konu (henüz kullanıcıya sorulup teyit edilmedi)

Şevâriku'l-Envâr'da (`app_data_v2.json`), bir bölümde (`sec5[13]`),
`sec5[14]`'ün kısaltılmış/yarım kalmış bir tekrarı gibi görünen bir translit
bloğu (`'Bismillâhi Kâf Hâ Yâ Ayn Sâd. Bismillâhi Hâ Mîm Ayn Sîn Kâf...'`nin
kesik hâli) tespit edilmişti — bkz. ROADMAP.md, "Kalıtsal Not" bölümü.
Silinmesi gerekip gerekmediği **kullanıcıya sorulmadan dokunulmadı**. İleride
gündeme gelirse önce ilgili iki bloğu kullanıcıya göster, onay almadan silme.

## 🧭 Yeni Bir Oturuma Nasıl Başlanır

1. Bu `CLAUDE.md` ve `ROADMAP.md`'yi oku.
2. Kullanıcının isteğini dinle — genelde ya (a) belirli bir kelime/kalıp
   düzeltmesi, ya (b) bir UI/özellik değişikliği (site görünümü/davranışı,
   `lib_template.html` içinde), ya da (c) yeni bir soru/inceleme olur.
3. Kural #4'e göre önce TARA, kapsamı doğrula, sonra uygula.
4. Kural #5'e göre rebuild → yerel doğrula → Artifact güncelle → kullanıcıya
   dosya gönder / (onayla) git push.
5. `ROADMAP.md`'ye yeni bir madde ekleyerek bu oturumun özetini kaydet —
   NetPlus projesindeki "her FAZ sonunda Roadmap işaretlenir" disiplininin
   hafif bir versiyonu.
