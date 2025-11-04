# Installation des dépendances (si nécessaire)
# !pip install faker pandas

import random
import pandas as pd
import os
from faker import Faker

print("Script de génération de dataset (Mode Entraînement) démarré...")

# --- 1. CONFIGURATION DES CHEMINS ---
# Le chemin RELATIF vers le dossier 'sign_data' (comme vous l'avez déplacé)
# Ce chemin doit être correct par rapport à l'endroit où vous exécutez ce script.
LOCAL_DATA_DIR = "backend/app/data/sign_data"

# Emplacement de sauvegarde du fichier CSV final
NOM_FICHIER_FINAL = "backend/app/data/clients_avec_signatures_ref.csv"

# --- 2. LISTES DE NOMS (Données marocaines) ---
fake = Faker('fr_FR')
noms_marocains = [
    "Alaoui", "Ait", "Alami", "Bennani", "Mohamed", "Idrissi", "Berrada", "Hassan",
    "Lahlou", "Tazi", "Aziz", "El idrissi", "Benjelloun", "Amine", "Ayoub", "Saidi",
    "Tahiri", "El mostafa", "Cherkaoui", "Filali", "Amrani", "Daoudi", "El alaoui",
    "Yassine", "Mohammed", "Karim", "Said", "El mehdi", "Naji", "Bennis", "Rachid",
    "Chakir", "Khalil", "Kamal", "Naciri", "El alami", "Ben", "Youssef", "Ahmed",
    "Salhi", "Drissi", "Hajji", "El amrani", "Fatima", "Hamza", "Mansouri", 
    "El hassan", "Benkirane", "Sbai", "Sabri", "Hassani", "Bel", "Kadiri", "Chraibi",
    "Benali", "Rachidi", "Sara", "Talbi", "Benchekroun", "Slimani", "Ali", "Belhaj",
    "Zaki", "Sabir", "Abou", "Bakkali", "Hicham", "Es", "Mounir", "Khalid", "Rami",
    "Fathi", "Abid", "Lotfi", "Chaoui", "Jamal", "Choukri", "Ouazzani", "Marsli",
    "Bensaid", "Saadi", "El hassane", "Badr", "Dahbi", "Abdo", "Tahri", "Chahid",
    "Benmoussa", "Slaoui", "Kabbaj", "Ismaili", "Zine", "Mehdi", "Moussaoui", 
    "Lamrani", "Zakaria", "Radi", "Saber", "Amal", "Salmi", "Ziani", "Lazrak", 
    "Abdel", "Saad", "Nabil", "Messaoudi", "Azizi", "Hilali", "Hamdi", "Loukili",
    "Sadik", "Hakim", "Taha", "Nour", "Omar", "Semlali", "Raji", "Fadil", "Bennouna",
    "El hassani", "Rochdi", "Maroc", "Taleb", "Omari", "Fikri", "Hamdaoui", "Hafid",
    "Abdellaoui", "Senhaji", "Jalal", "Salim", "Bouziane", "Zeroual", "Jabri",
    "Hamid", "Malki", "Hafidi", "Aarab", "Zahir", "El mansouri", "Mansour", 
    "Touzani", "Faouzi", "Hachimi", "Baba", "Fadili", "Adil", "Touil", "Zineb",
    "Amri", "Khadija", "Azzouzi", "El asri", "Naim", "El houssine", "Ait el", 
    "Chaouki", "Chafik", "Sami", "Samir", "Dahmani", "Rais", "Simo", "Nassiri",
    "Yousfi", "Laaroussi", "Lachhab", "Nait", "Rahmouni", "Nouri", "Elidrissi",
    "Moumen", "Rafik", "Amraoui", "Sebti", "Fares", "Regragui", "Farah", "Rahmani",
    "Allali", "Housni", "Sekkat", "Moussaid", "Guessous", "Ouali", "Zouhair",
    "El omari", "Benslimane", "Mustapha", "Karam", "Zerouali", "Hanane", "Benbrahim",
    "Salma", "Abdou", "Bouzid", "Rida", "Charaf", "Sadiki", "Soussi", "Ghazi",
    "Lakhal", "Amzil", "Badri", "Brahim", "Oussama", "Hamidi", "Bensouda", "Abbassi",
    "Badaoui", "Nadir", "Id", "Bentaleb", "Fahmi", "Mabrouk", "Hasnaoui", "Haddad",
    "Kettani", "Najib", "Mahfoud", "Soufiane", "Aissaoui", "Boukhari", "El hilali",
    "El mahdi", "Kasmi", "Reda", "Jabrane", "Wahbi", "Er", "Benomar", "El bakkali",
    "Salah", "Allaoui", "Fouad", "Mourad", "Sadki", "Adnane", "Bouayad", "Kaddouri",
    "Abdellah", "Ibrahimi", "Mokhtari", "Maarouf", "Toumi", "Younes", "Hanafi",
    "Taoufik", "Karimi", "Bouzidi", "Taibi", "Taki", "Faiz", "Anouar", "Hilal",
    "Moumni", "Yacoubi", "El filali", "Tijani", "Hamzaoui", "Nejjar", "El amri",
    "Oulad", "Mouhib", "Lachgar", "Mekkaoui", "Ouardi", "Chadli", "Benamar", "Chami",
    "Boutaleb", "Ramzi", "El bachir", "Khaldi", "Saoud", "Meziane", "Belghiti",
    "Hayat", "El mustapha", "Zaoui", "Diouri", "Zitouni", "Mahboub", "Barakat",
    "Tarik", "Marouane", "El ouardi", "Elalaoui", "Benani", "El ouazzani", "Cherif",
    "Fakir", "El ghazi", "El hachimi", "Nasri", "Hamdani", "Ismail", "Bahi",
    "Morchid", "Elasri", "El habib", "Benzakour", "Mekouar", "Erraji", "Anas",
    "Atif", "Bouali", "Amghar", "Rahali", "Saadaoui", "Fassi", "Bouazza", "Mimouni",
    "Chaib", "Lakhdar", "Kharbouch", "Jamali", "Mazouz", "Elamrani", "Farid", "Safi",
    "El azzouzi", "Mahmoudi", "Majid", "El kadiri", "Hatim", "Habib", "El mokhtar",
    "Cherradi", "Habibi", "Charif", "Saoudi", "Riad", "Jaafar", "Houari",
    "El haddad", "Meftah", "Halim", "Madani", "Achraf", "El abbassi", "Stitou",
    "Ennaji", "Zerhouni", "Kaoutar", "Chihab", "Khattabi", "Fadel", "Ameziane",
    "Zahraoui"
]

