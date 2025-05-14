import openai
from django.conf import settings
from typing import Dict, Any
import requests
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class AIGameGenerator:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def generate_game_content(self, title: str, genre: str, ambiance: str) -> Dict[str, Any]:
        """Génère le contenu d'un jeu vidéo en utilisant l'IA."""
        
        # Prompt principal pour la génération
        prompt = f"""Crée un concept de jeu vidéo avec les caractéristiques suivantes :
        Titre : {title}
        Genre : {genre}
        Ambiance : {ambiance}

        Génère les sections suivantes :
        1. Une description concise du jeu
        2. Les mécaniques de gameplay principales
        3. L'histoire et le contexte
        4. Les personnages principaux
        5. L'environnement et l'univers du jeu

        Format de réponse souhaité :
        Description: [description]
        Gameplay: [gameplay]
        Histoire: [histoire]
        Personnages: [personnages]
        Environnement: [environnement]"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un expert en conception de jeux vidéo."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            # Traitement de la réponse
            content = response.choices[0].message.content
            
            # Parsing de la réponse
            sections = {}
            current_section = None
            current_content = []

            for line in content.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if line.endswith(':'):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = line[:-1].lower()
                    current_content = []
                else:
                    current_content.append(line)

            if current_section:
                sections[current_section] = '\n'.join(current_content)

            return {
                'description': sections.get('description', ''),
                'gameplay': sections.get('gameplay', ''),
                'story': sections.get('histoire', ''),
                'characters': sections.get('personnages', ''),
                'environment': sections.get('environnement', '')
            }

        except Exception as e:
            raise Exception(f"Erreur lors de la génération du contenu : {str(e)}")

    def generate_concept_art(self, title: str, genre: str, ambiance: str) -> str:
        """Génère l'art conceptuel du jeu en utilisant DALL-E."""
        try:
            # Génération du prompt pour DALL-E
            prompt = self.generate_concept_art_prompt(title, genre, ambiance)
            
            # Appel à l'API DALL-E
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024",
                response_format="url"
            )
            
            # Récupération de l'URL de l'image
            image_url = response['data'][0]['url']
            
            # Téléchargement de l'image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Création du nom de fichier
                filename = f"concept_art_{title.lower().replace(' ', '_')}.png"
                
                # Sauvegarde de l'image
                file_path = default_storage.save(f'concept_art/{filename}', ContentFile(image_response.content))
                return file_path
            else:
                raise Exception("Erreur lors du téléchargement de l'image")
                
        except Exception as e:
            raise Exception(f"Erreur lors de la génération de l'art conceptuel : {str(e)}")

    def generate_concept_art_prompt(self, title: str, genre: str, ambiance: str) -> str:
        """Génère un prompt pour la création d'art conceptuel."""
        return f"""Crée une image conceptuelle pour un jeu vidéo avec les caractéristiques suivantes :
        Titre : {title}
        Genre : {genre}
        Ambiance : {ambiance}
        
        Style : Art conceptuel de jeu vidéo, détaillé, atmosphérique
        Format : 16:9, haute résolution
        Éléments clés : Représente l'ambiance générale du jeu, incluant des éléments caractéristiques du genre""" 