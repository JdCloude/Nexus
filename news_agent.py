#!/usr/bin/env python3
"""
Agente de Noticias Automatizado
==============================

Este script funciona como un agente de noticias automatizado que:
1. Consume feeds RSS de Google News
2. Extrae el contenido de los artículos
3. Genera resúmenes usando la API de OpenAI
4. Almacena los resultados en una base de datos de Notion

Instalación de dependencias:
pip install feedparser requests beautifulsoup4 openai notion-client python-dotenv

Autor: Desarrollador Python Senior
Fecha: 2024
"""

import os
import feedparser
import requests
from bs4 import BeautifulSoup
import openai
from notion_client import Client
from datetime import datetime
import time
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('news_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

class NewsAgent:
    """
    Clase principal del agente de noticias automatizado.
    Maneja la extracción, procesamiento y almacenamiento de noticias.
    """
    
    def __init__(self):
        """Inicializar el agente con las credenciales necesarias."""
        # Verificar variables de entorno
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.notion_database_id = os.getenv('NOTION_DATABASE_ID')
        
        if not all([self.openai_api_key, self.notion_token, self.notion_database_id]):
            raise ValueError(
                "Faltan variables de entorno requeridas. "
                "Asegúrate de tener configuradas: OPENAI_API_KEY, NOTION_TOKEN, NOTION_DATABASE_ID"
            )
        
        # Inicializar clientes
        openai.api_key = self.openai_api_key
        self.notion = Client(auth=self.notion_token)
        
        # Configuración del feed RSS (ejemplo con Google News)
        self.rss_url = "https://news.google.com/rss?hl=es&gl=ES&ceid=ES:es"
        
        # Headers para requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        logger.info("Agente de noticias inicializado correctamente")
    
    def get_article_content(self, url: str) -> Optional[str]:
        """
        Extrae el contenido principal de un artículo web.
        
        Args:
            url (str): URL del artículo a procesar
            
        Returns:
            Optional[str]: Texto limpio del artículo o None si hay error
        """
        try:
            logger.info(f"Extrayendo contenido de: {url}")
            
            # Realizar request con timeout
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # Parsear HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Eliminar elementos no deseados
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement']):
                element.decompose()
            
            # Estrategias para extraer contenido principal
            content_selectors = [
                'article',
                '[class*="content"]',
                '[class*="article"]',
                '[class*="post"]',
                '.entry-content',
                '.post-content',
                '.article-content',
                'main'
            ]
            
            content = None
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    # Tomar el elemento más largo (probablemente el contenido principal)
                    content = max(elements, key=lambda x: len(x.get_text()))
                    break
            
            if not content:
                # Fallback: usar el body completo
                content = soup.find('body')
            
            if content:
                # Extraer texto y limpiarlo
                text = content.get_text()
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                clean_text = ' '.join(lines)
                
                # Limitar longitud para evitar tokens excesivos
                if len(clean_text) > 8000:
                    clean_text = clean_text[:8000] + "..."
                
                logger.info(f"Contenido extraído exitosamente ({len(clean_text)} caracteres)")
                return clean_text
            else:
                logger.warning(f"No se pudo extraer contenido de: {url}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Error de red al acceder a {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado al procesar {url}: {e}")
            return None
    
    def summarize_with_openai(self, content: str) -> Optional[str]:
        """
        Genera un resumen del contenido usando la API de OpenAI.
        
        Args:
            content (str): Contenido del artículo a resumir
            
        Returns:
            Optional[str]: Resumen generado por la IA o None si hay error
        """
        try:
            logger.info("Generando resumen con OpenAI...")
            
            # Prompt del sistema para guiar a la IA
            system_prompt = """Eres un analista de noticias experto. Tu tarea es analizar el siguiente texto de un artículo y generar un resumen ejecutivo en español. El resumen debe estar en formato de lista (bullet points) y destacar los 3 a 5 puntos clave más importantes. Mantén un tono profesional y objetivo."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Por favor, analiza y resume el siguiente artículo:\n\n{content}"}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info("Resumen generado exitosamente")
            return summary
            
        except openai.error.OpenAIError as e:
            logger.error(f"Error de OpenAI: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado al generar resumen: {e}")
            return None
    
    def add_to_notion(self, title: str, url: str, summary: str, source: str) -> bool:
        """
        Añade un artículo a la base de datos de Notion.
        
        Args:
            title (str): Título del artículo
            url (str): URL del artículo
            summary (str): Resumen generado por la IA
            source (str): Fuente del artículo
            
        Returns:
            bool: True si se añadió exitosamente, False en caso contrario
        """
        try:
            logger.info(f"Añadiendo artículo a Notion: {title}")
            
            # Crear la página en Notion
            new_page = {
                "parent": {"database_id": self.notion_database_id},
                "properties": {
                    "Título del Artículo": {
                        "title": [
                            {
                                "text": {
                                    "content": title
                                }
                            }
                        ]
                    },
                    "URL": {
                        "url": url
                    },
                    "Resumen IA": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": summary
                                }
                            }
                        ]
                    },
                    "Fuente": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": source
                                }
                            }
                        ]
                    }
                }
            }
            
            response = self.notion.pages.create(**new_page)
            logger.info(f"Artículo añadido exitosamente a Notion con ID: {response['id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error al añadir artículo a Notion: {e}")
            return False
    
    def process_feed(self) -> None:
        """
        Procesa el feed RSS y ejecuta el pipeline completo de noticias.
        """
        try:
            logger.info("Iniciando procesamiento del feed RSS...")
            
            # Parsear el feed RSS
            feed = feedparser.parse(self.rss_url)
            
            if not feed.entries:
                logger.warning("No se encontraron entradas en el feed RSS")
                return
            
            logger.info(f"Encontradas {len(feed.entries)} entradas en el feed")
            
            processed_count = 0
            error_count = 0
            
            for entry in feed.entries[:10]:  # Limitar a 10 artículos por ejecución
                try:
                    title = entry.get('title', 'Sin título')
                    url = entry.get('link', '')
                    source = entry.get('source', {}).get('title', 'Fuente desconocida')
                    
                    logger.info(f"Procesando: {title}")
                    
                    # Extraer contenido del artículo
                    content = self.get_article_content(url)
                    if not content:
                        logger.warning(f"No se pudo extraer contenido de: {url}")
                        error_count += 1
                        continue
                    
                    # Generar resumen con OpenAI
                    summary = self.summarize_with_openai(content)
                    if not summary:
                        logger.warning(f"No se pudo generar resumen para: {url}")
                        error_count += 1
                        continue
                    
                    # Añadir a Notion
                    success = self.add_to_notion(title, url, summary, source)
                    if success:
                        processed_count += 1
                        logger.info(f"Artículo procesado exitosamente: {title}")
                    else:
                        error_count += 1
                    
                    # Pausa entre requests para ser respetuoso con las APIs
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error procesando entrada: {e}")
                    error_count += 1
                    continue
            
            logger.info(f"Procesamiento completado. Exitosos: {processed_count}, Errores: {error_count}")
            
        except Exception as e:
            logger.error(f"Error al procesar el feed RSS: {e}")
    
    def run(self) -> None:
        """
        Método principal para ejecutar el agente de noticias.
        """
        logger.info("=== INICIANDO AGENTE DE NOTICIAS ===")
        
        try:
            self.process_feed()
            logger.info("=== AGENTE DE NOTICIAS COMPLETADO ===")
        except Exception as e:
            logger.error(f"Error crítico en la ejecución del agente: {e}")
            raise


def main():
    """
    Función principal que orquesta todo el proceso.
    """
    try:
        agent = NewsAgent()
        agent.run()
    except Exception as e:
        logger.error(f"Error fatal en la aplicación: {e}")
        raise


if __name__ == "__main__":
    main() 