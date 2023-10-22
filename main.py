from fastapi import *
from BirdTools import BirdGlanceSuiteEdition as BirdGlance
from BirdTools import BirdScanSuiteEdition as BirdScan
import json
from pydantic import *


app = FastAPI()



@app.get("/")
async def root():

    return {'Hello World'}

@app.post("/BirdGlance")
async def BirdGlancePost(UserInput: Request):

    body = await UserInput.body()
    Data = body.decode("utf-8")

    JsonData = json.loads(Data)

    URL = JsonData.get("URL")

    print(f'URL Received: {URL}')

    StartBirdGlance = BirdGlance.Start(URL=URL)

    JsonDict = StartBirdGlance.JsonOutput()

    return JsonDict

@app.post("/BirdScan")
async def BirdScanPost(UserInput: Request):

    body = await UserInput.body()

    Data = body.decode("utf-8")

    JsonData = json.loads(Data)

    print(f'Data Received: {JsonData}')

    URLorIP = JsonData.get("URLorIP")

    ScanTypeChoice = JsonData.get("ScanType")

    if ScanTypeChoice == "Custom":

        InputRange = JsonData.get("InputRange")
        StartScan = BirdScan.PortScaner(URLorIP=URLorIP, ScanType=ScanTypeChoice, InputRange=InputRange)
        JsonDict = StartScan.JsonOutput()
        return JsonDict

    else:
        StartScan = BirdScan.PortScaner(URLorIP=URLorIP, ScanType=ScanTypeChoice)
        JsonDict = StartScan.JsonOutput()
        return JsonDict
