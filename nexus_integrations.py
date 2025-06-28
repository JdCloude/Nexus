#!/usr/bin/env python3
"""
Integraciones de Nexus con Plataformas Externas
==============================================

Módulo que maneja las integraciones nativas de Nexus con plataformas de colaboración
como Slack, Google Meet, Teams, Jira, etc. Permite que Nexus se integre de forma
transparente en el flujo de trabajo existente.
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from abc import ABC, abstractmethod
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

class PlatformIntegration(ABC):
    """Clase base para integraciones con plataformas externas."""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.is_connected = False
        self.webhook_url = None
        self.api_token = None
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establece conexión con la plataforma."""
        pass
    
    @abstractmethod
    async def send_message(self, channel: str, message: str, **kwargs) -> bool:
        """Envía un mensaje a la plataforma."""
        pass
    
    @abstractmethod
    async def get_conversation_history(self, channel: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtiene el historial de conversación."""
        pass
    
    @abstractmethod
    async def listen_for_events(self, callback: Callable) -> None:
        """Escucha eventos de la plataforma."""
        pass

class SlackIntegration(PlatformIntegration):
    """Integración con Slack."""
    
    def __init__(self):
        super().__init__("slack")
        self.api_token = os.getenv('SLACK_BOT_TOKEN')
        self.webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        self.client = None
    
    async def connect(self) -> bool:
        """Conecta con la API de Slack."""
        try:
            # En producción, usaría la librería oficial de Slack
            # from slack_sdk import WebClient
            # self.client = WebClient(token=self.api_token)
            
            # Verificación simple de conexión
            if self.api_token:
                self.is_connected = True
                logger.info("✅ Conexión con Slack establecida")
                return True
            else:
                logger.error("❌ Token de Slack no configurado")
                return False
                
        except Exception as e:
            logger.error(f"Error conectando con Slack: {e}")
            return False
    
    async def send_message(self, channel: str, message: str, **kwargs) -> bool:
        """Envía un mensaje a un canal de Slack."""
        try:
            if not self.is_connected:
                await self.connect()
            
            # Usar webhook para envío simple
            if self.webhook_url:
                payload = {
                    "channel": channel,
                    "text": message,
                    "username": "Nexus",
                    "icon_emoji": ":robot_face:"
                }
                
                response = requests.post(self.webhook_url, json=payload)
                if response.status_code == 200:
                    logger.info(f"Mensaje enviado a Slack: {channel}")
                    return True
                else:
                    logger.error(f"Error enviando mensaje a Slack: {response.status_code}")
                    return False
            
            return False
            
        except Exception as e:
            logger.error(f"Error enviando mensaje a Slack: {e}")
            return False
    
    async def get_conversation_history(self, channel: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtiene el historial de conversación de un canal."""
        try:
            # En producción, usaría la API de Slack para obtener historial real
            # messages = self.client.conversations_history(channel=channel, limit=limit)
            
            # Simulación de historial
            mock_history = [
                {
                    "user": "user1",
                    "text": "Hola equipo, necesitamos implementar el nuevo endpoint",
                    "timestamp": datetime.now().isoformat(),
                    "channel": channel
                },
                {
                    "user": "user2", 
                    "text": "Perfecto, ¿cuáles son los requisitos?",
                    "timestamp": datetime.now().isoformat(),
                    "channel": channel
                }
            ]
            
            return mock_history
            
        except Exception as e:
            logger.error(f"Error obteniendo historial de Slack: {e}")
            return []
    
    async def listen_for_events(self, callback: Callable) -> None:
        """Escucha eventos de Slack (mentions, messages, etc.)."""
        # En producción, implementaría un webhook endpoint
        # para recibir eventos de Slack en tiempo real
        logger.info("Escuchando eventos de Slack...")
        
        # Simulación de eventos
        while True:
            await asyncio.sleep(5)
            # Simular eventos periódicamente
            pass

class GoogleMeetIntegration(PlatformIntegration):
    """Integración con Google Meet."""
    
    def __init__(self):
        super().__init__("google_meet")
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.credentials = os.getenv('GOOGLE_CREDENTIALS')
    
    async def connect(self) -> bool:
        """Conecta con la API de Google Meet."""
        try:
            if self.api_key and self.credentials:
                self.is_connected = True
                logger.info("✅ Conexión con Google Meet establecida")
                return True
            else:
                logger.error("❌ Credenciales de Google Meet no configuradas")
                return False
                
        except Exception as e:
            logger.error(f"Error conectando con Google Meet: {e}")
            return False
    
    async def send_message(self, meeting_id: str, message: str, **kwargs) -> bool:
        """Envía un mensaje a una reunión de Google Meet."""
        try:
            if not self.is_connected:
                await self.connect()
            
            # En producción, usaría la API de Google Meet
            logger.info(f"Mensaje enviado a Google Meet: {meeting_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando mensaje a Google Meet: {e}")
            return False
    
    async def get_conversation_history(self, meeting_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtiene la transcripción de una reunión."""
        try:
            # En producción, usaría la API de Google Meet para obtener transcripciones
            mock_transcript = [
                {
                    "speaker": "Juan",
                    "text": "Bienvenidos a la reunión de planificación",
                    "timestamp": "00:00:10"
                },
                {
                    "speaker": "María",
                    "text": "Gracias, vamos a revisar los objetivos del sprint",
                    "timestamp": "00:00:25"
                }
            ]
            
            return mock_transcript
            
        except Exception as e:
            logger.error(f"Error obteniendo transcripción de Google Meet: {e}")
            return []
    
    async def listen_for_events(self, callback: Callable) -> None:
        """Escucha eventos de Google Meet."""
        logger.info("Escuchando eventos de Google Meet...")
        # Implementar webhook para eventos de Meet

class JiraIntegration(PlatformIntegration):
    """Integración con Jira."""
    
    def __init__(self):
        super().__init__("jira")
        self.api_token = os.getenv('JIRA_API_TOKEN')
        self.base_url = os.getenv('JIRA_BASE_URL')
        self.username = os.getenv('JIRA_USERNAME')
    
    async def connect(self) -> bool:
        """Conecta con la API de Jira."""
        try:
            if all([self.api_token, self.base_url, self.username]):
                self.is_connected = True
                logger.info("✅ Conexión con Jira establecida")
                return True
            else:
                logger.error("❌ Credenciales de Jira no configuradas")
                return False
                
        except Exception as e:
            logger.error(f"Error conectando con Jira: {e}")
            return False
    
    async def create_ticket(self, project_key: str, summary: str, description: str, 
                          issue_type: str = "Task", assignee: str = None) -> Dict[str, Any]:
        """Crea un ticket en Jira."""
        try:
            if not self.is_connected:
                await self.connect()
            
            # En producción, usaría la API de Jira
            ticket_data = {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type}
            }
            
            if assignee:
                ticket_data["assignee"] = {"name": assignee}
            
            # Simular creación de ticket
            mock_ticket = {
                "id": "JIRA-12345",
                "key": f"{project_key}-12345",
                "summary": summary,
                "status": "To Do",
                "assignee": assignee,
                "created": datetime.now().isoformat()
            }
            
            logger.info(f"Ticket creado en Jira: {mock_ticket['key']}")
            return mock_ticket
            
        except Exception as e:
            logger.error(f"Error creando ticket en Jira: {e}")
            return {"error": str(e)}
    
    async def update_ticket(self, ticket_key: str, updates: Dict[str, Any]) -> bool:
        """Actualiza un ticket en Jira."""
        try:
            if not self.is_connected:
                await self.connect()
            
            # En producción, usaría la API de Jira
            logger.info(f"Ticket actualizado en Jira: {ticket_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error actualizando ticket en Jira: {e}")
            return False
    
    async def get_ticket(self, ticket_key: str) -> Dict[str, Any]:
        """Obtiene información de un ticket."""
        try:
            if not self.is_connected:
                await self.connect()
            
            # Simular obtención de ticket
            mock_ticket = {
                "key": ticket_key,
                "summary": "Implementar nuevo endpoint",
                "description": "Crear endpoint para gestión de usuarios",
                "status": "In Progress",
                "assignee": "dev-team",
                "priority": "Medium"
            }
            
            return mock_ticket
            
        except Exception as e:
            logger.error(f"Error obteniendo ticket de Jira: {e}")
            return {"error": str(e)}

class NotionIntegration(PlatformIntegration):
    """Integración con Notion."""
    
    def __init__(self):
        super().__init__("notion")
        self.api_token = os.getenv('NOTION_TOKEN')
        self.database_id = os.getenv('NOTION_DATABASE_ID')
    
    async def connect(self) -> bool:
        """Conecta con la API de Notion."""
        try:
            if self.api_token and self.database_id:
                self.is_connected = True
                logger.info("✅ Conexión con Notion establecida")
                return True
            else:
                logger.error("❌ Credenciales de Notion no configuradas")
                return False
                
        except Exception as e:
            logger.error(f"Error conectando con Notion: {e}")
            return False
    
    async def create_page(self, title: str, content: str, properties: Dict[str, Any] = None) -> Dict[str, Any]:
        """Crea una nueva página en Notion."""
        try:
            if not self.is_connected:
                await self.connect()
            
            # En producción, usaría la API de Notion
            page_data = {
                "id": f"page_{datetime.now().timestamp()}",
                "title": title,
                "content": content,
                "properties": properties or {},
                "created": datetime.now().isoformat()
            }
            
            logger.info(f"Página creada en Notion: {title}")
            return page_data
            
        except Exception as e:
            logger.error(f"Error creando página en Notion: {e}")
            return {"error": str(e)}

class IntegrationManager:
    """Gestor central de todas las integraciones de Nexus."""
    
    def __init__(self):
        self.integrations: Dict[str, PlatformIntegration] = {}
        self.nexus_core = None  # Referencia al núcleo de Nexus
    
    def register_integration(self, integration: PlatformIntegration):
        """Registra una nueva integración."""
        self.integrations[integration.platform_name] = integration
        logger.info(f"Integración registrada: {integration.platform_name}")
    
    async def initialize_all_integrations(self):
        """Inicializa todas las integraciones registradas."""
        for name, integration in self.integrations.items():
            try:
                success = await integration.connect()
                if success:
                    logger.info(f"✅ {name} inicializado correctamente")
                else:
                    logger.warning(f"⚠️ {name} no pudo inicializarse")
            except Exception as e:
                logger.error(f"❌ Error inicializando {name}: {e}")
    
    async def send_message_to_platform(self, platform: str, target: str, 
                                     message: str, **kwargs) -> bool:
        """Envía un mensaje a una plataforma específica."""
        if platform in self.integrations:
            return await self.integrations[platform].send_message(target, message, **kwargs)
        else:
            logger.error(f"Plataforma no registrada: {platform}")
            return False
    
    async def get_context_from_platform(self, platform: str, source: str, 
                                      limit: int = 100) -> List[Dict[str, Any]]:
        """Obtiene contexto de una plataforma específica."""
        if platform in self.integrations:
            return await self.integrations[platform].get_conversation_history(source, limit)
        else:
            logger.error(f"Plataforma no registrada: {platform}")
            return []
    
    def set_nexus_core(self, nexus_core):
        """Establece referencia al núcleo de Nexus."""
        self.nexus_core = nexus_core
    
    async def handle_platform_event(self, platform: str, event_data: Dict[str, Any]):
        """Maneja eventos de plataformas externas."""
        if not self.nexus_core:
            logger.error("Nexus core no configurado")
            return
        
        try:
            # Procesar evento con Nexus
            if platform == "slack":
                await self._handle_slack_event(event_data)
            elif platform == "google_meet":
                await self._handle_meet_event(event_data)
            elif platform == "jira":
                await self._handle_jira_event(event_data)
            else:
                logger.warning(f"Plataforma no manejada: {platform}")
                
        except Exception as e:
            logger.error(f"Error manejando evento de {platform}: {e}")
    
    async def _handle_slack_event(self, event_data: Dict[str, Any]):
        """Maneja eventos específicos de Slack."""
        event_type = event_data.get("type")
        
        if event_type == "message":
            # Mensaje nuevo en Slack
            channel = event_data.get("channel")
            user = event_data.get("user")
            text = event_data.get("text", "")
            
            # Añadir contexto a Nexus
            self.nexus_core.add_conversation_context(
                platform="slack",
                conversation_id=channel,
                participants=[user],
                content=text,
                metadata={"event_type": event_type}
            )
            
            # Verificar si Nexus es mencionado
            if "nexus" in text.lower() or "<@nexus>" in text:
                # Procesar comando con Nexus
                result = await self.nexus_core.process_natural_language_command(text)
                
                # Responder en Slack
                await self.send_message_to_platform(
                    "slack", 
                    channel, 
                    f"Procesando tu solicitud...\n{result['synthesis']}"
                )
    
    async def _handle_meet_event(self, event_data: Dict[str, Any]):
        """Maneja eventos específicos de Google Meet."""
        event_type = event_data.get("type")
        
        if event_type == "meeting_started":
            # Nueva reunión iniciada
            meeting_id = event_data.get("meeting_id")
            participants = event_data.get("participants", [])
            
            # Añadir contexto de reunión
            self.nexus_core.add_conversation_context(
                platform="google_meet",
                conversation_id=meeting_id,
                participants=participants,
                content="Reunión iniciada",
                metadata={"event_type": event_type}
            )
    
    async def _handle_jira_event(self, event_data: Dict[str, Any]):
        """Maneja eventos específicos de Jira."""
        event_type = event_data.get("type")
        
        if event_type == "issue_created":
            # Nuevo ticket creado
            issue_key = event_data.get("issue_key")
            summary = event_data.get("summary")
            
            # Añadir contexto de decisión
            self.nexus_core.add_decision_context(
                decision_id=issue_key,
                decision=f"Crear ticket: {summary}",
                rationale="Ticket creado en Jira",
                participants=["jira-system"],
                project_id=event_data.get("project_key")
            )

# Instancia global del gestor de integraciones
integration_manager = IntegrationManager()

# Registrar integraciones por defecto
integration_manager.register_integration(SlackIntegration())
integration_manager.register_integration(GoogleMeetIntegration())
integration_manager.register_integration(JiraIntegration())
integration_manager.register_integration(NotionIntegration())

async def initialize_integrations():
    """Inicializa todas las integraciones."""
    await integration_manager.initialize_all_integrations()

if __name__ == "__main__":
    # Prueba de integraciones
    asyncio.run(initialize_integrations()) 