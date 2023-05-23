from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class PrimaryAddress:
    state: str
    city: str
    country: str
    postalCode: str

    @staticmethod
    def from_dict(obj: Any) -> 'PrimaryAddress':
        _state = str(obj.get("state"))
        _city = str(obj.get("city"))
        _country = str(obj.get("country"))
        _postalCode = str(obj.get("postalCode"))
        return PrimaryAddress(_state, _city, _country, _postalCode)
    
    @staticmethod
    def from_postalCodeFindResult(obj: Any, postalCode: str) -> 'PrimaryAddress':
        _state = str(obj.get("canton"))
        _city = str(obj.get("cityName"))
        _country = "CH"
        _postalCode = postalCode
        return PrimaryAddress(_state, _city, _country, _postalCode)
    
@dataclass
class DateOfBirth:
    year: int
    month: int
    day: int

    @staticmethod
    def from_dict(obj: Any) -> 'DateOfBirth':
        _year = int(obj.get("year"))
        _month = int(obj.get("month"))
        _day = int(obj.get("day"))
        return DateOfBirth(_year, _month, _day)

@dataclass
class AccountHolder:
    subtype: str
    accountHolder: bool
    primaryAddress: PrimaryAddress
    dateOfBirth: DateOfBirth
    primaryLanguage: str

    @staticmethod
    def from_dict(obj: Any) -> 'AccountHolder':
        _subtype = str(obj.get("subtype"))
        _accountHolder = True
        _primaryAddress = PrimaryAddress.from_dict(obj.get("primaryAddress"))
        _dateOfBirth = DateOfBirth.from_dict(obj.get("dateOfBirth"))
        _primaryLanguage = str(obj.get("primaryLanguage"))
        return AccountHolder(_subtype, _accountHolder, _primaryAddress, _dateOfBirth, _primaryLanguage)


@dataclass
class SumInsuredBasisProperty:
    amount: int

    @staticmethod
    def from_dict(obj: Any) -> 'SumInsuredBasisProperty':
        _amount = int(obj.get("amount"))
        return SumInsuredBasisProperty(_amount)
    
    @staticmethod
    def from_calculateSumInsuredResult(obj: Any):
        _amount = int(obj.get("amount"))
        return(SumInsuredBasisProperty(_amount))

@dataclass
class Household:
    numberOfAdultsAndTeenagers: str
    numberOfChildrenUntil14: str
    stdOfFurniture: str
    numOfRooms: str
    insuranceSumIndividual: bool
    sumInsuredBasisProperty: SumInsuredBasisProperty

    @staticmethod
    def from_dict(obj: Any) -> 'Household':
        _numberOfAdultsAndTeenagers = str(obj.get("numberOfAdultsAndTeenagers"))
        _numberOfChildrenUntil14 = str(obj.get("numberOfChildrenUntil14"))
        _stdOfFurniture = str(obj.get("stdOfFurniture"))
        _numOfRooms = str(obj.get("numOfRooms"))
        _sumInsuredBasisProperty = SumInsuredBasisProperty.from_dict(obj.get("sumInsuredBasisProperty"))
        return Household(_numberOfAdultsAndTeenagers, _numberOfChildrenUntil14, _stdOfFurniture, _numOfRooms, [] , _sumInsuredBasisProperty)
         
@dataclass
class PolicyLocation:
    state: str
    city: str
    country: str
    postalCode: str

    @staticmethod
    def from_dict(obj: Any) -> 'PolicyLocation':
        _state = str(obj.get("state"))
        _city = str(obj.get("city"))
        _country = str(obj.get("country"))
        _postalCode = str(obj.get("postalCode"))
        return PolicyLocation(_state, _city, _country, _postalCode)
    
    @staticmethod
    def from_PrimaryAddress(primaryAddress):
        return PolicyLocation(primaryAddress.state, primaryAddress.city, primaryAddress.country, primaryAddress.postalCode)


@dataclass
class Property:
    objectType: str
    ownershipType: str
    constructionType: str

    @staticmethod
    def from_dict(obj: Any) -> 'Property':
        _objectType = str(obj.get("objectType"))
        _ownershipType = str(obj.get("ownershipType"))
        _constructionType = str(obj.get("constructionType"))
        return Property(_objectType, _ownershipType, _constructionType)
    
@dataclass
class Location:
    property: Property
    policyLocation: PolicyLocation

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        _property = Property.from_dict(obj.get("property"))
        _policyLocation = PolicyLocation.from_dict(obj.get("policyLocation"))
        return Location(_property, _policyLocation)
       
@dataclass
class Coverables:
    locations: List[Location]
    household: Household

    @staticmethod
    def from_dict(obj: Any) -> 'Coverables':
        _locations = [Location.from_dict(y) for y in obj.get("locations")]
        _household = Household.from_dict(obj.get("household"))
        return Coverables(_locations, _household)

