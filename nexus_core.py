#!/usr/bin/env python3
"""
Nexus - Agente Cognitivo de Colaboración en Tiempo Real
======================================================

Nexus es un agente de trabajo cognitivo y autónomo que se integra de forma nativa
en plataformas de colaboración. Actúa como un "general contractor" orquestando
un ecosistema de sub-agentes especializados para eliminar la fricción entre
discusión, decisión y ejecución.

Arquitectura:
- Contexto Persistente y Transversal
- Orquestador de Agentes Especializados
- Interfaz de Lenguaje Natural Unificada
- Síntesis y Facilitación Proactiva
- Memoria Organizacional Colectiva
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentType(Enum):
    """Tipos de agentes especializados en el ecosistema Nexus."""
    NEXUS_DEV = "NexusDev"
    NEXUS_QA = "NexusQA"
    NEXUS_DESIGNER = "NexusDesigner"
    NEXUS_HR = "NexusHR"
    NEXUS_FINANCE = "NexusFinance"
    NEXUS_SALES = "NexusSales"
    NEXUS_MARKETING = "NexusMarketing"
    NEXUS_SUPPORT = "NexusSupport"
    NEXUS_ANALYST = "NexusAnalyst"
    NEXUS_RESEARCHER = "NexusResearcher"
    NEXUS_PROJECT_MANAGER = "NexusProjectManager"

@dataclass
class ContextItem:
    """Elemento de contexto persistente."""
    id: str
    type: str  # 'conversation', 'document', 'decision', 'meeting'
    content: str
    source: str  # 'slack', 'meet', 'jira', 'docs', etc.
    timestamp: datetime
    metadata: Dict[str, Any]
    importance_score: float = 0.5

@dataclass
class Task:
    """Tarea delegada a un agente especializado."""
    id: str
    description: str
    agent_type: AgentType
    priority: int = 1
    status: str = "pending"
    created_at: datetime = None
    completed_at: datetime = None
    result: Any = None
    error: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class MemoryStore:
    """Almacén de memoria organizacional colectiva."""
    
    def __init__(self):
        self.context_items: Dict[str, ContextItem] = {}
        self.conversation_history: List[Dict[str, Any]] = []
        self.decisions: List[Dict[str, Any]] = []
        self.documents: List[Dict[str, Any]] = []
    
    def add_context(self, context_item: ContextItem):
        """Añade un elemento de contexto a la memoria."""
        self.context_items[context_item.id] = context_item
        logger.info(f"Contexto añadido: {context_item.type} - {context_item.id}")
    
    def search_context(self, query: str, limit: int = 10) -> List[ContextItem]:
        """Busca contexto relevante basado en una consulta."""
        # Implementación simple de búsqueda semántica
        # En producción, usaría embeddings y vector search
        relevant_items = []
        query_lower = query.lower()
        
        for item in self.context_items.values():
            if (query_lower in item.content.lower() or 
                query_lower in item.type.lower() or
                any(query_lower in str(v).lower() for v in item.metadata.values())):
                relevant_items.append(item)
        
        # Ordenar por importancia y relevancia
        relevant_items.sort(key=lambda x: x.importance_score, reverse=True)
        return relevant_items[:limit]
    
    def get_project_context(self, project_id: str) -> List[ContextItem]:
        """Obtiene todo el contexto relacionado con un proyecto específico."""
        return [
            item for item in self.context_items.values()
            if item.metadata.get('project_id') == project_id
        ]

class BaseAgent:
    """Clase base para todos los agentes especializados."""
    
    def __init__(self, agent_type: AgentType, memory_store: MemoryStore):
        self.agent_type = agent_type
        self.memory_store = memory_store
        self.capabilities = self._define_capabilities()
        logger.info(f"Agente {agent_type.value} inicializado")
    
    def _define_capabilities(self) -> List[str]:
        """Define las capacidades específicas del agente."""
        return []
    
    async def execute_task(self, task: Task) -> Any:
        """Ejecuta una tarea específica."""
        raise NotImplementedError(f"Agente {self.agent_type.value} debe implementar execute_task")
    
    def can_handle_task(self, task_description: str) -> bool:
        """Determina si el agente puede manejar una tarea específica."""
        task_lower = task_description.lower()
        return any(cap.lower() in task_lower for cap in self.capabilities)

class NexusOrchestrator:
    """
    Orquestador principal de Nexus que coordina todos los sub-agentes
    y mantiene el contexto persistente.
    """
    
    def __init__(self):
        self.memory_store = MemoryStore()
        self.agents: Dict[AgentType, BaseAgent] = {}
        self.active_tasks: Dict[str, Task] = {}
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Inicializar agentes especializados
        self._initialize_agents()
        
        logger.info("Nexus Orchestrator inicializado")
    
    def _initialize_agents(self):
        """Inicializa todos los agentes especializados."""
        from nexus_agents import (
            NexusDevAgent, NexusQAAgent, NexusDesignerAgent,
            NexusHRAgent, NexusFinanceAgent, NexusSalesAgent,
            NexusMarketingAgent, NexusSupportAgent, NexusAnalystAgent
        )
        
        agent_classes = {
            AgentType.NEXUS_DEV: NexusDevAgent,
            AgentType.NEXUS_QA: NexusQAAgent,
            AgentType.NEXUS_DESIGNER: NexusDesignerAgent,
            AgentType.NEXUS_HR: NexusHRAgent,
            AgentType.NEXUS_FINANCE: NexusFinanceAgent,
            AgentType.NEXUS_SALES: NexusSalesAgent,
            AgentType.NEXUS_MARKETING: NexusMarketingAgent,
            AgentType.NEXUS_SUPPORT: NexusSupportAgent,
            AgentType.NEXUS_ANALYST: NexusAnalystAgent,
        }
        
        for agent_type, agent_class in agent_classes.items():
            self.agents[agent_type] = agent_class(self.memory_store)
    
    async def process_natural_language_command(self, command: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Procesa un comando en lenguaje natural y lo descompone en tareas
        para los agentes especializados.
        """
        logger.info(f"Procesando comando: {command}")
        
        # Analizar el comando con IA para identificar tareas
        tasks = await self._decompose_command(command, context)
        
        # Ejecutar tareas en paralelo
        results = await self._execute_tasks_parallel(tasks)
        
        # Sintetizar resultados
        synthesis = await self._synthesize_results(command, tasks, results)
        
        return {
            "original_command": command,
            "decomposed_tasks": [asdict(task) for task in tasks],
            "results": results,
            "synthesis": synthesis,
            "status": "completed"
        }
    
    async def _decompose_command(self, command: str, context: Dict[str, Any] = None) -> List[Task]:
        """Descompone un comando en lenguaje natural en tareas específicas."""
        
        # Buscar contexto relevante
        relevant_context = self.memory_store.search_context(command)
        context_summary = self._summarize_context(relevant_context)
        
        # Prompt para descomposición
        decomposition_prompt = f"""
        Eres Nexus, un orquestador de agentes especializados. Tu tarea es descomponer el siguiente comando en tareas específicas que pueden ser ejecutadas por agentes especializados.

        Comando: {command}
        
        Contexto relevante: {context_summary}
        
        Agentes disponibles:
        - NexusDev: Desarrollo de código, implementación de features, tests
        - NexusQA: Testing, calidad, casos de prueba
        - NexusDesigner: Diseño UI/UX, mockups, sistema de diseño
        - NexusHR: Onboarding, gestión de empleados, políticas
        - NexusFinance: Gastos, facturas, análisis financiero
        - NexusSales: CRM, demos, seguimiento de leads
        - NexusMarketing: Contenido, estrategia de marketing
        - NexusSupport: Soporte al cliente, éxito del cliente
        - NexusAnalyst: Análisis de datos, reportes, métricas

        Responde en formato JSON con la siguiente estructura:
        {{
            "tasks": [
                {{
                    "description": "Descripción clara de la tarea",
                    "agent_type": "NexusDev|NexusQA|NexusDesigner|NexusHR|NexusFinance|NexusSales|NexusMarketing|NexusSupport|NexusAnalyst",
                    "priority": 1-5,
                    "dependencies": ["task_id_1", "task_id_2"]
                }}
            ]
        }}
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": decomposition_prompt}],
                temperature=0.1
            )
            
            decomposition = json.loads(response.choices[0].message.content)
            tasks = []
            
            for task_data in decomposition["tasks"]:
                task = Task(
                    id=f"task_{len(tasks)}_{datetime.now().timestamp()}",
                    description=task_data["description"],
                    agent_type=AgentType(task_data["agent_type"]),
                    priority=task_data.get("priority", 1)
                )
                tasks.append(task)
            
            return tasks
            
        except Exception as e:
            logger.error(f"Error al descomponer comando: {e}")
            # Fallback: crear una tarea genérica
            return [Task(
                id=f"fallback_task_{datetime.now().timestamp()}",
                description=command,
                agent_type=AgentType.NEXUS_ANALYST,
                priority=1
            )]
    
    async def _execute_tasks_parallel(self, tasks: List[Task]) -> Dict[str, Any]:
        """Ejecuta múltiples tareas en paralelo."""
        results = {}
        
        # Agrupar tareas por agente para optimizar
        tasks_by_agent = {}
        for task in tasks:
            if task.agent_type not in tasks_by_agent:
                tasks_by_agent[task.agent_type] = []
            tasks_by_agent[task.agent_type].append(task)
        
        # Ejecutar tareas en paralelo por agente
        execution_tasks = []
        for agent_type, agent_tasks in tasks_by_agent.items():
            if agent_type in self.agents:
                for task in agent_tasks:
                    execution_tasks.append(self._execute_single_task(task))
        
        # Esperar a que todas las tareas se completen
        task_results = await asyncio.gather(*execution_tasks, return_exceptions=True)
        
        # Procesar resultados
        for i, task in enumerate(tasks):
            if i < len(task_results):
                if isinstance(task_results[i], Exception):
                    task.status = "error"
                    task.error = str(task_results[i])
                    results[task.id] = {"error": str(task_results[i])}
                else:
                    task.status = "completed"
                    task.result = task_results[i]
                    task.completed_at = datetime.now()
                    results[task.id] = task_results[i]
        
        return results
    
    async def _execute_single_task(self, task: Task) -> Any:
        """Ejecuta una tarea individual."""
        try:
            if task.agent_type in self.agents:
                result = await self.agents[task.agent_type].execute_task(task)
                return result
            else:
                raise ValueError(f"Agente {task.agent_type.value} no disponible")
        except Exception as e:
            logger.error(f"Error ejecutando tarea {task.id}: {e}")
            raise
    
    async def _synthesize_results(self, original_command: str, tasks: List[Task], results: Dict[str, Any]) -> str:
        """Sintetiza los resultados de múltiples tareas en una respuesta coherente."""
        
        synthesis_prompt = f"""
        Eres Nexus. Has ejecutado múltiples tareas basadas en el siguiente comando:
        
        Comando original: {original_command}
        
        Tareas ejecutadas:
        {json.dumps([asdict(task) for task in tasks], indent=2, default=str)}
        
        Resultados:
        {json.dumps(results, indent=2, default=str)}
        
        Proporciona una síntesis clara y concisa de lo que se ha completado, 
        incluyendo cualquier problema encontrado y próximos pasos recomendados.
        Mantén un tono profesional pero conversacional.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": synthesis_prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error al sintetizar resultados: {e}")
            return f"Tareas completadas con algunos errores. Revisa los logs para más detalles."
    
    def _summarize_context(self, context_items: List[ContextItem]) -> str:
        """Resume el contexto relevante para el análisis."""
        if not context_items:
            return "Sin contexto relevante disponible."
        
        summary_parts = []
        for item in context_items[:5]:  # Limitar a 5 elementos más relevantes
            summary_parts.append(f"- {item.type}: {item.content[:200]}...")
        
        return "\n".join(summary_parts)
    
    def add_conversation_context(self, platform: str, conversation_id: str, 
                               participants: List[str], content: str, 
                               metadata: Dict[str, Any] = None):
        """Añade contexto de una conversación a la memoria."""
        context_item = ContextItem(
            id=f"conv_{platform}_{conversation_id}_{datetime.now().timestamp()}",
            type="conversation",
            content=content,
            source=platform,
            timestamp=datetime.now(),
            metadata={
                "participants": participants,
                "conversation_id": conversation_id,
                **(metadata or {})
            },
            importance_score=0.7
        )
        
        self.memory_store.add_context(context_item)
        logger.info(f"Contexto de conversación añadido: {platform} - {conversation_id}")
    
    def add_decision_context(self, decision_id: str, decision: str, 
                           rationale: str, participants: List[str],
                           project_id: str = None):
        """Añade contexto de una decisión tomada."""
        context_item = ContextItem(
            id=f"decision_{decision_id}",
            type="decision",
            content=f"Decisión: {decision}\nRazonamiento: {rationale}",
            source="nexus",
            timestamp=datetime.now(),
            metadata={
                "participants": participants,
                "project_id": project_id,
                "decision_id": decision_id
            },
            importance_score=0.9
        )
        
        self.memory_store.add_context(context_item)
        logger.info(f"Contexto de decisión añadido: {decision_id}")
    
    async def proactive_intervention(self, current_context: str, 
                                   participants: List[str]) -> Optional[str]:
        """
        Interviene proactivamente cuando detecta conflictos o oportunidades
        basándose en el contexto histórico.
        """
        # Buscar decisiones o contexto relevante que pueda entrar en conflicto
        relevant_context = self.memory_store.search_context(current_context)
        
        conflicts = []
        for item in relevant_context:
            if item.type == "decision" and item.importance_score > 0.8:
                # Verificar si hay conflicto potencial
                if any(keyword in current_context.lower() for keyword in 
                      ["conflicto", "contradicción", "diferente", "cambio"]):
                    conflicts.append(item)
        
        if conflicts:
            # Generar intervención proactiva
            intervention_prompt = f"""
            Eres Nexus. Has detectado un posible conflicto con decisiones previas.
            
            Contexto actual: {current_context}
            
            Decisiones previas relevantes:
            {self._summarize_context(conflicts)}
            
            Genera una intervención proactiva y respetuosa que:
            1. Identifique el potencial conflicto
            2. Proporcione contexto de las decisiones previas
            3. Sugiera cómo proceder
            4. Mantenga un tono colaborativo
            
            Responde en formato conversacional directo.
            """
            
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": intervention_prompt}],
                    temperature=0.3
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                logger.error(f"Error generando intervención proactiva: {e}")
                return None
        
        return None

# Instancia global de Nexus
nexus = NexusOrchestrator()

async def main():
    """Función principal para demostrar Nexus."""
    logger.info("🚀 Iniciando Nexus - Agente Cognitivo de Colaboración")
    
    # Ejemplo de uso
    command = """
    Basándonos en la decisión que acabamos de tomar, por favor:
    1. Redacta un borrador del email para el cliente
    2. Crea un ticket en Jira para que el equipo de backend implemente el nuevo endpoint de la API
    3. Genera el código base en Python para ese endpoint incluyendo los tests unitarios
    """
    
    result = await nexus.process_natural_language_command(command)
    
    print("\n" + "="*60)
    print("RESULTADO DE NEXUS")
    print("="*60)
    print(f"Comando original: {result['original_command']}")
    print(f"\nTareas descompuestas: {len(result['decomposed_tasks'])}")
    print(f"Síntesis: {result['synthesis']}")

if __name__ == "__main__":
    asyncio.run(main()) 