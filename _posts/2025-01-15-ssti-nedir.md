---
title: "SSTI Zafiyeti Nedir?"
date: 2025-01-15 12:00:00 +0300
lang: tr
slug: ssti-nedir
---

# SSTI Zafiyeti Nedir?

Günümüzde çoğu web sitesi dinamik web sayfaları kullanmaktadır. Dinamik sayfalar, içeriği kullanıcıya göre server tarafında (server-side) veya istemcide (client-side) oluşturur. Bu oluşturma işlemi sırasında devreye template engine girer. Server-side saldırılar bir sunucu tarafından sağlanan uygulama veya hizmeti hedef alırken, Client-side saldırıları sunucunun kendisinde değil, istemcinin makinesinde gerçekleşir. İçeriğin nerede ve hangi tarafta oluşturulduğu, SSTI ile CSTI zafiyetleri arasındaki temel farkı ortaya koyar.

SSTI zafiyetlerinde içerik yukarıda da bahsedildiği gibi sunucu tarafında çalışan bir template engine ile rendering edilir ve çıktı HTML şeklinde client'a gönderilir. Eğer inputlar yeterince filtrelenmeden doğrudan template engine'e aktarılırsa, bu ifadeler template engine tarafından değişken değil template ifadeleri (template expressions) veya fonksiyon çağrıları olarak yorumlanabilir. Genelde karşımıza çıkan `{{7*7}}` ifadesi de:

Template engine input'u olması gerektiği gibi değişken olarak mı algılıyor? Yoksa injection gerçekleştirilebildi mi konusundaki kültleşmiş bir payload haline gelmiştir.

CSTI'da ise template işleme işlemi, kullanıcının tarayıcısı üzerinde gerçekleştirilir. Günümüzde kullanılan birçok frontend framework'ü, istemci tarafında da template rendering işlemi yapabilmektedir. Bu nedenle, template ifadelerinin içeren kullanıcı girdileri aracılığıyla CSTI zafiyetleri ortaya çıkabilir.

## Güvenli Kod Örneği

Örnek olarak jinja2 de güvenli bir template kısmı örneği:

```python
render() fonksiyonuna gönderilen template "Hello {{name}}" statik bir değerdir, input
"Arda" sadece "name" adlı değişkenin değeri olarak atanıyor.
```

Bu kodun çıktısı `Hello Arda` şeklinde olacaktır ve `{{7*7}}` ifadesi burada çalışmayacaktır.

## Zafiyetli Kod Örneği

Zafiyetli kod örneği ise aşağıdaki gibidir:

```python
template = "Hello " + user_input
render_template_string(template)
```

Bu kodda tehlikeli kısım render()'ın alacağı template sadece `{{7*7}}` değil `"Hello {{7*7}}"` şeklinde olacağıdır. Bu da çıktı olarak `Hello 49` ifadesini verir. İşte bu ve bu tür durumlar SSTI açığına neden olur.

# SSTI Saldırı Metodolojisi

Hedef sistemde bu açığın varlığı hata kodlarından veya gönderdiğimiz input'un render edip etmediğini yorumladığımızda ortaya çıkar. Farklı template engine'ler biraz faklı syntax'lar kullanabilir.

## SSTI Tespiti

SSTI'yı tespit etme süreci diğer injection'ları tespit etme süreçlerine benzer. Karşı tarafta bir hata mesajı oluşturtmak veya hangi özel karakterleri render ettiğini görmek için:

```
${{<%[%'"}}\.
```

Payloadını input olarak veririz. Bu SQL injection tespitlerinde tek tırnak (') inputu vererek SQL sorgusunun sözdizimini bozmasına ve hatayla karşılaşılmasına benzer. Ben bu payloadı verdikten sonra ya hata beklerim oradan Template injection var mı eğer varsa hangi template türünü kullanmış bununla ilgili bilgi almaya çalışırım ya da belirli bir kısmına bir belirteç koyarak örnek arda olsun:

```
${{<%[arda%'"}}\.
```

Şeklinde bu sefer de bu template çıktıyı sayfanın neresine yazıyorsa oraya bakarak hangi özel karakterleri rendering ettiğine bakarız ve bu doğrultu da hangi template engine kullanılmış anlamaya çalışırız.

Örnek olarak verdiğimiz input ve çıktı karşılaştırıldığında `<%` özel karakterlerin eksik olduğunu görüyoruz.

## SALDIRI SENARYOSU 1

Bu davranışı internette araştırdığımızda (book.hacktricks.wiki de önerilir, kullanılabilir.) ERB (Ruby), Mako (Python) gibi sık kullanılan template engine ile alakalı olduğunu görüyoruz.

ERB ile örnek olarak passwd dosyasını okumaya çalıştığımızda:

```erb
<%= system('cat /etc/passwd') %>
```

Bu sistemde başarılı oluyoruz. Eğer başarılı olamasaydık diğer ihtimaldeki (`<%` kullanan) template engine'leri denerdik veya bu sistemde ERB template kullanıldığından eminsek ve zafiyet olduğunu düşünüyorsak sistemde komut çalıştırma fonksiyonlarına erişimin engellendiğini düşünürüz. Fakat Ruby ve diğer OOP diller sayesinde, farklı yollar denememiz mümkün çünkü OOP de her şey nesnedir. Yani düşünce biçimimiz her nesne bir class'a sahip, o class üzerinden gelen methodlara erişebiliriz ve bazı methodlar ile başka class ve methodlara ulaşabiliriz.

`Object → Class → Method → Execute` şeklinde zincirleme olarak düşünebiliriz.

## SALDIRI SENARYOSU 2

Sistemde Template injection olduğunu anladıktan sonra:

İlk olarak `<%= "arda".class %>` yazıp çıktısını görürüz bu ilk adım. Bize şuan nerde durduğumuzu ve Ruby'de her sınıf başka bir sınıftan türetildiğini bildiğimizden zincirin ilk aşamasıdır. Bundan sonra bir üst sınıfa çıkacağız.

Diğer aşamada superclass'a çıkacağız `<%= "arda".class.superclass %>` yazdığımızda `Object` çıktısını alıyoruz. Object sınıfı Ruby'deki en temel sınıftır ve içinde bir çok işimize yarayabilecek method vardır.

Method aşamasında `<%= Object.methods %>` inputunu methodları görmek için kullanılırız. Burada uzunca bir method çıktısı alıyoruz.

Özellikle yukarıda altını çizdiğim aşağıdaki methodlar komut çalıştırmak ve RCE yapmak için güçlü methodlar:

- `:send`
- `:__send__`
- `:instance_eval`
- `:instance_exec`

Passwd dosyasını okumayı yukarıdan topladığımız bilgilerle:

```erb
<%= Object.const_get("File").read("/etc/passwd") %>
```

ile deneyebiliriz.

Eğer passwd dosyasını direkt `<%= system('cat /etc/passwd') %>` şeklinde okuyamasaydık senaryosu üzerine gittik ve en son kullandığımız payload ile okuduk.

---

> **Not**: Bu yazı, PDF içeriğinden dönüştürülmüştür. Orijinal PDF dosyası için [buraya tıklayın](/arda.tc/pdfs/ssti-nedir.pdf).
