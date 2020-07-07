import sys
import os
import threading
import time
import mysql.connector
import infos
from urllib.request import urlopen
import urllib.request
from requests import get

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import SessionNotCreatedException

from selenium.webdriver.chrome.options import Options
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui, QtCore

class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)

        self.splash = QSplashScreen(QPixmap('media/WELCOME.png'))

        # By default, SplashScreen will be in the center of the screen.
        # You can move it to a specific location if you want:
        # self.splash.move(10,10)

        self.splash.show()

        # Close SplashScreen after 2 seconds (2000 ms)
        QTimer.singleShot(1500, self.splash.close)
        time.sleep(1.5)
        self.loginProgram = TwitterBot()
        self.loginProgram.show()

class SeleniumManager(QtCore.QObject):
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    def start(self):
        threading.Thread(target=self._execute, daemon=True).start()

    def _execute(self):

        for hesaplar in range(len(infos.kullanici_adlari)):
            try:
                self.started.emit()
                try:
                    chromedriver = "chromedriver.exe"
                    options = Options()
                    options.headless = True
                    options.add_experimental_option('excludeSwitches', ['enable-logging'])
                    sys.stdout.write(str(infos.kullanici_adlari[hesaplar]) + " adresine gönderme işlemi başlatıldı")

                    browser = webdriver.Chrome(executable_path=chromedriver, options=options)

                    browser.get("https://twitter.com/login")
                    kontrol1 = WebDriverWait(browser, 30).until(
                        EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/form/div/div[1]/label/div/div[2]/div/input"))
                    )
                    username = browser.find_element_by_xpath(
                        "//*[@id='react-root']/div/div/div[2]/main/div/div/form/div/div[1]/label/div/div[2]/div/input")
                    username.send_keys(infos.kullanici_adlari[hesaplar])
                    password = browser.find_element_by_xpath(
                        "//*[@id='react-root']/div/div/div[2]/main/div/div/form/div/div[2]/label/div/div[2]/div/input")
                    password.send_keys(infos.sifreler[hesaplar])

                    kontrol2 = WebDriverWait(browser, 30).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "//*[@id='react-root']/div/div/div[2]/main/div/div/form/div/div[3]/div/div"))
                    )
                    login = browser.find_element_by_xpath(
                        "//*[@id='react-root']/div/div/div[2]/main/div/div/form/div/div[3]/div/div")
                    login.click()

                    kontrol3 = WebDriverWait(browser, 30).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']"))
                    )
                    tweet_at = browser.find_element_by_xpath(
                        "//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']")
                    tweet_at.send_keys(infos.the_tweet)
                    browser.find_element_by_xpath(
                        "//div[@id='react-root']//div//div//div//main//div//div//div//div//div//div//div//div//div//div//div//div//div//div//div//div//div//div//div//span//span[contains(text(),'Tweet')]").click()

                    print(str(infos.kullanici_adlari[
                                  hesaplar]) + " hesabına " + "*** " + infos.the_tweet + " *** tweetiniz gönderildi")
                    time.sleep(1)
                    browser.close()
                except:
                    print("Bir Hata Oluştu!")
            except SessionNotCreatedException:
                QMessageBox.critical(self, 'Chrome Versiyon Hatası', 'Bu Program Sadece Chrome 83 versiyonunu desteklemektedir. Lütfen Google Chrome 81.x versiyonu yükleyiniz!')
            except:
                QMessageBox.critical(self, 'Tanımlanamayan Hata',
                                     'Lütfen Yapımcı ile İletişime Geçiniz')

        self.finished.emit()

class LoadingScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 300)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.CustomizeWindowHint | Qt.FramelessWindowHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.label_animation = QtWidgets.QLabel(self)
        self.movie = QtGui.QMovie("media/loading-bot-with-text.gif")
        self.label_animation.setMovie(self.movie)

    def startAnimation(self):
        self.movie.start()
        self.show()
        # QtCore.QTimer.singleShot(25 * 1000, self.stopAnimation)

    def stopAnimation(self):
        self.movie.stop()
        self.hide()

