### användning från commandline , samt avrundas med att printa ut dataset-id - obs namn på dataset måste vara små bokstäver, korrigerar med hjälp av title nedan ():  python skapa_paket_med_variabler.py dreamdataset "Vårt dataset är bäst"

from ckanapi import RemoteCKAN, NotAuthorized, NotFound,ValidationError, SearchQueryError, SearchError, CKANAPIError, ServerIncompatibleError
import sys

## variabler ##
namn = str(sys.argv[1])
beskrivning =  str(sys.argv[2])
organisation = '<org_id>'
licens = 'cc-0'
utgivare = '<editor>'
mail = '<email>'
status = 'http://publications.europa.eu/resource/authority/access-right/PUBLIC'
kontakt = '<contact>'
sprak = 'http://publications.europa.eu/resource/authority/language/SWE'
tema = 'http://publications.europa.eu/resource/authority/data-theme/SOCI'
frekvens = 'http://publications.europa.eu/resource/authority/frequency/ANNUAL'
titel = namn.title()

#api-variabler#

ua = 'ckanapimalmo/1.0 (+https://ckan-malmo.dataplatform.se)'
malmoapi = RemoteCKAN('https://ckan-malmo.dataplatform.se/', user_agent=ua, apikey='<mykey>')

## skapa tomt dataset ###
try:
        malmoapi.action.package_create(
        package_id = namn,
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
print("Paket är skapat med id: " + idinfo)


