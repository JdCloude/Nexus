#!/usr/bin/env python3
"""
Nexus Voice Integration - ElevenLabs Integration
===============================================

Integración avanzada de ElevenLabs con Nexus para crear agentes conversacionales
con capacidades de voz realistas y transferencias entre agentes especializados.

Características:
- Síntesis de voz en tiempo real con ElevenLabs
- Clonación de voz personalizada
- Transferencias entre agentes especializados
- Agentes conversacionales con memoria persistente
- Integración con el ecosistema Nexus
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import requests
from elevenlabs import ElevenLabs, Voice, VoiceSettings
from elevenlabs.api import History
from elevenlabs import generate, clone, voices, set_api_key
from nexus_core import NexusOrchestrator, ContextItem, Task, AgentType

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceModel(Enum):
    """Modelos de voz disponibles en ElevenLabs."""
    ELEVEN_V3 = "eleven_v3"
    ELEVEN_MULTILINGUAL_V2 = "eleven_multilingual_v2"
    ELEVEN_FLASH_V2_5 = "eleven_flash_v2_5"
    ELEVEN_TURBO_V2_5 = "eleven_turbo_v2_5"

@dataclass
class VoiceConfig:
    """Configuración de voz para agentes Nexus."""
    voice_id: str
    model: VoiceModel
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True
    language: str = "en"

@dataclass
class ConversationContext:
    """Contexto de conversación con capacidades de voz."""
    conversation_id: str
    user_id: str
    current_agent: str
    voice_config: VoiceConfig
    conversation_history: List[Dict[str, Any]]
    transferred_from: Optional[str] = None
    transfer_reason: Optional[str] = None

class NexusVoiceAgent:
    """
    Agente conversacional de Nexus con capacidades de voz avanzadas.
    Integra ElevenLabs para síntesis de voz realista y transferencias entre agentes.
    """
    
    def __init__(self, api_key: str, nexus_core: NexusOrchestrator):
        self.elevenlabs = ElevenLabs(api_key=api_key)
        self.nexus_core = nexus_core
        self.voice_agents: Dict[str, VoiceAgent] = {}
        self.conversation_contexts: Dict[str, ConversationContext] = {}
        self.transfer_rules: Dict[str, List[Dict[str, Any]]] = {}
        
        # Configurar agentes de voz especializados
        self._setup_voice_agents()
        self._setup_transfer_rules()
        
        logger.info("Nexus Voice Agent inicializado con ElevenLabs")
    
    def _setup_voice_agents(self):
        """Configura los agentes de voz especializados."""
        self.voice_agents = {
            "nexus_dev": VoiceAgent(
                name="NexusDev",
                description="Especialista en desarrollo de código y tecnología",
                voice_config=VoiceConfig(
                    voice_id="pNInz6obpgDQGcFmaJgB",  # Adam - voz técnica
                    model=VoiceModel.ELEVEN_V3,
                    stability=0.7,
                    similarity_boost=0.8
                ),
                capabilities=["code_generation", "technical_support", "debugging"]
            ),
            "nexus_hr": VoiceAgent(
                name="NexusHR",
                description="Especialista en recursos humanos y onboarding",
                voice_config=VoiceConfig(
                    voice_id="EXAVITQu4vr4xnSDxMaL",  # Bella - voz amigable
                    model=VoiceModel.ELEVEN_V3,
                    stability=0.8,
                    similarity_boost=0.9
                ),
                capabilities=["onboarding", "hr_support", "policy_questions"]
            ),
            "nexus_sales": VoiceAgent(
                name="NexusSales",
                description="Especialista en ventas y relaciones con clientes",
                voice_config=VoiceConfig(
                    voice_id="VR6AewLTigWG4xSOukaG",  # Josh - voz profesional
                    model=VoiceModel.ELEVEN_V3,
                    stability=0.6,
                    similarity_boost=0.85
                ),
                capabilities=["sales_support", "demo_preparation", "lead_qualification"]
            ),
            "nexus_support": VoiceAgent(
                name="NexusSupport",
                description="Especialista en soporte técnico y resolución de problemas",
                voice_config=VoiceConfig(
                    voice_id="pNInz6obpgDQGcFmaJgB",  # Adam - voz técnica
                    model=VoiceModel.ELEVEN_FLASH_V2_5,
                    stability=0.5,
                    similarity_boost=0.75
                ),
                capabilities=["technical_support", "troubleshooting", "bug_reports"]
            ),
            "nexus_analyst": VoiceAgent(
                name="NexusAnalyst",
                description="Especialista en análisis de datos y reportes",
                voice_config=VoiceConfig(
                    voice_id="VR6AewLTigWG4xSOukaG",  # Josh - voz profesional
                    model=VoiceModel.ELEVEN_V3,
                    stability=0.7,
                    similarity_boost=0.8
                ),
                capabilities=["data_analysis", "reporting", "insights"]
            )
        }
    
    def _setup_transfer_rules(self):
        """Configura las reglas de transferencia entre agentes."""
        self.transfer_rules = {
            "nexus_dev": [
                {
                    "condition": "technical_question",
                    "target_agent": "nexus_support",
                    "reason": "Transferring to technical support specialist"
                },
                {
                    "condition": "code_generation",
                    "target_agent": "nexus_dev",
                    "reason": "Transferring to development specialist"
                }
            ],
            "nexus_hr": [
                {
                    "condition": "technical_question",
                    "target_agent": "nexus_dev",
                    "reason": "Transferring to technical specialist"
                },
                {
                    "condition": "sales_question",
                    "target_agent": "nexus_sales",
                    "reason": "Transferring to sales specialist"
                }
            ],
            "nexus_sales": [
                {
                    "condition": "technical_question",
                    "target_agent": "nexus_dev",
                    "reason": "Transferring to technical specialist"
                },
                {
                    "condition": "support_question",
                    "target_agent": "nexus_support",
                    "reason": "Transferring to sales specialist"
                }
            ],
            "nexus_support": [
                {
                    "condition": "development_question",
                    "target_agent": "nexus_dev",
                    "reason": "Transferring to development specialist"
                },
                {
                    "condition": "data_analysis",
                    "target_agent": "nexus_analyst",
                    "reason": "Transferring to data analyst"
                }
            ]
        }
    
    async def start_conversation(self, user_id: str, initial_agent: str = "nexus_dev") -> str:
        """Inicia una nueva conversación con capacidades de voz."""
        conversation_id = f"conv_{user_id}_{datetime.now().timestamp()}"
        
        # Crear contexto de conversación
        voice_agent = self.voice_agents[initial_agent]
        context = ConversationContext(
            conversation_id=conversation_id,
            user_id=user_id,
            current_agent=initial_agent,
            voice_config=voice_agent.voice_config,
            conversation_history=[]
        )
        
        self.conversation_contexts[conversation_id] = context
        
        # Generar mensaje de bienvenida con voz
        welcome_message = f"¡Hola! Soy {voice_agent.name}, tu {voice_agent.description.lower()}. ¿En qué puedo ayudarte hoy?"
        
        # Generar audio de bienvenida
        audio_url = await self._generate_speech(welcome_message, voice_agent.voice_config)
        
        # Añadir al historial
        context.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "agent": initial_agent,
            "message": welcome_message,
            "audio_url": audio_url,
            "type": "welcome"
        })
        
        logger.info(f"Conversación iniciada: {conversation_id} con agente {initial_agent}")
        
        return conversation_id
    
    async def process_message(self, conversation_id: str, user_message: str) -> Dict[str, Any]:
        """Procesa un mensaje del usuario y genera respuesta con voz."""
        if conversation_id not in self.conversation_contexts:
            raise ValueError(f"Conversación no encontrada: {conversation_id}")
        
        context = self.conversation_contexts[conversation_id]
        current_agent = self.voice_agents[context.current_agent]
        
        # Añadir mensaje del usuario al historial
        context.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": context.user_id,
            "message": user_message,
            "type": "user_input"
        })
        
        # Analizar si necesita transferencia
        transfer_info = await self._analyze_transfer_needed(user_message, context.current_agent)
        
        if transfer_info["should_transfer"]:
            # Realizar transferencia de agente
            new_agent_id = transfer_info["target_agent"]
            new_agent = self.voice_agents[new_agent_id]
            
            transfer_message = f"Te transfiero a {new_agent.name}, {new_agent.description.lower()}. {transfer_info['reason']}"
            
            # Generar audio de transferencia
            transfer_audio = await self._generate_speech(transfer_message, current_agent.voice_config)
            
            # Actualizar contexto
            context.current_agent = new_agent_id
            context.voice_config = new_agent.voice_config
            context.transferred_from = current_agent.name
            context.transfer_reason = transfer_info["reason"]
            
            # Generar respuesta del nuevo agente
            agent_response = await self._generate_agent_response(user_message, new_agent, context)
            response_audio = await self._generate_speech(agent_response, new_agent.voice_config)
            
            # Añadir al historial
            context.conversation_history.extend([
                {
                    "timestamp": datetime.now().isoformat(),
                    "agent": current_agent.name,
                    "message": transfer_message,
                    "audio_url": transfer_audio,
                    "type": "transfer"
                },
                {
                    "timestamp": datetime.now().isoformat(),
                    "agent": new_agent.name,
                    "message": agent_response,
                    "audio_url": response_audio,
                    "type": "agent_response"
                }
            ])
            
            return {
                "conversation_id": conversation_id,
                "transfer": True,
                "from_agent": current_agent.name,
                "to_agent": new_agent.name,
                "transfer_message": transfer_message,
                "transfer_audio": transfer_audio,
                "response": agent_response,
                "response_audio": response_audio,
                "context": asdict(context)
            }
        else:
            # Generar respuesta del agente actual
            agent_response = await self._generate_agent_response(user_message, current_agent, context)
            response_audio = await self._generate_speech(agent_response, current_agent.voice_config)
            
            # Añadir al historial
            context.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "agent": current_agent.name,
                "message": agent_response,
                "audio_url": response_audio,
                "type": "agent_response"
            })
            
            return {
                "conversation_id": conversation_id,
                "transfer": False,
                "agent": current_agent.name,
                "response": agent_response,
                "response_audio": response_audio,
                "context": asdict(context)
            }
    
    async def _analyze_transfer_needed(self, user_message: str, current_agent: str) -> Dict[str, Any]:
        """Analiza si se necesita transferir a otro agente especializado."""
        # Usar Nexus Core para analizar la intención del usuario
        analysis_result = await self.nexus_core.process_natural_language_command(
            f"Analiza esta consulta y determina qué agente especializado la manejaría mejor: {user_message}",
            {"current_agent": current_agent}
        )
        
        # Mapear análisis a reglas de transferencia
        if current_agent in self.transfer_rules:
            for rule in self.transfer_rules[current_agent]:
                if self._matches_condition(user_message, rule["condition"]):
                    return {
                        "should_transfer": True,
                        "target_agent": rule["target_agent"],
                        "reason": rule["reason"]
                    }
        
        return {"should_transfer": False}
    
    def _matches_condition(self, message: str, condition: str) -> bool:
        """Determina si un mensaje coincide con una condición de transferencia."""
        message_lower = message.lower()
        
        condition_keywords = {
            "technical_question": ["error", "bug", "code", "programming", "technical", "system"],
            "code_generation": ["write code", "generate", "create function", "implement"],
            "sales_question": ["pricing", "cost", "purchase", "buy", "sales", "demo"],
            "support_question": ["help", "support", "issue", "problem", "troubleshoot"],
            "development_question": ["development", "coding", "programming", "software"],
            "data_analysis": ["data", "analysis", "report", "metrics", "statistics"]
        }
        
        if condition in condition_keywords:
            return any(keyword in message_lower for keyword in condition_keywords[condition])
        
        return False
    
    async def _generate_agent_response(self, user_message: str, agent: 'VoiceAgent', context: ConversationContext) -> str:
        """Genera una respuesta del agente basada en su especialización."""
        # Usar Nexus Core para generar respuesta especializada
        prompt = f"""
        Eres {agent.name}, {agent.description}.
        Especialidades: {', '.join(agent.capabilities)}
        
        Usuario dice: {user_message}
        
        Proporciona una respuesta útil y especializada en tu área de expertise.
        Mantén un tono profesional pero amigable.
        """
        
        result = await self.nexus_core.process_natural_language_command(prompt, {
            "agent_type": agent.name,
            "user_message": user_message,
            "conversation_history": context.conversation_history[-5:]  # Últimos 5 mensajes
        })
        
        return result['synthesis']
    
    async def _generate_speech(self, text: str, voice_config: VoiceConfig) -> str:
        """Genera audio usando ElevenLabs."""
        try:
            # Generar audio con ElevenLabs
            audio = generate(
                text=text,
                voice=voice_config.voice_id,
                model=voice_config.model.value,
                voice_settings=VoiceSettings(
                    stability=voice_config.stability,
                    similarity_boost=voice_config.similarity_boost,
                    style=voice_config.style,
                    use_speaker_boost=voice_config.use_speaker_boost
                )
            )
            
            # Guardar audio (en producción, usaría S3 o similar)
            filename = f"audio_{datetime.now().timestamp()}.mp3"
            with open(filename, "wb") as f:
                f.write(audio)
            
            # En producción, subiría a CDN y devolvería URL
            audio_url = f"https://cdn.nexus-ai.com/audio/{filename}"
            
            logger.info(f"Audio generado: {filename}")
            return audio_url
            
        except Exception as e:
            logger.error(f"Error generando audio: {e}")
            return None
    
    async def clone_voice(self, name: str, audio_samples: List[str], description: str = "") -> str:
        """Clona una voz personalizada usando ElevenLabs."""
        try:
            # Clonar voz con ElevenLabs
            voice = clone(
                name=name,
                description=description,
                files=audio_samples
            )
            
            logger.info(f"Voz clonada: {voice.voice_id}")
            return voice.voice_id
            
        except Exception as e:
            logger.error(f"Error clonando voz: {e}")
            raise
    
    async def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Obtiene el historial completo de una conversación."""
        if conversation_id in self.conversation_contexts:
            return self.conversation_contexts[conversation_id].conversation_history
        return []
    
    async def get_available_voices(self) -> List[Dict[str, Any]]:
        """Obtiene todas las voces disponibles."""
        try:
            all_voices = voices()
            return [
                {
                    "voice_id": voice.voice_id,
                    "name": voice.name,
                    "description": voice.description,
                    "category": voice.category
                }
                for voice in all_voices
            ]
        except Exception as e:
            logger.error(f"Error obteniendo voces: {e}")
            return []

