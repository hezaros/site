# PDF'den Blog Yazısı - Hızlı Kullanım

## Terminal'den Çalıştırma

### Windows PowerShell veya CMD'de:

```bash
python pdf_to_blog.py <pdf_dosyasi.pdf>
```

## Örnekler

### 1. Basit Kullanım (Sadece PDF)
```bash
python pdf_to_blog.py arda.tc/pdfs/yeni-yazi.pdf
```
- Başlık: PDF dosya adından otomatik
- Dil: Türkçe (tr)
- Slug: Başlıktan otomatik

### 2. Başlık Belirterek
```bash
python pdf_to_blog.py yazi.pdf --title "SSTI Nedir?"
```

### 3. Dil Belirterek
```bash
python pdf_to_blog.py yazi.pdf --title "What is SSTI?" --lang en
```

### 4. Tam Özelleştirme
```bash
python pdf_to_blog.py yazi.pdf --title "SSTI Nedir?" --lang tr --slug ssti-nedir
```

## Parametreler

| Parametre | Açıklama | Varsayılan |
|-----------|----------|------------|
| `pdf_file` | PDF dosyasının yolu (zorunlu) | - |
| `--title` | Blog yazısı başlığı | PDF dosya adı |
| `--lang` | Dil: `tr`, `en`, `de` | `tr` |
| `--slug` | URL slug | Başlıktan otomatik |

## Çok Dilli Örnek

Aynı yazının farklı dilleri için **aynı slug** kullan:

```bash
# Türkçe
python pdf_to_blog.py yazi-tr.pdf --title "SSTI Nedir?" --lang tr --slug ssti-nedir

# İngilizce
python pdf_to_blog.py yazi-en.pdf --title "What is SSTI?" --lang en --slug ssti-nedir

# Almanca
python pdf_to_blog.py yazi-de.pdf --title "Was ist SSTI?" --lang de --slug ssti-nedir
```

## Sorun Giderme

### Terminal hemen kapanıyorsa:
- PowerShell veya CMD'den çalıştır (dosyaya çift tıklama)
- Script sonunda "Enter'a bas" mesajı çıkacak

### "python bulunamadı" hatası:
```bash
py pdf_to_blog.py yazi.pdf
```
veya
```bash
python3 pdf_to_blog.py yazi.pdf
```

