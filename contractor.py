class Contractor(object):
    def __init__(self, no: str, name: str, grade: str, state: str,
                 district: str, phoneNumber: str, fax: str, PRK: bool, SPKK: bool, STP: str, expiryDate: str = ''):
        self.no = no
        self.name = name
        self.grade = grade
        self.state = state
        self.district = district
        self.phoneNumber = phoneNumber
        self.fax= fax
        self.PRK = PRK
        self.SPKK = SPKK
        self.STP = STP
        self.expiryDate = expiryDate
        
    def set_expiryDate(self, date: str):
            self.expiryDate = date