class VoiceAgent:
    """Representa un agente especializado con configuración de voz."""
    
    def __init__(self, name: str, description: str, voice_config: VoiceConfig, capabilities: List[str]):
        self.name = name
        self.description = description
        self.voice_config = voice_config
        self.capabilities = capabilities

class NexusVoiceOrchestrator:
    """
    Orquestador principal que integra Nexus Core con capacidades de voz de ElevenLabs.
    """
    
    def __init__(self, elevenlabs_api_key: str):
        self.nexus_core = NexusOrchestrator()
        self.voice_agent = NexusVoiceAgent(elevenlabs_api_key, self.nexus_core)
        
        logger.info("Nexus Voice Orchestrator inicializado")
    
    async def create_voice_assistant(self, user_id: str, assistant_type: str = "general") -> str:
        """Crea un asistente de voz personalizado."""
        # Mapear tipo de asistente a agente especializado
        agent_mapping = {
            "general": "nexus_dev",
            "technical": "nexus_dev",
            "hr": "nexus_hr",
            "sales": "nexus_sales",
            "support": "nexus_support",
            "analyst": "nexus_analyst"
        }
        
        initial_agent = agent_mapping.get(assistant_type, "nexus_dev")
        conversation_id = await self.voice_agent.start_conversation(user_id, initial_agent)
        
        return conversation_id
    
    async def chat_with_voice(self, conversation_id: str, message: str) -> Dict[str, Any]:
        """Chatea con el asistente de voz."""
        return await self.voice_agent.process_message(conversation_id, message)
    
    async def clone_user_voice(self, name: str, audio_files: List[str], description: str = "") -> str:
        """Clona la voz del usuario para personalización."""
        return await self.voice_agent.clone_voice(name, audio_files, description)
    
    async def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """Obtiene un resumen de la conversación."""
        history = await self.voice_agent.get_conversation_history(conversation_id)
        
        if not history:
            return {"error": "Conversación no encontrada"}
        
        # Usar Nexus Core para generar resumen
        summary_prompt = f"""
        Genera un resumen ejecutivo de esta conversación:
        
        {json.dumps(history, indent=2)}
        
        Incluye:
        1. Temas principales discutidos
        2. Agentes involucrados
        3. Transferencias realizadas
        4. Acciones tomadas
        5. Próximos pasos recomendados
        """
        
        result = await self.nexus_core.process_natural_language_command(summary_prompt)
        
        return {
            "conversation_id": conversation_id,
            "summary": result['synthesis'],
            "total_messages": len(history),
            "agents_involved": list(set(msg.get('agent') for msg in history if msg.get('agent'))),
            "transfers": len([msg for msg in history if msg.get('type') == 'transfer'])
        }

