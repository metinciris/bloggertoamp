# bloggertoamp

Bu Python aracı, Blogger'da oluşturulan resimli ve videolu içerikleri AMP uyumlu HTML formatına dönüştürmek için kullanılır. Arayüz, kullanıcıdan aldığı verilerle AMP uyumlu HTML kodu oluşturur.

## Özellikler
- Resim linklerinden otomatik boyut belirleme.
- Facebook video linklerinden boyut belirleme.
- Tek bir alt metni tüm resimlere uygulama.
- Dönüştürülmüş AMP HTML kodunu panoya kopyalama.
- Giriş ve sonuç alanlarını temizleme.

## Kullanım

Python betiğini çalıştırdıktan sonra:
1. Resim HTML kodlarını Blogger'dan alın ve ilgili alana yapıştırın.
2. Tüm resimler için geçerli olacak alt metni girin.
3. Facebook video ve paylaşım linklerini girin.
4. "Dönüştür" butonuna tıklayın.
5. Dönüştürülen HTML kodunu kopyalayabilir veya giriş alanlarını temizleyebilirsiniz.

## Gereksinimler

- Python 3.x
- Gerekli Python paketleri: `beautifulsoup4`, `requests`, `Pillow`, `pyperclip`

## Kurulum

Gerekli Python paketlerini yüklemek için:

```bash
pip install beautifulsoup4 requests Pillow pyperclip
