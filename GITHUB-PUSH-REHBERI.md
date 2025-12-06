# GitHub Push Rehberi

## Personal Access Token ile Push

### Adım 1: GitHub'da Token Oluştur
1. GitHub'a giriş yap: https://github.com
2. Sağ üst köşedeki profil fotoğrafına tıkla → **Settings**
3. Sol menüden **Developer settings** → **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)** tıkla
5. **Note**: "Jekyll Site Push" yaz
6. **Expiration**: İstediğin süreyi seç (90 days önerilir)
7. **Select scopes**: En azından **repo** seçeneğini işaretle
8. **Generate token** butonuna tıkla
9. **ÖNEMLİ**: Token'ı kopyala (bir daha gösterilmeyecek!)

### Adım 2: Terminal'de Push Yap
Terminal'de şu komutu çalıştır:
```bash
git push
```

Username sorduğunda: `hezaros` yaz
Password sorduğunda: **Token'ı yapıştır** (şifre değil, token!)

---

## Alternatif: SSH Kullan (Daha Güvenli)

### SSH Key Oluştur
```bash
ssh-keygen -t ed25519 -C "semihturan46@gmail.com"
```

### SSH Key'i GitHub'a Ekle
1. `cat ~/.ssh/id_ed25519.pub` komutuyla public key'i kopyala
2. GitHub → Settings → SSH and GPG keys → New SSH key
3. Key'i yapıştır ve kaydet

### Remote URL'i SSH'a Çevir
```bash
git remote set-url origin git@github.com:hezaros/site.git
git push
```

