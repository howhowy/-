import speciesClass
import requests
from bs4 import BeautifulSoup
import re

allKingdom = []
allSpecies = []
tempSpecies = speciesClass.species()


for page in range(3) : #爬三頁    
    url = 'http://taibif.tw/zh/theme_species/iucn/endangered?page=' + str(page)
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    onePageSoup = soup.select('li.has-occurrence a.species')      #網站內物種連結
    #print (len(onePageSoup))
    
    for subPage in onePageSoup :
        img = []
        subPageURL = subPage['href'] #抓取新網頁
        subPageRes = requests.get(subPageURL)
        subPageSoup = BeautifulSoup(subPageRes.text,'html.parser')
        
        temp = subPageSoup.select('ul.section-ancestors li')      #分類整包
        if len(temp) != 0 :
              pagekingdomName = subPageSoup.select('ul.section-ancestors li')[0].text #子頁面所屬界 (抓取網頁"界"名稱
              pagedivisionName = subPageSoup.select('ul.section-ancestors li')[1].text  #子頁面所屬門 (抓取網頁"門"名稱
              
        temp = subPageSoup.select('ul.section-ancestors li.indent-6 a span')
        if len(temp) != 0 :
              pageSpeciesScientificName = subPageSoup.select('ul.section-ancestors li.indent-6 a span')[0].text  #子頁面所屬種學名 (抓取網頁"種"名稱

        temp = subPageSoup.select('div.img-container a')    #抓圖片
        if len(temp) != 0 :
              for m in temp :
                  img.append(m['href'])
                  
        [s.extract() for s in subPageSoup('a')]#去除pageSpeciesCommonName學名+年分(?)
        temp = subPageSoup.select('ul.section-ancestors li.indent-6')
        if len(temp) != 0 :
              pageSpeciesCommonName = subPageSoup.select('ul.section-ancestors li.indent-6')[0].text  #子頁面所屬種學名+年分(?)+俗名
              
        temp = subPageSoup.select('div.data-content p.taxon-distribution')
        if len(temp) != 0 :
              distribution = subPageSoup.select('div.data-content p.taxon-distribution')[0].text #抓分布
              
        temp = subPageSoup.select('div.data-content p.taxon-habitat')
        if len(temp) != 0 :
              ecology = subPageSoup.select('div.data-content p.taxon-habitat')[0].text #抓生態
              
        tempSpecies = speciesClass.species(pagekingdomName , pagedivisionName , pageSpeciesScientificName , pageSpeciesCommonName , img , distribution , ecology)
        allSpecies.append(tempSpecies)
              
for eachSpecies in range(len(allSpecies)) :
      kingdomExist = False
      kingdomExistNum = 0
      for eachKingdom in range(len(allKingdom)) :
            if allSpecies[eachSpecies].getKingdomName() == allKingdom[eachKingdom][0] :
                  kingdomExist = True
                  kingdomExistNum = eachKingdom
      if kingdomExist :
          DivisionExist = False
          DivisionExistNum = 0
          for eachDivision in range(len(allKingdom[kingdomExistNum][1])):
                  if allSpecies[eachSpecies].getDivisionName() == allKingdom[kingdomExistNum][1][eachDivision][0] :
                      DivisionExist=True
                      DivisionExistNum=eachDivision
          if DivisionExist :
              allKingdom[ kingdomExistNum ][1][DivisionExistNum][1].append( allSpecies[eachSpecies] )
          else :
              allKingdom[ kingdomExistNum ][ 1 ].append( [] )
              allKingdom[ kingdomExistNum ][ 1 ][ len(allKingdom[ kingdomExistNum ][ 1 ])-1 ].append( allSpecies[eachSpecies].getDivisionName() )
              allKingdom[ kingdomExistNum ][ 1 ][ len(allKingdom[ kingdomExistNum ][ 1 ])-1 ].append( [] )
              allKingdom[ kingdomExistNum ][ 1 ][ len(allKingdom[ kingdomExistNum ][ 1 ])-1 ][ 1 ].append( allSpecies[eachSpecies] )
      else :
            allKingdom.append([])
            allKingdom[ len(allKingdom)-1 ].append( allSpecies[eachSpecies].getKingdomName() )
            allKingdom[ len(allKingdom)-1 ].append( [] )
            allKingdom[ len(allKingdom)-1 ][ 1 ].append([])
            allKingdom[ len(allKingdom)-1 ][ 1 ][ len(allKingdom[ len(allKingdom)-1 ][ 1 ])-1 ].append( allSpecies[eachSpecies].getDivisionName() )
            allKingdom[ len(allKingdom)-1 ][ 1 ][ len(allKingdom[ len(allKingdom)-1 ][ 1 ])-1 ].append( [] )
            allKingdom[ len(allKingdom)-1 ][ 1 ][ len(allKingdom[ len(allKingdom)-1 ][ 1 ])-1 ][ 1 ].append( allSpecies[eachSpecies] )


f = open('Format.json','w',encoding = 'UTF-8')
f.write('[\n')
for l in range( len(allKingdom) ) :
      f.write('{\n')
      f.write('"界名": ')
      f.write('\"')
      f.write(allKingdom[l][1][0][1][0].getKingdomName())
      f.write('\",\n')
      f.write('"界成員": ')
      f.write('[\n')
      for m in range( len(allKingdom[l][1]) ) :
            f.write('{\n')
            f.write('\"門名\": ')
            f.write('\"')
            f.write(allKingdom[l][1][m][1][0].getDivisionName())
            f.write('\",\n')
            f.write('"門成員": ')
            f.write('[\n')

            for n in range( len(allKingdom[l][1][m][1]) ) :
                  f.write('{\n')
                  f.write('"學名": ')
                  f.write('\"')
                  f.write(allKingdom[l][1][m][1][n].getSpeciesInformationSN())
                  f.write('\",\n')
                  f.write('"俗名": ')
                  f.write('\"')
                  f.write(allKingdom[l][1][m][1][n].getSpeciesInformationCN())
                  f.write('\",\n')

                  ima = allKingdom[l][1][m][1][n].getSpeciesInformationIM()
                  f.write('"圖片": ')
                  f.write('[\n')
                  for p in range(len(ima)) :
                        f.write('\"')
                        f.write(ima[p])
                        f.write('\"')
                        if(p != (len(ima)-1)) :
                              f.write(',\n')
                  f.write('],\n')
                  
                  f.write('"分布": ')
                  f.write('\"')
                  Di = []
                  Di = allKingdom[l][1][m][1][n].getSpeciesInformationDI()
                  Di = Di.replace('\r','')
                  Di = Di.replace('\n','')
                  f.write(Di)
                  f.write('\",\n')
                  f.write('"生態": ')
                  f.write('\"')
                  Ec = []
                  Ec = allKingdom[l][1][m][1][n].getSpeciesInformationEC()
                  Ec = Ec.replace('\r','')
                  Ec = Ec.replace('\n','')
                  f.write(Ec)
                  f.write('\"\n')
                  f.write('}\n')
                  if(n != (len(allKingdom[l][1][m][1])-1)) :
                        f.write(',\n')

            f.write(']\n')
            f.write('}\n')
            if(m != (len(allKingdom[l][1])-1)) :
                  f.write(',\n')
            
      f.write(']\n')
      f.write('}\n')
      if(l != (len(allKingdom)-1)) :
                  f.write(',\n')

f.write(']')

f.close()
