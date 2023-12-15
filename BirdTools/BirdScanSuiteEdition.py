import socket, os, json, sys
import datetime
import threading as t

datetime = datetime.datetime


class PortScaner(object):

    def __init__(self, URLorIP=any, ScanType=any, InputRange=int):

        self.CommonPortsDict = {
            1: 'TCPMUX', 5: 'RJE', 7: 'ECHO', 9: 'DISCARD',
            11: 'SYSTAT', 13: 'DAYTIME', 17: 'QOTD', 18: 'MSP',
            19: 'CHARGEN', 20: 'FTP_DATA', 21: 'FTP_CONTROL', 22: 'SSH',
            23: 'TELNET', 25: 'SMTP', 37: 'TIME', 42: 'NAMESERVER',
            43: 'WHOIS', 49: 'TACACS', 53: 'DNS', 67: 'DHCP_CLIENT',
            68: 'DHCP_SERVER', 69: 'TFTP', 70: 'Gopher', 79: 'Finger',
            80: 'HTTP', 88: 'Kerberos', 102: 'MS Exchange', 110: 'POP3',
            113: 'IDENT', 119: 'NNTP', 123: 'NTP', 135: 'RPC',
            137: 'NetBIOS-NS', 138: 'NetBIOS-DGM', 139: 'NetBIOS-SSN', 143: 'IMAP',
            161: 'SNMP', 179: 'BGP', 194: 'IRC', 201: 'AppleTalk',
            220: 'IMAP3', 389: 'LDAP', 443: 'HTTPS', 445: 'SMB',
            464: 'Kerberos Change/Set password', 465: 'SMTPS', 500: 'ISAKMP', 514: 'Syslog',
            520: 'RIP', 530: 'RPC', 543: 'Kerberos (klogin)', 544: 'Kerberos (kshell)',
            546: 'DHCPv6 Client', 547: 'DHCPv6 Server', 554: 'RTSP', 587: 'SMTP (Message Submission)',
            631: 'Internet Printing Protocol (IPP)', 636: 'LDAPS', 873: 'rsync', 902: 'VMware Server Console',
            989: 'FTPS (data)', 990: 'FTPS (control)', 993: 'IMAPS', 995: 'POP3S',
            1025: 'Microsoft RPC', 1433: 'Microsoft SQL Server', 1434: 'Microsoft SQL Monitor',
            1521: 'Oracle database default listener',
            1723: 'PPTP', 1724: 'PPTP', 2049: 'NFS', 2082: 'cPanel',
            2083: 'cPanel', 2181: 'ZooKeeper', 2222: 'DirectAdmin', 3306: 'MySQL',
            3389: 'RDP', 3690: 'SVN', 4333: 'mSQL', 4444: 'Metasploit',
            5060: 'SIP', 5432: 'PostgreSQL', 5900: 'VNC', 5984: 'CouchDB',
            6379: 'Redis', 6667: 'IRC', 6881: 'BitTorrent', 8000: 'HTTP alternate',
            8080: 'HTTP alternate', 8443: 'HTTPS alternate', 8888: 'HTTP alternate', 9000: 'SonarQube',
            9090: 'Openfire Administration Console', 9200: 'Elasticsearch', 9300: 'Elasticsearch', 9418: 'Git',
            27017: 'MongoDB', 27018: 'MongoDB', 27019: 'MongoDB', 50000: 'SAP',
            50070: 'Hadoop NameNode', 50075: 'Hadoop DataNode', 50090: 'Hadoop Secondary NameNode', 5601: 'Kibana',
            5985: 'WinRM (Windows Remote Management)', 7077: 'Apache Spark', 9091: 'Transmission (BitTorrent client)',
            10000: 'Webmin (Web-based interface for system administration)',
            11211: 'Memcached', 28017: 'MongoDB Web Status Page', 3260: 'iSCSI',
            51413: 'Transmission (BitTorrent client)',
            64738: 'Mumble (Voice chat protocol)'
        }
        self.OpenPortsList = []

        self.ScanTypeChoice = ScanType
        self.URLorIP =  URLorIP
        self.InputRange = InputRange

        self.Start()

    def Start(self):

        self.ScanTypeInputCheck()
        self.HostToScan()
        self.StartScan()
        self.JsonOutput()

    def ScanTypeInputCheck(self):
        if self.ScanTypeChoice == 'Common':
            self.CommonRange = True

        if self.ScanTypeChoice == 'Full':
            self.CommonRange = False
            self.PortRangeInt = 65535

        if self.ScanTypeChoice == 'Custom':
            self.CommonRange = False
            self.PortRangeInt = self.InputRange


            #self.PortRangeInt = input(f'Please Enter Max Range: ')
            #if not self.PortRangeInt.isdigit():
            #    print(f'Port number must be a single number for example if you set 100 as the max range this program will scan ports 0 through 100')
            #    self.ScanTypeInputs()


    def HostToScan(self):
        global host
        self.host = self.URLorIP

    def Scan(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((self.host, port))
            self.OpenPortsList.append(port)
        except:
            pass
        finally:
            s.close()

    def StartScan(self):
        threads = []
        if self.CommonRange is True:
            for port in self.CommonPortsDict.keys():
                thread = t.Thread(target=self.Scan, args=(port,))
                thread.start()
                threads.append(thread)
        else:
            for port in range(0, int(self.PortRangeInt)):
                thread = t.Thread(target=self.Scan, args=(port,))
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join()
    def JsonOutput(self):
        self.PortsOutputDict = {}
        for port in self.OpenPortsList:
            if port in self.CommonPortsDict.keys():
                self.PortsOutputDict[port] = self.CommonPortsDict.get(port)
            else:
                self.PortsOutputDict[port] = "is open its use can not be identified by this program"

        return self.PortsOutputDict



class DownloadResults:

    def __init__(self, JsonData, URLorIP, FileType):

        if FileType == 'txt':
            self.DownloadResultsTXT(JsonData=JsonData,URLorIP=URLorIP)
        else:
            print('Not Yet Added CSV Download')

    def DownloadResultsTXT(self, JsonData, URLorIP):


        self.Date = datetime.now()
        Date = self.Date

        MainDir = os.getcwd()

        print(MainDir)

        if not os.path.exists('Temp'):
            os.mkdir('Temp')
            os.chdir('Temp')
        else:
            os.chdir('Temp')


        FileName = self.StorageFileName = (f'{URLorIP} {Date.month}-{Date.day}-{Date.year} ({Date.strftime("%I")}_{Date.strftime("%M")}_{Date.strftime("%S")} {Date.strftime("%p")})')
        with open(f"{FileName}.txt", 'x') as File:
            File.write(f"{FileName} - Port Scan Results")
            File.write('\n\n')
            File.write('Service  Port')
            File.write('\n')

        for Service in JsonData.keys():
            for Port in JsonData.values():
                with open(f"{URLorIP}.txt", "a") as File:
                    File.write(f"{Service}  {Port}")
                    File.write('\n')

        os.chdir(MainDir)


        if sys.platform.startswith("linux"):
            self.FilePathForDownload = f"{MainDir}/Temp/{FileName}.txt"
            print(self.FilePathForDownload)
            return self.FilePathForDownload
        elif sys.platform.startswith("win"):
            self.FilePathForDownload = f"{MainDir}\\Temp\\{FileName}.txt"
            print(self.FilePathForDownload)
            return self.FilePathForDownload





# Built on BirdScan 1.0.4
# Suite Edition
# A simple Python port scanner

# Not A Bird
# CEO of Bird Inc.
