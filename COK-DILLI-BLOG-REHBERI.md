# Çok Dilli Blog Sistemi Kullanım Rehberi

## Nasıl Çalışıyor?

1. **Varsayılan Dil**: Türkçe (TR)
2. **Desteklenen Diller**: Türkçe (TR), İngilizce (EN), Almanca (DE)
3. **Dil Seçici**: Sağ üstte TR/EN/DE butonları
4. **Otomatik Filtreleme**: Seçilen dile göre blog yazıları filtrelenir
5. **Kalıcı Seçim**: Seçilen dil localStorage'da saklanır

## Blog Yazısı Nasıl Yazılır?

### Aynı Yazının Farklı Dillerdeki Versiyonları

Her dil için ayrı bir markdown dosyası oluştur, ama **aynı `slug` değerini kullan**:

#### Türkçe Versiyon:
```markdown
---
title: "Deneme Blog Yazısı"
date: 2025-01-10 12:00:00 +0300
lang: tr
slug: deneme-blog-yazisi
---

Bu Türkçe içerik...
```

#### İngilizce Versiyon:
```markdown
---
title: "Test Blog Post"
date: 2025-01-10 12:00:00 +0300
lang: en
slug: deneme-blog-yazisi
---

This is English content...
```

#### Almanca Versiyon:
```markdown
---
title: "Test Blog Beitrag"
date: 2025-01-10 12:00:00 +0300
lang: de
slug: deneme-blog-yazisi
---

Dies ist deutscher Inhalt...
```

**Önemli**: 
- `slug` değeri **aynı** olmalı (böylece sistem bunların aynı yazının farklı dilleri olduğunu anlar)
- `lang` değeri farklı olmalı (tr/en/de)
- `title` her dilde farklı olabilir

## Özellikler

### Ana Sayfa
- Sağ üstte dil seçici (TR/EN/DE)
- Seçilen dile göre blog listesi filtrelenir
- Seçim localStorage'da saklanır

### Blog Yazısı Sayfası
- Sağ üstte dil seçici
- Aktif dil vurgulanır
- Diğer dillerdeki versiyonlarına link gösterilir
- Eğer diğer dilde versiyon yoksa buton disabled olur

## Örnek Kullanım

1. **Türkçe blog yazısı oluştur:**
   ```
   _posts/2025-01-10-deneme-yazisi-tr.md
   ```
   ```yaml
   lang: tr
   slug: deneme-yazisi
   ```

2. **İngilizce versiyonunu oluştur:**
   ```
   _posts/2025-01-10-deneme-yazisi-en.md
   ```
   ```yaml
   lang: en
   slug: deneme-yazisi
   ```

3. **Almanca versiyonunu oluştur:**
   ```
   _posts/2025-01-10-deneme-yazisi-de.md
   ```
   ```yaml
   lang: de
   slug: deneme-yazisi
   ```

## Notlar

- Eğer bir yazının sadece bir dilde versiyonu varsa, sadece o dilde görünür
- `slug` değeri olmayan eski yazılar varsayılan olarak Türkçe kabul edilir
- Dil seçimi tarayıcıda saklanır, tekrar geldiğinde aynı dil seçili olur