prenoms_h = [
    "Abad", "Abdennasser", "Amghar", "Abbas",
    "Abdelmoula", "Amimar", "Abbou", "Allal",
    "Amine", "Abdelaalim", "Abdennour", "Amjad",
    "Abdelaati", "Abderaouf", "Ammar", "Abdeladim",
    "Abderrafie", "Amrane", "Abdelali", "Abderrazak",
    "Anis", "Abdelaziz", "Abdessabour", "Anouar",
    "Abdelbadie", "Abdessadek", "Antar", "Abdelbaki",
    "Abdessafi", "Antara", "Abdelbasset", "Abdessalam",
    "Aouab", "Abdelfattah", "Abdessamad", "Aouiss",
    "Abdelghafour", "Abdessamie", "Arbi", "Abdelghani",
    "Abdessatar", "Archane", "Abdelhadi", "Abdou",
    "Aref", "Abdelhafid", "Abdourabih", "Arif",
    "Abdelhak", "Abdrabbou", "Arij", "Abdelhakim",
    "Abed", "Arkam", "Abdelhalim", "Abid",
    "Arsalane", "Abdelhamid", "Aboubaki", "Assad",
    "Abdelhaq", "Aboubakr", "Assil", "Abdelilah",
    "Aboud", "Assou", "Abdeljabbar", "Achour",
    "Atef", "Abdeljalil", "Achraf", "Atf",
    "Abdeljaouad", "Adam", "Atik", "Abdelkabir",
    "Addi", "Atiq", "Abdelkader", "Adel",
    "Atouf", "Abdelkamel", "Adham", "Ayache",
    "Abdelkarim", "Adib", "Ayachi", "Abdelkhalek",
    "Adil", "Ayad", "Abdelkouddous", "Adnane",
    "Ayich", "Abdellah", "Afif", "Ayman",
    "Abdellatif", "Ahmed", "Ayoub", "Abdelmalek",
    "Aissa", "Azam", "Abdelmoghit", "Akram",
    "Azhar", "Abdelmonaim", "Alaeeddine", "Azmi",
    "Abdelmouaiz", "Alami", "Azzam", "Abdelmoughit",
    "Ali", "Azzeddine", "Abdelmouhaimin", "Aliane",
    "Azzelarab", "Abdelmoujib", "Alif", "Azzouz",
    "Abdelmoumen", "Alilou", "Abdelmouttalib", "Allali",
    "Abdelouadoud", "Allou", "Abdelouafi", "Allouch",
    "Abdelouahab", "Amar", "Abdelouahid", "Amara",
    "Abdelouali", "Amer", "Abdelouarete", "Ameur",
    "Abdenbi", "Ameziane",
    "Baaka", "Bachar", "Baaqa", "Baba",
    "Badr", "Badr Ezzamane", "Badr Eddine", "Badri",
    "Bahae", "Bahi", "Bahssin", "Bachir",
    "Bakkar", "Bakr", "Bamou", "Barouk",
    "Belkassem", "Benissa", "Bassam", "Bassou",
    "Belaid", "Belkas", "Benaissa", "Benasser",
    "Bendaoud", "Bennacer", "Benyaakoub", "Bichara",
    "Bichr", "Bikr", "Bilal", "Bouamama",
    "Bouamar", "Bouamrou", "Bouazza", "Bouchaib",
    "Bouekri", "Bouchta", "Bouhout", "Boujemaa",
    "Bourhim", "Bourhime", "Bousedra", "Bouselham",
    "Bouziane", "Brahim", "Brik",
    "Chaabane", "Chaddad", "Chadi", "Chadli",
    "Chafai", "Chafik", "Chafiq", "Chahed",
    "Chahid", "Chaib", "Chakib", "Chakir",
    "Chaouki", "Charaf", "Charaf Eddine", "Charki",
    "Chedad", "Cherqi", "Chihab", "Choaib",
    "Chouaib", "Choukri",
    "Dahane", "Dahbi", "Dah Mane", "Daidai",
    "Dalil", "Daoud", "Daoui", "Darid",
    "Darous", "Diab", "Diae", "Diae Eddine",
    "Didi", "Douraid", "Driss",
    "Eddaoui", "Elaid", "Elarabi", "Elarbi",
    "Elaydi", "Elbachir", "Elbouchtaoui", "Elchafii",
    "Elchahid", "Ebdelkahar", "Ebdelkayyaoum", "Elfatmi",
    "Elghali", "Elghaouti", "Elghazouani", "Elhabib",
    "Elmokhtar", "Elhachemi", "Elhassan", "Elhouari",
    "Elkebir", "Elkhadioui", "Elkhadir", "Elkhamar",
    "Elmadani", "Essghir", "Elmostafa", "Elmouloudi",
    "Elouafi", "Elyazi", "Ezzine", "Eloualid",
    "Elmahdi", "Elmahi", "Elmahjoub", "Elmakki",
    "Fadoul", "Fael", "Fathoune", "Fahd",
    "Faras", "Fahim", "Fettah", "Fikri",
    "Fouad", "Frahat", "Fahmi", "Farji",
    "Farouk", "Faik", "Farid", "Fath Allah",
    "Fath Elkhir", "Fail", "Faraji", "Fares",
    "Farhate", "Fathi", "Faissal", "Fadel",
    "Faiz", "Fakher", "Fakhr Eddine", "Faouaz",
    "Faouzi",
    "Ghafour", "Ghali", "Ghanem", "Ghanim",
    "Gharib", "Ghassan", "Ghazal", "Ghazi", "Ghazil",
    "Habib", "Hossam", "Habib Allah", "Hossam Eddine",
    "Habika", "Houari", "Hachem", "Houcine",
    "Haddaoui", "Houd", "Haddou", "Houdaifa",
    "Hadi", "Houmad", "Hadou", "Houmam",
    "Hafid", "Houmane", "Hafs", "Hoummane",
    "Haidar", "Hourma", "Haitam", "Houssam",
    "Hajaj", "Houssine", "Hajjaj", "Houssni",
    "Hakim", "Hsina", "Halim", "Hssina",
    "Hamd", "Hamda", "Hamdane", "Hamdi",
    "Hamid", "Hamidan", "Hammadi", "Hamiddouche",
    "Hammam", "Hammed", "Hamou", "Hamoud",
    "Hamouda", "Hamza", "Hanafi", "Hani",
    "Hanifa", "Harouch", "Harrou", "Hassan",
    "Haroun", "Hassoun", "Hatim", "Hazaz",
    "Hazem", "Hazim", "Hicham", "Hilmi",
    "Hmad", "Hmida", "Hmidane", "Hmidouch",
    "Horma", "Hosni",
    "Iad", "Ibrahim", "Ider", "Idriss",
    "Ihssane", "Ikbal", "Ilias", "Ilyas",
    "Imad", "Imad Eddine", "Imran", "Irchad",
    "Isaad", "Ishaq", "Ismail", "Issa",
    "Iyad", "Issam",
    "Jaafar", "Jabbour", "Jaber", "Jabir",
    "Jabour", "Jabrane", "Jad", "Jad Elmoula",
    "Jadouane", "Jalal", "Jalal Eddine", "Jalil",
    "Jaloul", "Jamae", "Jamal", "Jamal Eddine",
    "Jamea", "Jamil", "Jaouad", "Jaouhar",
    "Jar Allah", "Jarrah", "Jbilou", "Jilali",
    "Jnina", "Joundol",
    "Kabbour", "Kabir", "Kacem", "Kadem",
    "Kadhem", "Kadour", "Kais", "Kamal",
    "Kamel", "Kandouz", "Karam", "Karim",
    "Kassem", "Kassou", "Kebour", "Khachane",
    "Khair Eddine", "Khairi", "Khales", "Khalid",
    "Khalifa", "Khalil", "Khalis", "Khatib",
    "Kotb", "Kouider",
    "Labib", "Lahbib", "Lahcen", "Laite",
    "Laith", "Lakbir", "Lakhdar", "Larbi",
    "Latif", "Layachi", "Lokmane", "Lotfi",
    "Louay", "Loukman", "Lounes", "Lounis",
    "Loutfi",
    "Mahdi", "Maamar", "Maamoun", "Maarouf",
    "Maatallah", "Maati", "Mabrouk", "Machich",
    "Madani", "Mahboub", "Maher", "Mahfoud",
    "Mahjoub", "Mahjoubi", "Mahmoud", "Mahraz",
    "Mahrez", "Majd", "Majdoub", "Majid",
    "Makhlouf", "Malek", "Malih", "Mallal",
    "Mamdouh", "Mamoun", "Mandil", "Mansour",
    "Marouane", "Marzak", "Marzouk", "Masaoud",
    "Masrour", "Massoud", "Mazigh", "M’barek",
    "Mesbah", "Meziane", "M’hamed", "Mimoun",
    "Mnaouar", "Moad", "Moaouia", "Moataz",
    "Mobarek", "Mofid", "Moflih",
    "Nabih", "Nabil", "Nacer", "Nader",
    "Nadim", "Nadir", "Nafie", "Nafis",
    "Nail", "Naim", "Najah", "Najd",
    "Najem", "Naji", "Najib", "Najm Eddine",
    "Namir", "Naoufal", "Nasr", "Nasr Eddine",
    "Nassef", "Nassif", "Nassih", "Nassim",
    "Nazih", "Nezar", "Nizar", "Nouaman",
    "Nouh", "Nour", "Nour Eddine", "Nouri",
    "Okacha", "Okba", "Omar", "Osmane",
    "Otaiba", "Othmane", "Ouadie", "Ouael",
    "Ouafi", "Ouafik", "Ouahab", "Ouahib",
    "Ouahid", "Ouail", "Ouajdi", "Ouajih",
    "Oualid", "Oualim", "Ouassim", "Ounssi",
    "Oussama", "Outaiba",
    "Rabbah", "Rabeh", "Rabie", "Rachad",
    "Rached", "Rachid", "Radi", "Raed",
    "Rafie", "Rafik", "Rahali", "Rahim",
    "Rahmoun", "Raif", "Ramdane", "Ramzi",
    "Raouad", "Raouf", "Rayan", "Razane",
    "Razek", "Razouk", "Reda", "Reda Allah",
    "Redad", "Redouane", "Refki", "Reyad",
    "Rezki", "Rhassane", "Riad", "Rouchdi",
    "Rostom",
    "Saad", "Saad Eddine", "Saadoune", "Saber",
    "Sabih", "Sabri", "Sadik", "Saeb",
    "Safi", "Safouane", "Saghir", "Sahel",
    "Said", "Saif", "Saif Eddine", "Saif Elarab",
    "Saif Elislam", "Salah", "Salah Eddine", "Salam",
    "Salama", "Saleh", "Salem", "Salim",
    "Sallam", "Salmane", "Samad", "Sami",
    "Samih", "Samir", "Saoud Rochd", "Sarhane",
    "Sarie", "Seddik", "Sedki", "Selam",
    "Seouar", "Sobhi", "Sofiane", "Sohaib",
    "Soltan", "Soubhi", "Souhaib", "Souhail",
    "Soulaimane", "Soultane", "Sourour", "Stela",
    "Tachfine", "Taha", "Taher", "Taib",
    "Taibi", "Taj Eddine", "Taki Eddine", "Talal",
    "Taleb", "Talha", "Tami", "Tamime",
    "Taoufik", "Tarik", "Tareq", "Thami",
    "Tijani", "Tofail", "Touhami",
    "Yaakoob", "Yachou", "Yahia", "Yahya",
    "Yakd", "Yanis", "Yasser", "Yassine",
    "Yassir", "Yazid", "Younes", "Yousri",
    "Youssef",
    "Zahid", "Zahir", "Zaid", "Zakaria",
    "Zaki", "Zekri", "Zeriab", "Zeroual",
    "Zeryab", "Zidane", "Zine", "Zine Eddine",
    "Zine Elabidine", "Ziyad", "Zoubir", "Zouhir"
]

