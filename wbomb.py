from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyperclip 

# --- Ayarlar ---
MESSAGE_DELAY_SECONDS = 0.01  # Her mesaj arası minimum gecikme (saniye)
SEARCH_DELAY_SECONDS = 2     # Sohbet araması sonrası bekleme süresi

# --- Başlangıç ---
def setup_driver():
    """Firefox WebDriver'ı başlatır ve döndürür."""
    try:
        driver = webdriver.Firefox()
        return driver
    except Exception as e:
        print(f"WebDriver başlatılamadı: {e}")
        print("GeckoDriver'ın doğru PATH'e eklendiğinden ve Firefox'un yüklü olduğundan emin olun.")
        return None

# find_chat_and_send_messages fonksiyonunun dışına taşıdım ki driver'ı dışarıdan kullanabilelim
global_driver = None 

def find_chat_and_send_messages(driver_instance, chat_name):
    """Belirtilen sohbeti bulur ve mesajı gönderir."""
    try:
        # ARAMA KUTUSU XPATH'İ
        search_box_xpath = "//div[@data-tab='3']" 
        
        print(f"'{chat_name}' sohbetini aramak için arama kutusunu buluyor...")
        search_box = WebDriverWait(driver_instance, 15).until( # driver_instance kullanıyoruz
            EC.visibility_of_element_located((By.XPATH, search_box_xpath))
        )
        
        actions = ActionChains(driver_instance) # driver_instance kullanıyoruz
        actions.move_to_element(search_box).click().perform() 
        
        search_box.send_keys(chat_name) 
        time.sleep(SEARCH_DELAY_SECONDS) 
        print(f"'{chat_name}' arandı. Sonuçların yüklenmesi bekleniyor...")

        # SOHBETİ BUL VE TIKLA 
        chat_element_xpath = f"//span[@title='{chat_name}']" 
        
        print(f"'{chat_name}' sohbet elementini buluyor ve tıklıyor...")
        
        chat_element = WebDriverWait(driver_instance, 15).until( # driver_instance kullanıyoruz
            EC.element_to_be_clickable((By.XPATH, chat_element_xpath))
        )
        
        try:
            chat_element.click()
        except Exception as click_error:
            print(f"Normal tıklama başarısız oldu, JavaScript ile deniyor: {click_error}")
            driver_instance.execute_script("arguments[0].click();", chat_element) # driver_instance kullanıyoruz
            
        time.sleep(1.5) 
        print(f"'{chat_name}' sohbeti açıldı.")

        # MESAJ KUTUSU XPATH'İ (Senin verdiğin boş halinin XPath'i)
        msg_box_xpath = "/html/body/div[1]/div/div/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[2]/div/div[3]/div[1]"
        
        print("Mesaj kutusunu buluyor...")
        
        msg_box = WebDriverWait(driver_instance, 15).until( # driver_instance kullanıyoruz
            EC.element_to_be_clickable((By.XPATH, msg_box_xpath)) 
        )
        print("Mesaj kutusu bulundu.")

        # Mesajı bir kez al ve sürekli gönder
        girilen_yazi = input("Göndermek istediğiniz mesajı girin (çıkmak için 'q' tuşuna basın): ")
        if girilen_yazi.lower() == 'q':
            print("Mesaj gönderme durduruldu.")
            return # Fonksiyondan çık, ana döngüye geri döner

        print(f"'{girilen_yazi}' mesajı '{chat_name}' sohbetine gönderiliyor. Durdurmak için CTRL+C yapın.")
        
        # Mesaj gönderme döngüsü
        while True: 
            try:
                pyperclip.copy(girilen_yazi)
                actions.move_to_element(msg_box).click().perform()
                msg_box.send_keys(Keys.CONTROL, 'v') 
                msg_box.send_keys(Keys.ENTER)
                time.sleep(MESSAGE_DELAY_SECONDS)
                
            except Exception as loop_error:
                print(f"Mesaj gönderme döngüsünde hata oluştu (tekrar denenecek): {loop_error}")
                # Hata durumunda elementi tekrar bulmayı deneyebiliriz
                msg_box = WebDriverWait(driver_instance, 5).until( # driver_instance kullanıyoruz
                    EC.element_to_be_clickable((By.XPATH, msg_box_xpath))
                )
                time.sleep(MESSAGE_DELAY_SECONDS) 
    
    # Bu catch bloğu, fonksiyon içinde oluşan tüm hataları yakalar ve tarayıcının kapanmasını engeller.
    except Exception as e:
        print(f"Bir sorun oluştu: {e}")
        print("Spam işlemi durduruldu. Yeni bir sohbet denemek için lütfen bekleyin.")
        # Burada driver_instance.quit() YAPMIYORUZ!
        return 

# --- Ana Program Akışı ---
if __name__ == "__main__":
    global_driver = setup_driver() # driver'ı global_driver'a atıyoruz
    if global_driver: 
        global_driver.get("https://web.whatsapp.com/")
        print("Lütfen QR kodunu tarayın ve WhatsApp Web'e giriş yapın...")
        
        pane_side_xpath = '//*[@id="pane-side"]' 
        try:
            WebDriverWait(global_driver, 45).until( 
                EC.presence_of_element_located((By.XPATH, pane_side_xpath)) 
            )
            print("WhatsApp Web'e başarıyla giriş yapıldı.")
        except:
            print("WhatsApp Web'e giriş yapılamadı veya zaman aşımına uğradı. Lütfen tekrar deneyin.")
            if global_driver: global_driver.quit() 
            exit() 

        # Sürekli yeni bir hedef belirleyebilmek için ana döngü
        while True:
            try:
                chat_to_target = input("\nMesaj göndermek istediğiniz grup veya kişi adını girin (çıkmak için 'q' tuşuna basın): ")
                if chat_to_target.lower() == 'q':
                    print("Programdan çıkılıyor...")
                    break # Bu, programı tamamen sonlandırır
                else:
                    # global_driver'ı find_chat_and_send_messages fonksiyonuna iletiyoruz
                    find_chat_and_send_messages(global_driver, chat_to_target)
            
            # Ctrl+C'ye basıldığında bu kısım çalışır
            except KeyboardInterrupt: 
                print("") # Sadece terminalde temiz bir satır bırakmak için
                continue 

        # Program tamamen sonlandığında tarayıcıyı kapat
        if global_driver: 
            global_driver.quit()
            print("Tarayıcı kapatıldı.")
