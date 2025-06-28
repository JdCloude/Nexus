#!/usr/bin/env python3
"""
Demostración de Nexus - Agente Cognitivo de Colaboración
=======================================================

Este script demuestra las capacidades completas de Nexus en un escenario
realista de trabajo colaborativo, mostrando cómo Nexus puede:
1. Procesar comandos en lenguaje natural
2. Orquestar múltiples agentes especializados
3. Mantener contexto persistente
4. Integrarse con plataformas externas
5. Intervenir proactivamente
"""

import asyncio
import json
import logging
from datetime import datetime
from nexus_core import NexusOrchestrator, ContextItem
from nexus_integrations import integration_manager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NexusDemo:
    """Clase para demostrar las capacidades de Nexus."""
    
    def __init__(self):
        self.nexus = NexusOrchestrator()
        self.demo_scenarios = []
        self.setup_demo_scenarios()
    
    def setup_demo_scenarios(self):
        """Configura los escenarios de demostración."""
        self.demo_scenarios = [
            {
                "name": "Escenario 1: Desarrollo de Feature Completo",
                "description": "Nexus procesa una solicitud compleja de desarrollo",
                "command": """
                Basándonos en la decisión que acabamos de tomar en la reunión, por favor:
                1. Redacta un borrador del email para el cliente explicando la nueva funcionalidad
                2. Crea un ticket en Jira para que el equipo de backend implemente el nuevo endpoint /users/{id}/settings
                3. Genera el código base en Python para ese endpoint incluyendo los tests unitarios
                4. Crea un mockup básico de la interfaz de usuario para la configuración
                """,
                "context": {
                    "meeting_id": "meeting_123",
                    "participants": ["Juan", "María", "Carlos"],
                    "project": "Sistema de Usuarios v2.0"
                }
            },
            {
                "name": "Escenario 2: Onboarding de Nuevo Empleado",
                "description": "Nexus automatiza el proceso de onboarding",
                "command": """
                Ana López se incorpora mañana como desarrolladora frontend. Por favor:
                1. Envía un mensaje de bienvenida en Slack al canal #general
                2. Crea un plan de onboarding personalizado para su primera semana
                3. Asigna a Carlos como su buddy
                4. Agenda las reuniones de introducción con el equipo
                5. Prepara las credenciales necesarias para todas las herramientas
                """,
                "context": {
                    "new_employee": "Ana López",
                    "role": "Desarrolladora Frontend",
                    "start_date": "2024-01-15"
                }
            },
            {
                "name": "Escenario 3: Análisis de Datos y Reportes",
                "description": "Nexus genera análisis complejos en tiempo real",
                "command": """
                Necesito un análisis urgente para la reunión con inversores:
                1. Analiza la correlación entre las funcionalidades lanzadas en Q2 y la activación de nuevos usuarios
                2. Genera un reporte ejecutivo con gráficos
                3. Identifica las 3 métricas más importantes para presentar
                4. Prepara un resumen de 2 minutos para la presentación
                """,
                "context": {
                    "quarter": "Q2 2024",
                    "audience": "Inversores",
                    "urgency": "Alta"
                }
            },
            {
                "name": "Escenario 4: Intervención Proactiva",
                "description": "Nexus detecta conflictos y interviene proactivamente",
                "command": "Vamos a cambiar la arquitectura de autenticación para usar JWT en lugar de sesiones",
                "context": {
                    "meeting_id": "meeting_456",
                    "participants": ["Laura", "Miguel", "Sofía"],
                    "current_topic": "Arquitectura de Autenticación"
                }
            }
        ]
    
    async def run_demo_scenario(self, scenario_index: int):
        """Ejecuta un escenario de demostración específico."""
        if scenario_index >= len(self.demo_scenarios):
            logger.error(f"Escenario {scenario_index} no existe")
            return
        
        scenario = self.demo_scenarios[scenario_index]
        
        print("\n" + "="*80)
        print(f"🚀 {scenario['name']}")
        print("="*80)
        print(f"📝 {scenario['description']}")
        print(f"🎯 Comando: {scenario['command'].strip()}")
        print(f"📊 Contexto: {json.dumps(scenario['context'], indent=2)}")
        print("-"*80)
        
        # Añadir contexto previo para el escenario
        await self._add_scenario_context(scenario)
        
        # Procesar comando con Nexus
        start_time = datetime.now()
        result = await self.nexus.process_natural_language_command(
            scenario['command'], 
            scenario['context']
        )
        end_time = datetime.now()
        
        # Mostrar resultados
        await self._display_results(result, end_time - start_time)
    
    async def _add_scenario_context(self, scenario: dict):
        """Añade contexto previo para el escenario."""
        if scenario['name'] == "Escenario 4: Intervención Proactiva":
            # Añadir decisión previa que entrará en conflicto
            self.nexus.add_decision_context(
                decision_id="auth_decision_2024_01",
                decision="Mantener autenticación basada en sesiones",
                rationale="Las sesiones son más seguras para nuestra aplicación y ya están implementadas. JWT requeriría refactoring completo.",
                participants=["Laura", "Miguel", "Sofía"],
                project_id="auth_system"
            )
            
            # Añadir contexto de conversación previa
            self.nexus.add_conversation_context(
                platform="slack",
                conversation_id="auth_discussion",
                participants=["Laura", "Miguel", "Sofía"],
                content="Discutimos mantener sesiones por seguridad y estabilidad",
                metadata={"topic": "autenticación", "date": "2024-01-10"}
            )
    
    async def _display_results(self, result: dict, execution_time):
        """Muestra los resultados de la ejecución de Nexus."""
        print("\n📊 RESULTADOS DE NEXUS")
        print("="*50)
        
        print(f"⏱️ Tiempo de ejecución: {execution_time.total_seconds():.2f} segundos")
        print(f"🔧 Tareas descompuestas: {len(result['decomposed_tasks'])}")
        
        print("\n📋 TAREAS EJECUTADAS:")
        for i, task in enumerate(result['decomposed_tasks'], 1):
            print(f"  {i}. [{task['agent_type']}] {task['description']}")
            if task['id'] in result['results']:
                task_result = result['results'][task['id']]
                if isinstance(task_result, dict) and 'error' in task_result:
                    print(f"     ❌ Error: {task_result['error']}")
                else:
                    print(f"     ✅ Completado")
        
        print(f"\n🎯 SÍNTESIS:")
        print(f"   {result['synthesis']}")
        
        # Mostrar detalles específicos por tipo de agente
        await self._display_agent_details(result)
    
    async def _display_agent_details(self, result: dict):
        """Muestra detalles específicos de cada agente."""
        print(f"\n🔍 DETALLES POR AGENTE:")
        
        for task in result['decomposed_tasks']:
            agent_type = task['agent_type']
            task_id = task['id']
            
            if task_id in result['results']:
                task_result = result['results'][task_id]
                
                print(f"\n  🤖 {agent_type}:")
                
                if agent_type == "NexusDev" and isinstance(task_result, dict):
                    if 'endpoint_code' in task_result:
                        print(f"     📝 Endpoint generado: {len(task_result['endpoint_code'])} caracteres")
                    if 'test_code' in task_result:
                        print(f"     🧪 Tests generados: {len(task_result['test_code'])} caracteres")
                
                elif agent_type == "NexusMarketing" and isinstance(task_result, dict):
                    if 'email_content' in task_result:
                        print(f"     📧 Email generado: {len(task_result['email_content'])} caracteres")
                
                elif agent_type == "NexusHR" and isinstance(task_result, dict):
                    if 'onboarding_plan' in task_result:
                        print(f"     👥 Plan de onboarding creado")
                
                elif agent_type == "NexusAnalyst" and isinstance(task_result, dict):
                    if 'correlation_analysis' in task_result:
                        print(f"     📊 Análisis de correlación completado")
    
    async def run_interactive_demo(self):
        """Ejecuta una demostración interactiva."""
        print("🤖 NEXUS - AGENTE COGNITIVO DE COLABORACIÓN")
        print("="*60)
        print("Bienvenido a la demostración de Nexus")
        print("Nexus es un agente que orquesta múltiples sub-agentes especializados")
        print("para eliminar la fricción entre discusión, decisión y ejecución.\n")
        
        while True:
            print("\n📋 ESCENARIOS DISPONIBLES:")
            for i, scenario in enumerate(self.demo_scenarios, 1):
                print(f"  {i}. {scenario['name']}")
            print("  0. Salir")
            
            try:
                choice = input("\n🎯 Selecciona un escenario (0-4): ").strip()
                
                if choice == "0":
                    print("👋 ¡Gracias por probar Nexus!")
                    break
                
                scenario_index = int(choice) - 1
                if 0 <= scenario_index < len(self.demo_scenarios):
                    await self.run_demo_scenario(scenario_index)
                else:
                    print("❌ Opción inválida. Por favor selecciona 0-4.")
                    
            except ValueError:
                print("❌ Por favor ingresa un número válido.")
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
    
    async def run_quick_demo(self):
        """Ejecuta una demostración rápida de todos los escenarios."""
        print("🚀 DEMOSTRACIÓN RÁPIDA DE NEXUS")
        print("="*50)
        
        for i in range(len(self.demo_scenarios)):
            await self.run_demo_scenario(i)
            print("\n" + "="*80)
            
            if i < len(self.demo_scenarios) - 1:
                input("Presiona Enter para continuar con el siguiente escenario...")

async def main():
    """Función principal de la demostración."""
    demo = NexusDemo()
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        await demo.run_quick_demo()
    else:
        await demo.run_interactive_demo()

if __name__ == "__main__":
    asyncio.run(main()) 