prenoms_f = [
    "Aafrae","Aasmae","Abida","Abir","Abla","Abouch","Achouak","Achoura",
    "Adba","Adiba","Adila","Adrae","Afaf","Afifa","Afnane","Ahlam",
    "Aicha","Aida","Ainaya","Aissaouia","Aizza","Akida","Alia","Aliana",
    "Alou","Amal","Amane","Amani","Amat Errahmane","Amina","Amria","Anbar",
    "Anika","Anissa","Ansam","Anssi","Aouatif","Aouich","Aouicha","Arbia",
    "Arifa","Arije","Arjouane","Arwa","Asmae","Assala","Assia","Assila",
    "Atiba","Atifa","Atika","Atouch","Awicha","Aya","Ayacha","Ayada",
    "Azhar","Aziza","Azouzia","Azza","Bachira","Bada","Badda","Badia",
    "Badr Essououd","Badra","Badria","Bahia","Bahija","Bahria","Bahrya","Bakhta",
    "Bamou","Bardis","Barka","Baroudia","Basima","Basma","Batoul","Baya",
    "Bouchra","Bouchtaouia","Boutaina","Bouthaina","Brika","Chaden","Chadia",
    "Chadlia","Chafia","Chafika","Chahbae","Chahida","Chahrazad","Chaimae",
    "Chakira","Chama","Chams","Chams Eddouha","Charifa","Charkia","Chefae",
    "Chehabe","Chihab","Chmicha","Chokria","Chomeysa","Chouhaiba","Choukria",
    "Choumaissa","Chourouk","Dahbia","Dalal","Dalila","Daouia","Darifa",
    "Darous","Dikra","Dina","Doha","Dounia","Drissia","Elaidya","Elamria",
    "Elazzouzia","Elbahia","Elbatoul","Eldaouia","Elissaouia","Elkasmia",
    "Elkhamsa","Elmalha","Elzahia","Ettahra","Ettam","Ezzahiria","Fada",
    "Fadila","Fadma","Fadoua","Fahima","Fairouz","Faiza","Fakhita","Fakira",
    "Fama","Fanida","Farah","Farha","Farida","Fariha","Fathia","Fatima",
    "Fatima Zohra","Fatine","Fatna","Fatou","Fatouch","Fatoum","Fattouch",
    "Fattoum","Fayda","Fikria","Firdaous","Fouzia","Ghada","Ghalia","Ghania",
    "Ghanima","Ghannou","Gharae","Ghariba","Ghazala","Ghazil","Ghenou",
    "Ghita","Ghizlane","Hababa","Habbouba","Habiba","Hachmia","Hachouma",
    "Hada","Hadbae","Hadda","Hadhoum","Hadia","Hadifa","Hadil","Hadir",
    "Hafida","Hafsa","Haifae","Hajar","Hajiba","Hajjou","Hakima","Hala",
    "Halal","Halima","Hallouma","Hamdaouia","Hamida","Hammout","Hamou",
    "Hanae","Hanane","Hania","Hanifa","Hannou","Hasiba","Hasnae","Hassana",
    "Hassna","Haya","Hayat","Heba","Hedaya","Hiba","Hibat Allah","Hidaya",
    "Hikma","Hind","Hinda","Houbaba","Houda","Houria","Ibtihaj","Ibtihal",
    "Ibtissame","Ichraf","Ichrak","Ichraq","Ifak","Ihssan","Ijja","Ijjou",
    "Ijlal","Ikbal","Ikhlas","Ikram","Ilham","Ilhame","Imane","Inaam",
    "Inas","Inaya","Ines","Insaf","Intissar","Irchad","Irfane","Isaad",
    "Israe","Issoua","Istirae","Izdihar","Jadia","Jahina","Jalila","Jamila",
    "Jaouahir","Jaouda","Jaydae","Jeddia","Jenane","Jenna","Jennate","Jihane",
    "Jmia","Jouayria","Jouda","Jouhaina","Jouhairia","Joumala","Joumana",
    "Joumane","Jounaina","Kabira","Kaema","Kaeda","Kaima","Kamar","Kamaria",
    "Kamila","Kamilia","Kamria","Kaouakib","Kaoukeb","Kaoutar","Karima",
    "Kattou","Kawakib","Kawkab","Keltoum","Kenza","Ketou","Khaddouj",
    "Khadija","Khadijatou","Khadouja","Khadra","Khalfia","Khalida","Khalila",
    "Khansae","Khaoula","Khattou","Khdijtou","Khdrae","Kheira","Khira",
    "Khlifia","Khnata","Labiba","Lajin","Lamiae","Lamyae","Lara","Latifa",
    "Layla","Leila","Lina","Lobaba","Loubana","Loubna","Louiza","Loujain",
    "Maazouza","Mabrouka","Madiha","Maessa","Maha","Mahasine","Mahbouba",
    "Mahdia","Mahjouba","Maisae","Maisane","Maissa","Majda","Marzouka",
    "Majida","Malak","Malha","Maliha","Malika","Mama","Mamat","Manal",
    "Manar","Mansoura","Maouahib","Maounia","Maria","Mariem","Marima",
    "Marjana","Marjane","Maroua","Masen","Masouda","Mayada","Mazouara",
    "M’Barka","M’Birika","Menna","Mennana","Messouda","Mezouara","Milad",
    "Milouda","Miloudia","Mimouna","Mina","Momtaza","Morjana","Mouada",
    "Moufida","Mouina","Moumna","Mouna","Mounia","Mounira","Nabaouia",
    "Nabiha","Nabila","Nachita","Nachoua","Nachwa","Nada","Nadia","Nadifa",
    "Nadira","Nadoua","Nafissa","Naghma","Nahed","Nahid","Nahida","Nahila",
    "Nahla","Naima","Najat","Najda","Najia","Najiba","Najlae","Najma",
    "Najoua","Namae","Namira","Naoual","Naouar","Naouara","Narjis","Nasiba",
    "Nasima","Nasira","Nasma","Nasria","Nassiba","Nassria","Nazha","Naziha",
    "Neama","Nehad","Nehal","Nihad","Nihal","Nisrine","Nofayla","Nora",
    "Nouma","Nour","Odria","Olaya","Olfa","Omra","Omria","Othmana",
    "Ouadia","Ouafae","Ouahiba","Ouahida","Oualada","Oualida","Ouarda",
    "Ouardia","Ouasila","Ouasima","Oud Elouard","Ouiame","Ouidad","Ouihab",
    "Ouijdane","Ouissal","Oum Elaid","Oum Elbanine","Oum Elez","Oum Elghait",
    "Oum Elhine","Oum Elkhir","Oum Essaad","Oum Hani","Oum Keltoum","Oumama",
    "Oumayya","Oumelghit","Oumnia","Ourida","Rabab","Rabha","Rabia","Racha",
    "Rachida","Rachika","Radia","Radoua","Raeda","Raeja","Rafiaa","Rafika",
    "Rahiba","Rahila","Rahima","Rahma","Rahmouna","Raida","Raihana","Raihane",
    "Rajae","Rajia","Rakouch","Rana","Randa","Rania","Raoua","Raouane",
    "Ratiba","Rayda","Rayhana","Razika","Rehab","Rehame","R’Himou","Rim",
    "Rima","Rkia","Rochdia","Rouaya","Rouhia","Roukaya","Saadia","Sabhia",
    "Sabiha","Sabira","Sabra","Sabria","Sabrina","Sadika","Safae","Safia",
    "Safira","Safoua","Sahila","Saida","Saila","Sakina","Saliha","Salima",
    "Salma","Saloua","Salsabil","Samae","Samar","Samara","Samia","Samiha",
    "Samira","Samrae","Sanae","Saousane","Sara","Sarah","Seddika","Siham",
    "Siouar","Smahane","Sofia","Sonia","Soraya","Souad","Souhaila","Souhir",
    "Soukaina","Soultana","Soumia","Tafout","Tahera","Tahour","Tahra",
    "Taimae","Takwa","Tama","Tamimount","Tamou","Tamra","Taoufika","Tasnim",
    "Thouriya","Tilila","Tisba","Tlaitmas","Tohfa","Touda","Touiba","Wadia",
    "Wahida","Wiam","Widad","Widen-May","Wissal","Yaja","Yajjou","Yakout",
    "Yamama","Yamane","Yamina","Yamna","Yasamine","Yasmina","Yasmine",
    "Yassira","Yattou","Yazza","Yetou","Yezza","Yousra","Zahia","Zahida",
    "Zahira","Zahoua","Zahra","Zahria","Zaima","Zaina","Zaineb","Zakia",
    "Zanba","Zannouba","Zanou","Zanouba","Zaytouna","Zaytounia","Zhirou",
    "Zina","Zinba","Zineb","Zohra","Zoubida","Zouina","Zoulikha"
]

