from mimesis import Generic
from django.core.files import File # Importez File pour traiter les liens d'image
import os
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen 
from datetime import datetime, timedelta
from PIL import Image
import random
import requests
from urllib.parse import urlparse
from faker import Faker
from purchases.models import *
from products.models import *
from users.models import *
from banners.models import *

def generer_categories(number_of_categories):
    generic = Generic()

    for _ in range(number_of_categories):
        name = generic.text.word()

        # Générer un lien d'image aléatoire
        image_url = generate_random_image_url()
        
        # Télécharger l'image depuis le lien
        img_temp = NamedTemporaryFile()
        img_temp.write(urlopen(image_url).read())
        img_temp.flush()
        
        # Extraire l'extension de l'URL de l'image
        image_extension = os.path.splitext(urlparse(image_url).path)[-1]

        # Créer l'objet Category avec les données aléatoires et l'image téléchargée
        category = Category.objects.create(name=name)
        image_url=image_url+'.png'
        
        category.image.save(os.path.basename(image_url), File(img_temp))
        category.save()

def generate_random_image_url(width=400, height=400):
    # Choisissez un service d'hébergement d'images aléatoire
    image_services = ['https://picsum.photos', 'https://source.unsplash.com']
    image_service = random.choice(image_services)

    # Générer un identifiant d'image aléatoire
    image_id = random.randint(1, 1000)

    # Générer le lien d'image aléatoire
    image_url = f'{image_service}/{width}/{height}?image={image_id}'
    return image_url

def get_random_product_image_url():
    # Requête à l'API "Unsplash" pour obtenir des images de produits
    url = "https://api.unsplash.com/photos/random"
    headers = {
        "Authorization": "Client-ID VOTRE_CLE_API_UNSPLASH",
        "Accept-Version": "v1"
    }
    params = {
        "query": "product",
        "orientation": "squarish"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        # Analyse de la réponse JSON pour obtenir l'URL de l'image
        data = response.json()
        image_url = data["urls"]["regular"]
        return image_url
    else:
        print("Erreur lors de la requête à l'API Unsplash.")
        return None


def generer_subcategory(nombre_subcategory):
    generic = Generic()

    # Récupérez toutes les catégories existantes dans la base de données
    categories = Category.objects.all()

    for _ in range(nombre_subcategory):
        name = generic.text.word()

        # Choisissez une catégorie aléatoire parmi les catégories existantes
        categorie_aleatoire = generic.random.choice(categories)

        # Créez l'objet Subcategory lié à la catégorie choisie
        subcategory = SubCategory.objects.create(name=name, category=categorie_aleatoire)
        subcategory.save()

def generer_events(nombre_events):
    generic = Generic()

    for _ in range(nombre_events):
        title = generic.text.word()
        date_limite = datetime.now() + timedelta(days=generic.random.randint(1, 30))
        contenu = generic.text.text()

         # Générer un lien d'image aléatoire
        image_url = generate_random_image_url()

        # Téléchargez l'image depuis le lien
        img_temp = NamedTemporaryFile()
        img_temp.write(urlopen(image_url).read())
        img_temp.flush()
        
        # Extraire l'extension de l'URL de l'image
        image_extension = os.path.splitext(urlparse(image_url).path)[-1]
        
        # Créez l'objet Event avec les données aléatoires et l'image téléchargée
        event = Event.objects.create(title=title, date_limite=date_limite, contenu=contenu)
        image_url=image_url+'.png'
        event.images.save(os.path.basename(image_url), File(img_temp))

        # Enregistrez l'objet Event dans la base de données
        event.save()
        

def generate_random_integer():
    generic = Generic()
    random_integer = generic.random.randint(100, 500000)  # Change the range as needed
    return random_integer

def generer_produits(nombre_produits, nombre_images_par_produit):
    generic = Generic()

    subcategory = SubCategory.objects.all()
    event = Event.objects.all()
    #variantes=[obj['id'] for obj in Variantes.objects.all().values()]
    
    for _ in range(nombre_produits):
      
        name = generic.text.word()
        subcategory_aleatoire = generic.random.choice(subcategory)
        extras = generic.text.words()
        event_aleatoire = generic.random.choice(event)
        #variantes_aleatoire_id =[generic.random.choice(variantes) for _ in range(1)] 
        price = generate_random_integer()
        description = generic.text.text()
        description_precise = generic.text.text()
       
        

        # Créez l'objet Product sans enregistrement dans la base de données
        product = Products(name=name, sub_category=subcategory_aleatoire, extras=extras,
                           event=event_aleatoire,  price=price,description=description,
                           description_precise=description_precise)
        #variantes_aleatoire = Variantes.objects.filter(id__in=variantes_aleatoire_id)
        #product.variantes.set(variantes_aleatoire)
        product.save()

        for _ in range(nombre_images_par_produit):
            image_url = generate_random_image_url()
            img_temp = NamedTemporaryFile()
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()
            
            # Extraire l'extension de l'URL de l'image
            image_extension = os.path.splitext(urlparse(image_url).path)[-1]
            image_url=image_url+'.png'
            
            image = Image(product=product)
            image.image.save(os.path.basename(image_url), File(img_temp))
            image.save()
        

def generer_commandes(nombre_commandes, nombre_produits):
    generic = Generic()

    products = Products.objects.all()
    users = CustomUser.objects.all()
    #variantes=[obj['id'] for obj in Variantes.objects.all().values()]
    quantity_def = [1,2,3,4,5,6,7,8,9]
    for _ in range(nombre_commandes):
      
        user = generic.random.choice(users)

        # Créez l'objet Product sans enregistrement dans la base de données
        commande = Commandes(user=user)
        #variantes_aleatoire = Variantes.objects.filter(id__in=variantes_aleatoire_id)
        #product.variantes.set(variantes_aleatoire)
        commande.save()

        for _ in range(nombre_produits):
            product = generic.random.choice(products)
            quantity = generic.random.choice(quantity_def)

            produits_commandes = ProduitsCommandes(commande=commande,product=product, quantity=quantity)
            produits_commandes.save()