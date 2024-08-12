import tkinter as tk
from tkinter import scrolledtext, messagebox
from urllib.request import urlopen
from PIL import Image
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import pyperclip

def get_image_size(url):
    with urlopen(url) as img:
        image = Image.open(BytesIO(img.read()))
        return image.size

def get_fb_video_size(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    width_tag = soup.find('meta', property="og:video:width")
    height_tag = soup.find('meta', property="og:video:height")
    if width_tag and height_tag:
        return int(width_tag['content']), int(height_tag['content'])
    return 476, 316  # Varsayılan boyut

def extract_image_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    images = []
    for img in soup.find_all('img'):
        src = img.get('src')
        alt = img.get('alt', '')  # Alt text, kullanıcının belirlediği genel alt text ile değiştirilecek
        width = img.get('data-original-width') or img.get('width')
        height = img.get('data-original-height') or img.get('height')
        if not width or not height:  # Eğer width ve height mevcut değilse, resmin boyutlarını internetten alalım
            width, height = get_image_size(src)
        images.append((src, width, height))
    return images

def convert_to_amp():
    # Giriş alanlarından verileri al
    html_content = images_text.get("1.0", tk.END).strip()
    fb_video_links = fb_video_text.get("1.0", tk.END).strip().split('\n')
    fb_share_link = fb_share_text.get().strip()
    alt_text = alt_text_entry.get().strip()
    
    amp_content = ""
    
    # HTML içinden resim URL'lerini çıkarma
    images = extract_image_urls(html_content)
    
    # Resimleri işleme
    for idx, (img_url, width, height) in enumerate(images):
        if idx == 0:  # İlk resim <noscript> ile
            img_tag = f"""
            <div class="separator" style="clear: both;">
            <noscript><img alt="{alt_text}" src="{img_url}" width="{width}" height="{height}"/></noscript>
            <amp-img alt="{alt_text}" src="{img_url}" width="{width}" height="{height}" layout="responsive"></amp-img>
            </div>
            <div style="height: 20px;"></div>
            """
        else:
            img_tag = f"""
            <div class="separator" style="clear: both;">
            <amp-img alt="{alt_text}" src="{img_url}" width="{width}" height="{height}" layout="responsive"></amp-img>
            </div>
            <div style="height: 20px;"></div>
            """
        amp_content += img_tag
    
    # Facebook videolarını işleme
    for fb_video_link in fb_video_links:
        if fb_video_link:
            width, height = get_fb_video_size(fb_video_link)
            fb_video_tag = f"""
            <amp-facebook width="{width}" height="{height}" 
                          data-allowfullscreen
                          layout="responsive"
                          data-embed-as="video"
                          data-href="{fb_video_link}">
            </amp-facebook>
            """
            amp_content += fb_video_tag
    
    # Facebook paylaşım linki için <a> etiketi oluşturma
    if fb_share_link:
        fb_share_tag = f"""
        <a href="{fb_share_link}">Facebook paylaşımına gitmek için TIKLAYIN</a>
        """
        amp_content += fb_share_tag

    # Sonuçları çıktı alanına yazdırma
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, amp_content)

def clear_all():
    """Tüm giriş ve sonuç alanlarını temizle."""
    images_text.delete("1.0", tk.END)
    fb_video_text.delete("1.0", tk.END)
    fb_share_text.delete(0, tk.END)
    alt_text_entry.delete(0, tk.END)
    result_text.delete("1.0", tk.END)

def copy_to_clipboard():
    """Sonuç alanındaki içeriği panoya kopyala."""
    result_content = result_text.get("1.0", tk.END).strip()
    if result_content:
        pyperclip.copy(result_content)
        messagebox.showinfo("Başarılı", "AMP HTML çıktısı panoya kopyalandı!")
    else:
        messagebox.showwarning("Uyarı", "Panoya kopyalanacak içerik yok.")

# Kullanıcı arayüzü
root = tk.Tk()
root.title("AMP Uyumlu HTML Dönüştürücü")

# Resim HTML kodu giriş alanı
tk.Label(root, text="Resim HTML Kodu (Blogger'dan)").grid(row=0, column=0)
images_text = scrolledtext.ScrolledText(root, width=60, height=10)
images_text.grid(row=1, column=0, padx=10, pady=5)

# Alt metin girişi
tk.Label(root, text="Tüm Resimler için Alt Metin").grid(row=2, column=0)
alt_text_entry = tk.Entry(root, width=60)
alt_text_entry.grid(row=3, column=0, padx=10, pady=5)

# Facebook video linki giriş alanı
tk.Label(root, text="Facebook Video Linkleri (her satıra bir URL)").grid(row=4, column=0)
fb_video_text = scrolledtext.ScrolledText(root, width=60, height=5)
fb_video_text.grid(row=5, column=0, padx=10, pady=5)

# Facebook paylaşım linki giriş alanı
tk.Label(root, text="Facebook Paylaşım Linki").grid(row=6, column=0)
fb_share_text = tk.Entry(root, width=60)
fb_share_text.grid(row=7, column=0, padx=10, pady=5)

# Dönüştürme butonu
convert_button = tk.Button(root, text="Dönüştür", command=convert_to_amp)
convert_button.grid(row=8, column=0, pady=10)

# Sonuç gösterim alanı
tk.Label(root, text="AMP Uyumlu HTML Çıktısı").grid(row=9, column=0)
result_text = scrolledtext.ScrolledText(root, width=60, height=20)
result_text.grid(row=10, column=0, padx=10, pady=5)

# Temizle ve Kopyala butonları
clear_button = tk.Button(root, text="Temizle", command=clear_all)
clear_button.grid(row=11, column=0, sticky="w", padx=10, pady=5)

copy_button = tk.Button(root, text="Kod Kopyala", command=copy_to_clipboard)
copy_button.grid(row=11, column=0, sticky="e", padx=10, pady=5)

# Arayüzü çalıştır
root.mainloop()
