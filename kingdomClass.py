import divisionClass
class kingdom :
    def __init__(self,kN='Nodata'):
        self.kingdomName = kN
        self.belongDivision = []
    def getkingdomName(self):
        return self.kingdomName
    def setBelongDivision(self,dC=divisionClass.division()):
        self.belongDivision.append( dC )
    def getBelongDivision(self):
        return self.belongDivision