class TwitterBot(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Twitter Bot")
        self.setStyleSheet(open("themes/Aqua.qss","r").read())
        self.setWindowIcon(QIcon("media/bot.ico"))
        # self.resize(500, 500)
        self.center()

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Nasıl Kullanılır?")
        self.tabs.addTab(self.tab2, "Kullanılacak Olan Hesaplar")
        self.tabs.addTab(self.tab3, "Tweet Gönder")

        # Create first tab
        self.console_label_baslik = QtWidgets.QLabel("\n>> PROGRAM NASIL KULLANILIR? <<")
        self.console_label_baslik.setAlignment(Qt.AlignHCenter)
        self.console_label_baslik.setStyleSheet('color: red')
        self.console_label_baslik.setFont(QFont("Helvetica", 20, QFont.Bold))

        self.console_label = QtWidgets.QLabel("\n1. Tweet içeriğini boş alana yazınız.\n\n"
                                              "2. Hashtag'le beraber 280 karakter kuralını unutmayınız\naksi takdirde program hata verecektir!\n\n"
                                              "3. Gönderilecek hisse senedini seçiniz\n\n"
                                              "4. Hesaptan hashtag olmadan normal tweet atmak için\naşağıda bulunan ÖZEL butonunu seçiniz\n\n"
                                              "5. İşlemi başlat butonuna tıklayınız\n\n")

        self.console_label.setAlignment(Qt.AlignHCenter)
        self.console_label.setStyleSheet('color: #646464')
        self.console_label.setFont(QFont("Helvetica", 14, QFont.Bold))

        self.diger_label_baslik = QtWidgets.QLabel("\n>> ÖNEMLİ NOTLAR <<")
        self.diger_label_baslik.setAlignment(Qt.AlignHCenter)
        self.diger_label_baslik.setStyleSheet('color: red')
        self.diger_label_baslik.setFont(QFont("Helvetica", 20, QFont.Bold))

        self.diger_label = QtWidgets.QLabel(
            "\n- Seçim yaptıktan sonra eklenen yazılar, tweet'e eklenmez!"
            "\nEklemek için tekrardan aynı butona tıklayınız"
            "\n\n"
            "- Hesap Eklemek için uygulama klasöründe bulunan\n"
            "'bilgiler' dosyasına gidin. Kullanıcı adlarınızı\n"
            "ve şifrelerinizi ilgili text dosyalarına aynı sıralama\n"
            "olacak şekilde girişlerini sağlayın.")

        self.diger_label.setAlignment(Qt.AlignHCenter)
        self.diger_label.setStyleSheet('color: #646464')
        self.diger_label.setFont(QFont("Helvetica", 14, QFont.Bold))

        digerLayout = QtWidgets.QVBoxLayout()
        digerLayout.addStretch()
        digerLayout.addWidget(self.diger_label_baslik)
        digerLayout.addWidget(self.diger_label)
        digerLayout.addStretch()

        consoleLayout = QtWidgets.QVBoxLayout()
        consoleLayout.addStretch()
        consoleLayout.addWidget(self.console_label_baslik)
        consoleLayout.addWidget(self.console_label)
        consoleLayout.addStretch()

        bilgilendirmeLayout = QHBoxLayout()
        bilgilendirmeLayout.addStretch()
        bilgilendirmeLayout.addLayout(consoleLayout)
        bilgilendirmeLayout.addStretch()
        bilgilendirmeLayout.addLayout(digerLayout)
        bilgilendirmeLayout.addStretch()

        self.tab1.setLayout(bilgilendirmeLayout)

        # Create second tab
        self.twitter_icon = QtWidgets.QLabel("")
        self.twitter_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.pixmap = QtGui.QPixmap("media/twitter.png")
        self.pixmap = self.pixmap.scaled(
            64, 64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation
        )
        self.twitter_icon.setPixmap(self.pixmap)
        self.hesaplar_baslik = QtWidgets.QLabel("KULLANILACAK OLAN HESAPLAR")
        self.hesaplar_baslik.setAlignment(Qt.AlignCenter)
        self.hesaplar_baslik.setStyleSheet('color: #1DA1F2')
        self.hesaplar_baslik.setFont(QFont("Arial", 20, QFont.Bold))

        self.hesaplar = QtWidgets.QLabel("\n\n")
        for i in range(len(infos.kullanici_adlari)):
            self.hesaplar.setText(self.hesaplar.text() + "\n" + infos.kullanici_adlari[i])
        self.hesaplar.setAlignment(Qt.AlignHCenter)
        self.hesaplar.setStyleSheet('color: black')
        self.hesaplar.setFont(QFont("Arial", 16, QFont.Bold))

        twitterHesaplariLayout = QtWidgets.QVBoxLayout()
        twitterHesaplariLayout.addStretch()
        twitterHesaplariLayout.addWidget(self.twitter_icon)
        twitterHesaplariLayout.addWidget(self.hesaplar_baslik)
        twitterHesaplariLayout.addWidget(self.hesaplar)
        twitterHesaplariLayout.addStretch()

        self.tab2.setLayout(twitterHesaplariLayout)

        # tab3 layout
        self.loading = LoadingScreen()
        self._manager = SeleniumManager()

        self._manager.started.connect(self.loading.startAnimation)
        self._manager.finished.connect(self.loading.stopAnimation)

        self._manager.started.connect(self.hide)
        self._manager.finished.connect(self.show)

        self.hisse_senetleri_hepsi = ['ACSEL', 'ADANA', 'ADBGR', 'ADEL', 'ADESE', 'ADNAC', 'AEFES', 'AFYON', 'AGHOL',
                                      'AGYO', 'AKBNK', 'AKCNS', 'AKENR', 'AKFGY', 'AKGRT', 'AKGUV', 'AKMGY', 'AKSA',
                                      'AKSEN', 'AKSGY', 'AKSUE', 'ALARK', 'ALBRK', 'ALCAR', 'ALCTL', 'ALGYO', 'ALKA',
                                      'ALKIM', 'ANACM', 'ANELE', 'ANHYT', 'ANSGR', 'ARCLK', 'ARDYZ', 'ARENA', 'ARMDA',
                                      'ARSAN', 'ASELS', 'ASLAN', 'ASUZU', 'ATAGY', 'ATEKS', 'AVGYO', 'AVHOL', 'AVISA',
                                      'AVOD', 'AVTUR', 'AYCES', 'AYEN', 'AYGAZ', 'BAGFS', 'BAKAB', 'BANVT', 'BERA',
                                      'BEYAZ', 'BFREN', 'BIMAS', 'BIZIM', 'BJKAS', 'BLCYT', 'BNTAS', 'BOLUC', 'BOSSA',
                                      'BRISA', 'BRKSN', 'BRMEN', 'BRSAN', 'BRYAT', 'BSOKE', 'BTCIM', 'BUCIM', 'BURCE',
                                      'BURVA', 'CCOLA', 'CELHA', 'CEMAS', 'CEMTS', 'CEOEM', 'CIMSA', 'CLEBI', 'CMBTN',
                                      'CMENT', 'CRDFA', 'CRFSA', 'CUSAN', 'DAGHL', 'DAGI', 'DENCM', 'DENGE', 'DERAS',
                                      'DERIM', 'DESA', 'DESPC', 'DEVA', 'DGATE', 'DGGYO', 'DGKLB', 'DITAS', 'DMSAS',
                                      'DOAS', 'DOBUR', 'DOCO', 'DOGUB', 'DOHOL', 'DOKTA', 'DURDO', 'DYOBY', 'DZGYO',
                                      'ECILC', 'ECZYT', 'EDIP', 'EGEEN', 'EGGUB', 'EGPRO', 'EGSER', 'EKGYO', 'EMKEL',
                                      'ENJSA', 'ENKAI', 'ERBOS', 'EREGL', 'ERSU', 'ESCOM', 'EUHOL', 'FENER', 'FLAP',
                                      'FMIZP', 'FONET', 'FORMT', 'FROTO', 'GARAN', 'GARFA', 'GEDIK', 'GEDZA', 'GENTS',
                                      'GEREL', 'GLBMD', 'GLRYH', 'GLYHO', 'GOLTS', 'GOODY', 'GOZDE', 'GSDDE', 'GSDHO',
                                      'GSRAY', 'GUBRF', 'GUSGR', 'GYHOL', 'HALKB', 'HATEK', 'HDFGS', 'HEKTS', 'HLGYO',
                                      'HUBVC', 'HURGZ', 'ICBCT', 'IDEAS', 'IDGYO', 'IEYHO', 'IHEVA', 'IHGZT', 'IHLAS',
                                      'IHLGM', 'IHYAY', 'INDES', 'INFO', 'INTEM', 'IPEKE', 'ISATR', 'ISBTR', 'ISCTR',
                                      'ISDMR', 'ISFIN', 'ISGSY', 'ISGYO', 'ISMEN', 'ITTFH', 'IZFAS', 'IZMDC', 'IZTAR',
                                      'JANTS', 'KAPLM', 'KAREL', 'KARSN', 'KARTN', 'KATMR', 'KCHOL', 'KENT', 'KERVT',
                                      'KFEIN', 'KLGYO', 'KLMSN', 'KLNMA', 'KNFRT', 'KONYA', 'KORDS', 'KOZAA', 'KOZAL',
                                      'KRDMA', 'KRDMB', 'KRDMD', 'KRGYO', 'KRONT', 'KRSTL', 'KRTEK', 'KUTPO', 'KUYAS',
                                      'LIDFA', 'LINK', 'LKMNH', 'LOGO', 'LUKSK', 'MAALT', 'MAKTK', 'MARKA', 'MARTI',
                                      'MAVI', 'MEGAP', 'MEPET', 'MERKO', 'METRO', 'METUR', 'MGROS', 'MIPAZ', 'MNDRS',
                                      'MPARK', 'MRDIN', 'MRGYO', 'MRSHL', 'MSGYO', 'NATEN', 'NETAS', 'NIBAS', 'NTHOL',
                                      'NUGYO', 'NUHCM', 'ODAS', 'OLMIP', 'ORGE', 'OSMEN', 'OSTIM', 'OTKAR', 'OYLUM',
                                      'OZBAL', 'OZGYO', 'OZKGY', 'OZRDN', 'PAGYO', 'PAPIL', 'PARSN', 'PEGYO', 'PEKGY',
                                      'PENGD', 'PETKM', 'PETUN', 'PGSUS', 'PINSU', 'PKART', 'PKENT', 'PNSUT', 'POLHO',
                                      'POLTK', 'PRKAB', 'PRKME', 'PRZMA', 'PSDTC', 'QNBFB', 'QNBFL', 'RALYH', 'RAYSG',
                                      'RHEAG', 'RODRG', 'RTALB', 'RYGYO', 'RYSAS', 'SAFKR', 'SAHOL', 'SAMAT', 'SANEL',
                                      'SANFM', 'SANKO', 'SARKY', 'SASA', 'SAYAS', 'SEKFK', 'SEKUR', 'SELEC', 'SEYKM',
                                      'SILVR', 'SISE', 'SKBNK', 'SKTAS', 'SMART', 'SNGYO', 'SNKRN', 'SNPAM', 'SODA',
                                      'SOKM', 'SONME', 'SRVGY', 'TATGD', 'TAVHL', 'TBORG', 'TCELL', 'TDGYO', 'TEKTU',
                                      'TGSAS', 'THYAO', 'TIRE', 'TKFEN', 'TKNSA', 'TKURU', 'TLMAN', 'TMPOL', 'TMSN',
                                      'TOASO', 'TRCAS', 'TRGYO', 'TRKCM', 'TSGYO', 'TSKB', 'TSPOR', 'TTKOM', 'TTRAK',
                                      'TUCLK', 'TUKAS', 'TUPRS', 'TURGG', 'ULAS', 'ULKER', 'ULUSE', 'ULUUN', 'UNYEC',
                                      'USAK', 'UTPYA', 'VAKBN', 'VAKFN', 'VAKKO', 'VANGD', 'VERTU', 'VERUS', 'VESBE',
                                      'VESTL', 'VKGYO', 'VKING', 'YAPRK', 'YATAS', 'YAYLA', 'YESIL', 'YGGYO', 'YGYO',
                                      'YKBNK', 'YKGYO', 'YKSLN', 'YUNSA', 'YYAPI', 'ZOREN']

        self.tweetContent_baslik = QtWidgets.QLabel("Atacağınız tweeti aşağıya giriniz ")
        self.tweetContent = QtWidgets.QTextEdit()
        self.tweetContent.setPlaceholderText("Tweetinizi Buraya Giriniz...")
        self.tweetContent.setStyleSheet("color: white")
        self.tweetContent.setFont(QFont("Helvetica", 16))
        # self.tweetYukle = QtWidgets.QPushButton("Yukle")
        self.tweetAt = QtWidgets.QPushButton("İşlemi başlat")
        self.tweetAt.setStyleSheet("background-color: green; color: white")
        self.tweetAt.setFont(QFont("Calibri", 20, QFont.Bold))
        self.tweetTemizle = QtWidgets.QPushButton("Tweet içeriğini temizle")
        self.tweetTemizle.setStyleSheet("background-color: red; color: white")
        self.tweetTemizle.setFont(QFont("Calibri", 20, QFont.Bold))

        ##Borsa hisse senetleri için layout tanımlaması
        hisseLayout0 = QtWidgets.QHBoxLayout()
        hisseLayout1 = QtWidgets.QHBoxLayout()
        hisseLayout2 = QtWidgets.QHBoxLayout()
        hisseLayout3 = QtWidgets.QHBoxLayout()
        hisseLayout4 = QtWidgets.QHBoxLayout()
        hisseLayout5 = QtWidgets.QHBoxLayout()
        hisseLayout6 = QtWidgets.QHBoxLayout()
        hisseLayout7 = QtWidgets.QHBoxLayout()
        hisseLayout8 = QtWidgets.QHBoxLayout()
        hisseLayout9 = QtWidgets.QHBoxLayout()
        hisseLayout10 = QtWidgets.QHBoxLayout()
        hisseLayout11 = QtWidgets.QHBoxLayout()
        hisseLayout12 = QtWidgets.QHBoxLayout()
        hisseLayout13 = QtWidgets.QHBoxLayout()
        hisseLayout14 = QtWidgets.QHBoxLayout()
        hisseLayout15 = QtWidgets.QHBoxLayout()
        hisseLayout16 = QtWidgets.QHBoxLayout()
        hisseLayout17 = QtWidgets.QHBoxLayout()
        hisseLayout18 = QtWidgets.QHBoxLayout()
        hisseLayout19 = QtWidgets.QHBoxLayout()
        hisseLayout20 = QtWidgets.QHBoxLayout()
        hisseLayout21 = QtWidgets.QHBoxLayout()
        hisseLayout22 = QtWidgets.QHBoxLayout()
        hisseLayout23 = QtWidgets.QHBoxLayout()

        h_box0 = QtWidgets.QHBoxLayout()
        h_box0.addWidget(self.tweetTemizle)
        h_box0.addWidget(self.tweetAt)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.tweetContent)
        v_box.addStretch()
        v_box.addLayout(hisseLayout0)
        v_box.addLayout(hisseLayout1)
        v_box.addLayout(hisseLayout2)
        v_box.addLayout(hisseLayout3)
        v_box.addLayout(hisseLayout4)
        v_box.addLayout(hisseLayout5)
        v_box.addLayout(hisseLayout6)
        v_box.addLayout(hisseLayout7)
        v_box.addLayout(hisseLayout8)
        v_box.addLayout(hisseLayout9)
        v_box.addLayout(hisseLayout10)
        v_box.addLayout(hisseLayout11)
        v_box.addLayout(hisseLayout12)
        v_box.addLayout(hisseLayout13)
        v_box.addLayout(hisseLayout14)
        v_box.addLayout(hisseLayout15)
        v_box.addLayout(hisseLayout16)
        v_box.addLayout(hisseLayout17)
        v_box.addLayout(hisseLayout18)
        v_box.addLayout(hisseLayout19)
        v_box.addLayout(hisseLayout20)
        v_box.addLayout(hisseLayout21)
        v_box.addLayout(hisseLayout22)
        v_box.addLayout(hisseLayout23)
        v_box.addStretch()
        v_box.addLayout(h_box0)

        # Borsa hisse senetlerinin arayüz için tanımlanması ve fonksyion ataması
        for i in range(358):  # <---
            if i + 1 <= 15:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout0.addWidget(self.myPushButton)
            elif i + 1 <= 30:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout1.addWidget(self.myPushButton)
            elif i + 1 <= 45:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout2.addWidget(self.myPushButton)
            elif i + 1 <= 60:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout3.addWidget(self.myPushButton)
            elif i + 1 <= 75:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout4.addWidget(self.myPushButton)
            elif i + 1 <= 90:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout5.addWidget(self.myPushButton)
            elif i + 1 <= 105:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout6.addWidget(self.myPushButton)
            elif i + 1 <= 120:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout7.addWidget(self.myPushButton)
            elif i + 1 <= 135:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout8.addWidget(self.myPushButton)
            elif i + 1 <= 150:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout9.addWidget(self.myPushButton)
            elif i + 1 <= 165:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout10.addWidget(self.myPushButton)
            elif i + 1 <= 180:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout11.addWidget(self.myPushButton)
            elif i + 1 <= 195:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout12.addWidget(self.myPushButton)
            elif i + 1 <= 210:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout13.addWidget(self.myPushButton)
            elif i + 1 <= 225:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout14.addWidget(self.myPushButton)
            elif i + 1 <= 240:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout15.addWidget(self.myPushButton)
            elif i + 1 <= 255:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout16.addWidget(self.myPushButton)
            elif i + 1 <= 270:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout17.addWidget(self.myPushButton)
            elif i + 1 <= 285:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout18.addWidget(self.myPushButton)
            elif i + 1 <= 300:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout19.addWidget(self.myPushButton)
            elif i + 1 <= 315:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout20.addWidget(self.myPushButton)
            elif i + 1 <= 330:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout21.addWidget(self.myPushButton)
            elif i + 1 <= 345:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout22.addWidget(self.myPushButton)
            elif i + 1 <= 357:
                self.myPushButton = QtWidgets.QRadioButton("#" + self.hisse_senetleri_hepsi[i])
                self.myPushButton.clicked.connect(lambda ch, mpb=self.myPushButton.text(): self.stocks(mpb))
                hisseLayout23.addWidget(self.myPushButton)

            else:
                self.dldr1 = QtWidgets.QLabel("")
                self.dldr2 = QtWidgets.QLabel("")
                self.dldr3 = QtWidgets.QLabel("")
                self.dldr4 = QtWidgets.QLabel("")
                # self.dldr1.setStyleSheet('color: red')
                # self.dldr1.setFont(QFont("Arial", 10,QFont.Bold))
                # self.dldr2.setStyleSheet('color: red')
                # self.dldr2.setFont(QFont("Arial", 10,QFont.Bold))
                self.ozel = QtWidgets.QRadioButton("ÖZEL")
                self.ozel.setFont(QFont("Calibri", 12, QFont.Bold))
                self.ozel.clicked.connect(self.ozelTweet)
                hisseLayout23.addWidget(self.dldr1)
                hisseLayout23.addWidget(self.dldr2)
                # hisseLayout23.addWidget(self.dldr3)
                # hisseLayout23.addWidget(self.dldr4)
                hisseLayout23.addWidget(self.ozel)
        self.tab3.setLayout(v_box)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.tweetTemizle.clicked.connect(self.temizle)
        self.tweetAt.clicked.connect(self._manager.start)

    def temizle(self):
        self.tweetContent.clear()

    def ozelTweet(self):
        infos.the_tweet = str(self.tweetContent.toPlainText())

    def stocks(self, hisse):
        infos.the_tweet = str(hisse + " " + self.tweetContent.toPlainText())


    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dialog()
    # ex.showMaximized()
    # ex.show()
    sys.exit(app.exec_())
