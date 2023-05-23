import requests
import base64
from datetime import datetime
from datetime import timedelta
from balDataTypes import *
import json
from types import SimpleNamespace
from dateutil import parser

def call(url: str, rootObj: Root):
    request = json_encode(rootObj.__dict__)
    request_b64 = base64.b64encode(request.encode())
    headers = {'Content-Type': 'text/plain; charset=UTF-8'}
    response = requests.post(url, request_b64, headers=headers)
    result=response.json()
    return result

#{"id":"QID: -|SID: -|requestID: 12b540dfa6","method":"findCityByPostalCode","params":[{"postalCode":"4133"}],"jsonrpc":"2.0"}
def findCityByPostalCode(postalCode: str):
#https://www.baloise.ch/mybaloise-api/public/api/householdoffering/v1/address/lookup
    postalCodeObj = PostalCode(postalCode)
    params = [postalCodeObj]
    rootObj = Root("", "findCityByPostalCode", params, "2.0")
    rootObj.params = [postalCodeObj]
    result = call("https://www.baloise.ch/mybaloise-api/public/api/householdoffering/v1/address/lookup", rootObj)
    primaryAddress = PrimaryAddress.from_postalCodeFindResult(result.get('result')[0], postalCode)
    print(primaryAddress.__dict__)
    return primaryAddress

#{"id":"QID: -|SID: -|requestID: 1c614955a8","method":"calculateSumInsured","params":[{"numOfRooms":"4.5","numOfChildren":"2","stdOfFurniture":"normal","numOfAdults":"2"}],"jsonrpc":"2.0"}
def getSumInsured(numOfRooms: str, numOfChildren: str, numOfAdults: str):
    #https://www.baloise.ch/mybaloise-api/public/api/householdoffering/v1/quote/quote
    insuranceSumRelevantData = InsuranceSumRelevantData(numOfRooms, numOfChildren, "normal", numOfAdults)
    params = [insuranceSumRelevantData]
    rootObj = Root("", "calculateSumInsured", params, "2.0")
    result = call("https://www.baloise.ch/mybaloise-api/public/api/householdoffering/v1/quote/quote", rootObj)
    sumInsuredBasisProperty = SumInsuredBasisProperty.from_calculateSumInsuredResult(result.get('result'))
    print(sumInsuredBasisProperty.__dict__)
    return sumInsuredBasisProperty

def getHouseHold(numOfRooms: str, numOfChildren: str, numOfAdults: str) :
    sumInsuredBasisProperty = getSumInsured(numOfRooms=numOfRooms, numOfChildren=numOfChildren, numOfAdults=numOfAdults)
    household = Household(numOfAdults, numOfChildren, "normal", numOfRooms, False, sumInsuredBasisProperty)
    return household

def getCoverables(primaryAddress: PrimaryAddress, numOfRooms: str, numOfChildren: str, numOfAdults: str):
    property = Property('multiple_family_dwelling', 'Rental', 'M')
    policyLocation = PolicyLocation.from_PrimaryAddress(primaryAddress=primaryAddress) 
    location = Location(property=property, policyLocation=policyLocation)
    household = getHouseHold(numOfAdults=numOfAdults, numOfChildren=numOfChildren, numOfRooms=numOfRooms)
    return Coverables(locations=[location], household=household)

def getLobData(primaryAddress: PrimaryAddress, numOfRooms: str, numOfChildren: str, numOfAdults: str):
    coverables = getCoverables(numOfAdults=numOfAdults, numOfChildren=numOfChildren, numOfRooms=numOfRooms, primaryAddress=primaryAddress)
    hhline = HHLine(householdOfferingPackage='HHHouseholdLiability1', coverables=coverables)
    lobData = LobData(hHLine=hhline)
    return lobData

def getAccountHolder(primaryAddress: PrimaryAddress, birthdate: datetime):
    dateOfBirth=DateOfBirth(year=birthdate.year,month=birthdate.month-1,day=birthdate.day)
    accountHolder = AccountHolder(subtype='Person',accountHolder=True, primaryAddress=primaryAddress, dateOfBirth=dateOfBirth, primaryLanguage="de") 
    return accountHolder

def getBaseData(primaryAddress: PrimaryAddress, birthdate: datetime):
    accountHolder = getAccountHolder(primaryAddress=primaryAddress, birthdate= birthdate)
    trackingCode = []
    tomorrow = datetime.now() + timedelta(days=1)
    periodStartDate = PeriodStartDate(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day)
    policyAddress = PolicyAddress.from_PrimaryAddress(primaryAddress)
    return BaseData(salespoint='portal', accountHolder=accountHolder, productCode='BaloiseDirectHaushalt', employeeMode=False, trackingCode=trackingCode, periodStartDate=periodStartDate, policyAddress=policyAddress)

def getParams(primaryAddress: PrimaryAddress, birthdate: datetime, numOfRooms: str, numOfChildren: str, numOfAdults: str):
    baseData = getBaseData(primaryAddress=primaryAddress, birthdate=birthdate)
    lobData = getLobData(primaryAddress=primaryAddress, numOfAdults=numOfAdults, numOfChildren=numOfChildren, numOfRooms=numOfRooms)
    return {"directPage" : "RiskRelevantData", "baseData" : baseData, "lobData" : lobData}

def quoteToPremiumMap(quote: OfferedQuote):
    if (quote.branchName == "X_HH_PH_001"):
        return {"s" : quote.premium.total.amount}
    elif (quote.branchName == "X_HH_PH_002"):
        return {"m" : quote.premium.total.amount}
    else:    
        return {"l" : quote.premium.total.amount}
    

def quotesToPremiumMap(*quotes: OfferedQuote) :
    premiumMap = map(quoteToPremiumMap, quotes[0])
    result = list(premiumMap)
    return result


def getHHKQuote(postalCode: str, numberOfAdults: str, numberOfChildren: str, numberOfRooms: str, birthdate: datetime ):
    primaryAddress = findCityByPostalCode(postalCode)

    params = [getParams(primaryAddress=primaryAddress,birthdate=birthdate, numOfAdults=numberOfAdults, numOfChildren=numberOfChildren, numOfRooms=numberOfRooms)]
    rootObj = Root('',method='createAndQuote', params=params, jsonrpc='2.0')
    print(json_encode(rootObj.__dict__))
    result = call("https://www.baloise.ch/mybaloise-api/public/api/householdoffering/v1/quote/quote", rootObj)
    print(result.get('result').get('quoteData'))
    offeredQuotesRoot = OQRoot.from_dict(result.get('result').get('quoteData'))
    offeredQuotes = offeredQuotesRoot.offeredQuotes
    premiums = quotesToPremiumMap(offeredQuotes)
    print(premiums)
    print("done.")
    return premiums

def main(args):
    request = args.get('request', args)
    print(type(args))
    request_json = json.loads(json.dumps(request), object_hook=lambda d: SimpleNamespace(**d))
    print(request_json)
    print(type(request_json))
    postalCode = request_json.QuoteRequest.postalCode
    numberOfRooms = request_json.QuoteRequest.numberOfRooms
    numberOfAdults = request_json.QuoteRequest.numberOfAdults
    numberOfChildren = request_json.QuoteRequest.numberOfChildren
    birthdate_str = request_json.QuoteRequest.birthdate
    birthdate = parser.isoparse(birthdate_str)
    premiums = getHHKQuote(postalCode=postalCode, numberOfAdults=numberOfAdults, numberOfChildren=numberOfChildren, numberOfRooms=numberOfRooms, birthdate=birthdate)
    return {"body": json_encode(premiums)}