prenoms_disponibles = prenoms_h + prenoms_f

# --- 3. FONCTIONS DE GÉNÉRATION DE DONNÉES SYNTHÉTIQUES ---

def generer_ribs_rapide(nombre_total=686):
    banques_cibles = {"230": "CIH Bank", "007": "Attijariwafa Bank", "145": "Banque Populaire", "011": "BMCE Bank of Africa"}
    ribs = []
    clients_par_banque = nombre_total // len(banques_cibles)
    if nombre_total % len(banques_cibles) != 0: clients_par_banque += 1
        
    for code_banque, _ in banques_cibles.items():
        for i in range(clients_par_banque):
             if len(ribs) >= nombre_total: break
             rib = f"{code_banque}{random.randint(10000, 99999):05d}{(i * 1234567) % 100000000000000:014d}{random.randint(0, 99):02d}"
             ribs.append({"RIB": rib})
    return ribs[:nombre_total]

def generer_client_unique(combinaisons_uniques, noms_famille, prenoms_disponibles, max_tentatives=1000):
    tentative = 0
    while tentative < max_tentatives:
        nom = random.choice(noms_famille)
        prenom = random.choice(prenoms_disponibles)
        combinaison = f"{nom}_{prenom}"
        if combinaison not in combinaisons_uniques:
            combinaisons_uniques.add(combinaison)
            return nom, prenom
        tentative += 1
    raise Exception("Impossible de générer un nom unique. Les listes sont trop petites.")

