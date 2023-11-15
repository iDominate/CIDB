from typing import Union, Dict
import constants
StrOrInt = Union[str, int]
class FilterFactory(object):
    comName: str
    comState: StrOrInt
    CategoryID: StrOrInt
    RegisterationNumber: StrOrInt 
    comDistrict: StrOrInt
    comSpecID: StrOrInt
    type: StrOrInt
    validity: StrOrInt
    pageSize: int
    currenctPage: int
    grade: StrOrInt
    
    filterData = {
        'comName': '', #Contactor Name
        'ComState': '', #State ID
        'ComCategoryID': '', #Category ID
        'SSMNo': '', #Registration Number
        'ComDistrict': '', #District
        'ComSpecID': '', #Specification ID
        'ComGradeID': '', #Grade ID
        'seltype': '', #Type
        'selvalidity': '', #Validity
        'hdnpagesize': 10, #Page Size (this one overrides the below selpagesize)
        'hdnctpage': 1, #Current Page
        'hdntotpage': 12967,
        'hdnsortcol': 'ComName',
        'hdnsortdir': 0,
        'hdntotalrecs': 129669,
        'hdnexportopts': 0,
        'txtgoto': '', #Go to
        'selpagesize': 1000 #Page Size
        }
    def setName(self, name: str = ''):
        self.comName = name
        return self
    
    def setState(self, state: StrOrInt = ''):
        self.comState = state
        return self
    
    def setCategorID(self, categoryID: StrOrInt = ''):
        self.CategoryID = categoryID
        return self
    
    def setRegistrationNumber(self, registrationNumber: StrOrInt = ''):
        self.RegisterationNumber = registrationNumber
        return self
    
    def setDistrict(self, district: StrOrInt = ''):
        self.comDistrict = district
        return self
    
    def setSpecifiactionID(self, specID: StrOrInt = ''):
        self.comSpecID = specID
        return self
    
    def setType(self, type: int = constants.LOCAL):
        self.type = type
        return self
    
    def setValidity(self, validity: int = constants.VA_VALID):
        self.validity = validity
        return self
    
    def setPageSize(self, pageSize: int = 10):
        self.pageSize = pageSize
        return self
    
    def setPage(self, page: int = 1):
        self.currenctPage = page
        return self
    
    def setGrade(self, grade: StrOrInt = ''):
        self.grade = grade
        return self
    
    def build(self) -> Dict[str, StrOrInt]:
        self.filterData['comName'] = self.comName
        self.filterData['ComState'] = self.comState
        self.filterData['ComDistrict'] = self.comDistrict
        self.filterData['ComCategoryID'] = self.CategoryID
        self.filterData['SSMNo'] = self.RegisterationNumber
        self.filterData['ComGradeID'] = self.grade
        self.filterData['ComSpecID'] = self.comSpecID
        self.filterData['seltype'] = self.type
        self.filterData['selvalidity'] = self.validity
        self.filterData['hdnpagesize'] = self.pageSize
        self.filterData['hdnctpage'] = self.currenctPage
        return self.filterData