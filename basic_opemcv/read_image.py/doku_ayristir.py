import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# 📂 DOSYA YOLLARI (Senin bilgisayarındaki yollar)
base_path = r"C:\Users\diyar\Documents\MS-Atrophy-Analysis\python_makale"
healthy_dir = os.path.join(base_path, "Sağlıklı Kişiler")
schz_dir = os.path.join(base_path, "Şizofreni Kişiler")

def get_visual_slice(directory, group_name):
    # Klasördeki ilk dosyayı bul (Alfabetik sıraya göre ilkini alır)
    files = [f for f in os.listdir(directory) if f.endswith(('.nii', '.nii.gz'))]
    
    if not files:
        print(f"⚠️ Hata: {group_name} klasöründe dosya bulunamadı!")
        return None, None

    # İlk dosyayı yükle
    # (Eğer özellikle seçmek istediğin bir dosya varsa files[0] yerine dosya adını yazabilirsin)
    file_path = os.path.join(directory, files[0])
    print(f"📸 {group_name} grubundan görüntülenen dosya: {files[0]}")
    
    try:
        img = nib.load(file_path)
        data = img.get_fdata()
        
        # Beynin tam ortasından bir kesit al (Axial view - Kuş bakışı)
        mid_index = data.shape[2] // 2 
        mid_slice = data[:, :, mid_index]
        
        # Görüntüyü düzelt (Genelde yan durur, 90 derece çevirelim)
        mid_slice = np.rot90(mid_slice)
        
        # --- RENKLENDİRME MANTIĞI ---
        # VBR hesabında kullandığımız mantığın aynısı:
        # Piksel çok karanlıksa (suysa) onu seçiyoruz.
        
        # Eşik değeri (Threshold): Sıfır olmayan piksellerin en karanlık %15'i
        threshold = np.percentile(mid_slice[mid_slice > 0], 15)
        
        # Maskeyi oluştur (Ventrikül olan yerler True, diğer yerler False olsun)
        ventricle_mask = (mid_slice < threshold) & (mid_slice > 0)
        
        return mid_slice, ventricle_mask
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None, None

print("🎨 BEYİN GÖRSELLEŞTİRME BAŞLADI...\n")

# Verileri al
h_slice, h_mask = get_visual_slice(healthy_dir, "Sağlıklı")
s_slice, s_mask = get_visual_slice(schz_dir, "Şizofreni")

if h_slice is not None and s_slice is not None:
    # --- ÇİZİM ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # 1. SAĞLIKLI KONTROL
    axes[0].imshow(h_slice, cmap='gray') # Beyni gri tonlamalı çiz
    # Maskeyi üzerine kırmızı olarak ekle (Maske olmayan yerleri şeffaf yap)
    axes[0].imshow(np.ma.masked_where(~h_mask, h_mask), cmap='spring', alpha=0.6) # 'spring' rengi parlak pembe/kırmızıdır
    axes[0].set_title("Healthy Control\n(Normal Ventricles)", fontsize=14, color='green', fontweight='bold')
    axes[0].axis('off')

    # 2. ŞİZOFRENİ HASTASI
    axes[1].imshow(s_slice, cmap='gray') # Beyni gri tonlamalı çiz
    axes[1].imshow(np.ma.masked_where(~s_mask, s_mask), cmap='spring', alpha=0.6)
    axes[1].set_title("Schizophrenia Patient\n(Enlarged Ventricles)", fontsize=14, color='darkred', fontweight='bold')
    axes[1].axis('off')

    # Başlık ve Kayıt
    plt.suptitle("Visual Comparison of Ventricular Enlargement", fontsize=16)
    plt.tight_layout()
    
    save_name = 'Figure2_Brain_Visualization.png'
    plt.savefig(save_name, dpi=300)
    print(f"\n✅ Çizim tamamlandı! '{save_name}' adıyla kaydedildi.")
    plt.show()
else:
    print("\n❌ Dosyalar eksik olduğu için çizim yapılamadı. Klasörlerini kontrol et.")