# --- 4. DÉCOUVERTE DES SIGNATURES DISPONIBLES ---

print(f"🔍 Scan du dossier de données : {LOCAL_DATA_DIR}")
try:
    # Déterminer la plage d'IDs de signatures
    signer_dirs = [d for d in os.listdir(LOCAL_DATA_DIR) if os.path.isdir(os.path.join(LOCAL_DATA_DIR, d)) and d.isdigit()]
    SIGNATURE_IDS = sorted(signer_dirs)
    NOMBRE_SIGNATAIRES_DS = len(SIGNATURE_IDS)
    if NOMBRE_SIGNATAIRES_DS == 0:
         raise ValueError(f"Aucun dossier de signataire trouvé dans {LOCAL_DATA_DIR}.")

except FileNotFoundError:
    print(f"ERREUR FATALE: Le dossier '{LOCAL_DATA_DIR}' n'a pas été trouvé.")
    print(f"Assurez-vous que le dossier 'sign_data' est bien dans '{os.path.abspath('backend/app/data/')}'.")
    exit()

print(f"Nombre de signataires disponibles dans le DS : {NOMBRE_SIGNATAIRES_DS}")

# --- 5. GÉNÉRATION DES CLIENTS ET LIAISON AUX DOSSIERS (Mise à jour) ---

