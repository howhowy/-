class species :
    def __init__(self,kN='Nodata',diN='Nodata',sN='Nodata',cN='Nodata',img=[],dtb='Nodata',ecl='Nodata'):
        self.kingdomName = kN
        self.divisionName = diN
        self.scientificName = sN
        self.commonName = cN
        self.image = img
        self.distribution = dtb
        self.ecology = ecl
        
    def getKingdomName(self):
        return self.kingdomName
    
    def getDivisionName(self):
        return self.divisionName
    
    def getSpeciesInformationSN(self):
        return self.scientificName

    def getSpeciesInformationCN(self):
        return self.commonName

    def getSpeciesInformationIM(self):
        return self.image

    def getSpeciesInformationDI(self):
        return self.distribution
    
    def getSpeciesInformationEC(self):
        return self.ecology
    
        
        
        
    
