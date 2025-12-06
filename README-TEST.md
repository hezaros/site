# Jekyll Site Test Etme Rehberi

## Hızlı Test (GitHub Pages)

1. Değişiklikleri GitHub'a push edin:
   ```bash
   git add .
   git commit -m "Blog layout eklendi"
   git push
   ```

2. GitHub Pages otomatik olarak siteyi build edecek (1-2 dakika sürebilir)

3. `https://arda.tc/arda.tc/blog/deneme-blog-yazisi/` adresine gidin

## Local Test (Jekyll Kurulumu)

### Adım 1: Ruby Kurulumu
Windows için RubyInstaller indirin: https://rubyinstaller.org/
- Ruby+Devkit versiyonunu indirin
- Kurulum sırasında "Add Ruby executables to your PATH" seçeneğini işaretleyin

### Adım 2: Jekyll Kurulumu
Terminal'de çalıştırın:
```bash
gem install jekyll bundler
```

### Adım 3: Gemfile Oluşturma
Site klasöründe `Gemfile` oluşturun:
```ruby
source "https://rubygems.org"
gem "jekyll"
```

### Adım 4: Jekyll Server Başlatma
```bash
bundle install
bundle exec jekyll serve
```

### Adım 5: Tarayıcıda Açma
`http://localhost:4000` adresine gidin

## Not
- GitHub Pages'de test etmek daha hızlı ve kolaydır
- Local test için Ruby kurulumu gereklidir

