import random
import requests
from typing import List, Dict
import time
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import logging
import argparse
import re
from urllib.parse import quote

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Chargement des variables d'environnement
load_dotenv()

USER_AGENT = "TYPO3ContentCraft/1.0 (https://votre-site.com; votre-email@example.com)"

# Configuration de la base de données
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT')
}

def get_database_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        logging.error(f"Erreur lors de la connexion à MySQL: {e}")
    return None

def clean_theme(theme):
    # Supprime les caractères spéciaux et les espaces excessifs
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', theme)).strip()

def get_wikipedia_content(theme: str, language: str, num_words: int) -> Dict[str, str]:
    base_url = f"https://{language}.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": theme,
        "srlimit": "1"
    }
    headers = {"User-Agent": USER_AGENT}
    
    try:
        search_response = requests.get(base_url, params=search_params, headers=headers)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        if search_data["query"]["search"]:
            page_title = search_data["query"]["search"][0]["title"]
            
            content_params = {
                "action": "query",
                "format": "json",
                "titles": page_title,
                "prop": "extracts",
                "exintro": True,
                "explaintext": True,
            }
            
            content_response = requests.get(base_url, params=content_params, headers=headers)
            content_response.raise_for_status()
            content_data = content_response.json()
            
            page = next(iter(content_data["query"]["pages"].values()))
            if "extract" in page:
                summary = page["extract"]
                words = summary.split()
                if len(words) > num_words:
                    summary = ' '.join(words[:num_words]) + '...'
                return {
                    "title": generate_title(theme),
                    "body": summary
                }
        
        # Si aucun résultat n'est trouvé, essayez avec les mots-clés
        keywords = clean_theme(theme).split()
        for keyword in keywords:
            keyword_params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": keyword,
                "srlimit": "1"
            }
            keyword_response = requests.get(base_url, params=keyword_params, headers=headers)
            keyword_response.raise_for_status()
            keyword_data = keyword_response.json()
            
            if keyword_data["query"]["search"]:
                page_title = keyword_data["query"]["search"][0]["title"]
                return get_wikipedia_content(page_title, language, num_words)
        
        return {"title": generate_title(theme), "body": f"Contenu sur {theme} non trouvé."}
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la récupération du contenu Wikipedia: {e}")
        return {"title": generate_title(theme), "body": f"Erreur lors de la récupération du contenu sur {theme}."}

def generate_title(theme: str) -> str:
    templates = [
        f"Les bases de {theme}",
        f"Tout savoir sur {theme}",
        f"Exploration de {theme}",
        f"{theme} : un guide complet",
        f"Découvrez {theme}",
        f"L'essentiel de {theme}",
        f"{theme} pour les débutants",
        f"Les secrets de {theme}",
        f"Le monde fascinant de {theme}",
        f"{theme} : mythes et réalités"
    ]
    return random.choice(templates)

def create_pages_and_content(connection, parent_id: int, num_pages: int, language: str, themes: List[str], num_words: int):
    cursor = connection.cursor(dictionary=True)
    current_time = int(time.time())

    try:
        insert_page_query = """
        INSERT INTO pages (pid, title, doktype, slug, sys_language_uid, hidden, deleted, crdate, tstamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        insert_content_query = """
        INSERT INTO tt_content (pid, CType, header, bodytext, sys_language_uid, colPos, crdate, tstamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        for i in range(num_pages):
            theme = random.choice(themes)
            content = get_wikipedia_content(theme, language, num_words)

            base_slug = quote(content['title'].lower().replace(' ', '-'))
            slug = base_slug
            j = 1
            while True:
                cursor.execute("SELECT COUNT(*) as count FROM pages WHERE slug = %s", (slug,))
                if cursor.fetchone()['count'] == 0:
                    break
                slug = f"{base_slug}-{j}"
                j += 1

            page_values = (parent_id, content['title'], 1, slug, get_language_id(language), 0, 0, current_time, current_time)
            cursor.execute(insert_page_query, page_values)
            page_id = cursor.lastrowid

            content_values = (page_id, 'text', content['title'], content['body'], get_language_id(language), 0, current_time, current_time)
            cursor.execute(insert_content_query, content_values)

            connection.commit()
            logging.info(f"Page créée : {content['title']}")

    except Error as e:
        logging.error(f"Erreur lors de la création des pages : {e}")
        connection.rollback()
    finally:
        cursor.close()

def get_language_id(language: str) -> int:
    language_map = {"fr": 0, "en": 1, "de": 2} 
    return language_map.get(language, 0)

def main():
    parser = argparse.ArgumentParser(description="Générateur de pages TYPO3")
    parser.add_argument("--parent_id", type=int, help="ID de la page parente")
    parser.add_argument("--num_pages", type=int, help="Nombre de pages à créer")
    parser.add_argument("--language", help="Code de la langue (ex: fr, en)")
    parser.add_argument("--num_words", type=int, help="Nombre de mots pour le contenu")
    parser.add_argument("--themes", help="Thématiques séparées par des virgules")
    args = parser.parse_args()

    connection = get_database_connection()
    if not connection:
        logging.error("Impossible de se connecter à la base de données. Vérifiez vos paramètres de connexion.")
        return

    try:
        parent_id = args.parent_id if args.parent_id is not None else int(input("Entrez l'ID de la page parente : "))
        num_pages = args.num_pages if args.num_pages is not None else int(input("Entrez le nombre de pages à créer : "))
        language = args.language if args.language is not None else input("Entrez le code de la langue (ex: fr pour français, en pour anglais) : ")
        num_words = args.num_words if args.num_words is not None else int(input("Entrez le nombre de mots pour le contenu : "))

        if args.themes:
            themes = [theme.strip() for theme in args.themes.split(',')]
        else:
            print("Entrez les thématiques souhaitées (séparées par des virgules) :")
            themes_input = input()
            themes = [theme.strip() for theme in themes_input.split(',')]

        create_pages_and_content(connection, parent_id, num_pages, language, themes, num_words)

        logging.info(f"{num_pages} pages ont été créées avec succès dans la base de données TYPO3.")

    except Exception as e:
        logging.error(f"Une erreur est survenue : {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
            logging.info("La connexion à la base de données est fermée.")

if __name__ == "__main__":
    main()