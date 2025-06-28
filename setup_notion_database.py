#!/usr/bin/env python3
"""
Script auxiliar para configurar automáticamente la base de datos de Notion
para el agente de noticias automatizado.

Este script crea una nueva base de datos en Notion con las propiedades
correctas para almacenar los artículos procesados.
"""

import os
from notion_client import Client
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

def setup_notion_database():
    """
    Crea una nueva base de datos en Notion con las propiedades necesarias
    para el agente de noticias.
    """
    try:
        # Verificar token de Notion
        notion_token = os.getenv('NOTION_TOKEN')
        if not notion_token:
            raise ValueError("NOTION_TOKEN no encontrado en variables de entorno")
        
        # Inicializar cliente de Notion
        notion = Client(auth=notion_token)
        
        # Obtener página padre (puedes cambiar esto por el ID de tu workspace o página)
        # Por defecto, usará tu workspace principal
        parent_page_id = None
        
        logger.info("Creando base de datos en Notion...")
        
        # Crear la base de datos
        database = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id} if parent_page_id else {"type": "workspace"},
            title=[
                {
                    "type": "text",
                    "text": {
                        "content": "📰 Artículos de Noticias - Agente IA"
                    }
                }
            ],
            properties={
                "Título del Artículo": {
                    "title": {}
                },
                "URL": {
                    "url": {}
                },
                "Resumen IA": {
                    "rich_text": {}
                },
                "Fuente": {
                    "rich_text": {}
                },
                "Fecha de Procesamiento": {
                    "date": {}
                },
                "Estado": {
                    "select": {
                        "options": [
                            {
                                "name": "Nuevo",
                                "color": "blue"
                            },
                            {
                                "name": "Procesado",
                                "color": "green"
                            },
                            {
                                "name": "Error",
                                "color": "red"
                            }
                        ]
                    }
                }
            }
        )
        
        database_id = database['id']
        database_url = database['url']
        
        logger.info(f"✅ Base de datos creada exitosamente!")
        logger.info(f"📋 ID de la base de datos: {database_id}")
        logger.info(f"🔗 URL de la base de datos: {database_url}")
        logger.info("\n📝 Añade esta línea a tu archivo .env:")
        logger.info(f"NOTION_DATABASE_ID={database_id}")
        
        return database_id, database_url
        
    except Exception as e:
        logger.error(f"❌ Error al crear la base de datos: {e}")
        raise

def verify_database_structure(database_id):
    """
    Verifica que la base de datos tiene la estructura correcta.
    """
    try:
        notion_token = os.getenv('NOTION_TOKEN')
        notion = Client(auth=notion_token)
        
        # Obtener la base de datos
        database = notion.databases.retrieve(database_id)
        
        logger.info("🔍 Verificando estructura de la base de datos...")
        
        # Verificar propiedades requeridas
        required_properties = [
            "Título del Artículo",
            "URL", 
            "Resumen IA",
            "Fuente"
        ]
        
        existing_properties = list(database['properties'].keys())
        
        missing_properties = []
        for prop in required_properties:
            if prop not in existing_properties:
                missing_properties.append(prop)
        
        if missing_properties:
            logger.warning(f"⚠️ Propiedades faltantes: {missing_properties}")
            return False
        else:
            logger.info("✅ Todas las propiedades requeridas están presentes")
            return True
            
    except Exception as e:
        logger.error(f"❌ Error al verificar la base de datos: {e}")
        return False

def main():
    """
    Función principal del script de configuración.
    """
    logger.info("🚀 Configurador de Base de Datos de Notion")
    logger.info("=" * 50)
    
    try:
        # Crear nueva base de datos
        database_id, database_url = setup_notion_database()
        
        # Verificar estructura
        if verify_database_structure(database_id):
            logger.info("\n🎉 Configuración completada exitosamente!")
            logger.info("📋 Próximos pasos:")
            logger.info("1. Copia el ID de la base de datos a tu archivo .env")
            logger.info("2. Ejecuta el agente de noticias: python news_agent.py")
        else:
            logger.error("❌ La base de datos no tiene la estructura correcta")
            
    except Exception as e:
        logger.error(f"❌ Error en la configuración: {e}")
        logger.info("\n💡 Solución de problemas:")
        logger.info("1. Verifica que tu NOTION_TOKEN es válido")
        logger.info("2. Asegúrate de que tu integración tiene permisos de escritura")
        logger.info("3. Revisa los logs para más detalles")

if __name__ == "__main__":
    main() 