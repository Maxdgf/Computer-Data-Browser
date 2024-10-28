import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
from appReloader import reload
from loadingScreen import loadingScreen
import pywifi
from pywifi import *
from datetime import *
import time
import os
import platform
import psutil
import subprocess
import socket
import threading
import requests
import wmi
import pythoncom
import locale

ctk.set_default_color_theme("green")  

class MyApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.running = True

        self.title("Computer Data Browser")
        self.geometry("900x600")
        self.theme = "dark"
        ctk.set_appearance_mode(self.theme)

        

        loadingScreen()
        time.sleep(2)

        self.exitBtn = ctk.CTkButton(self, fg_color="red", text="exit", hover_color="#B22222", command=self.exit_app)
        self.exitBtn.pack(anchor="se")

        self.reportsFrame = ctk.CTkFrame(self)
        self.reportTXTBtn = ctk.CTkButton(self.reportsFrame, fg_color="yellow", text="configure half data report (.txt)", text_color="black", hover_color="gold", command=self.configure_txt_report)
        self.reportTXTBtn.pack()
        self.reportHTMLBtn = ctk.CTkButton(self.reportsFrame, fg_color="yellow", text="configure full data report (.html)", text_color="black", hover_color="gold", command=self.configure_html_report)
        self.reportHTMLBtn.pack(pady=10)
        self.reportsFrame.place(x=0, y=0)

        self.labelName = ctk.CTkLabel(self, text="Сomputer Data Browser", text_color="#7FFF00", font=("Tahoma", 40))
        self.labelName.pack()

        self.mainDataFrame = ctk.CTkFrame(self, border_color="green", border_width=5)
        self.currentComputer = ctk.CTkLabel(self.mainDataFrame, text="Computer: none", text_color="#7FFF00", font=("Arial", 20))
        self.currentComputer.pack(pady=15)
        self.computerName = ctk.CTkLabel(self.mainDataFrame, text="Device name: none", text_color="#7FFF00", font=("Arial", 20))
        self.computerName.pack()
        self.mainDataFrame.pack(pady=10)

        self.commandBtnsFrame = ctk.CTkFrame(self)

        self.configurateReportBtn = ctk.CTkButton(self.commandBtnsFrame, text="turn sleep mode", fg_color="green", hover_color="#32CD32", command=self.turn_sleep_mode_computer)
        self.configurateReportBtn.pack(side="left", padx=10)
        self.turnOffBtn = ctk.CTkButton(self.commandBtnsFrame, text="turn off computer", fg_color="green", hover_color="#32CD32", command=self.turn_off_computer)
        self.turnOffBtn.pack(side="left", padx=10)
        self.rebootBtn = ctk.CTkButton(self.commandBtnsFrame, text="restart computer", fg_color="green", hover_color="#32CD32", command=self.restart_computer)
        self.rebootBtn.pack(side="left", padx=10)

        self.commandBtnsFrame.pack(anchor="center" , pady=20)

        self.openConsoleBtn = ctk.CTkButton(self, text="open console", fg_color="black", text_color="white", hover_color="gray", command=self.open_console)
        self.openConsoleBtn.pack(fill="x")

        self.widgetsFrame = ctk.CTkScrollableFrame(self, border_width=5, border_color="green")


        self.hardwareSpecificationsFrame = ctk.CTkFrame(self.widgetsFrame, fg_color="green")

        self.hsName = ctk.CTkLabel(self.hardwareSpecificationsFrame, text="Hardware Specifications", text_color="#7FFF00", font=("Tahoma", 25))
        self.hsName.pack(pady=10)
        self.proccesorName = ctk.CTkLabel(self.hardwareSpecificationsFrame, text="processor: none")
        self.proccesorName.pack()
        self.processorCoreCountName = ctk.CTkLabel(self.hardwareSpecificationsFrame, text="processor core count: none")
        self.processorCoreCountName.pack()
        self.processorClockSpeedName = ctk.CTkLabel(self.hardwareSpecificationsFrame, text="processor clock speed: none")
        self.processorClockSpeedName.pack()

        self.processorAdditionalInfoFrame = ctk.CTkFrame(self.hardwareSpecificationsFrame, fg_color="green")
        self.paLabel = ctk.CTkLabel(self.processorAdditionalInfoFrame, text="Additional processor information: ")
        self.paLabel.pack(side="left")
        self.paViewData = ctk.CTkButton(self.processorAdditionalInfoFrame, text="view data", bg_color="green", hover_color="#32CD32", command=self.view_additional_processor_window)
        self.paViewData.pack(side="left")
        self.processorAdditionalInfoFrame.pack()

        self.ramMemoryName = ctk.CTkLabel(self.hardwareSpecificationsFrame, text="RAM memory: none")
        self.ramMemoryName.pack()

        self.diskHddDataFrame = ctk.CTkFrame(self.hardwareSpecificationsFrame, fg_color="green")
        self.hardDrivesName = ctk.CTkLabel(self.diskHddDataFrame, text="Hard drives: ")
        self.hardDrivesName.pack(side="left")
        self.viewHddDisksDataBtn = ctk.CTkButton(self.diskHddDataFrame, text="view data", bg_color="green", hover_color="#32CD32", command=self.view_hard_drives_window)
        self.viewHddDisksDataBtn.pack(side="left")
        self.diskHddDataFrame.pack()

        self.videoCardDataFrame = ctk.CTkFrame(self.hardwareSpecificationsFrame, fg_color="green")
        self.videoCardName = ctk.CTkLabel(self.videoCardDataFrame, text="Video cards: ")
        self.videoCardName.pack(side="left")
        self.viewVideoCardDataBtn = ctk.CTkButton(self.videoCardDataFrame, text="view data", bg_color="green", hover_color="#32CD32", command=self.view_video_cards_window)
        self.viewVideoCardDataBtn.pack(side="left")
        self.videoCardDataFrame.pack(pady=10)

        self.hardwareSpecificationsFrame.pack(anchor="center", fill="x", pady=10)


        self.softFrame = ctk.CTkFrame(self.widgetsFrame, fg_color="green")

        self.sName = ctk.CTkLabel(self.softFrame, text="Software", text_color="#7FFF00", font=("Tahoma", 25))
        self.sName.pack(pady=10)
        self.osName = ctk.CTkLabel(self.softFrame, text="OS: none")
        self.osName.pack()
        self.osName2 = ctk.CTkLabel(self.softFrame, text="additional OS: none")
        self.osName2.pack()

        self.driversVersionsFrame = ctk.CTkFrame(self.softFrame, fg_color="green")
        self.driverVersionsName = ctk.CTkLabel(self.driversVersionsFrame, text="Driver versions: ")
        self.driverVersionsName.pack(side="left")
        self.viewDriversVersDataBtn = ctk.CTkButton(self.driversVersionsFrame, text="view data", bg_color="green", hover_color="#32CD32", command=self.view_drivers_data_window)
        self.viewDriversVersDataBtn.pack(side="left")
        self.driversVersionsFrame.pack()

        self.appsViewerFrame = ctk.CTkFrame(self.softFrame, fg_color="green")
        self.hardAppsName = ctk.CTkLabel(self.appsViewerFrame, text="Installed apps: ")
        self.hardAppsName.pack(side="left")
        self.viewAppsBtn = ctk.CTkButton(self.appsViewerFrame, text="view apps", bg_color="green", hover_color="#32CD32", command=self.view_apps_data_window)
        self.viewAppsBtn.pack(side="left")
        self.appsViewerFrame.pack(pady=10)

        self.softFrame.pack(anchor="center", fill="x", pady=10)


        self.networkSettingsFrame = ctk.CTkFrame(self.widgetsFrame, fg_color="green")

        self.nsName = ctk.CTkLabel(self.networkSettingsFrame, text="Network Settings", text_color="#7FFF00", font=("Tahoma", 25))
        self.nsName.pack(pady=10)

        self.netFacesFrame = ctk.CTkFrame(self.networkSettingsFrame, fg_color="green")
        self.networkInterfacesName = ctk.CTkLabel(self.netFacesFrame, text="Network interfaces: ")
        self.networkInterfacesName.pack(side="left")
        self.viewNetFacesBtn = ctk.CTkButton(self.netFacesFrame, text="view data", bg_color="green", hover_color="#32CD32", command=self.view_network_interfaces_window)
        self.viewNetFacesBtn.pack(side="left")
        self.netFacesFrame.pack()

        self.ipDataName = ctk.CTkLabel(self.networkSettingsFrame, text="IP addresses: searching...")
        self.ipDataName.pack()
        self.internetSpeedDataName = ctk.CTkLabel(self.networkSettingsFrame, text="Internet connection speed: calculating connection speed...")
        self.internetSpeedDataName.pack()
        self.connectedInternetName = ctk.CTkLabel(self.networkSettingsFrame, text="Internet connection: loading...")
        self.connectedInternetName.pack()

        self.networkSettingsFrame.pack(anchor="center", fill="x", pady=10)


        self.systemDataFrame = ctk.CTkFrame(self.widgetsFrame, fg_color="green")

        self.sdName = ctk.CTkLabel(self.systemDataFrame, text="System status", text_color="#7FFF00", font=("Tahoma", 25))
        self.sdName.pack(pady=10)
        self.systemUsageName = ctk.CTkLabel(self.systemDataFrame, text="CPU load: none")
        self.systemUsageName.pack()
        self.systemElementsUsageName = ctk.CTkLabel(self.systemDataFrame, text="Memory usage: none")
        self.systemElementsUsageName.pack()
        self.diskDataName = ctk.CTkLabel(self.systemDataFrame, text="Disk usage: none")
        self.diskDataName.pack()

        self.systemDataFrame.pack(anchor="center", fill="x", pady=10)


        self.otherDataFrame = ctk.CTkFrame(self.widgetsFrame, fg_color="green")

        self.odName = ctk.CTkLabel(self.otherDataFrame, text="Other", text_color="#7FFF00", font=("Tahoma", 25))
        self.odName.pack(pady=10)
        self.localeData = ctk.CTkLabel(self.otherDataFrame, text="Computer locale: none")
        self.localeData.pack()
        self.computerEncoding = ctk.CTkLabel(self.otherDataFrame, text="Computer encoding: none")
        self.computerEncoding.pack()
        self.machineName = ctk.CTkLabel(self.otherDataFrame, text="Machine: none")
        self.machineName.pack()
        self.computerTimeName = ctk.CTkLabel(self.otherDataFrame, text="Computer time: none")
        self.computerTimeName.pack()
        self.computerCalendarName = ctk.CTkLabel(self.otherDataFrame, text="Computer calendar data: none")
        self.computerCalendarName.pack()
        self.computerBatteryName = ctk.CTkLabel(self.otherDataFrame, text="Computer battery data: none")
        self.computerBatteryName.pack()
        self.computerWifiLinkName = ctk.CTkLabel(self.otherDataFrame, text="Connected WIFI: none")
        self.computerWifiLinkName.pack()

        self.otherDataFrame.pack(anchor="center", fill="x", pady=10)

        
        self.widgetsFrame.pack(expand=True, fill="both", pady=10)


        self.reloadBtn = ctk.CTkButton(self, text="reload data", fg_color="#00CC00", hover_color="green", command=self.restart_app)
        self.reloadBtn.pack(fill="x")

        #self.main_process()
        #self.execute_hardware_specifications_data()
        #self.execute_software_data()
        #self.execute_network_settings_data()
        #self.wifi_analyser()
        #...

        self.thread1 = threading.Thread(target=self.main_process, daemon=True)
        self.thread2 = threading.Thread(target=self.execute_processor_data, daemon=True)
        self.thread3 = threading.Thread(target=self.execute_os_data, daemon=True)
        self.thread4 = threading.Thread(target=self.execute_ip_data, daemon = True)
        self.thread5 = threading.Thread(target=self.wifi_analyser, daemon=True)
        self.thread6 = threading.Thread(target=self.execute_computer_time_data, daemon=True)
        self.thread7 = threading.Thread(target=self.execute_RAM_data, daemon=True)
        self.thread8 = threading.Thread(target=self.execute_internet_connection_data, daemon=True)
        self.thread9 = threading.Thread(target=self.execute_internet_speed_data, daemon=True)
        self.thread10 = threading.Thread(target=self.execute_computer_calendar_data, daemon=True)
        self.thread11 = threading.Thread(target=self.execute_battery_data, daemon=True)
        self.thread12 = threading.Thread(target=self.execute_additional_os_data, daemon=True)
        self.thread13 = threading.Thread(target=self.execute_computer_locale, daemon=True)
        self.thread14 = threading.Thread(target=self.execute_computer_encoding, daemon=True)
        self.thread15 = threading.Thread(target=self.execute_computer_machine, daemon=True)
        self.thread16 = threading.Thread(target=self.execute_cpu_load_data, daemon=True)
        self.thread17 = threading.Thread(target=self.execute_memory_usage_data, daemon=True)
        self.thread18 = threading.Thread(target=self.execute_disk_usage_data, daemon=True)

        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        self.thread4.start()
        self.thread5.start()
        self.thread6.start()
        self.thread7.start()
        self.thread8.start()
        self.thread9.start()
        self.thread10.start()
        self.thread11.start()
        self.thread12.start()
        self.thread13.start()
        self.thread14.start()
        self.thread15.start()
        self.thread16.start()
        self.thread17.start()
        self.thread18.start()


    def exit_app(self):
        self.destroy()

    def restart_app(self):
        pythoncom.CoUninitialize()
        self.destroy()
        time.sleep(2)
        reload()

    def execute_computer_locale(self):
        try:
            while self.running:
                self.locale = locale.getlocale()
                self.localeInfo = str(self.locale)
                self.localeData.configure(text = f"Computer locale: {self.locale}")
                time.sleep(60)
        except:
            messagebox.showerror("Error", "Failed to get information about computer locale!")
            self.localeData.configure(text = "Computer locale: none")

    def execute_computer_encoding(self):
        try:
            while self.running:
                self.encoding = locale.getencoding()
                self.encodingInfo = str(self.encoding)
                self.computerEncoding.configure(text = f"Computer encoding: {self.encodingInfo}")
                time.sleep(60)
        except:
            messagebox.showerror("Error", "Failed to get information about computer encoding!")
            self.computerEncoding.configure(text = f"Computer encoding: none")

    def execute_computer_machine(self):
        try:
            while self.running:
                self.system = platform.uname()
                self.machine = self.system.machine
                self.machineName.configure(text = f"Machine: {self.machine}")
                time.sleep(60)
        except:
            messagebox.showerror("Error", "Failed to get information about computer machine!")
            self.machineName.configure(text = "Machine:")

    def main_process(self):
        time.sleep(1)
        try:
            while self.running:
                self.output = subprocess.check_output("wmic csproduct get vendor", shell=True).decode().strip().split('\n')
                if len(self.output) > 1:
                    self.finalResult = self.output[1].strip()
                else:
                    self.currentComputer.configure(text="Computer: none")
                    messagebox.showwarning("Warning", "Computer is not defined!")

                self.currentComputer.configure(text=f"Computer: {self.finalResult}")

                self.deviceName = platform.node()
                if len(self.deviceName) > 0:
                    self.computerName.configure(text=f"Device name: {self.deviceName}")
                else:
                    messagebox.showwarning("Warning", "Device name is not defined!")
                    self.computerName.configure(text="Device name: none")
        except:
            self.currentComputer.configure(text="Computer: none")
            messagebox.showwarning("Warning", "Computermodel, Device name and Node name is not defined!")

    def execute_processor_data(self):
        try:
            while self.running:
                time.sleep(1)
                self.processorData = platform.processor()
                self.proccesorName.configure(text=f"processor: {self.processorData}")
                self.coreCount = os.cpu_count()
                self.processorCoreCountName.configure(text=f"processor core count: {self.coreCount}")
                self.clockSpeed = psutil.cpu_freq().current
                self.clockSpeedMin = psutil.cpu_freq().min
                self.clockSpeedMax = psutil.cpu_freq().max
                self.processorClockSpeedName.configure(text=f"processor clock speed: {self.clockSpeed} [min({self.clockSpeedMin})/max({self.clockSpeedMax})]")
        except:
            messagebox.showerror("Error", "Failed to get information about processor!")

    def execute_RAM_data(self):
        try:
            while self.running:
                time.sleep(1)
                self.ramDataAll = psutil.virtual_memory().total
                self.ramDataUsed = psutil.virtual_memory().used
                self.ramData1 = self.ramDataAll / (1024 ** 2)
                self.ramData2 = self.ramDataUsed / (1024 ** 2)
                self.a = int(self.ramData1)
                self.b = int(self.ramData2)
                self.freeRamData = self.a - self.b
                str(self.freeRamData)
                self.ramMemoryName.configure(text=f"RAM memory: total {self.ramData1:.2f} mb | used {self.ramData2:.2f} mb | free {self.freeRamData} mb")
        except:
            messagebox.showerror("Error", "Failed to get information about RAM memory!")


    def execute_os_data(self):
        try:
            while self.running:
                time.sleep(1)
                self.osNameData = platform.platform()
                self.osName.configure(text = f"OS: {self.osNameData}")
        except:
            messagebox.showerror("Error", "The process of retrieving software data was not successful!")

    def execute_additional_os_data(self):
        try:
            while self.running:
                time.sleep(1)
                self.osPlatform = platform.system()
                if self.osPlatform == "Windows":
                    pythoncom.CoInitialize()
                    self.computer = wmi.WMI()
                    self.osVersion = self.computer.Win32_OperatingSystem()[0]
                    self.osVersionSimpleData = self.osVersion.Name.split('|')[0]
                    self.finalOsData = 'additional: {0}'.format(self.osVersionSimpleData)
                    self.osName2.configure(text = f"additional OS:({self.finalOsData})")
                else:
                    self.osName2.configure(text = "additional OS: none")
        except Exception as e:
            #print(e)
            messagebox.showerror("Error", "Failed to get information about additional data of OS!")
            self.finalOsData = "none"

    def wifi_analyser(self):
        try:
            while self.running:   
                time.sleep(1)  
                self.wifiDetector = pywifi.PyWiFi()
                self.wifiFace = self.wifiDetector.interfaces()[0]
                self.wifiFace.scan()
                self.wifiResults = self.wifiFace.scan_results()
                for self.wifi in self.wifiResults:
                    if self.wifiFace.status() == pywifi.const.IFACE_CONNECTED:
                        self.wifiAnswer = self.wifi.ssid
                        self.computerWifiLinkName.configure(text = f"Connected WIFI: wifi name ({self.wifiAnswer})")
                    else:
                        self.wifiAnswer = "Connected WIFI: wifi not connected!"
                        self.computerWifiLinkName.configure(text = self.wifiAnswer)
                return None
        except:
            messagebox.showerror("Error", "The connected wifi could not be detected! Check your WIFI connection.")
            self.wifiAnswer = "Connected WIFI: none"
            self.computerWifiLinkName.configure(text = self.wifiAnswer)

    
    def execute_ip_data(self):
        try:
            while self.running:
                time.sleep(1)
                self.localIp = socket.gethostbyname(socket.gethostname())
                self.externalIp = socket.gethostbyname(socket.getfqdn())
                str(self.localIp)
                str(self.externalIp)
                self.ipDataName.configure(text = f"Ip adresses: local {self.localIp} | external {self.externalIp}")
        except:
            messagebox.showerror("Error", "Failed to get information about Ip adresses!")

    def execute_internet_connection_data(self):
        try:
            while self.running:
                time.sleep(1)
                self.connectionString = "http://ya.ru"
                if requests.get(self.connectionString).ok:
                    self.txtAnswer = "Internet connection: connected +"
                    self.connectedInternetName.configure(text = self.txtAnswer)
                else:
                    self.txtAnswer = "Internet connection: not connected -"
                    self.connectedInternetName.configure(text = self.txtAnswer)
        except:
            messagebox.showerror("Error", "Failed to get information about Internet connection!")
        
    def execute_internet_speed_data(self):
        try:
            while self.running:
                time.sleep(1)
                self.netSpeed = psutil.net_io_counters()
                self.bytesSent = self.netSpeed.bytes_sent
                self.bytesRecv = self.netSpeed.bytes_recv
                self.speed = (self.bytesSent + self.bytesRecv) / 1024 / 1024
                self.speedAnswer = "Internet speed connection: {:.2f} mbit/s".format(self.speed)
                self.internetSpeedDataName.configure(text = self.speedAnswer)
        except:
            messagebox.showerror("Error", "Failed to get information about Internet speed connection!")


    def execute_cpu_load_data(self):
        try:
            while self.running:
                time.sleep(2)
                self.cpuLoad = psutil.cpu_percent(interval=1)
                self.systemUsageName.configure(text = f"CPU load: {self.cpuLoad}")
        except:
            messagebox.showerror("Error", "Failed to get information about CPU load!")
            self.systemUsageName.configure(text = "CPU load: none")


    def execute_memory_usage_data(self):
        try:
            while self.running:
                time.sleep(2)
                self.memoryLoad = psutil.virtual_memory()
                self.memoryUsage = self.memoryLoad.percent
                self.systemElementsUsageName.configure(text = f"Memory usage: {self.memoryUsage}%")
        except:
            messagebox.showerror("Error", "Failed to get information about memory usage!")
            self.systemElementsUsageName.configure(text = "Memory usage: none")

    def execute_disk_usage_data(self):
        try:
            while self.running:
                time.sleep(2)
                self.diskLoad = psutil.disk_usage('/')
                self.diskUsage = self.diskLoad.percent
                self.diskDataName.configure(text = f"Disk usage: {self.diskUsage}%")
        except:
            messagebox.showerror("Error", "Failed to get information about disk usage!")
            self.diskDataName.configure(text = "Disk usage: none")


    def execute_computer_time_data(self):
        try:
            while self.running:
                time.sleep(1)
                self.currentTime = datetime.now().time()
                self.computerTimeName.configure(text = f"Computer time: {self.currentTime}")
        except:
            messagebox.showerror("Error", "Failed to get information about computer time!")
        
    def execute_computer_calendar_data(self):
        try:
            while self.running:
                time.sleep(1)
                self.currentDate = datetime.now().date()
                self.computerCalendarName.configure(text = f"Computer calendar data: {self.currentDate}")    
        except:
            messagebox.showerror("Error", "Failed to get information about compputer date!")   

    def execute_battery_data(self):
        try:
            while self.running:
                time.sleep(1)
                self.batteryData = psutil.sensors_battery()
                self.batteryCharge = self.batteryData.percent
                self.batteryIsPlugged = self.batteryData.power_plugged
                if self.batteryData is not None:
                    self.batteryAnswer = f"Computer battery data: charge {self.batteryCharge}%"
                    self.computerBatteryName.configure(text = self.batteryAnswer)
                    if self.batteryIsPlugged:
                        self.batteryAnswer = f"Computer battery data: charge {self.batteryCharge}% | battery is connected to the charger"
                        self.computerBatteryName.configure(text = self.batteryAnswer)
                    else:
                        self.batteryAnswer = f"Computer battery data: charge {self.batteryCharge}% | battery is not connected to the charger"
                        self.computerBatteryName.configure(text = self.batteryAnswer)
        except:
            messagebox.showerror("Error", "Failed to get information about computer battery!")
            self.batteryAnswer = "Computer battery data:  battery is missing or there is no access to it"
            self.computerBatteryName.configure(text = self.batteryAnswer)

    def view_hard_drives_window(self):
        self.hardDrivesWin = ctk.CTkToplevel()
        self.hardDrivesWin.title("hard drives data (view)")
        self.hardDrivesWin.geometry("500x200")
        self.hardDrivesWin.resizable(0, 0)
        
        self.harddrivesdataView = ctk.CTkTextbox(self.hardDrivesWin, border_color="green", border_width=5, activate_scrollbars=False)
        self.harddrivesdataView.pack(fill="both", side="left", expand=True)
        self.yScrollBar = ctk.CTkScrollbar(self.hardDrivesWin, command=self.harddrivesdataView.yview)
        self.yScrollBar.pack(side="right", fill="y")
        self.harddrivesdataView.configure(yscrollcommand=self.yScrollBar.set)

        self.hdds = psutil.disk_partitions(all=True)
        try:
            time.sleep(1)
            for self.hdd in self.hdds:
                self.point = self.hdd.mountpoint
                self.usage = psutil.disk_usage(self.point)

                self.device = self.hdd.device
                self.mountpoint = self.hdd.mountpoint
                self.fstype = self.hdd.fstype
                self.total = self.usage.total
                self.free = self.usage.free
                self.used = self.usage.used
                self.usagePercent = self.usage.percent

                self.allData = f"Hard Drives Data:\n\nDevice: {self.device}\nMountpoint: {self.mountpoint}\nFstype: {self.fstype}\n Total: {self.total / (1024 ** 3):.2f} gb\n Free: {self.free / (1024 ** 3):.2f} gb\n Used: {self.used / (1024 ** 3):.2f} gb\n Usage: {self.usagePercent}%"

                self.harddrivesdataView.insert("0.0", self.allData)
        except:
            messagebox.showerror("Error", "Failed to get information about computer hard drives!")
            self.harddrivesdataView.insert("0.0", "none data")

        self.harddrivesdataView.configure(state="disabled")
        self.hardDrivesWin.attributes("-topmost", True)

    def view_video_cards_window(self):
        self.videoCardsWin = ctk.CTkToplevel()
        self.videoCardsWin.title("video cards data (view)")
        self.videoCardsWin.geometry("500x200")
        self.videoCardsWin.resizable(0, 0)

        self.videocardsView = ctk.CTkTextbox(self.videoCardsWin, border_color="green", border_width=5, activate_scrollbars=False)
        self.videocardsView.pack(fill="both", side="left", expand=True)
        self.yScrollBar = ctk.CTkScrollbar(self.videoCardsWin, command=self.videocardsView.yview)
        self.yScrollBar.pack(side="right", fill="y")
        self.videocardsView.configure(yscrollcommand=self.yScrollBar.set)

        try:
            self.os = platform.system()

            if self.os == "Windows":
                time.sleep(1)
                self.info = os.popen('wmic path win32_videocontroller get name', 'r')
                self.text = self.info.read()
                self.videocardsView.insert("0.0", f"Graphics processors and cards:\n\n {self.text}")   
            elif self.os == "Darwin":
                time.sleep(1)
                self.info = os.popen('system_profiler SPDisplaysDataType', 'r') 
                self.text = self.info.read()   
                self.videocardsView.insert("0.0", f"Graphics processors and cards:\n\n {self.text}") 
            else:
                time.sleep(1)
                self.info = os.popen('lshw', 'r')
                self.text = self.info.read()
                self.videocardsView.insert("0.0", f"Graphics processors and cards:\n\n {self.text}") 

        except:
            messagebox.showerror("Error", "Failed to get information about computer video cards!")
            self.videocardsView.insert("0.0", "none data") 

        self.videocardsView.configure(state="disabled")
        self.videoCardsWin.attributes("-topmost", True)

    def view_additional_processor_window(self):
        self.additionalProcessorWin = ctk.CTkToplevel()
        self.additionalProcessorWin.title("video cards data (view)")
        self.additionalProcessorWin.geometry("500x200")
        self.additionalProcessorWin.resizable(0, 0)

        self.addprocessorView = ctk.CTkTextbox(self.additionalProcessorWin, border_color="green", border_width=5, activate_scrollbars=False)
        self.addprocessorView.pack(fill="both", side="left", expand=True)
        self.yScrollBar = ctk.CTkScrollbar(self.additionalProcessorWin, command=self.addprocessorView.yview)
        self.yScrollBar.pack(side="right", fill="y")
        self.addprocessorView.configure(yscrollcommand=self.yScrollBar.set)

        self.osInfo = platform.system()
        try:
            if self.osInfo == "Windows":
                time.sleep(1)
                self.computer = wmi.WMI()
                self.procInfo = self.computer.Win32_Processor()[0]
                self.procInfo2 = self.procInfo.Name
                self.finalInfo = f"{self.procInfo2}\n\n{self.procInfo}"
                self.addprocessorView.insert("0.0", self.finalInfo)
            else:
                time.sleep(1)
                self.SimpleProcData = platform.processor()
                self.addprocessorView.insert("0.0", f"{self.SimpleProcData}")

        except:
            messagebox.showerror("Error", "Failed to get information about additional processor data!")
            self.addprocessorView.insert("0.0", "none")

        self.addprocessorView.configure(state="disabled")
        self.additionalProcessorWin.attributes("-topmost", True)

    def view_apps_data_window(self):
        self.appsWin = ctk.CTkToplevel()
        self.appsWin.title("installed apps data (view)")
        self.appsWin.geometry("500x200")
        #self.appsWin.resizable(0, 0)

        self.appsListView = ctk.CTkTextbox(self.appsWin, border_color="green", border_width=5, activate_scrollbars=False)
        self.appsListView.pack(fill="both", side="left", expand=True)
        self.appsListView.tag_config("center", justify="center")
        self.yScrollBar = ctk.CTkScrollbar(self.appsWin, command=self.appsListView.yview)
        self.yScrollBar.pack(side="right", fill="y")
        self.appsListView.configure(yscrollcommand=self.yScrollBar.set)

        
        self.osVersion = platform.system()

        try:
            if self.osVersion == "Windows":
                time.sleep(1)
                self.appsData = subprocess.check_output(['wmic', 'product', 'get', 'name'])
                self.finalAppsData = str(self.appsData)
                time.sleep(1)
                try:
                    for i in range(len(self.finalAppsData)):
                        self.appList = self.finalAppsData.split("\\r\\r\\n")[6:][i]
                        self.appList.strip()
                        self.appsListView.insert("end", self.appList, "center")
                
                except:
                    messagebox.showerror("Error", "Failed to get list of computer apps!")
                    self.appsListView.insert("0.0", "none")


            elif self.osVersion == "Darwin":
                time.sleep(1)
                self.appsData = subprocess.check_output(['ls', '/Applications'])
                self.finalAppsData = str(self.appsData)
                time.sleep(1)
                try:
                    for i in range(len(self.finalAppsData)):
                        self.appList = self.finalAppsData.split("\\r\\r\\n")[6:][i]
                        self.appList.strip()
                        self.appsListView.insert("end", self.appList, "center")

                except:
                    messagebox.showerror("Error", "Failed to get list of computer apps!")
                    self.appsListView.insert("0.0", "none")   

            else:
                time.sleep(1)
                self.appsData = subprocess.check_output(['ls', '/usr/share/applications'])
                self.finalAppsData = str(self.appsData)
                time.sleep(1)
                try:
                    for i in range(len(self.finalAppsData)):
                        self.appList = self.finalAppsData.split("\\r\\r\\n")[6:][i]
                        self.appList.strip()
                        self.appsListView.insert("end", self.appList, "center")

                except:
                    messagebox.showerror("Error", "Failed to get list of computer apps!")
                    self.appsListView.insert("0.0", "none")

        except:
            messagebox.showerror("Error", "Failed to get information about installed computer apps!")
            self.appsListView.insert("0.0", "none") 


        self.appsListView.configure(state="disabled")
        self.appsWin.attributes("-topmost", True)

    def view_drivers_data_window(self):
        self.DriversWin = ctk.CTkToplevel()
        self.DriversWin.title("drivers data (view)")
        self.DriversWin.geometry("500x200")

        self.driversListView = ctk.CTkTextbox(self.DriversWin, border_color="green", border_width=5, activate_scrollbars=False)
        self.driversListView.pack(fill="both", side="left", expand=True)
        self.driversListView.tag_config("center", justify="center")
        self.yScrollBar = ctk.CTkScrollbar(self.DriversWin, command=self.driversListView.yview)
        self.yScrollBar.pack(side="right", fill="y")
        self.driversListView.configure(yscrollcommand=self.yScrollBar.set)
        self.encodeString = ctk.CTkEntry(self.DriversWin, placeholder_text="enter encoding name", border_color="green", border_width=5)
        self.encodeString.pack(side="top", fill="x", padx=5)
        self.applyEncoding = ctk.CTkButton(self.DriversWin, text="apply encoding", fg_color="green", hover_color="#32CD32", command=self.change_driver_data_encoding)
        self.applyEncoding.pack(side="right", fill="both", pady=10, padx=5)

        self.osVersion = platform.system()

        if self.osVersion == "Windows":
            try:
                try:
                    self.result = subprocess.check_output(['driverquery', '/V'], shell=True).decode("cp866")
                    time.sleep(1)
                    self.data = str(self.result)
                    with open("drivers.txt", "w", encoding="UTF-8") as file:
                        file.write(self.data)
                    time.sleep(1)
                    with open("drivers.txt", "r", encoding="UTF-8") as file:
                        self.text = file.read()
                        self.driversListView.insert("0.0", self.text)
                    time.sleep(1)
                    self.a = os.path.abspath("drivers.txt")
                    messagebox.showinfo("Info", f"A text file with driver data has been created!\nfile path: {self.a}")
                except:
                    self.result = subprocess.check_output(['driverquery', '/V'], shell=True).decode("ISO-8859-1")
                    time.sleep(1)
                    self.data = str(self.result)
                    with open("drivers.txt", "w", encoding="UTF-8") as file:
                        file.write(self.data)
                    time.sleep(1)
                    with open("drivers.txt", "r", encoding="UTF-8") as file:
                        self.text = file.read()
                        self.driversListView.insert("0.0", self.text)
                    time.sleep(1)
                    self.a = os.path.abspath("drivers.txt")
                    messagebox.showinfo("Info", f"A text file with driver data has been created!\nfile path: {self.a}")
            except:
                self.result = subprocess.check_output(['driverquery', '/V'], shell=True)
                time.sleep(1)
                self.data = str(self.result)
                with open("drivers.txt", "w", encoding="UTF-8") as file:
                    file.write(self.data)
                time.sleep(1)
                with open("drivers.txt", "r", encoding="UTF-8") as file:
                    self.text = file.read()
                    self.driversListView.insert("0.0", self.text)
                time.sleep(1)
                self.a = os.path.abspath("drivers.txt")
                messagebox.showinfo("Info", f"A text file with driver data has been created!\nfile path: {self.a}")

        elif self.osVersion == "Darwin":
            try:
                try:
                    self.result = subprocess.check_output(['kextstat'], shell=True).decode("ISO-8859-1")
                    time.sleep(1)
                    self.data = str(self.result)
                    with open("drivers.txt", "w", encoding="UTF-8") as file:
                        file.write(self.data)
                    time.sleep(1)
                    with open("drivers.txt", "r", encoding="UTF-8") as file:
                        self.text = file.read()
                        self.driversListView.insert("0.0", self.text)
                    time.sleep(1)
                    self.a = os.path.abspath("drivers.txt")
                    messagebox.showinfo("Info", f"A text file with driver data has been created!\nfile path: {self.a}")
                except:
                    self.result = subprocess.check_output(['kextstat'], shell=True).decode("UTF-8")
                    time.sleep(1)
                    self.data = str(self.result)
                    with open("drivers.txt", "w", encoding="UTF-8") as file:
                        file.write(self.data)
                    time.sleep(1)
                    with open("drivers.txt", "r", encoding="UTF-8") as file:
                        self.text = file.read()
                        self.driversListView.insert("0.0", self.text)
                    time.sleep(1)
                    self.a = os.path.abspath("drivers.txt")
                    messagebox.showinfo("Info", f"A text file with driver data has been created!\nfile path: {self.a}")
            except:
                self.result = subprocess.check_output(['kextstat'], shell=True)
                time.sleep(1)
                self.data = str(self.result)
                with open("drivers.txt", "w", encoding="UTF-8") as file:
                    file.write(self.data)
                time.sleep(1)
                with open("drivers.txt", "r", encoding="UTF-8") as file:
                    self.text = file.read()
                    self.driversListView.insert("0.0", self.text)
                time.sleep(1)
                self.a = os.path.abspath("drivers.txt")
                messagebox.showinfo("Info", f"A text file with driver data has been created!\nfile path: {self.a}")
        else:
            try:
                try:
                    self.result = subprocess.check_output(['lsmod'], shell=True).decode("KOI8-R")
                    time.sleep(1)
                    self.data = str(self.result)
                    with open("drivers.txt", "w", encoding="UTF-8") as file:
                        file.write(self.data)
                    time.sleep(1)
                    with open("drivers.txt", "r", encoding="UTF-8") as file:
                        self.text = file.read()
                        self.driversListView.insert("0.0", self.text)
                    self.a = os.path.abspath("drivers.txt")
                    messagebox.showinfo("Info", f"A text file with driver data has been created!\nfile path: {self.a}")
                except:
                    self.result = subprocess.check_output(['lsmod'], shell=True).decode("ISO-8859-1")
                    time.sleep(1)
                    self.data = str(self.result)
                    with open("drivers.txt", "w", encoding="UTF-8") as file:
                        file.write(self.data)
                    time.sleep(1)
                    with open("drivers.txt", "r", encoding="UTF-8") as file:
                        self.text = file.read()
                        self.driversListView.insert("0.0", self.text)
                    time.sleep(1)
                    self.a = os.path.abspath("drivers.txt")
                    messagebox.showinfo("Info", f"A text file with driver data has been created!\nfile path: {self.a}")
            except:
                self.result = subprocess.check_output(['lsmod'], shell=True)
                time.sleep(1)
                self.data = str(self.result)
                with open("drivers.txt", "w", encoding="UTF-8") as file:
                    file.write(self.data)
                time.sleep(1)
                with open("drivers.txt", "r", encoding="UTF-8") as file:
                    self.text = file.read()
                    self.driversListView.insert("0.0", self.text)
                time.sleep(1)
                self.a = os.path.abspath("drivers.txt")
                messagebox.showinfo("Info", f"A text file with driver data has been created!\nfile path: {self.a}")

        time.sleep(2)
        messagebox.showwarning("Warning", "Driver data is taken directly from the computer system and decoded with the necessary encoding. If your computer does not support the necessary encoding, then this may lead to a decrease in the readability of the data")
        
        self.driversListView.configure(state="disabled")
        self.DriversWin.attributes("-topmost", True)

    def change_driver_data_encoding(self):
        try:
            time.sleep(1)
            self.textData = self.driversListView.get("0.0", "end")
            self.encodeData = self.encodeString.get()
            self.encodingStr = str(self.textData)
            self.Encoding = str(self.encodeData)
            self.encodedResult = self.encodingStr.encode(self.Encoding)
            time.sleep(2)
            self.driversListView.insert("0.0", self.encodedResult)
        except UnicodeEncodeError:
            messagebox.showerror("Error", "Failed to change encoding!")

    def view_network_interfaces_window(self):
        self.NetFacesWin = ctk.CTkToplevel()
        self.NetFacesWin.title("network interfaces (view)")
        self.NetFacesWin.geometry("500x200")
        self.NetFacesWin.resizable(0, 0)

        self.netFacesListView = ctk.CTkTextbox(self.NetFacesWin, border_color="green", border_width=5, activate_scrollbars=False)
        self.netFacesListView.pack(fill="both", side="left", expand=True)
        self.netFacesListView.tag_config("center", justify="center")
        self.yScrollBar = ctk.CTkScrollbar(self.NetFacesWin, command=self.netFacesListView.yview)
        self.yScrollBar.pack(side="right", fill="y")
        self.netFacesListView.configure(yscrollcommand=self.yScrollBar.set)

        try:
            time.sleep(1)
            self.addrs = psutil.net_if_addrs()
            self.info = self.addrs.keys()

            for self.key in self.addrs:
                self.keYS =  self.key + "\n"
                self.netFacesListView.insert("0.0", self.keYS)
        except:
            messagebox.showerror("Error", "Failed to get information about computer network interfaces!")
            self.netFacesListView.insert("0.0", "none")

        self.netFacesListView.configure(state="disabled")
        self.NetFacesWin.attributes("-topmost", True)

    def turn_sleep_mode_computer(self):
        try:
            self.osVersion = platform.system()

            if self.osVersion == "Windows":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            elif self.osVersion == "Darwin":
                os.system("pmset sleepnow")
            else:
                os.system("systemctl suspend")
        except:
            messagebox.showerror("Error", "Sleep mode failed!")

    def turn_off_computer(self):
        try:
            self.osVersion = platform.system()

            if self.osVersion == "Windows":
                os.system("shutdown -s")
            elif self.osVersion == "Darwin":
                os.system("shutdown -h now")
            else:
                os.system("sudo shutdown now")
        except:
            messagebox.showerror("Error", "Turn off computer failed!")

    def restart_computer(self):
        try:
            self.osVersion = platform.system()

            if self.osVersion == "Windows":
                os.system("shutdown /r /t 0")
            elif self.osVersion == "Darwin":
                os.system("sudo shutdown -r now")
            else:
                os.system("sudo reboot")
        except:
            messagebox.showerror("Error", "Restart computer failed!")

    def configure_txt_report(self):
        time.sleep(1)
        try:
            self.dataTXTToSave = (f"""Half Computer Data Text Report\n
|-----------------------------------|
 Computer model: {self.finalResult}
 Device name: {self.deviceName}
|-----------------------------------|
_________________________________________________________________________________________________________________________
Data report was created based on the state of the computer at the time({self.currentTime}) and date({self.currentDate})  
Warning, this is not a complete report! Not all the data is here.                                                        
_________________________________________________________________________________________________________________________

|Hardware Specifications|\n
processor: {self.processorData}\n
processor core count: {self.coreCount}\n
processor clock speed: {self.clockSpeed} (min - {self.clockSpeedMin} | max - {self.clockSpeedMax})\n
RAM memory: (total - {self.ramData1:.2f} mb | used - {self.ramData2:.2f} mb | free - {self.freeRamData} mb\n
|Software|\n
OS: {self.osNameData}\n
Additional OS data: {self.finalOsData}\n
|Network Settings|
Ip adresses: (local - {self.localIp} | external - {self.externalIp})\n
Internet connection: {self.txtAnswer}\n
Internet speed: {self.speedAnswer}\n
|System Status|\n
CPU load: {self.cpuLoad}\n
Memory usage: {self.memoryUsage}%\n
Disk usage: {self.diskUsage}%\n
|Other|\n
Computer locale: {self.locale}\n
Computer encoding: {self.encodingInfo}\n
Machine: {self.machine}\n
Computer time: {self.currentTime}\n
Computer calendar data: {self.currentDate}\n
Computer battery data: {self.batteryAnswer}\n
Connected WIFI: {self.wifiAnswer}

Done.
____________________________________________________________________________________
            """)
            self.fileName = f"HalfTextComputerDataReport{self.currentDate}.txt"
            self.filePath = filedialog.askdirectory()
            if os.path.exists(self.filePath):
                loadingScreen()
                with open(os.path.join(self.filePath, self.fileName), "w", encoding="UTF-8") as file:
                    file.write(self.dataTXTToSave)
                time.sleep(1)
                messagebox.showinfo("Info", f"Half Computer Data Text Report was created!\nfile path: {self.filePath}")
                time.sleep(2)
                os.open(self.filePath)

        except:
            messagebox.showerror("Error", "A text data report creation error! Please, check all settings and try again.")
            
    def fetch_net_faces(self):
        try:
            time.sleep(1)
            self.addrs = psutil.net_if_addrs()
            self.info = self.addrs.keys()
            self.keYS = []

            for self.key in self.addrs:
                self.keYS.append(self.key)
            #print(self.keYS)
        except:
            self.keYS = "none"

    def fetch_drivers_data(self):
        self.osVersion = platform.system()

        self.filePath = "drivers.txt"

        time.sleep(1)
        if os.path.exists(self.filePath):
            with open("drivers.txt", "r", encoding="UTF-8") as file:
                self.textDrivers = file.read()
                #self.textDrivers = str(self.textDrivers1)
                #print(self.textDrivers)

        else:
            time.sleep(1)
            if self.osVersion == "Windows":
                try:
                    try:
                        self.result = subprocess.check_output(['driverquery', '/V'], shell=True).decode("cp866")
                        time.sleep(1)
                        self.data = str(self.result)
                        with open("drivers.txt", "w", encoding="UTF-8") as file:
                            file.write(self.data)
                        time.sleep(1)
                        with open("drivers.txt", "r", encoding="UTF-8") as file:
                            self.textDrivers = file.read()
                        
                    except:
                        self.result = subprocess.check_output(['driverquery', '/V'], shell=True).decode("ISO-8859-1")
                        time.sleep(1)
                        self.data = str(self.result)
                        with open("drivers.txt", "w", encoding="UTF-8") as file:
                            file.write(self.data)
                        time.sleep(1)
                        with open("drivers.txt", "r", encoding="UTF-8") as file:
                            self.textDrivers = file.read()
                except:
                    self.result = subprocess.check_output(['driverquery', '/V'], shell=True)
                    time.sleep(1)
                    self.data = str(self.result)
                    with open("drivers.txt", "w", encoding="UTF-8") as file:
                        file.write(self.data)
                    time.sleep(1)
                    with open("drivers.txt", "r", encoding="UTF-8") as file:
                        self.textDrivers = file.read()
            elif self.osVersion == "Darwin":
                try:
                    try:
                        self.result = subprocess.check_output(['kextstat'], shell=True).decode("ISO-8859-1")
                        time.sleep(1)
                        self.data = str(self.result)
                        with open("drivers.txt", "w", encoding="UTF-8") as file:
                            file.write(self.data)
                        time.sleep(1)
                        with open("drivers.txt", "r", encoding="UTF-8") as file:
                            self.textDrivers = file.read()
                    except:
                        self.result = subprocess.check_output(['kextstat'], shell=True).decode("UTF-8")
                        time.sleep(1)
                        self.data = str(self.result)
                        with open("drivers.txt", "w", encoding="UTF-8") as file:
                            file.write(self.data)
                        time.sleep(1)
                        with open("drivers.txt", "r", encoding="UTF-8") as file:
                            self.textDrivers = file.read()
                except:
                    self.result = subprocess.check_output(['kextstat'], shell=True)
                    time.sleep(1)
                    self.data = str(self.result)
                    with open("drivers.txt", "w", encoding="UTF-8") as file:
                        file.write(self.data)
                    time.sleep(1)
                    with open("drivers.txt", "r", encoding="UTF-8") as file:
                        self.textDrivers = file.read()
            else:
                try:
                    try:
                        self.result = subprocess.check_output(['lsmod'], shell=True).decode("KOI8-R")
                        time.sleep(1)
                        self.data = str(self.result)
                        with open("drivers.txt", "w", encoding="UTF-8") as file:
                            file.write(self.data)
                        time.sleep(1)
                        with open("drivers.txt", "r", encoding="UTF-8") as file:
                            self.textDrivers = file.read()
                    except:
                        self.result = subprocess.check_output(['lsmod'], shell=True).decode("ISO-8859-1")
                        time.sleep(1)
                        self.data = str(self.result)
                        with open("drivers.txt", "w", encoding="UTF-8") as file:
                            file.write(self.data)
                        time.sleep(1)
                        with open("drivers.txt", "r", encoding="UTF-8") as file:
                            self.textDrivers = file.read()
                except:
                    self.result = subprocess.check_output(['lsmod'], shell=True)
                    time.sleep(1)
                    self.data = str(self.result)
                    with open("drivers.txt", "w", encoding="UTF-8") as file:
                        file.write(self.data)
                    time.sleep(1)
                    with open("drivers.txt", "r", encoding="UTF-8") as file:
                        self.textDrivers = file.read()

    def fetch_hard_drives_data(self):
        self.hdds = psutil.disk_partitions(all=True)
        try:
            time.sleep(1)
            for self.hdd in self.hdds:
                self.point = self.hdd.mountpoint
                self.usage = psutil.disk_usage(self.point)

                self.device = self.hdd.device
                self.mountpoint = self.hdd.mountpoint
                self.fstype = self.hdd.fstype
                self.total = self.usage.total
                self.free = self.usage.free
                self.used = self.usage.used
                self.usagePercent = self.usage.percent

                time.sleep(1)
                self.hardDrives = f"Hard Drives Data:\n\nDevice: {self.device}\nMountpoint: {self.mountpoint}\nFstype: {self.fstype}\n Total: {self.total / (1024 ** 3):.2f} gb\n Free: {self.free / (1024 ** 3):.2f} gb\n Used: {self.used / (1024 ** 3):.2f} gb\n Usage: {self.usagePercent}%"
        except:
            self.hardDrives = "none"

    def fetch_video_cards_data(self):
        self.os = platform.system()
        try:
            if self.os == "Windows":
                time.sleep(1)
                self.info = os.popen('wmic path win32_videocontroller get name', 'r')
                self.text = self.info.read()
                self.videoCardsInfo = f"Graphics processors and cards:\n\n {self.text}"

            elif self.os == "Darwin":
                time.sleep(1)
                self.info = os.popen('system_profiler SPDisplaysDataType', 'r') 
                self.text = self.info.read()   
                self.videoCardsInfo = f"Graphics processors and cards:\n\n {self.text}"

            else:
                time.sleep(1)
                self.info = os.popen('lshw', 'r')
                self.text = self.info.read()
                self.videoCardsInfo = f"Graphics processors and cards:\n\n {self.text}"

        except:
            self.videoCardsInfo = f"Graphics processors and cards:\n\n none"

    def fetch_installed_apps_data(self):
        self.osVersion = platform.system()
        time.sleep(1)
        try:
            if self.osVersion == "Windows":
                self.getApps = subprocess.check_output(['wmic', 'product', 'get', 'name'])
                self.installedApps = str(self.getApps)

                try:
                    for i in range(len(self.installedApps)):
                        self.listOfApps = self.installedApps.split("\\r\\r\\n")[6:][i]
                except IndexError as e:
                    self.listOfApps += ""

            elif self.osVersion == "Darwin":
                self.getApps = subprocess.check_output(['ls', '/Applications'])
                self.installedApps = str(self.getApps)
                
                try:
                    for i in range(len(self.installedApps)):
                        self.listOfApps = self.installedApps.split("\\r\\r\\n")[6:][i]
                except IndexError as e:
                    self.listOfApps += "Done."
                    
            else:
                self.getApps = subprocess.check_output(['ls', '/usr/share/applications'])
                self.installedApps = str(self.getApps)

                try:
                    for i in range(len(self.installedApps)):
                        self.listOfApps = self.installedApps.split("\\r\\r\\n")[6:][i]
                except IndexError as e:
                    self.listOfApps += "Done."

        except:
            self.listOfApps = "none"

    def configure_html_report(self):
        time.sleep(1)

        self.threadNF = threading.Thread(target=self.fetch_net_faces, daemon=True)
        self.threadDV = threading.Thread(target=self.fetch_drivers_data, daemon=True)
        self.threadHD = threading.Thread(target=self.fetch_hard_drives_data, daemon=True)
        self.threadVD = threading.Thread(target=self.fetch_video_cards_data, daemon=True)
        self.threadIA = threading.Thread(target=self.fetch_installed_apps_data, daemon=True)

        self.threadNF.start()
        self.threadDV.start()
        self.threadHD.start()
        self.threadVD.start()
        self.threadIA.start()

        try:
            self.dataHTMLToSave = (f"""<center><h1>Full Computer Data Report</h1></center>

<center><h2>Computer model: {self.finalResult}<h2></center>
<center><h2>Device name: {self.deviceName}<h2></center>

<center><h2>Data report was created based on the state of the computer at the time({self.currentTime}) and date({self.currentDate})</h2></center>
<br>
<br>
<center><p>processor: {self.processorData}</p></center>
<center><p>processor core count: {self.coreCount}</p></center>
<center><p>processor clock speed: {self.clockSpeed} (min - {self.clockSpeedMin} | max - {self.clockSpeedMax})</p></center>
<center><p>RAM memory: (total - {self.ramData1:.2f} mb | used - {self.ramData2:.2f} mb | free - {self.freeRamData} mb</p></cemter>
<center><p>Hard drives:</p></center>
<center><textarea>{self.hardDrives}</textarea></center>
<center><p>Video cards:</p></center>
<center><textarea>{self.videoCardsInfo}</textarea></center>
<br>
<br>
<center><p>OS: {self.osNameData}</p></center>
<center><p>Additional OS data: {self.finalOsData}</p></center>
<center><p>Driver versions:</p></center>
<center><textarea>{self.textDrivers}</textarea></center>
<center><p>Installed apps:</p></center>
<center><textarea>{self.listOfApps}</textarea></center>
<br>
<br>
<center><p>Network interfaces:</p></center>
<center><textarea>{self.keYS}</textarea></center>
<center><p>Ip adresses: (local - {self.localIp} | external - {self.externalIp})</p></center>
<center><p>Internet connection: {self.txtAnswer}</p></center>
<center><p>Internet speed: {self.speedAnswer}</p></center>
<br>
<br>
<center><p>CPU load: {self.cpuLoad}</p></center>
<center><p>Memory usage: {self.memoryUsage}%</p></center>
<center><p>Disk usage: {self.diskUsage}%</p></center>
<br>
<br>
<center><p>Computer locale: {self.locale}</p></center>
<center><p>Computer encoding: {self.encodingInfo}</p></center>
<center><p>Machine: {self.machine}</p></center>
<center><p>Computer time: {self.currentTime}</p></center>
<center><p>Computer calendar data: {self.currentDate}</p></center>
<center><p>Computer battery data: {self.batteryAnswer}</p></center>
<center><p>Connected WIFI: {self.wifiAnswer}</p></center>


<center><h1>Done.</h1><?center
""")
            self.fileName = f"FullHtmlComputerDataReport{self.currentDate}.html"
            self.filePath = filedialog.askdirectory()
            self.openPath = self.filePath + self.fileName
            loadingScreen()
            if os.path.exists(self.filePath):
                with open(os.path.join(self.filePath, self.fileName), "w", encoding="UTF-8") as file:
                    file.write(self.dataHTMLToSave)
                time.sleep(1)
                messagebox.showinfo("Info", f"Full Computer Data Html Report was created!\nfile path: {self.filePath}")
                time.sleep(2)
        except Exception as e:
            messagebox.showerror("Error", f"A html data report creation error! Please, check all settings and try again.\n {e}")

    def open_console(self):
        try:
            self.osVersion = platform.system()
            time.sleep(1)

            if self.osVersion == "Windows":
                os.system("cmd.exe")
            elif self.osVersion == "Darwin":
                os.system("open -a Terminal")
            else:
                os.system("konsole")

        except:
            messagebox.showerror("Error", "Failed to open console!")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
