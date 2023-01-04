import requests
from bs4 import BeautifulSoup
import pandas as pd

title = []
prix_liste=[]
ratings=[]
liste_dispo = []

for page in range (1, 51):
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'.format(page=page)
    req = requests.get(url)
    soup = BeautifulSoup(req.text)

    for books in soup.find_all("article", {"class":"product_pod"}):

        # syntaxe quand il y a plusieurs attributs 
        l=books.find_all('a')[-1]['title']
        title.append(l)

        prix = books.find_all("p", {"class": "price_color"})
        for i in prix:
            prix_liste.append(i.text.replace("Â£",""))
        
    
        # les étoiles 
        for i in books.find_all("p", class_="star-rating"):
            if i['class'] == ['star-rating', 'One']:
                a=1 
            if i['class'] == ['star-rating', 'Two']:
                a=2
            if i['class'] == ['star-rating', 'Three']:
                a=3
            if i['class'] == ['star-rating', 'Four']:
                a=4
            if i['class'] == ['star-rating', 'Five']:
                a=5
            ratings.append(a)

    # mise en page nécessaire pour le stock : 
        dispo = books.find_all("p", class_="instock availability")
        for i in dispo :
            z = i.text
            #la fonction replace permet d'enlever les attributs dans la liste
            liste_dispo.append(z.replace("                                                                                    ", "")
            .replace("\n\n    \n        ", "")
            .replace("\n    \n",""))
        
# création d'un dataframe
data = {
"Titre":title,
"Prix":prix_liste,
"Note":ratings,
"Stock":liste_dispo
}
df = pd.DataFrame(data=data)
df['Prix'] = df['Prix'].astype(float)

print(df)

# intégration des 50 pages dans un fichier csv.
# df.to_csv("brief_14_web_scrapping\df.csv", index=False)  
df.to_csv('df_books.csv')