import requests
import socket as s
import json
from urllib.parse import urlparse
from dns.resolver import *
import sys

from colorama import init, Fore, Back, Style

from PyEnhance import Stamps

Stamp = Stamps.Stamp

Input = Stamp.Input
Output = Stamp.Output
Error = Stamp.Error
Info = Stamp.Info
Warn = Stamp.Warn

PositiveStatusCodes = [200, 201, 202, 203, 204, 205, 206,
                       300, 301, 302, 303, 304, 305, 307,
                       308, 401]

class Start(object):

    def __init__(self,  URL=any):
        self.SpecialCharacters = [
            '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-',
            '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
            '_', '`', '{', '|', '}', '~'
        ]

        self.URL = URL
        print('\n')
        self.BasicInfo()


    def BasicInfo(self):
        self.Stage1()
        self.Stage2()
        self.Stage3()
        self.Stage4()

    def FetchTLDS(self):
        TLDSs = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
        response = requests.get(TLDSs)
        response.raise_for_status()
        self.TLDS = [line.strip().lower() for line in response.text.splitlines() if not line.startswith('#')]

    def CheckTLDS(self):
        self.TLDSValid = False
        for i in self.TLDS:
            if self.URL.endswith("/"):
                self.URL = self.URL[:-1]
            if self.URL.endswith(i):
                self.TLDSValid = True
                print(f"{Info} URL has a valid TLDS (.com, .org, .xyz, etc.)")
                break

        if self.TLDSValid is False:
            inp = input(f"{Error} URL does not have a valid TLDS. Do you want to continue? [Y/N] ")
            if inp in ["y", "Y"]:
                print("Continuing...")
            else:
                print("Exiting...")
                sys.exit()

    def IsURLAnIP(self):
        try:
            s.inet_aton(self.URL)
            print(f"{Info} URL is an IP address")
        except s.error:
            print(f"{Info} URL is not an IP address")

    def Refactor(self, URL):
        self.TLDSValid = False

        for i in ["https://", "http://"]:
            if URL.startswith(i):
                if i == "https://":
                    self.URLHTTPS = URL
                    self.URLHTTP = URL.replace("https://", "http://")
                if i == "http//":
                    self.URLHTTP = URL
                    self.URLHTTPS = URL.replace("http://", "https://")
                break
            else:
                self.URLHTTP = f"http://{URL}"
                self.URLHTTPS = f"https://{URL}"


    def Checks(self):
        def HTTPcheck():
            GetReqStatus = requests.get(url=self.URLHTTP)
            if GetReqStatus.status_code in PositiveStatusCodes:
                print(f"{Info} HTTP Valid")
            else:
                print(f"{self.URL} is not a valid URL")

        def HTTPScheck():
            GetReqStatus = requests.get(url=self.URLHTTPS)
            if GetReqStatus.status_code == 200:
                print(f"{Info} HTTPS Valid")
            else:
                print(f"{self.URL} is not a valid URL")

        HTTPcheck()
        HTTPScheck()


    def Stage1(self):
        self.FetchTLDS()
        self.CheckTLDS()
        self.IsURLAnIP()
        self.Refactor(self.URL)
        self.Checks()

    def Stage2(self):
        o = urlparse(self.URLHTTP)
        self.HostnameForIP = o.hostname
        self.WebSiteIP = s.gethostbyname(self.HostnameForIP)

    def Stage3(self):
        def Country():
            URL = f'http://ip-api.com/json/{self.WebSiteIP}?fields=1'
            GetIpInfoCountry = requests.get(url=URL)
            self.IPinfoCountryOutput = json.loads(GetIpInfoCountry.text)["country"]

        def StateOrRegion():
            URL = f'http://ip-api.com/json/{self.WebSiteIP}?fields=8'
            GetIpInfoStateOrRegion = requests.get(url=URL)
            self.IPinfoStateOrRegionOutput = json.loads(GetIpInfoStateOrRegion.text)["regionName"]

        def City():
            URL = f'http://ip-api.com/json/{self.WebSiteIP}?fields=16'
            GetIpInfoCity = requests.get(url=URL)
            self.IPinfoCityOutput = json.loads(GetIpInfoCity.text)["city"]

        def ISP():
            URL = f'http://ip-api.com/json/{self.WebSiteIP}?fields=512'
            GetIPinfoISP = requests.get(url=URL)
            self.IPinfoISPOutput = json.loads(GetIPinfoISP.text)["isp"]

        Country()
        StateOrRegion()
        City()
        ISP()

    def Stage4(self):
        print('\n')
        print(f"{Output} Hostname: {self.HostnameForIP}")
        print(f"{Output} IP Address: {self.WebSiteIP}")
        print(f"{Output} ISP: {self.IPinfoISPOutput}")
        print(f"{Output} Country: {self.IPinfoCountryOutput}")
        print(f"{Output} State or Region: {self.IPinfoStateOrRegionOutput}")
        print(f"{Output} City: {self.IPinfoCityOutput}")



    def JsonOutput(self):

        JsonDict = {
            "Hostname": self.HostnameForIP.strip(),
            "IP Address": self.WebSiteIP.strip(),
            "ISP": self.IPinfoISPOutput.strip(),
            "Country": self.IPinfoCountryOutput.strip(),
            "State or Region": self.IPinfoStateOrRegionOutput.strip(),
            "City": self.IPinfoCityOutput.strip()
        }

        return JsonDict





