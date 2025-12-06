# PDF'den Blog Yazısı Oluşturucu - Kullanım Rehberi

## Kurulum

Önce gerekli Python kütüphanelerini kurun:

```bash
pip install PyMuPDF pdfplumber
```

## Kullanım

### Temel Kullanım

```bash
python pdf_to_blog.py <pdf_dosyasi.pdf>
```

Örnek:
```bash
python pdf_to_blog.py arda.tc/pdfs/ssti-nedir.pdf
```

### Özelleştirilmiş Kullanım

```bash
python pdf_to_blog.py <pdf_dosyasi.pdf> --title "Başlık" --lang tr --slug slug-adi
```

Örnekler:

```bash
# Türkçe blog yazısı
python pdf_to_blog.py document.pdf --title "SSTI Nedir?" --lang tr

# İngilizce blog yazısı
python pdf_to_blog.py document.pdf --title "What is SSTI?" --lang en --slug what-is-ssti

# Almanca blog yazısı
python pdf_to_blog.py document.pdf --title "Was ist SSTI?" --lang de --slug was-ist-ssti
```

## Parametreler

- `pdf_file` (zorunlu): PDF dosyasının yolu
- `--title`: Blog yazısı başlığı (varsayılan: PDF dosya adı)
- `--lang`: Dil kodu - `tr`, `en`, veya `de` (varsayılan: `tr`)
- `--slug`: URL slug (varsayılan: başlıktan otomatik oluşturulur)
- `--date`: Tarih (varsayılan: şimdi)

## Ne Yapar?

1. ✅ PDF'den metin çıkarır
2. ✅ PDF'den görselleri çıkarır
3. ✅ Metni temizler ve düzenler
4. ✅ Markdown formatına çevirir
5. ✅ Görselleri doğru klasöre kaydeder
6. ✅ Blog yazısı dosyası oluşturur (`_posts/YYYY-MM-DD-slug.md`)
7. ✅ Frontmatter ekler (title, date, lang, slug)

## Çıktı

- Blog yazısı: `_posts/YYYY-MM-DD-slug.md`
- Görseller: `arda.tc/images/slug/page_X_img_Y.jpeg`

## Çok Dilli Blog Yazıları

Aynı PDF'in farklı dillerdeki versiyonları için:

1. **Türkçe versiyon:**
   ```bash
   python pdf_to_blog.py document.pdf --title "Başlık" --lang tr --slug ortak-slug
   ```

2. **İngilizce versiyon:**
   ```bash
   python pdf_to_blog.py document-en.pdf --title "Title" --lang en --slug ortak-slug
   ```

3. **Almanca versiyon:**
   ```bash
   python pdf_to_blog.py document-de.pdf --title "Titel" --lang de --slug ortak-slug
   ```

**Önemli**: Aynı yazının farklı dilleri için **aynı slug** kullanın!

## Sonraki Adımlar

1. Blog yazısını kontrol et: `_posts/` klasöründe
2. Gerekirse düzenle
3. Git'e ekle: `git add .`
4. Commit yap: `git commit -m "Yeni blog yazısı eklendi"`
5. Push et: `git push`

## Sorun Giderme

### "pdfplumber kurulu değil" hatası
```bash
pip install pdfplumber
```

### "PyMuPDF kurulu değil" uyarısı
Görseller çıkarılamaz ama metin çıkarılabilir:
```bash
pip install PyMuPDF
```

### Görseller görünmüyor
- Görseller `arda.tc/images/slug/` klasöründe olmalı
- Markdown'daki görsel path'lerini kontrol et

## Örnek Workflow

```bash
# 1. PDF'i blog yazısına dönüştür
python pdf_to_blog.py arda.tc/pdfs/yeni-yazi.pdf --title "Yeni Yazı" --lang tr

# 2. Oluşan dosyayı kontrol et
cat _posts/2025-01-15-yeni-yazi.md

# 3. Git'e ekle ve push et
git add .
git commit -m "Yeni blog yazısı: Yeni Yazı"
git push
```