@dataclass
class HHLine:
    householdOfferingPackage: str
    coverables: Coverables

    @staticmethod
    def from_dict(obj: Any) -> 'HHLine':
        _householdOfferingPackage = str(obj.get("householdOfferingPackage"))
        _coverables = Coverables.from_dict(obj.get("coverables"))
        return HHLine(_householdOfferingPackage, _coverables)



@dataclass
class LobData:
    hHLine: HHLine

    @staticmethod
    def from_dict(obj: Any) -> 'LobData':
        _hHLine = HHLine.from_dict(obj.get("hHLine"))
        return LobData(_hHLine)
    
@dataclass
class PeriodStartDate:
    year: int
    month: int
    day: int

    @staticmethod
    def from_dict(obj: Any) -> 'PeriodStartDate':
        _year = int(obj.get("year"))
        _month = int(obj.get("month"))
        _day = int(obj.get("day"))
        return PeriodStartDate(_year, _month, _day)

@dataclass
class PolicyAddress:
    state: str
    city: str
    country: str
    postalCode: str

    @staticmethod
    def from_dict(obj: Any) -> 'PolicyAddress':
        _state = str(obj.get("state"))
        _city = str(obj.get("city"))
        _country = str(obj.get("country"))
        _postalCode = str(obj.get("postalCode"))
        return PolicyAddress(_state, _city, _country, _postalCode)
    
    @staticmethod
    def from_PrimaryAddress(primaryAddress):
        return PolicyAddress(primaryAddress.state, primaryAddress.city, primaryAddress.country, primaryAddress.postalCode)

@dataclass
class BaseData:
    salespoint: str
    accountHolder: AccountHolder
    productCode: str
    employeeMode: bool
    trackingCode: List[object]
    periodStartDate: PeriodStartDate
    policyAddress: PolicyAddress

    @staticmethod
    def from_dict(obj: Any) -> 'BaseData':
        _salespoint = str(obj.get("salespoint"))
        _accountHolder = AccountHolder.from_dict(obj.get("accountHolder"))
        _productCode = str(obj.get("productCode"))
        _employeeMode = False
        _periodStartDate = PeriodStartDate.from_dict(obj.get("periodStartDate"))
        _policyAddress = PolicyAddress.from_dict(obj.get("policyAddress"))
        return BaseData(_salespoint, _accountHolder, _productCode, _employeeMode, [], _periodStartDate, _policyAddress)


@dataclass
class Param:
    directPage: str
    baseData: BaseData
    lobData: LobData

    @staticmethod
    def from_dict(obj: Any) -> 'Param':
        _directPage = str(obj.get("directPage"))
        _baseData = BaseData.from_dict(obj.get("baseData"))
        _lobData = LobData.from_dict(obj.get("lobData"))
        return Param(_directPage, _baseData, _lobData)

@dataclass
class PostalCode:
    postalCode: str

    @staticmethod
    def from_dict(obj: Any) -> 'Param':
        _postalCode = str(obj.get("postalCode"))
        return Param(_postalCode)
    
@dataclass
class InsuranceSumRelevantData:
    numOfRooms: str
    numOfChildren: str
    stdOfFurniture: str
    numOfAdults: str

@dataclass
class Root:
    id: str
    method: str
    params: List[Param]
    jsonrpc: str

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _id = str(obj.get("id"))
        _method = str(obj.get("method"))
        _params = [Param.from_dict(y) for y in obj.get("params")]
        _jsonrpc = str(obj.get("jsonrpc"))
        return Root(_id, _method, _params, _jsonrpc)
    
    @staticmethod
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
@dataclass
class MonthlyPremium:
    currency: str
    amount: float

    @staticmethod
    def from_dict(obj: Any) -> 'MonthlyPremium':
        _currency = str(obj.get("currency"))
        _amount = float(obj.get("amount"))
        return MonthlyPremium(_currency, _amount)

@dataclass
class Taxes:
    currency: str
    amount: float

    @staticmethod
    def from_dict(obj: Any) -> 'Taxes':
        _currency = str(obj.get("currency"))
        _amount = float(obj.get("amount"))
        return Taxes(_currency, _amount)

@dataclass
class Total:
    currency: str
    amount: float

    @staticmethod
    def from_dict(obj: Any) -> 'Total':
        _currency = str(obj.get("currency"))
        _amount = float(obj.get("amount"))
        return Total(_currency, _amount)

@dataclass
class TotalBeforeTaxes:
    currency: str
    amount: float

    @staticmethod
    def from_dict(obj: Any) -> 'TotalBeforeTaxes':
        _currency = str(obj.get("currency"))
        _amount = float(obj.get("amount"))
        return TotalBeforeTaxes(_currency, _amount)
        
