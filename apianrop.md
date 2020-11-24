Några Grundläggande CKAN API anrop för webläsaren, curl eller för att enklare uttyda informationen rekommenderas ett verktyg som exempelvis postman. 

All detaljerad information om nedanstående exempel och mer kan hitta på: 

https://docs.ckan.org/en/latest/api/index.html#action-api-reference 
 

# ANVÄNDARHANTERING (Via API) 

* Pre-reqs: 
Se nedan i GET exemplen för att ta fram information om vilka organisationer du har att använda dig av (name eller id på organisation ska in i group_id i exemplet) 
Se också sidan om Behörigheter inom organisation för information om vilken behörighet du vill ge din inbjudna användare (member, editor eller admin ska in I role I exemplet) 
Kontrollera din API-nyckel via din ckan-inloggning (lägg in den vid Authorization I exemplet) 
Kontrollera epost till mottagaren som inbjudan ska skickas till 

* EXEMPEL 

curl -X POST 'https://ckan-malmo.dataplatform.se/api/3/action/user_invite' \ 
-H "Authorization: <din-apinyckel>" \ 
-d '{"email": "<fornamn.efternamn@malmo.se>", "group_id": "malmo", "role":"member"}' 

# GET (Hämta information) 
* ORGANISATIONER 
Om du vill lista vilka organisationer som finns: 
https://ckan-malmo.dataplatform.se/api/action/organization_list 

En detaljerad lista över organisationerna: 
https://ckan-malmo.dataplatform.se/api/action/organization_list?all_fields=true 

För att lista vilka datamängder som finns per organisation (använder organisationen malmo som vi fann i exemplet ovan): 
https://ckan-malmo.dataplatform.se/api/action/organization_show?id=malmo&include_datasets=true&include_users=false 

* DATAMÄNGDER 

Ett alternativ till ovan att hitta vilka datamängder som finns: 
https://ckan-malmo.dataplatform.se/api/action/package_list 

För en detaljerad lista om en viss datamängd samt deras delmängder (datamängden kkik som du får fram från exemplet ovan)  
https://ckan-malmo.dataplatform.se/api/action/package_show?id=kkik 

Alternativt går det använda package_search (samma exempel som ovan men nu med id) 
https://ckan-malmo.dataplatform.se/api/action/package_search?q=&fq=id:688452d5-c455-463d-9183-2f030bb7401c 

Samma exempel fast datamängdens namn istället för id 
https://ckan-malmo.dataplatform.se/api/action/package_search?q=&fq=name:kkik 
 
* DELMÄNGDER 

Om du vill gräva dig ner i delmängderna så kan du fortsätta med det genom att (här väljer vi  delmängden "Brukarbedömning särskilt boende äldreomsorg -  helhetssyn, andel (%")   
https://ckan-malmo.dataplatform.se/api/action/resource_show?id=8e5310ea-fccc-4b80-9258-d802f6f17e1f 

# CREATE (Skapa information) 

Innan vi börjar behöver vi ha samlat in lite information: 
* LICENSER (Via API) 
För att få information om vilka licenser du har att välja på för dina datamängder (notera ner det id som matchar den licens du vill använda (i dagsläget cc-0 eller cc-by)): 
https://ckan-malmo.dataplatform.se/api/action/license_list 

* TEMA (Via API) 
För att få information om vilka teman som finns för att använda när du skapar dina datamängder: 
https://ckan-malmo.dataplatform.se/api/action/group_list 

* TAGS (Via API) 
För att få information om vilka tags som finns för att använda när du skapar dina datamängder: 
https://ckan-malmo.dataplatform.se/api/action/tag_list 

 
