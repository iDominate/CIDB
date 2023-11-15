from bs4 import BeautifulSoup
from requests import get, post
from contractor import Contractor
from concurrent import futures
import constants
import filterFactory
from os import _exit
from typing import List, Dict
from time import time
import csv

url = 'https://cims.cidb.gov.my/smis/regcontractor/reglocalsearchcontractor.vbhtml?language=2'
data = {
'comName': 'hello', #Contactor Name
'ComState': '', #State ID
'ComCategoryID': '', #Category ID
'SSMNo': '', #Registration Number
'ComDistrict': '', #District
'ComSpecID': '', #Specification ID
'ComGradeID': '', #Grade ID
'seltype': constants.FOREIGN, #Type
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

response = post(url, data=data)

executor = futures.ThreadPoolExecutor(max_workers=25)


contractors: List[Contractor] = []
expiryUrls: List[str] = []
expiryDates: List[str] = []

def get_soup(url: str, data: Dict[str, str]) -> BeautifulSoup:
    data = filterFactory.FilterFactory().filterData
    response = post(url, data=data)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup
    
def get_all_contractors(soup: BeautifulSoup) -> None:
    rows = soup.find_all('table')[2].find('table', class_='f-14').tbody.find_all('tr')
    if len(rows) == 0:
        print('No table found for the entry make sure the paramters are given to the correct method, happened with me :(')
        exit(1)
    for row in rows:
        contractor = row.find_all('td')
        no = contractor[0].text #NO
        cName = contractor[1].text #ContactorName
        grade = contractor[2].text #Grade
        state = contractor[3].text #State
        district = contractor[4].text #District
        phone = contractor[5].text #phoneNumber
        fax =contractor[6].text #faxNumber #Could be Empty
        if fax == '':
            fax = 'NO FAX'
        prk = contractor[7].text #PRK
        spkk = contractor[8].text #SPKK #Could be Empty
        if spkk == '':
            spkk = 'NO SPKK'
        stp = contractor[9].text #STP #Could be empty
        if stp == '':
            stp = 'NO STP'
        Id = contractor[10].a.attrs['data-flag']
        expiryUrls.append(f'https://cims.cidb.gov.my/smis/regcontractor/reglocalsearch_view.vbhtml?search=P&comSSMNo={Id}')
        contractor = Contractor(no=no, name=cName, grade=grade, state=state, district=district, phoneNumber=phone, fax=fax, PRK=prk, SPKK=spkk, STP=stp)
        contractors.append(contractor)



def get_expiry_date(expiryUrl: str) -> str:
    response = get(expiryUrl)
    viewSoup = BeautifulSoup(response.text, 'lxml')
    expiryDate = viewSoup.find('table', class_='f-14').find_all('tr')[7].find_all('th')[1].text.strip()
    if expiryDate == '':
        expiryDate = 'No expiry date'
    return expiryDate

def store_in_csv_file(contractors: List[Contractor]) -> None:
    filename: str = f'contractors_{time()}.csv'
    with open(filename, 'w') as csvfile:
        csvWriter = csv.writer(csvfile)
        csvWriter.writerow(['NO.', 'NAMA KONTRAKTOR', 'Gred', 'NEGERI', 'DERAH', 'NO.TELEFON', 'NO.FAKS', 'PPK', 'SPKK', 'STB', 'EXPIRY DATE'])
        for contractor in contractors:
            csvWriter.writerow([contractor.no, contractor.name, contractor.grade,
                                contractor.state, contractor.district, contractor.phoneNumber,
                                contractor.fax, contractor.PRK, contractor.SPKK, contractor.STP, contractor.expiryDate])
    return 'Success'

    
if __name__ == '__main__':
    data = filterFactory.FilterFactory()
    data.setGrade()
    data.setName()
    data.setRegistrationNumber()
    data.setDistrict()
    data.setCategorID()
    data.setType()
    data.setPageSize(1000)
    data.setPage()
    data.setValidity()
    data.setSpecifiactionID()
    data.setState()
    
    data = data.build()
    soup = get_soup(url, data)
    get_all_contractors(soup)
    
    with futures.ThreadPoolExecutor() as executor:
        for i in executor.map(get_expiry_date, expiryUrls):
            expiryDates.append(i)
    for i in range(len(contractors)):
        name = contractors[i].name
        expiryDate = expiryDates[i]
        #print(f"Setting {name} to Date: {expiryDate}")
        contractors[i].set_expiryDate(expiryDates[i])
    
    print(store_in_csv_file(contractors))


    