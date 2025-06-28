# 🚀 Nexus - AI Voice Integration Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ElevenLabs](https://img.shields.io/badge/ElevenLabs-Integration-orange.svg)](https://elevenlabs.io/)

> **Nexus** es una plataforma revolucionaria de agentes conversacionales con voz realista que combina la arquitectura enterprise con las capacidades de síntesis de voz de ElevenLabs.

## 🎯 Visión General

Nexus representa el futuro de la interacción por voz con IA, proporcionando agentes conversacionales especializados que pueden transferirse inteligentemente entre sí, ofreciendo una experiencia verdaderamente humana y profesional.

### 🌟 Características Principales

- 🎭 **Agentes Conversacionales con Voz Realista** usando ElevenLabs
- 🔄 **Transferencias Inteligentes** entre agentes especializados
- 🌍 **Soporte Multiidioma** con 70+ idiomas
- 🎨 **Clonación de Voz Personalizada** con consentimiento
- 📊 **Analytics Avanzados** de conversaciones
- 🔒 **Seguridad y Ética** integradas

## 🎭 Agentes Especializados

| Agente | Voz | Personalidad | Especialidades |
|--------|-----|--------------|----------------|
| **NexusDev** | Adam | Técnica | Desarrollo, debugging, arquitectura |
| **NexusHR** | Bella | Amigable | Onboarding, políticas, relaciones |
| **NexusSales** | Josh | Ventas | Demos, calificación, precios |
| **NexusSupport** | Emily | Soporte | Troubleshooting, ayuda técnica |
| **NexusAnalyst** | Charlie | Analítica | Datos, reportes, insights |
| **NexusMarketing** | Domi | Creativa | Contenido, campañas, estrategia |
| **NexusLeadership** | Thomas | Autoritativa | Estrategia, liderazgo, decisiones |
| **NexusFinance** | Rachel | Profesional | Finanzas, presupuestos, compliance |

## 🚀 Instalación Rápida

### 1. Clonar el Repositorio

```bash
git clone https://github.com/JdCloude/Nexus.git
cd Nexus
```

### 2. Instalar Dependencias

```bash
pip install -r nexus_voice_requirements.txt
```

### 3. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp nexus_voice_env_example.txt .env

# Editar .env con tu API key de ElevenLabs
# Obtén tu clave en: https://elevenlabs.io/
```

### 4. Ejecutar Demo

```bash
python nexus_voice_demo.py
```

## 🎯 Casos de Uso

### Soporte Técnico Inteligente
```
Usuario: "Tengo un error en mi código Python"
→ NexusDev responde con solución técnica

Usuario: "Necesito ayuda con la configuración"
→ NexusDev → NexusSupport (transferencia automática)
```

### Ventas y Demos
```
Usuario: "¿Cuáles son los precios?"
→ NexusSales responde con información comercial

Usuario: "Necesito una demo técnica"
→ NexusSales → NexusDev (transferencia automática)
```

### Onboarding de Empleados
```
Usuario: "Soy nuevo en la empresa"
→ NexusHR inicia proceso de onboarding

Usuario: "Necesito configurar mi entorno"
→ NexusHR → NexusDev → NexusSupport
```

## 🛠️ Arquitectura

### Componentes Principales

- **NexusVoiceOrchestrator**: Orquestador principal del sistema
- **NexusVoiceAgent**: Agente conversacional con capacidades de voz
- **VoiceAgent**: Representación de agentes especializados
- **ConversationContext**: Contexto persistente de conversaciones
- **VoiceConfig**: Configuración personalizada de voz

### Integración con ElevenLabs

- **API REST** para síntesis de voz
- **WebSocket** para streaming en tiempo real
- **SDK oficial** de Python
- **Manejo robusto** de errores y rate limiting

## 📁 Estructura del Proyecto

```
Nexus/
├── nexus_voice_integration.py    # Integración principal con ElevenLabs
├── nexus_voice_config.py         # Configuraciones de voz y agentes
├── nexus_voice_demo.py           # Demostración completa
├── nexus_voice_requirements.txt  # Dependencias de Python
├── nexus_voice_env_example.txt   # Variables de entorno de ejemplo
├── NEXUS_VOICE_README.md         # Documentación detallada
├── NEXUS_VOICE_SUMMARY.md        # Resumen ejecutivo
├── .gitignore                    # Archivos a excluir
└── README.md                     # Este archivo
```

## 🔧 Configuración Avanzada

### Personalidades de Voz

```python
from nexus_voice_config import VoicePersonality, NexusVoiceConfigurations