NOMBRE_CLIENTS = 686 
ribs_rapides = generer_ribs_rapide(NOMBRE_CLIENTS)

print("\n👥 Génération des clients et liaison aux dossiers d'entraînement...")
clients = []
combinaisons_uniques = set()

for i, rib_data in enumerate(ribs_rapides):
    try:
        nom, prenom = generer_client_unique(combinaisons_uniques, noms_marocains, prenoms_disponibles)
    except Exception as e:
        print(f"\nERREUR: {e}. Arrêt à {i} clients.")
        break
    
    # Attribution circulaire de l'ID de signature
    signature_id_ref = SIGNATURE_IDS[i % NOMBRE_SIGNATAIRES_DS]
    
    # --- CHANGEMENT CLÉ ---
    # Chemin relatif vers le dossier des signatures VRAIES (Genuine)
    path_genuine = os.path.join(LOCAL_DATA_DIR, signature_id_ref)
    
    # Chemin relatif vers le dossier des signatures FAUSSES (Forged)
    path_forged = os.path.join(LOCAL_DATA_DIR, f"{signature_id_ref}_forg")
    
    solde = round(random.uniform(100, 100000), 2)

    clients.append({
        "ID_CLIENT_SYNTH": i + 1,
        "RIB": rib_data["RIB"],
        "Nom": nom,
        "Prénom": prenom,
        "Solde_MAD": solde,
        "SIGNATURE_ID_REF": signature_id_ref, # L'ID du signataire (ex: '001')
        "PATH_GENUINE": path_genuine,     # Chemin vers le dossier des vraies signatures
        "PATH_FORGED": path_forged        # Chemin vers le dossier des fausses signatures
    })

df = pd.DataFrame(clients)

# --- 6. SAUVEGARDE LOCALE ---

df.to_csv(NOM_FICHIER_FINAL, index=False, encoding='utf-8')

print("\n--- RÉSULTAT FINAL ---")
print(f"🎉 TERMINÉ ! {len(df)} clients synthétiques liés à {NOMBRE_SIGNATAIRES_DS} dossiers de signataires.")
print(f"💾 Fichier CSV de mapping sauvegardé dans: {NOM_FICHIER_FINAL}")
print("\nExemple de structure du CSV (premiers clients) :")
print(df[['ID_CLIENT_SYNTH', 'Nom', 'SIGNATURE_ID_REF', 'PATH_GENUINE', 'PATH_FORGED']].head())