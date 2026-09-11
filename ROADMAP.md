# Evrâd Kitaplığı — Proje Geçmişi / Roadmap

Bu dosya, projenin başından bugüne yapılan tüm işleri kronolojik olarak
özetler. Yeni bir sohbet oturumu bu klasörle devam ederken önce
[CLAUDE.md](CLAUDE.md)'yi, sonra bu dosyayı okumalı.

---

## 📖 Proje Özeti

6 kitaplık, statik (backend'siz) bir dinî metin okuma web sitesi:

1. **Şevâriku'l-Envâr** — es-Seyyid Muhammed bin Alevî el-Mâlikî el-Hasenî
2. **Sabah Evrâdı**
3. **Akşam Evrâdı**
4. **Kalbî Kemâlât Virdi** (şifreli — `102030`)
5. **Kasîde-i Muhammediyye** — İmam Bûsîrî
6. **Muhammed el-Mâlikî'nin Hayatı, Eserleri ve Tasavvufî Görüşleri** — Azat
   Toktonalıev, Ankara Üniversitesi SBE, Doktora Tezi (2016)

Her okunabilir blok üç katmandan (Arapça / Okunuş [translit, mavi] / Meâl
[turkish, yeşil]) birine ait olabilir; kullanıcı bu üç katmanı ayrı ayrı
açıp kapatabilir (dock'taki Arapça/Okunuş/Meâl butonları).

---

## 🗓️ Kronolojik Geçmiş

### Faz 0 — Kaynak kitaplığın kuruluşu ve ilk düzeltmeler (kalıtsal)
- Sabah/Akşam/Kalbî Kemâlât/Kasîde metinleri (`four_data_v2.json`) orijinal
  PDF'lere birebir sadık kalınarak dijitalleştirildi; yalnızca Türkçe
  yazım hataları (boşluk/noktalama, büyük harf tutarlılığı) düzeltildi,
  Arapça metne dokunulmadı.
- Şevâriku'l-Envâr'da (`app_data_v2.json`) parantez kullanım kuralı
  (paren-convention) tutarlılığı sağlandı: boş parantez yok, ters/negatif
  denge yok, "(N defa)" gibi sayaç ifadeleri doğru biçimde parantezlenmiş.
- **Kalıtsal not — henüz çözülmedi:** `app_data_v2.json`'da bir bölümde
  (`sec5[13]`), `sec5[14]`'ün ("Bismillâhi Kâf Hâ Yâ Ayn Sâd. Bismillâhi Hâ
  Mîm Ayn Sîn Kâf. Kemâin enzelnâhü mines semâi") kısaltılmış/satır-kaydırma
  kalıntısı gibi görünen bir kopyası bulunmuştu. Silinmesi düşünülmüş ama
  kullanıcıya sorulmadan dokunulmamıştı. **Hâlâ açık bir konu** — ileride
  gündeme gelirse önce kullanıcıya göster.

### Faz 1 — İki yeni PDF kitabın değerlendirilmesi
Kullanıcı iki PDF gönderdi:
- **"Kâmil İnsan Hazreti Muhammed"** (308 sayfa, 63MB) — tamamen TARANMIŞ
  GÖRÜNTÜLERDEN oluşuyor, dijital metin katmanı yok. Bu ortamda OCR aracı
  yok; ayrıca Claude Artifact platformunda "assets" (dosya yükleme)
  kapasitesi bu hesapta mevcut değil (63MB'lık ham dosya barındırılamaz).
  **Kullanıcı kararı: "bunu atla işlem yapma, eklemeyelim."** Bu kitap
  kitaplığa HİÇ eklenmedi.
- **"Seyyid Muhammed Maliki Hayatı Eserleri ve Tasavvufi Görüşleri"** (162
  sayfa, 1,7MB) — gerçek bir dijital metin katmanına sahip (PyMuPDF/`fitz`
  ile metin çıkarılabildi). **Kullanıcı kararı: "Evet, metni çıkarıp ekle."**
  Metin çıkarılıp 7 bölüme ayrıldı (Önsöz/Giriş/Birinci Bölüm/İkinci
  Bölüm/Sonuç/Bibliyografya/Özet), sayfa numarası satırları temizlendi,
  satır-sonu kelime bölme tireleri (`çalışma-` + `mızı` → `çalışmamızı`)
  birleştirildi — ama "el-Mâlikî", "eş-Şâfiî" gibi gerçek Arapça-transliterasyon
  isim öneklerindeki tirelere DOKUNULMADI (bir prefix beyaz listesiyle ayırt
  edildi). Sonuç `thesis1_data.json` olarak kitaplığın **6. kitabı** oldu
  (rol her yerde `"turkish"` — ayrı Arapça/okunuş katmanı yok, düz akademik
  Türkçe metin).
- Bu vesileyle `lib_template.html`'deki okuma dock'u (Arapça/Okunuş/Meâl
  butonları) HER KİTAP için o kitapta GERÇEKTEN var olan katmanlara göre
  DİNAMİK hale getirildi — önceden hep 3 buton sabit gösteriliyordu, bu da
  hem yeni tek-katmanlı tez kitabında hem de translit'i olmayan Kalbî
  Kemâlât Virdi'de (geriye dönük fark edilen bir hata) yanlış/ölü butonlar
  gösteriyordu.

### Faz 2 — Gerçek web sitesine taşıma
- Kullanıcı "yeni aldığım bir web sitesine ekleyelim" dedi; hosting türü
  netleştirildi: **cPanel/FTP (paylaşımlı hosting)**, ana sayfaya yerleştirme.
- `make_standalone.py` yazıldı — Claude Artifact'ın otomatik sardığı
  doctype/html/head/body iskeletini `lib.html`'e elle ekleyip gerçek bir
  web sitesinde çalışacak `index.html` üretir.
- Site https://seyyidmuhammedmaliki.com/ adresine yüklendi, canlı doğrulandı
  (6 kitap, şifre kilidi, arama, mobil uyumluluk, HTTPS — hepsi çalışıyor).

### Faz 3 — Güncelleme iş akışı (o dönem: FTP-only, ARTIK GEÇERLİ DEĞİL)
- Kullanıcı gelecekteki değişiklikleri Claude'un canlıda doğrudan
  güncellemesini istedi. Hosting'in SSH sunmadığı netleşti (yalnızca
  FTP/cPanel Dosya Yöneticisi). Şifre/FTP bilgilerini Claude'un kendisi
  girmesi güvenlik politikası gereği YASAK (kullanıcı izin verse bile).
- O dönem kurulan iş akışı: Claude kaynak dosyaları düzenler → 3 adımlı
  derleme → yeni `index.html`'i kullanıcıya gönderir → kullanıcı elle
  cPanel'e yükler.
- **2026-09-11 itibarıyla bu model TERK EDİLDİ** — bkz. Faz 7 (Vercel/GitHub).

### Faz 4 — "Türkçe okunuş (N defa) → doğru Arapça terim" düzeltmesi, 1. tur
Kullanıcı: mavi (Okunuş/translit) satırlarda "(3 defa)", "(4 defa)",
"(7 defa)", "(50 defa)" gibi Türkçe sayaç ifadelerinin yanlış olduğunu, doğru
Arapça karşılıklarının kullanılması gerektiğini bildirdi. Tam eşleştirme
tablosu:

| Yanlış | Doğru |
|---|---|
| (3 defa) | (Salâse) |
| (4 defa) | (Erbea) |
| (7 defa) | (Seb'a) |
| (40 defa) | (Erbe'îne) |
| (50 defa) | (Hamsîne) |
| (11 defa) | (İhdâ 'aşrete merraten) |

**Kesin kısıt: SADECE mavi (translit) bloklar — yeşil (turkish/mana) veya
Arapça bloklar KESİNLİKLE dokunulmayacak**, aynı kalıp orada da geçse bile.

- `role`/`k`'ye göre filtrelenmiş bir tarama yapıldı, **19 blok** düzeltildi
  (çoğu Akşam Evrâdı, 1 tanesi Sabah Evrâdı). **Bu tur, regex'te
  `re.IGNORECASE` KULLANMADIĞI için "(3 Defa)" gibi büyük-D'li yazılmış
  onlarca kaydı KAÇIRDI — bu hata Faz 8'de bulunup düzeltildi.**
- Ayrıca kullanıcının bahsettiği "(selasen)"/"(erbea(" gibi ek varyantlar
  arandı: Şevâriku'l-Envâr'ın translit bloklarında ZATEN doğru Arapça
  terimlerin (Selâsen, Erba'an, Seb'an, Aşran gibi tanwin'li klasik biçimler)
  kullanıldığı görüldü — bu kitap için düzeltme gerekmedi, zaten doğruydu.
  Yalnızca bir bölümde ("Bahr Hizbi" civarı) "(Selâsen)" yerine yanlışlıkla
  "(selasen)"/"(Selasen)" (â şapkası eksik) yazılmış 2 kayıt bulunup
  kullanıcıya bildirildi (henüz kullanıcı onayı beklenmedi, ayrı bir konu
  olarak flagly bırakıldı — sonra Faz 5'te kullanıcı onaylayıp düzeltildi).

### Faz 5 — İki ek düzeltme (kullanıcı onayıyla)
1. `"ᣒ LÂ İLÂHE İLLALLÂHU..."` (Kalbî Kemâlât Virdi) satırının başındaki
   anlamsız/bozuk karakter (muhtemelen eski bir metin dönüşümünden kalma
   encoding artığı, U+18D2) kaldırıldı.
2. Aynı kitapta "UĞLİG"/"SEBEG"/"MİGDÂRİHİL" (Arapça ق harfinin "g" yerine
   "k" ile transliterasyonu gerekirken hatalı yazılmış) → "UĞLİKA"/
   "SEBEKA"/"MİKDÂRİHİL" olarak düzeltildi.

### Faz 6 — Kelime düzeltmeleri: GUVVETE/GADÎR
Kullanıcı "kitapların içerisinde GUVVETE→KUVVETE, GADÎR→KADÎR" düzeltmesini
istedi. Kitaplığın TAMAMI tarandı, her iki kelimenin de yalnızca **Kalbî
Kemâlât Virdi**'de birer kez geçtiği bulundu ve düzeltildi:
- "LÂ HAVLE VE LÂ GUVVETE İLLÂ..." → "...LÂ KUVVETE İLLÂ..."
- "...HUVE ALÂ KULLİ ŞEY'İN GADÎR" → "...GADÎR" → "...KADÎR"

### Faz 7 — UI/UX iyileştirmeleri (site görünümü/davranışı)
1. **Kaydırma-kayması hatası düzeltildi:** Bir katmanı (Arapça/Okunuş/Meâl)
   açıp kapatınca, o katmandaki bloklar TÜM kitap boyunca gizlenip
   sayfanın toplam yüksekliği değişiyor, ama tarayıcı `scrollY`'yi olduğu
   gibi koruyordu — bu da okuyucunun "birkaç bölüm geriye gitmiş" gibi
   hissetmesine yol açıyordu (bazı senaryolarda 1000+ piksel kayma
   ölçüldü). Çözüm: katman değişmeden hemen önce ekranda görünen (ve
   kapatılan katmana AİT OLMAYAN) bir referans bloğun ekran konumu
   kaydedilir, değişiklikten sonra `window.scrollBy` ile o blok TAM AYNI
   ekran konumuna geri getirilir. `lib_template.html`'deki `d.layer`
   click-handler'ında (`document.addEventListener('click', ...)`).
2. **Güneş/ay hızlı tema geçişi eklendi:** Üst çubuğa (Arama ile Ayarlar
   ikonu arasına) tek dokunuşla Gündüz↔Gece geçişi yapan bir ikon
   eklendi (`data-themetoggle`, `effectiveDark()` yardımcı fonksiyonu).
   Önceden yalnızca "AA" (Ayarlar) panelinin içindeki "Görünüm" bölümünde
   Gündüz/Gece/Cihaz seçeneği vardı (hâlâ duruyor, ikisi senkron).
3. **Ana sayfa metin değişiklikleri:**
   - Başlık: "Evrâd ve Ezkâr" + alt yazı "Vird, ezkâr ve tasavvufî eserler
     kitaplığı" → tek satır **"Evrâd ve Ezkâr Kütüphanesi"**.
   - Alt not: "Metinler asıllarına birebir sadık alınmıştır. Okuduklarınızı
     cem edenlerin..." → **"Metinlerde asıllarına birebir sadık
     kalınmıştır. Yanlışlık görülmesi durumunda, düzeltilmesi için 0534 370
     5858 nolu hat kullanıcısına bildiriniz. Rabbim rızasından
     ayırmasın."**

### Faz 8 — "(N defa)" düzeltmesi, 2. tur — case-insensitivity hatası bulundu
Kullanıcı "sabah evradında hâlâ birçok yerde (3 defa) vs. yazıyor" dedi.
İlk taramanın **case-sensitive** olduğu (küçük harf "defa" arayıp büyük
"Defa"yı atladığı) fark edildi — bu, Faz 4'ün gerçek bir hatasıydı.

- Tüm kitaplık `re.IGNORECASE` ile yeniden tarandı: **28 ek blok** bulundu,
  hepsi Sabah Evrâdı'nda, hepsi "(N **D**efa)" (büyük D) biçimindeydi.
  Aynı 6 maddelik tabloyla düzeltildi.
- Kapsamlı bir final taramasında (tüm 6 kitap, tüm translit blokları) **4
  ek özel kalıp** bulundu, kullanıcının verdiği 6 maddelik tabloya
  UYMADIĞI için kullanıcıya soruldu, doğru terimler alındı ve uygulandı:

  | Yanlış | Doğru | Kitap |
  |---|---|---|
  | (1 defa) | (Merrah) | Akşam Evrâdı |
  | (10 Defa) ×2 | (Aşra marrât) | Sabah Evrâdı |
  | (40 veya 100 Defa) | (Erba'îne merrah veya Mi'ete merrah) | Sabah Evrâdı |

- Bu turdan sonra kitaplığın TAMAMI (6 kitap × tüm bölümler × tüm bloklar)
  JavaScript ile taranıp **mavi (translit) bloklarda "defa" kelimesinin SIFIR**
  kaldığı, yeşil (turkish/mana) bloklarda ise (beklendiği gibi, dokunulmadan)
  hâlâ 78 kez geçtiği doğrulandı.

### Faz 9 — Proje klasörü taşındı, dağıtım modeli Vercel'e geçti (2026-09-11)
- Kullanıcı `C:\Claude\sseyyidmuhammedmaliki` klasörünü oluşturup buraya
  git (`.git`) + bir `güncelle.bat` (git add/commit/push scripti) kurdu.
- **Dağıtım modeli tamamen değişti:** artık cPanel/FTP yerine **GitHub
  (tatesci/seyyidmuhammedmaliki) + Vercel (serverless) entegrasyonu**
  kullanılıyor — `main` dalına push, Vercel'de otomatik dağıtım tetikliyor.
  Eski "SSH yok, elle FTP yükle" kısıtı artık geçerli değil.
- Tüm kaynak dosyalar (`app_data_v2.json`, `four_data_v2.json`,
  `thesis1_data.json`, `lib_template.html`, `combine.py`, `mklib.py`,
  `make_standalone.py`, `library.json`) eski Desktop klasöründen bu yeni
  proje klasörüne kopyalandı; 3 adımlı derleme burada TEKRAR çalıştırılıp
  üretilen `index.html`'in mevcut (git'teki) `index.html` ile **byte-byte
  (MD5) birebir aynı** olduğu doğrulandı — yani kaynak ile canlı dosya
  senkron, kayıp/fark yok.
- Bu `CLAUDE.md` ve `ROADMAP.md` bu oturumda ilk kez oluşturuldu.

---

## 🧰 Öğrenilen Dersler / Tekrarlanan Hatalar

1. **Regex'i her zaman `re.IGNORECASE` yaz** — Faz 8'in kök nedeni buydu.
2. **Bash `-c` inline Python kodu Türkçe/Arapça karakterleri bozar** —
   her zaman `Write` tool ile ayrı `.py` dosyası oluştur.
3. **"Karşılığı bilinmeyen bir varyant kalıp" bulununca ASLA tahmin
   etme** — kullanıcıya sor (Faz 8'deki 4 özel kalıp örneği gibi).
4. **Bir düzeltmeyi "tamamlandı" ilan etmeden önce TÜM kitaplığı (yalnızca
   bahsedilen kitabı değil) tarayarak çapraz doğrula** — kullanıcının "X
   kitabında hâlâ var" demesi, aslında sorunun her yerde olabileceğinin
   işaretidir.
5. **Aynı porttaki eski bir yerel önizleme sunucusu bir sonraki testi
   bozabilir** — her doğrulama turunda taze/boş bir port kullan, işin
   bitince kapat.