# Ejemplo de uso
async def demo_voice_integration():
    """Demostración de la integración de voz con Nexus."""
    elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
    
    if not elevenlabs_api_key:
        logger.error("ELEVENLABS_API_KEY no configurada")
        return
    
    orchestrator = NexusVoiceOrchestrator(elevenlabs_api_key)
    
    # Crear asistente de voz
    user_id = "demo_user_123"
    conversation_id = await orchestrator.create_voice_assistant(user_id, "technical")
    
    print(f"Conversación iniciada: {conversation_id}")
    
    # Simular conversación
    messages = [
        "Hola, necesito ayuda con un error en mi código Python",
        "¿Puedes ayudarme con la configuración de una base de datos?",
        "Necesito información sobre precios de tu servicio"
    ]
    
    for message in messages:
        print(f"\nUsuario: {message}")
        
        response = await orchestrator.chat_with_voice(conversation_id, message)
        
        print(f"Agente: {response['agent']}")
        print(f"Respuesta: {response['response']}")
        print(f"Audio: {response['response_audio']}")
        
        if response.get('transfer'):
            print(f"🔄 Transferido de {response['from_agent']} a {response['to_agent']}")
        
        await asyncio.sleep(1)  # Pausa para simular tiempo real
    
    # Obtener resumen
    summary = await orchestrator.get_conversation_summary(conversation_id)
    print(f"\n📊 Resumen de conversación:")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    asyncio.run(demo_voice_integration()) 