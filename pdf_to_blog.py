#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF'den Blog Yazısı Oluşturucu
Kullanım: python pdf_to_blog.py <pdf_dosyasi.pdf> [--title "Başlık"] [--lang tr] [--slug slug-adi]
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime
import argparse

try:
    import fitz  # PyMuPDF
    has_pymupdf = True
except ImportError:
    has_pymupdf = False
    print("Uyarı: PyMuPDF kurulu değil. Görseller çıkarılamayacak.")
    print("Kurulum: pip install PyMuPDF")

try:
    import pdfplumber
    has_pdfplumber = True
except ImportError:
    has_pdfplumber = False
    print("Uyarı: pdfplumber kurulu değil. Metin çıkarılamayacak.")
    print("Kurulum: pip install pdfplumber")

def extract_text_pdfplumber(pdf_path):
    """pdfplumber ile metin çıkar"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
    except Exception as e:
        print(f"Hata: Metin çıkarılırken sorun oluştu: {e}")
    return text

def extract_images_pymupdf(pdf_path, output_dir):
    """PyMuPDF ile görselleri çıkar"""
    images = []
    if not has_pymupdf:
        return images
    
    try:
        pdf_document = fitz.open(pdf_path)
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_filename = f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
                image_path = os.path.join(output_dir, image_filename)
                
                os.makedirs(output_dir, exist_ok=True)
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)
                
                images.append({
                    'page': page_num + 1,
                    'filename': image_filename,
                    'path': image_path,
                    'relative_path': f"/arda.tc/images/{os.path.basename(output_dir)}/{image_filename}"
                })
        
        pdf_document.close()
    except Exception as e:
        print(f"Uyarı: Görseller çıkarılırken sorun oluştu: {e}")
    
    return images

def clean_text(text):
    """Metni temizle ve düzenle"""
    # PDF'den gelen karakter hatalarını düzelt
    text = text.replace('(cid:284)', 'ı')
    text = text.replace('(cid:286)', 'ğ')
    text = text.replace('(cid:287)', 'ğ')
    text = text.replace('(cid:305)', 'ı')
    text = text.replace('(cid:351)', 'ş')
    text = text.replace('(cid:350)', 'Ş')
    text = text.replace('(cid:231)', 'ç')
    text = text.replace('(cid:199)', 'Ç')
    text = text.replace('(cid:252)', 'ü')
    text = text.replace('(cid:220)', 'Ü')
    text = text.replace('(cid:246)', 'ö')
    text = text.replace('(cid:214)', 'Ö')
    
    # Fazla boşlukları temizle
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)
        elif cleaned_lines and cleaned_lines[-1]:  # Boş satır ekle ama çift boşluk olmasın
            cleaned_lines.append('')
    
    return '\n'.join(cleaned_lines)

def format_markdown(text, images):
    """Metni Markdown formatına çevir"""
    lines = text.split('\n')
    markdown_lines = []
    image_index = 0
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            markdown_lines.append('')
            continue
        
        # Başlık tespiti (büyük harflerle, kısa satırlar)
        if len(line) < 100 and line.isupper() and len(line) > 3:
            markdown_lines.append(f"# {line}")
        # Alt başlık tespiti (sayı ile başlayan veya özel karakterler)
        elif re.match(r'^##?\s+', line) or re.match(r'^SALDIRI|^ÖRNEK|^GÜVENLİ|^ZAFİYET', line, re.IGNORECASE):
            if not line.startswith('#'):
                markdown_lines.append(f"## {line}")
            else:
                markdown_lines.append(line)
        # Kod bloğu tespiti
        elif line.startswith('```') or (line.startswith('```') and 'python' in line.lower()):
            markdown_lines.append(line)
        # Normal metin
        else:
            markdown_lines.append(line)
            
            # Her 3-4 paragraftan sonra görsel ekle (eğer varsa)
            if images and image_index < len(images) and i % 15 == 0:
                img = images[image_index]
                markdown_lines.append(f"\n![Görsel {image_index + 1}]({img['relative_path']})")
                image_index += 1
    
    # Kalan görselleri sona ekle
    while image_index < len(images):
        img = images[image_index]
        markdown_lines.append(f"\n![Görsel {image_index + 1}]({img['relative_path']})")
        image_index += 1
    
    return '\n'.join(markdown_lines)

def generate_slug(title):
    """Başlıktan slug oluştur"""
    # Türkçe karakterleri değiştir
    replacements = {
        'ı': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g',
        'ş': 's', 'Ş': 's', 'ç': 'c', 'Ç': 'c',
        'ü': 'u', 'Ü': 'u', 'ö': 'o', 'Ö': 'o'
    }
    
    slug = title.lower()
    for tr_char, en_char in replacements.items():
        slug = slug.replace(tr_char, en_char)
    
    # Özel karakterleri temizle
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = slug.strip('-')
    
    return slug

def create_blog_post(pdf_path, title=None, lang='tr', slug=None, date=None):
    """PDF'den blog yazısı oluştur"""
    
    if not os.path.exists(pdf_path):
        print(f"Hata: {pdf_path} dosyası bulunamadı!")
        return False
    
    # Başlık belirleme
    if not title:
        title = os.path.splitext(os.path.basename(pdf_path))[0]
        title = title.replace('-', ' ').replace('_', ' ').title()
    
    # Slug belirleme
    if not slug:
        slug = generate_slug(title)
    
    # Tarih belirleme
    if not date:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S +0300")
    
    print(f"📄 PDF okunuyor: {pdf_path}")
    
    # Metin çıkar
    if has_pdfplumber:
        text = extract_text_pdfplumber(pdf_path)
        text = clean_text(text)
    else:
        print("Hata: Metin çıkarılamadı! pdfplumber kurulu değil.")
        return False
    
    if not text.strip():
        print("Uyarı: PDF'den metin çıkarılamadı!")
        return False
    
    print(f"✅ Metin çıkarıldı ({len(text)} karakter)")
    
    # Görselleri çıkar
    image_dir = f"arda.tc/images/{slug}"
    images = extract_images_pymupdf(pdf_path, image_dir)
    
    if images:
        print(f"✅ {len(images)} görsel çıkarıldı: {image_dir}")
    else:
        print("ℹ️  Görsel bulunamadı veya çıkarılamadı")
    
    # Markdown formatına çevir
    markdown_content = format_markdown(text, images)
    
    # Frontmatter oluştur
    frontmatter = f"""---
title: "{title}"
date: {date}
lang: {lang}
slug: {slug}
---

"""
    
    # Blog yazısı dosyası oluştur
    posts_dir = "_posts"
    os.makedirs(posts_dir, exist_ok=True)
    
    # Dosya adı: YYYY-MM-DD-slug.md
    date_part = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_part}-{slug}.md"
    filepath = os.path.join(posts_dir, filename)
    
    # Dosyayı yaz
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter)
        f.write(markdown_content)
        f.write(f"\n\n---\n\n> **Not**: Bu yazı, PDF içeriğinden otomatik olarak dönüştürülmüştür.\n")
    
    print(f"✅ Blog yazısı oluşturuldu: {filepath}")
    print(f"\n📝 Özet:")
    print(f"   - Başlık: {title}")
    print(f"   - Dil: {lang}")
    print(f"   - Slug: {slug}")
    print(f"   - Görsel sayısı: {len(images)}")
    print(f"   - Dosya: {filepath}")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description='PDF dosyasını blog yazısına dönüştür',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python pdf_to_blog.py document.pdf
  python pdf_to_blog.py document.pdf --title "Yeni Başlık"
  python pdf_to_blog.py document.pdf --title "Test" --lang en --slug test-post
        """
    )
    
    parser.add_argument('pdf_file', help='PDF dosyasının yolu')
    parser.add_argument('--title', help='Blog yazısı başlığı (varsayılan: PDF dosya adı)')
    parser.add_argument('--lang', default='tr', choices=['tr', 'en', 'de'], 
                       help='Dil kodu (varsayılan: tr)')
    parser.add_argument('--slug', help='URL slug (varsayılan: başlıktan otomatik)')
    parser.add_argument('--date', help='Tarih (varsayılan: şimdi)')
    
    args = parser.parse_args()
    
    # Gerekli kütüphaneleri kontrol et
    if not has_pdfplumber:
        print("Hata: pdfplumber kurulu değil!")
        print("Kurulum: pip install pdfplumber")
        sys.exit(1)
    
    success = create_blog_post(
        args.pdf_file,
        title=args.title,
        lang=args.lang,
        slug=args.slug,
        date=args.date
    )
    
    if success:
        print("\n🎉 Başarılı! Blog yazısı hazır.")
        print("💡 Şimdi 'git add .' ve 'git push' yapabilirsin.")
    else:
        print("\n❌ Hata oluştu!")
        sys.exit(1)
    
    # Windows'ta pencere kapanmasın diye bekle
    input("\nDevam etmek için Enter'a bas...")

if __name__ == "__main__":
    main()