@dataclass
class Premium:
    total: Total
    termMonths: int
    totalBeforeTaxes: TotalBeforeTaxes
    monthlyPremium: MonthlyPremium
    taxes: Taxes

    @staticmethod
    def from_dict(obj: Any) -> 'Premium':
        _total = Total.from_dict(obj.get("total"))
        _termMonths = int(obj.get("termMonths"))
        _totalBeforeTaxes = TotalBeforeTaxes.from_dict(obj.get("totalBeforeTaxes"))
        _monthlyPremium = MonthlyPremium.from_dict(obj.get("monthlyPremium"))
        _taxes = Taxes.from_dict(obj.get("taxes"))
        return Premium(_total, _termMonths, _totalBeforeTaxes, _monthlyPremium, _taxes)
    
@dataclass
class OfferedQuote:
    status: str
    premium: Premium
    publicID: str
    branchCode: str
    branchName: str
    encryptedDocId: str
    isCustomized: bool
    isCustom: bool

    @staticmethod
    def from_dict(obj: Any) -> 'OfferedQuote':
        _status = str(obj.get("status"))
        _premium = Premium.from_dict(obj.get("premium"))
        _publicID = str(obj.get("publicID"))
        _branchCode = str(obj.get("branchCode"))
        _branchName = str(obj.get("branchName"))
        _encryptedDocId = str(obj.get("encryptedDocId"))
        _isCustomized = bool(obj.get("isCustomized"))
        _isCustom = bool(obj.get("isCustom"))
        return OfferedQuote(_status, _premium, _publicID, _branchCode, _branchName, _encryptedDocId, _isCustomized, _isCustom)

@dataclass
class OQRoot:
    offeredQuotes: List[OfferedQuote]

    @staticmethod
    def from_dict(obj: Any) -> 'OQRoot':
        _offeredQuotes = [OfferedQuote.from_dict(y) for y in obj.get("offeredQuotes")]
        return OQRoot(_offeredQuotes)

class RQuotes:
    sPremium: int
    mPremium: int
    lPremium: int

# extend the json.JSONEncoder class
class JSONEncoder(json.JSONEncoder):

    # overload method default
    def default(self, obj):

        # Match all the types you want to handle in your converter
        if isinstance(obj, PostalCode):
            return {"postalCode": obj.postalCode}
        elif isinstance(obj, InsuranceSumRelevantData):
            return {"numOfRooms": str(obj.numOfRooms), "numOfChildren": str(obj.numOfChildren), "stdOfFurniture": str(obj.stdOfFurniture), "numOfAdults":str(obj.numOfAdults)}
        elif isinstance(obj, BaseData):
            return {"salespoint": obj.salespoint, "accountHolder": obj.accountHolder, "productCode": obj.productCode, "employeeMode": obj.employeeMode, "periodStartDate": obj.periodStartDate, "policyAddress": obj.policyAddress}
        elif (isinstance(obj, AccountHolder)):
            return {"subtype": obj.subtype, "accountHolder": obj.accountHolder, "primaryAddress": obj.primaryAddress, "dateOfBirth": obj.dateOfBirth, "primaryLanguage" : obj.primaryLanguage}
        elif (isinstance(obj, PrimaryAddress)|isinstance(obj, PolicyAddress)|isinstance(obj, PolicyLocation)):
            return {"city": obj.city, "country": obj.country, "postalCode": obj.postalCode, "state": obj.state}
        elif (isinstance(obj, DateOfBirth)|isinstance(obj, PeriodStartDate)):
            return {"year": obj.year, "month": obj.month, "day": obj.day}
        elif (isinstance(obj, LobData)):
            return {"hHLine":obj.hHLine}
        elif (isinstance(obj, HHLine)):
            return {"coverables":obj.coverables, "householdOfferingPackage":obj.householdOfferingPackage}
        elif (isinstance(obj, Coverables)):
            return {"household":obj.household, "locations":obj.locations}
        elif (isinstance(obj,Household)):
            return {"insuranceSumIndividual":obj.insuranceSumIndividual, "numberOfAdultsAndTeenagers": str(obj.numberOfAdultsAndTeenagers), "numberOfChildrenUntil14": str(obj.numberOfChildrenUntil14), "numOfRooms": str(obj.numOfRooms), 
                    "stdOfFurniture": obj.stdOfFurniture, "sumInsuredBasisProperty": obj.sumInsuredBasisProperty}
        elif (isinstance(obj, SumInsuredBasisProperty)):
            return {"amount": obj.amount}
        elif (isinstance(obj, Location)):
            return {"policyLocation": obj.policyLocation, "property": obj.property}
        elif (isinstance(obj, Property)):
            return {"constructionType": obj.constructionType, "objectType": obj.objectType, "ownershipType": obj.ownershipType}
        # Call the default method for other types
        return json.JSONEncoder.default(self, obj)

def json_encode(data):
    return JSONEncoder().encode(data)
# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)