# Configurar personalidad profesional
config = NexusVoiceConfigurations.create_custom_voice_config(
    voice_id="tu_voice_id",
    personality=VoicePersonality.PROFESSIONAL,
    model=VoiceModel.ELEVEN_V3,
    language=VoiceLanguage.SPANISH
)
```

### Transferencias Personalizadas

```python
# Configurar reglas de transferencia
transfer_rules = {
    "nexus_dev": [
        {
            "condition": "billing_question",
            "target_agent": "nexus_finance",
            "reason": "Transferring to finance specialist"
        }
    ]
}
```

## 🌍 Soporte Multiidioma

Nexus soporta múltiples idiomas a través de los modelos de ElevenLabs:

- **Eleven v3**: 70+ idiomas con expresividad emocional
- **Eleven Multilingual v2**: 29 idiomas con alta consistencia
- **Eleven Flash v2.5**: 32 idiomas con latencia ultra-baja (~75ms)
- **Eleven Turbo v2.5**: 32 idiomas con equilibrio calidad-velocidad

## 🔒 Seguridad y Ética

### Implementaciones de Seguridad
- ✅ **Consentimiento explícito** para clonación de voz
- ✅ **Encriptación** de datos de audio
- ✅ **Auditoría completa** de uso
- ✅ **Cumplimiento GDPR/CCPA**

### Consideraciones Éticas
- ✅ **Detección de deepfakes** integrada
- ✅ **Marcas de agua digitales** en audio
- ✅ **Transparencia** sobre uso de IA
- ✅ **Políticas de uso responsable**

## 📊 Monitoreo y Analytics

### Métricas Disponibles
- **Total de mensajes** por conversación
- **Agentes involucrados** en cada interacción
- **Transferencias realizadas** y razones
- **Duración de conversaciones**
- **Análisis de patrones** de uso

### Ejemplo de Uso

```python
# Obtener resumen de conversación
summary = await orchestrator.get_conversation_summary(conversation_id)

print(f"Total mensajes: {summary['total_messages']}")
print(f"Agentes involucrados: {summary['agents_involved']}")
print(f"Transferencias: {summary['transfers']}")
```

## 🚀 Roadmap

### Fase 1: Core Features ✅
- [x] Integración básica con ElevenLabs
- [x] Agentes conversacionales con voz
- [x] Transferencias entre agentes
- [x] Configuraciones de personalidad

### Fase 2: Advanced Features 🚧
- [ ] Integración con plataformas (Slack, Teams, Discord)
- [ ] Análisis de sentimiento en tiempo real
- [ ] Adaptación de voz basada en contexto emocional
- [ ] Integración con sistemas de CRM

### Fase 3: Enterprise Features 📋
- [ ] Escalabilidad horizontal
- [ ] Integración con sistemas de monitoreo
- [ ] APIs RESTful completas
- [ ] Dashboard de analytics

### Fase 4: AI Enhancement 🔮
- [ ] Aprendizaje de patrones de conversación
- [ ] Optimización automática de voces
- [ ] Predicción de transferencias
- [ ] Personalización adaptativa

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor, lee nuestras guías de contribución:

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Desarrollo Local

```bash
# Clonar repositorio
git clone https://github.com/JdCloude/Nexus.git
cd Nexus

# Instalar dependencias de desarrollo
pip install -r nexus_voice_requirements.txt

# Ejecutar tests
pytest tests/

# Formatear código
black nexus_voice_integration.py
flake8 nexus_voice_integration.py
```

## 📞 Soporte

### Recursos
- **Documentación Detallada**: [NEXUS_VOICE_README.md](NEXUS_VOICE_README.md)
- **Resumen Ejecutivo**: [NEXUS_VOICE_SUMMARY.md](NEXUS_VOICE_SUMMARY.md)
- **Configuración de Entorno**: [nexus_voice_env_example.txt](nexus_voice_env_example.txt)

### Contacto
- **GitHub Issues**: [Reportar un problema](https://github.com/JdCloude/Nexus/issues)
- **Discussions**: [Discutir ideas](https://github.com/JdCloude/Nexus/discussions)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **ElevenLabs** por su tecnología de síntesis de voz revolucionaria
- **Gemini** por los modelos de lenguaje que potencian Nexus
- **La comunidad de desarrolladores** que contribuye al proyecto

## 🎉 Estado del Proyecto

**Estado**: ✅ **IMPLEMENTACIÓN COMPLETA**
**Próximo**: 🚀 **Despliegue y Escalabilidad**

---

**Nexus** - Revolucionando la interacción por voz con IA 🤖🎤

*Desarrollado con ❤️ por [Juan David Pérez López](https://github.com/JdCloude)* 
