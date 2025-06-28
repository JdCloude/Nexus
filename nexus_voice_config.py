#!/usr/bin/env python3
"""
Nexus Voice Configuration
========================

Configuración avanzada para las voces de Nexus integradas con ElevenLabs.
Incluye configuraciones predefinidas para diferentes tipos de agentes y casos de uso.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum
from nexus_voice_integration import VoiceConfig, VoiceModel

class VoicePersonality(Enum):
    """Personalidades de voz para diferentes contextos."""
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    TECHNICAL = "technical"
    SALES = "sales"
    SUPPORT = "support"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    AUTHORITATIVE = "authoritative"

class VoiceLanguage(Enum):
    """Idiomas soportados por ElevenLabs."""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    JAPANESE = "ja"
    KOREAN = "ko"
    CHINESE = "zh"

@dataclass
class VoicePersonalityConfig:
    """Configuración de personalidad de voz."""
    personality: VoicePersonality
    stability: float
    similarity_boost: float
    style: float
    use_speaker_boost: bool
    description: str
    use_cases: List[str]

class NexusVoiceConfigurations:
    """
    Configuraciones predefinidas de voz para diferentes agentes y contextos de Nexus.
    """
    
    # Configuraciones de personalidad
    PERSONALITY_CONFIGS = {
        VoicePersonality.PROFESSIONAL: VoicePersonalityConfig(
            personality=VoicePersonality.PROFESSIONAL,
            stability=0.7,
            similarity_boost=0.8,
            style=0.0,
            use_speaker_boost=True,
            description="Voz clara y profesional para entornos corporativos",
            use_cases=["meetings", "presentations", "formal_communication"]
        ),
        VoicePersonality.FRIENDLY: VoicePersonalityConfig(
            personality=VoicePersonality.FRIENDLY,
            stability=0.8,
            similarity_boost=0.9,
            style=0.2,
            use_speaker_boost=True,
            description="Voz cálida y amigable para interacciones informales",
            use_cases=["customer_service", "onboarding", "casual_chat"]
        ),
        VoicePersonality.TECHNICAL: VoicePersonalityConfig(
            personality=VoicePersonality.TECHNICAL,
            stability=0.6,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True,
            description="Voz clara y precisa para contenido técnico",
            use_cases=["code_explanation", "technical_support", "documentation"]
        ),
        VoicePersonality.SALES: VoicePersonalityConfig(
            personality=VoicePersonality.SALES,
            stability=0.5,
            similarity_boost=0.85,
            style=0.3,
            use_speaker_boost=True,
            description="Voz persuasiva y energética para ventas",
            use_cases=["sales_pitches", "demos", "lead_qualification"]
        ),
        VoicePersonality.SUPPORT: VoicePersonalityConfig(
            personality=VoicePersonality.SUPPORT,
            stability=0.7,
            similarity_boost=0.8,
            style=0.1,
            use_speaker_boost=True,
            description="Voz paciente y comprensiva para soporte",
            use_cases=["troubleshooting", "help_desk", "user_support"]
        ),
        VoicePersonality.ANALYTICAL: VoicePersonalityConfig(
            personality=VoicePersonality.ANALYTICAL,
            stability=0.8,
            similarity_boost=0.7,
            style=0.0,
            use_speaker_boost=True,
            description="Voz clara y estructurada para análisis",
            use_cases=["data_analysis", "reporting", "insights"]
        ),
        VoicePersonality.CREATIVE: VoicePersonalityConfig(
            personality=VoicePersonality.CREATIVE,
            stability=0.4,
            similarity_boost=0.9,
            style=0.5,
            use_speaker_boost=True,
            description="Voz expresiva y dinámica para contenido creativo",
            use_cases=["storytelling", "marketing", "entertainment"]
        ),
        VoicePersonality.AUTHORITATIVE: VoicePersonalityConfig(
            personality=VoicePersonality.AUTHORITATIVE,
            stability=0.9,
            similarity_boost=0.8,
            style=0.1,
            use_speaker_boost=True,
            description="Voz firme y confiable para liderazgo",
            use_cases=["announcements", "leadership", "authority"]
        )
    }
    
    # Voces predefinidas de ElevenLabs (IDs reales)
    PREDEFINED_VOICES = {
        "adam": {
            "voice_id": "pNInz6obpgDQGcFmaJgB",
            "name": "Adam",
            "description": "Voz masculina profesional y técnica",
            "personality": VoicePersonality.TECHNICAL,
            "languages": [VoiceLanguage.ENGLISH]
        },
        "bella": {
            "voice_id": "EXAVITQu4vr4xnSDxMaL",
            "name": "Bella",
            "description": "Voz femenina amigable y cálida",
            "personality": VoicePersonality.FRIENDLY,
            "languages": [VoiceLanguage.ENGLISH]
        },
        "josh": {
            "voice_id": "VR6AewLTigWG4xSOukaG",
            "name": "Josh",
            "description": "Voz masculina profesional y confiable",
            "personality": VoicePersonality.PROFESSIONAL,
            "languages": [VoiceLanguage.ENGLISH]
        },
        "rachel": {
            "voice_id": "21m00Tcm4TlvDq8ikWAM",
            "name": "Rachel",
            "description": "Voz femenina clara y profesional",
            "personality": VoicePersonality.PROFESSIONAL,
            "languages": [VoiceLanguage.ENGLISH]
        },
        "domi": {
            "voice_id": "AZnzlk1XvdvUeBnXmlld",
            "name": "Domi",
            "description": "Voz femenina expresiva y dinámica",
            "personality": VoicePersonality.CREATIVE,
            "languages": [VoiceLanguage.ENGLISH]
        },
        "thomas": {
            "voice_id": "GBv7mTt0atIp3Br8iCZE",
            "name": "Thomas",
            "description": "Voz masculina autoritativa y firme",
            "personality": VoicePersonality.AUTHORITATIVE,
            "languages": [VoiceLanguage.ENGLISH]
        },
        "charlie": {
            "voice_id": "IKne3meq5aSn9XLyUdCD",
            "name": "Charlie",
            "description": "Voz masculina analítica y estructurada",
            "personality": VoicePersonality.ANALYTICAL,
            "languages": [VoiceLanguage.ENGLISH]
        },
        "emily": {
            "voice_id": "LcfcDJNUP1GQjkzn1xUU",
            "name": "Emily",
            "description": "Voz femenina de soporte y ayuda",
            "personality": VoicePersonality.SUPPORT,
            "languages": [VoiceLanguage.ENGLISH]
        }
    }
    
    # Configuraciones específicas para agentes Nexus
    AGENT_VOICE_CONFIGS = {
        "nexus_dev": {
            "voice_id": "pNInz6obpgDQGcFmaJgB",  # Adam
            "model": VoiceModel.ELEVEN_V3,
            "personality": VoicePersonality.TECHNICAL,
            "language": VoiceLanguage.ENGLISH,
            "description": "Especialista en desarrollo y tecnología",
            "capabilities": ["code_generation", "technical_support", "debugging", "architecture"]
        },
        "nexus_hr": {
            "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella
            "model": VoiceModel.ELEVEN_V3,
            "personality": VoicePersonality.FRIENDLY,
            "language": VoiceLanguage.ENGLISH,
            "description": "Especialista en recursos humanos",
            "capabilities": ["onboarding", "hr_support", "policy_questions", "employee_relations"]
        },
        "nexus_sales": {
            "voice_id": "VR6AewLTigWG4xSOukaG",  # Josh
            "model": VoiceModel.ELEVEN_V3,
            "personality": VoicePersonality.SALES,
            "language": VoiceLanguage.ENGLISH,
            "description": "Especialista en ventas y relaciones",
            "capabilities": ["sales_support", "demo_preparation", "lead_qualification", "pricing"]
        },
        "nexus_support": {
            "voice_id": "LcfcDJNUP1GQjkzn1xUU",  # Emily
            "model": VoiceModel.ELEVEN_FLASH_V2_5,
            "personality": VoicePersonality.SUPPORT,
            "language": VoiceLanguage.ENGLISH,
            "description": "Especialista en soporte técnico",
            "capabilities": ["technical_support", "troubleshooting", "bug_reports", "user_help"]
        },
        "nexus_analyst": {
            "voice_id": "IKne3meq5aSn9XLyUdCD",  # Charlie
            "model": VoiceModel.ELEVEN_V3,
            "personality": VoicePersonality.ANALYTICAL,
            "language": VoiceLanguage.ENGLISH,
            "description": "Especialista en análisis de datos",
            "capabilities": ["data_analysis", "reporting", "insights", "metrics"]
        },
        "nexus_marketing": {
            "voice_id": "AZnzlk1XvdvUeBnXmlld",  # Domi
            "model": VoiceModel.ELEVEN_V3,
            "personality": VoicePersonality.CREATIVE,
            "language": VoiceLanguage.ENGLISH,
            "description": "Especialista en marketing y creatividad",
            "capabilities": ["content_creation", "campaign_planning", "brand_strategy", "social_media"]
        },
        "nexus_leadership": {
            "voice_id": "GBv7mTt0atIp3Br8iCZE",  # Thomas
            "model": VoiceModel.ELEVEN_V3,
            "personality": VoicePersonality.AUTHORITATIVE,
            "language": VoiceLanguage.ENGLISH,
            "description": "Especialista en liderazgo y estrategia",
            "capabilities": ["strategic_planning", "decision_making", "team_leadership", "vision"]
        },
        "nexus_finance": {
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
            "model": VoiceModel.ELEVEN_V3,
            "personality": VoicePersonality.PROFESSIONAL,
            "language": VoiceLanguage.ENGLISH,
            "description": "Especialista en finanzas y contabilidad",
            "capabilities": ["financial_analysis", "budgeting", "reporting", "compliance"]
        }
    }
    
    @classmethod
    def get_voice_config(cls, agent_type: str) -> VoiceConfig:
        """Obtiene la configuración de voz para un tipo de agente específico."""
        if agent_type not in cls.AGENT_VOICE_CONFIGS:
            raise ValueError(f"Tipo de agente no encontrado: {agent_type}")
        
        agent_config = cls.AGENT_VOICE_CONFIGS[agent_type]
        personality_config = cls.PERSONALITY_CONFIGS[agent_config["personality"]]
        
        return VoiceConfig(
            voice_id=agent_config["voice_id"],
            model=agent_config["model"],
            stability=personality_config.stability,
            similarity_boost=personality_config.similarity_boost,
            style=personality_config.style,
            use_speaker_boost=personality_config.use_speaker_boost,
            language=agent_config["language"].value
        )
    
    @classmethod
    def get_personality_config(cls, personality: VoicePersonality) -> VoicePersonalityConfig:
        """Obtiene la configuración de personalidad de voz."""
        return cls.PERSONALITY_CONFIGS[personality]
    
    @classmethod
    def get_predefined_voice(cls, voice_name: str) -> Dict[str, Any]:
        """Obtiene información de una voz predefinida."""
        if voice_name not in cls.PREDEFINED_VOICES:
            raise ValueError(f"Voz predefinida no encontrada: {voice_name}")
        
        return cls.PREDEFINED_VOICES[voice_name]
    
    @classmethod
    def list_available_agents(cls) -> List[str]:
        """Lista todos los agentes disponibles con sus configuraciones."""
        return list(cls.AGENT_VOICE_CONFIGS.keys())
    
    @classmethod
    def list_available_personalities(cls) -> List[VoicePersonality]:
        """Lista todas las personalidades de voz disponibles."""
        return list(cls.PERSONALITY_CONFIGS.keys())
    
    @classmethod
    def list_predefined_voices(cls) -> List[str]:
        """Lista todas las voces predefinidas disponibles."""
        return list(cls.PREDEFINED_VOICES.keys())
    
    @classmethod
    def get_agent_capabilities(cls, agent_type: str) -> List[str]:
        """Obtiene las capacidades de un agente específico."""
        if agent_type not in cls.AGENT_VOICE_CONFIGS:
            raise ValueError(f"Tipo de agente no encontrado: {agent_type}")
        
        return cls.AGENT_VOICE_CONFIGS[agent_type]["capabilities"]
    
    @classmethod
    def find_agent_by_capability(cls, capability: str) -> List[str]:
        """Encuentra agentes que tienen una capacidad específica."""
        matching_agents = []
        
        for agent_type, config in cls.AGENT_VOICE_CONFIGS.items():
            if capability in config["capabilities"]:
                matching_agents.append(agent_type)
        
        return matching_agents
    
    @classmethod
    def create_custom_voice_config(cls, 
                                 voice_id: str, 
                                 personality: VoicePersonality,
                                 model: VoiceModel = VoiceModel.ELEVEN_V3,
                                 language: VoiceLanguage = VoiceLanguage.ENGLISH) -> VoiceConfig:
        """Crea una configuración de voz personalizada."""
        personality_config = cls.PERSONALITY_CONFIGS[personality]
        
        return VoiceConfig(
            voice_id=voice_id,
            model=model,
            stability=personality_config.stability,
            similarity_boost=personality_config.similarity_boost,
            style=personality_config.style,
            use_speaker_boost=personality_config.use_speaker_boost,
            language=language.value
        )

# Configuraciones específicas para diferentes contextos
class ContextualVoiceConfigs:
    """Configuraciones de voz específicas para diferentes contextos de uso."""
    
    # Configuraciones para reuniones
    MEETING_CONFIGS = {
        "daily_standup": {
            "agent": "nexus_leadership",
            "personality": VoicePersonality.PROFESSIONAL,
            "model": VoiceModel.ELEVEN_FLASH_V2_5,  # Baja latencia
            "description": "Para reuniones diarias rápidas"
        },
        "client_presentation": {
            "agent": "nexus_sales",
            "personality": VoicePersonality.PROFESSIONAL,
            "model": VoiceModel.ELEVEN_V3,  # Alta calidad
            "description": "Para presentaciones a clientes"
        },
        "technical_review": {
            "agent": "nexus_dev",
            "personality": VoicePersonality.TECHNICAL,
            "model": VoiceModel.ELEVEN_V3,
            "description": "Para revisiones técnicas"
        }
    }
    
    # Configuraciones para soporte
    SUPPORT_CONFIGS = {
        "first_level": {
            "agent": "nexus_support",
            "personality": VoicePersonality.FRIENDLY,
            "model": VoiceModel.ELEVEN_FLASH_V2_5,
            "description": "Soporte de primer nivel"
        },
        "technical_support": {
            "agent": "nexus_dev",
            "personality": VoicePersonality.TECHNICAL,
            "model": VoiceModel.ELEVEN_V3,
            "description": "Soporte técnico especializado"
        },
        "escalation": {
            "agent": "nexus_leadership",
            "personality": VoicePersonality.AUTHORITATIVE,
            "model": VoiceModel.ELEVEN_V3,
            "description": "Escalación de problemas críticos"
        }
    }
    
    # Configuraciones para contenido
    CONTENT_CONFIGS = {
        "tutorial": {
            "agent": "nexus_dev",
            "personality": VoicePersonality.TECHNICAL,
            "model": VoiceModel.ELEVEN_V3,
            "description": "Tutoriales técnicos"
        },
        "marketing": {
            "agent": "nexus_marketing",
            "personality": VoicePersonality.CREATIVE,
            "model": VoiceModel.ELEVEN_V3,
            "description": "Contenido de marketing"
        },
        "announcement": {
            "agent": "nexus_leadership",
            "personality": VoicePersonality.AUTHORITATIVE,
            "model": VoiceModel.ELEVEN_V3,
            "description": "Anuncios importantes"
        }
    }
    
    @classmethod
    def get_context_config(cls, context_type: str, context_name: str) -> Dict[str, Any]:
        """Obtiene la configuración para un contexto específico."""
        context_configs = {
            "meeting": cls.MEETING_CONFIGS,
            "support": cls.SUPPORT_CONFIGS,
            "content": cls.CONTENT_CONFIGS
        }
        
        if context_type not in context_configs:
            raise ValueError(f"Tipo de contexto no encontrado: {context_type}")
        
        if context_name not in context_configs[context_type]:
            raise ValueError(f"Contexto no encontrado: {context_name}")
        
        return context_configs[context_type][context_name]

# Ejemplo de uso
if __name__ == "__main__":
    # Mostrar configuraciones disponibles
    print("🎤 Configuraciones de Voz de Nexus")
    print("=" * 50)
    
    print("\n📋 Agentes Disponibles:")
    for agent in NexusVoiceConfigurations.list_available_agents():
        config = NexusVoiceConfigurations.AGENT_VOICE_CONFIGS[agent]
        print(f"  • {agent}: {config['description']}")
        print(f"    Capacidades: {', '.join(config['capabilities'])}")
    
    print("\n🎭 Personalidades de Voz:")
    for personality in NexusVoiceConfigurations.list_available_personalities():
        config = NexusVoiceConfigurations.get_personality_config(personality)
        print(f"  • {personality.value}: {config.description}")
        print(f"    Casos de uso: {', '.join(config.use_cases)}")
    
    print("\n🔊 Voces Predefinidas:")
    for voice in NexusVoiceConfigurations.list_predefined_voices():
        voice_info = NexusVoiceConfigurations.get_predefined_voice(voice)
        print(f"  • {voice_info['name']}: {voice_info['description']}")
    
    # Ejemplo de configuración personalizada
    print("\n⚙️ Ejemplo de Configuración Personalizada:")
    custom_config = NexusVoiceConfigurations.create_custom_voice_config(
        voice_id="custom_voice_123",
        personality=VoicePersonality.CREATIVE,
        model=VoiceModel.ELEVEN_V3,
        language=VoiceLanguage.SPANISH
    )
    print(f"Configuración creada: {custom_config}") 