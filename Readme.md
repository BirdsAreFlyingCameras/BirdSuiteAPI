# BirdSuiteAPI

Version Number: 0.1.1

About:

 BirdSuiteAPI brings together my best OSINT scripts, all fine-tuned to work smoothly with FastAPI. 
 My goal is to use this API to create a user-friendly front-end OSINT tool that's efficient and effective.

Libaries used:

- FastAPI,  
- json,  
- socket,  
- threading,  
- requests,  
- dns.resolver,  
- sys

OSINT scripts added:

- BirdGlance, 
- BirdScan

OSINT scripts to add:

- WebParse,  
- HistorianDNS,
- BirdBuster 

## Usage

### installation

1. Clone the repo

       git clone https://github.com/BirdsAreFlyingCameras/BirdSuiteAPI

2. CD into the repos directory 

       cd BirdSuiteAPI

3. Install python requirements

       pip install -r requirements.txt

### Usage

#### Starting the server

    uvicorn main:app --host 0.0.0.0 --port 8000

#### Sending Requests

#### Curl:

Not working at the moment I'm currently fixing this issue 
will be fixed soon.

#### Postman:

**BirdGlace Request**: 

Request Type: Post  

Headers: All

Request Body:

    {
    "URL": "www.google.com"
    }

Single Line Version:

    {"URL": "www.google.com"}


**BirdScan Requests**

Request Type: Post  

Headers: All


**Common Scan:**

Notes:

Common Scan will only can the most commonly used port numbers
luckily due to these ports being commonly used I was able to 
add the services in use on the particular port.

Request Body:

    {
    "URLorIP": "www.google.com",
    "ScanType": "Common"
    }

Single Line Version:

    {"URLorIP": "www.google.com", "ScanType": "Common"}



**Full Scan:**

Notes:

Full Scan as the name implies will scan all 65535 ports,
due to the sheer amount of request being sent out this 
can take a while depending on the host.

Request Body:

    {
    "URLorIP": "www.google.com",
    "ScanType": "Full"
    }

Single Line Version:

    {"URLorIP": "www.google.com", "ScanType": "Full"}
    

**Custom Scan:**

Notes: 

InputRange is the number of ports to scan so 100 means your 
scanning ports 0 through 100.

Request Body:

    {
    "URLorIP": "www.google.com",
    "ScanType": "Custom",
    "InputRange" 100
    }

Single Line Version:

    {"URLorIP": "www.google.com", "ScanType": "Custom", "InputRange" 100}

***Not A Bird | CEO of Bird Inc.***
