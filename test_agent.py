#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del agente de noticias.
Este script prueba cada componente individualmente antes de ejecutar el agente completo.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

def test_environment_variables():
    """Prueba que todas las variables de entorno estén configuradas."""
    logger.info("🔍 Probando variables de entorno...")
    
    required_vars = ['OPENAI_API_KEY', 'NOTION_TOKEN', 'NOTION_DATABASE_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Variables de entorno faltantes: {missing_vars}")
        return False
    else:
        logger.info("✅ Todas las variables de entorno están configuradas")
        return True

def test_dependencies():
    """Prueba que todas las dependencias estén instaladas."""
    logger.info("🔍 Probando dependencias...")
    
    dependencies = [
        'feedparser',
        'requests', 
        'beautifulsoup4',
        'openai',
        'notion_client',
        'dotenv'
    ]
    
    missing_deps = []
    
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
        except ImportError:
            missing_deps.append(dep)
    
    if missing_deps:
        logger.error(f"❌ Dependencias faltantes: {missing_deps}")
        logger.info("💡 Ejecuta: pip install -r requirements.txt")
        return False
    else:
        logger.info("✅ Todas las dependencias están instaladas")
        return True

def test_openai_connection():
    """Prueba la conexión con OpenAI."""
    logger.info("🔍 Probando conexión con OpenAI...")
    
    try:
        import openai
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Prueba simple con OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Responde solo con 'OK' si puedes leer este mensaje."}
            ],
            max_tokens=10
        )
        
        if response.choices[0].message.content.strip() == 'OK':
            logger.info("✅ Conexión con OpenAI exitosa")
            return True
        else:
            logger.error("❌ Respuesta inesperada de OpenAI")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error de conexión con OpenAI: {e}")
        return False

def test_notion_connection():
    """Prueba la conexión con Notion."""
    logger.info("🔍 Probando conexión con Notion...")
    
    try:
        from notion_client import Client
        
        notion = Client(auth=os.getenv('NOTION_TOKEN'))
        database_id = os.getenv('NOTION_DATABASE_ID')
        
        # Intentar obtener la base de datos
        database = notion.databases.retrieve(database_id)
        
        logger.info(f"✅ Conexión con Notion exitosa")
        logger.info(f"📋 Base de datos: {database.get('title', [{}])[0].get('text', {}).get('content', 'Sin título')}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error de conexión con Notion: {e}")
        return False

def test_rss_feed():
    """Prueba la conexión con el feed RSS."""
    logger.info("🔍 Probando feed RSS...")
    
    try:
        import feedparser
        
        # URL de prueba (Google News España)
        test_url = "https://news.google.com/rss?hl=es&gl=ES&ceid=ES:es"
        
        feed = feedparser.parse(test_url)
        
        if feed.entries:
            logger.info(f"✅ Feed RSS accesible - {len(feed.entries)} entradas encontradas")
            logger.info(f"📰 Ejemplo: {feed.entries[0].get('title', 'Sin título')}")
            return True
        else:
            logger.error("❌ No se encontraron entradas en el feed RSS")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error al acceder al feed RSS: {e}")
        return False

def test_web_scraping():
    """Prueba la funcionalidad de web scraping."""
    logger.info("🔍 Probando web scraping...")
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # URL de prueba (una página simple)
        test_url = "https://httpbin.org/html"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(test_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.get_text()
        
        if len(content) > 0:
            logger.info(f"✅ Web scraping funcional - {len(content)} caracteres extraídos")
            return True
        else:
            logger.error("❌ No se pudo extraer contenido")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error en web scraping: {e}")
        return False

def run_full_test():
    """Ejecuta todas las pruebas."""
    logger.info("🚀 Iniciando pruebas del agente de noticias")
    logger.info("=" * 50)
    
    tests = [
        ("Variables de entorno", test_environment_variables),
        ("Dependencias", test_dependencies),
        ("Conexión OpenAI", test_openai_connection),
        ("Conexión Notion", test_notion_connection),
        ("Feed RSS", test_rss_feed),
        ("Web Scraping", test_web_scraping)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Ejecutando: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                logger.error(f"❌ Prueba fallida: {test_name}")
        except Exception as e:
            logger.error(f"❌ Error en prueba {test_name}: {e}")
    
    logger.info("\n" + "=" * 50)
    logger.info(f"📊 Resultados: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        logger.info("🎉 ¡Todas las pruebas pasaron! El agente está listo para usar.")
        logger.info("💡 Ejecuta: python news_agent.py")
        return True
    else:
        logger.error("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        return False

def main():
    """Función principal del script de prueba."""
    try:
        success = run_full_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n⏹️ Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 