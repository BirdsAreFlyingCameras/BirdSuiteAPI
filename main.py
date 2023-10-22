from fastapi import *
from BirdTools import BirdGlanceSuiteEdition as BirdGlance
from BirdTools import BirdScanSuiteEdition as BirdScan
import json
from pydantic import *

from typing import *

app = FastAPI()

class BirdScanerInput(BaseModel):

    URLorIP: str
    ScanType: str
    InputRange: Optional[int] = None

    @root_validator(pre=True)

    def CheckInput(cls, JsonData):

        if JsonData.get("ScanType") not in ["Common", "Full", "Custom"]:
            raise ValueError("[ERROR] SCAN TYPE MUST BE ONE OF THESE Common, Full, or Custom [ERROR] ")

        if JsonData.get("ScanType") == "Custom" and JsonData.get("InputRange") is None:
            raise ValueError("[ERROR] SCAN TYPE CUSTOM MUST HAVE A RANGE [ERROR] ")

        if JsonData.get("ScanType") == "Custom" and JsonData.get("InputRange") is not int:
            raise ValueError("[ERROR] INPUT RANGE MUST BE INT [ERROR]")

        return JsonData

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
async def BirdScanPost(UserInput: BirdScanerInput):


    URLorIP = UserInput.URLorIP
    ScanTypeChoice = UserInput.ScanType

    if ScanTypeChoice == "Custom":
        InputRange = UserInput.InputRange
        StartScan = BirdScan.PortScaner(URLorIP=URLorIP, ScanType=ScanTypeChoice, InputRange=InputRange)
        JsonDict = StartScan.JsonOutput()
        return JsonDict

    else:
        StartScan = BirdScan.PortScaner(URLorIP=URLorIP, ScanType=ScanTypeChoice)
        JsonDict = StartScan.JsonOutput()
        return JsonDict
