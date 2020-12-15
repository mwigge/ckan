import requests
import pandas as pd
from pandas import json_normalize
from ckanapi import RemoteCKAN, NotAuthorized, NotFound,ValidationError, SearchQueryError, SearchError, CKANAPIError, ServerIncompatibleError
import json
import sys

###block för kpi-data ####
#ange vilken kommun du vill hämta 1280 = Malmö
kommun = '1280'
#ange vilket kpi du vill hämta - nu som systemparameter  (exempel python skapa_dataset_inkl_kolada.py N01804)
#kpi = 'N01804'
kpi = str(sys.argv[1])
#ange vilken url som ska hämtas in
url = 'https://api.kolada.se/v2/data/municipality/' #ange url
toturl = (url + kommun + '/kpi/' + kpi) #bygg ihop urlen
response = requests.get(toturl) #hämta ovanstående url
dictr = response.json() #läs in den som json

df = pd.json_normalize(data=dictr['values'], record_path='values', meta=['period','kpi', 'municipality'])  #normalisera jsonen - sätt start punkt och nästlad json i record path
df.drop(['count','kpi','status', 'municipality'], axis=1, inplace=True) #släng de kolumner du inte behöver - gender behövs bara i befolkningsstatistik
df.columns = ['Kön','Antal','År'] #byt namn på kolumnerna till svensk översättning
df = df[['År','Kön','Antal']] #bestäm ordning på kolumnerna

####block för csv namn baserat på kpi title information ######
#hämta information om kpi (title)
kpiurl = 'http://api.kolada.se/v2/kpi/' #ange url
kpiurl = (kpiurl + kpi) #bygg ihop urlen
kpiresponse = requests.get(kpiurl)
kpidictr = kpiresponse.json()
#print(kpidictr)
kpidf = pd.json_normalize(data=kpidictr['values'], meta=['title'])  #normalisera json
kpidf.drop(['auspices','has_ou_data','id','is_divided_by_gender','perspective','prel_publication_date','publ_period','publication_date','description', 'municipality_type','operating_area','ou_publication_date'],axis=1, inplace=True) 
#släng de kolumner du inte behöver, vi är bara intresserade av title 
kpidf = kpidf.to_string(index=False,header=False)
##skapa en sträng av title
##assigna strängen till ett värde:
kpiinfo = kpidf.lstrip()
#print(kpiinfo)



#hämta beskrivning av kpi (beskrivning)
bkpiurl = 'http://api.kolada.se/v2/kpi/' #ange url
bkpiurl = (bkpiurl + kpi) #bygg ihop urlen
bkpiresponse = requests.get(bkpiurl)
bkpidictr = bkpiresponse.json()
#print(kpidictr)
bkpidf = pd.json_normalize(data=bkpidictr['values'], meta=['description'])  #normalisera json
bkpidf.drop(['auspices','has_ou_data','id','is_divided_by_gender','perspective','prel_publication_date','publ_period','publication_date','title', 'municipality_type','operating_area','ou_publication_date'],axis=1, inplace=True) 
#släng de kolumner du inte behöver, vi är bara intresserade av beskrivningen 
bkpidf = bkpidf.to_string(index=False,header=False)
#bkpidf = bkpidf.to_string()
##skapa en sträng av beskrivningen
##assigna strängen till ett värde:
beskrivning = bkpidf


#filskapande 
path = '/home/morgan/csv/' #sökväg till var filerna ska mellanlanda lokalt
### namn plus (Kolada) plus (kpi)
df=df.to_csv(path + kpiinfo + ' -' + kpi + '.csv', index=False) #spara som csvfil med fullständigt namn
## variabler ##
namn = kpi.lower()
namn = namn
# prod: 
organisation = '3a274c48-f578-4236-9af3-3f4402081809'
#test
#organisation = '5983b634-d2bf-4321-8dd7-7eb5eb6f1208'
licens = 'cc-0'
utgivare = 'Malmö stad'
mail = 'malmostad@malmo.se'
status = 'http://publications.europa.eu/resource/authority/access-right/PUBLIC'
kontakt = 'Malmö stad'
sprak = 'http://publications.europa.eu/resource/authority/language/SWE'
tema = 'http://publications.europa.eu/resource/authority/data-theme/EDUC'
frekvens = 'http://publications.europa.eu/resource/authority/frequency/ANNUAL'
titel = kpiinfo

#api-variabler#
#skapa datamängden#

ua = 'ckanapimalmo/1.0 (+https://ckan-malmo.dataplatform.se)'
#prod : 
malmoapi = RemoteCKAN('https://ckan-malmo.dataplatform.se/', user_agent=ua, apikey='<apikey>')
#test
#malmoapi = RemoteCKAN('https://acc-ckan-malmo.dataplatform.se/', user_agent=ua, apikey='<apikey>')
## skapa tomt dataset ###
try:
        malmoapi.action.package_create(
        name = namn ,
        notes =  beskrivning,
        owner_org = organisation,
        license_id = licens,
        author = utgivare,
        author_email = mail,
        #private = 'false',
        access_rights = status,
        contact_name = kontakt,
        language = sprak,
        theme = tema,
        # for a list of themes check https://docs.dataportal.se/dcat/en/#5.3
        frequency = frekvens,
        title = titel)
       
except (NotAuthorized, NotFound,ValidationError, SearchQueryError, SearchError, CKANAPIError, ServerIncompatibleError) as e:
        print (e)
        print (e.args)


paketinfo = malmoapi.call_action('package_show', {'id': namn})
idinfo = paketinfo['id']
# print("Paket är skapat med id: " + idinfo)


#ladda upp filen till datamängden
try:
        malmoapi.call_action('resource_create',
        {'package_id': idinfo, 'name': kpiinfo +" (" +kpi +")" , 'description': beskrivning},
       
            files={'upload': open(path + kpiinfo + ' -' + kpi + '.csv', 'rb')})
except (NotAuthorized, NotFound,ValidationError, SearchQueryError, SearchError, CKANAPIError, ServerIncompatibleError) as e:
        print (e)
        print (e.args)
files = (kpiinfo + ' -' + kpi + '.csv')
fil = files
print(fil + " är nu uppladdad till: " + idinfo)
