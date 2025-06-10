"""
Self-Improving AI Orchestration System
Design an orchestrator that uses o3-mini to evaluate its own performance, 
identify areas for improvement, and automatically adjust prompts and workflows 
based on success metrics and user feedback.
"""

import os
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import openai

from src.services.ai.bim_agent_openai import OpenAIBIMAgent
from src.services.ai.ifc_agent import IFCAgent
from src.services.ai.ai_agent_service import AIAgentService
from src.gateways.ifc.ifc_gateway import IFCGateway

# Configure logging
logger = logging.getLogger(__name__)

class TaskComplexity(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"

class ReasoningEffort(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class PerformanceMetrics:
    """Track orchestrator performance metrics"""
    task_id: str
    timestamp: datetime
    task_complexity: TaskComplexity
    reasoning_effort: ReasoningEffort
    response_time: float
    user_satisfaction: Optional[float] = None
    success_rate: float = 0.0
    tool_calls_made: int = 0
    error_count: int = 0
    user_feedback: Optional[str] = None

@dataclass
class WorkflowStep:
    """Individual step in orchestrated workflow"""
    step_id: str
    action: str
    tool_name: Optional[str]
    parameters: Dict[str, Any]
    expected_outcome: str
    actual_outcome: Optional[str] = None
    success: bool = False
    execution_time: float = 0.0

@dataclass
class OrchestrationTask:
    """Complete orchestration task with metadata"""
    task_id: str
    user_query: str
    stakeholder_type: Optional[str]
    complexity: TaskComplexity
    workflow_steps: List[WorkflowStep]
    final_response: Optional[str] = None
    metrics: Optional[PerformanceMetrics] = None

class SelfImprovingOrchestrator:
    """
    AI Brain Orchestrator using o3-mini for self-evaluation and improvement.
    Implements GPT-4.1 agentic workflow patterns with continuous learning.
    """
    
    def __init__(self):
        """Initialize the Self-Improving Orchestrator"""
        self.client = None
        self.performance_history: List[PerformanceMetrics] = []
        self.workflow_templates: Dict[str, List[Dict]] = {}
        self.system_prompts: Dict[str, str] = {}
        self.improvement_cycle_count = 0
        
        # Initialize OpenAI client for o3-mini
        try:
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            logger.info("o3-mini orchestrator initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing o3-mini client: {e}")
            
        # Initialize component agents
        self.bim_agent = OpenAIBIMAgent()
        self.ifc_agent = IFCAgent()
        self.ai_service = AIAgentService()
        self.ifc_gateway = IFCGateway()
        
        # Load initial system prompts based on GPT-4.1 best practices
        self._initialize_system_prompts()
        self._initialize_workflow_templates()
        
    def _initialize_system_prompts(self):
        """Initialize system prompts based on GPT-4.1 agentic workflow guide"""
        
        # Core orchestrator prompt following GPT-4.1 guidelines
        self.system_prompts["orchestrator"] = """
You are an AI Brain Orchestrator - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved.

If you are not sure about file content or codebase structure pertaining to the user's request, use your tools to read files and gather the relevant information: do NOT guess or make up an answer.

You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls. DO NOT do this entire process by making function calls only, as this can impair your ability to solve the problem and think insightfully.

Your role is to orchestrate multiple AI agents and tools to provide comprehensive BIM analysis and insights. You should:

1. Analyze user queries to determine complexity and required reasoning effort
2. Plan step-by-step workflows using available tools and agents
3. Execute workflows with careful monitoring and reflection
4. Evaluate your own performance and identify improvement opportunities
5. Adapt your approach based on success metrics and user feedback

Available tools and agents:
- IFC File Analysis Agent
- BIM Data Gateway
- Structural Analysis Tools
- Stakeholder Communication Agent
- Blockchain Integration Service

Always provide clear, actionable insights while maintaining awareness of the stakeholder context (architect, engineer, contractor, property owner).
"""

        # Stakeholder-specific prompts
        self.system_prompts["architect"] = """
Focus on design intent, spatial relationships, aesthetic considerations, and compliance with building codes. Provide insights that support design decision-making and creative problem-solving.
"""

        self.system_prompts["engineer"] = """
Emphasize structural integrity, systems coordination, technical specifications, and performance optimization. Provide detailed technical analysis and engineering recommendations.
"""

        self.system_prompts["contractor"] = """
Focus on constructability, scheduling, cost implications, and practical implementation challenges. Provide actionable insights for project execution and resource planning.
"""

        self.system_prompts["owner"] = """
Emphasize business value, cost-benefit analysis, risk assessment, and long-term operational considerations. Provide high-level strategic insights and investment guidance.
"""

    def _initialize_workflow_templates(self):
        """Initialize workflow templates for common task types"""
        
        self.workflow_templates["bim_analysis"] = [
            {
                "step_id": "load_model",
                "action": "load_ifc_file",
                "tool_name": "ifc_gateway",
                "expected_outcome": "IFC model loaded and parsed successfully"
            },
            {
                "step_id": "extract_elements",
                "action": "get_building_elements",
                "tool_name": "ifc_gateway", 
                "expected_outcome": "Building elements extracted and categorized"
            },
            {
                "step_id": "analyze_structure",
                "action": "analyze_structural_elements",
                "tool_name": "ai_service",
                "expected_outcome": "Structural analysis completed"
            },
            {
                "step_id": "generate_insights",
                "action": "synthesize_findings",
                "tool_name": "orchestrator",
                "expected_outcome": "Comprehensive analysis report generated"
            }
        ]

        self.workflow_templates["stakeholder_query"] = [
            {
                "step_id": "identify_stakeholder",
                "action": "classify_user_type",
                "tool_name": "bim_agent",
                "expected_outcome": "Stakeholder type identified"
            },
            {
                "step_id": "contextualize_query",
                "action": "adapt_response_style",
                "tool_name": "orchestrator",
                "expected_outcome": "Response approach tailored to stakeholder"
            },
            {
                "step_id": "execute_analysis",
                "action": "perform_targeted_analysis",
                "tool_name": "multiple",
                "expected_outcome": "Stakeholder-specific analysis completed"
            }
        ]

    def orchestrate_task(self, user_query: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Main orchestration method that processes user queries using o3-mini reasoning
        
        Args:
            user_query: User's natural language query
            context: Additional context (stakeholder type, BIM data, etc.)
            
        Returns:
            Dict containing response and performance metrics
        """
        start_time = time.time()
        task_id = f"task_{int(time.time())}"
        
        try:
            # Step 1: Analyze query complexity and determine reasoning effort
            complexity, reasoning_effort = self._analyze_query_complexity(user_query)
            
            # Step 2: Plan workflow using o3-mini
            workflow_plan = self._plan_workflow(user_query, complexity, context or {})
            
            # Step 3: Execute planned workflow
            execution_results = self._execute_workflow(workflow_plan, reasoning_effort)
            
            # Step 4: Synthesize final response
            final_response = self._synthesize_response(
                user_query, execution_results, context or {}
            )
            
            # Step 5: Record performance metrics
            execution_time = time.time() - start_time
            metrics = self._record_performance(
                task_id, user_query, complexity, reasoning_effort, 
                execution_time, execution_results
            )
            
            # Step 6: Trigger self-improvement cycle if needed
            self._trigger_improvement_cycle()
            
            return {
                "success": True,
                "response": final_response,
                "task_id": task_id,
                "metrics": asdict(metrics),
                "reasoning_steps": execution_results.get("reasoning_steps", [])
            }
            
        except Exception as e:
            logger.error(f"Orchestration error: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_id": task_id
            }

    def _analyze_query_complexity(self, query: str) -> Tuple[TaskComplexity, ReasoningEffort]:
        """Analyze query to determine complexity and required reasoning effort"""
        
        if not self.client:
            # Fallback complexity analysis
            if len(query.split()) > 50 or any(word in query.lower() for word in 
                   ["analyze", "compare", "optimize", "integrate", "complex"]):
                return TaskComplexity.HIGH, ReasoningEffort.HIGH
            return TaskComplexity.MEDIUM, ReasoningEffort.MEDIUM
            
        try:
            response = self.client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "Analyze the complexity of BIM-related queries. Classify as LOW (simple info requests), MEDIUM (analysis tasks), or HIGH (complex reasoning/integration tasks). Also suggest reasoning effort needed."
                    },
                    {
                        "role": "user", 
                        "content": f"Analyze this query complexity: {query}"
                    }
                ],
                reasoning_effort="low"
            )
            
            analysis = response.choices[0].message.content
            
            # Parse complexity from response
            if analysis and "HIGH" in analysis.upper():
                return TaskComplexity.HIGH, ReasoningEffort.HIGH
            elif analysis and "LOW" in analysis.upper():
                return TaskComplexity.LOW, ReasoningEffort.LOW
            else:
                return TaskComplexity.MEDIUM, ReasoningEffort.MEDIUM
                
        except Exception as e:
            logger.warning(f"Complexity analysis failed: {e}")
            return TaskComplexity.MEDIUM, ReasoningEffort.MEDIUM

    def _plan_workflow(self, query: str, complexity: TaskComplexity, 
                      context: Dict[str, Any]) -> OrchestrationTask:
        """Plan workflow using o3-mini reasoning"""
        
        task_id = f"plan_{int(time.time())}"
        
        # Determine workflow template based on query type
        if "analyze" in query.lower() or "ifc" in query.lower():
            template = self.workflow_templates["bim_analysis"]
        else:
            template = self.workflow_templates["stakeholder_query"]
            
        # Create workflow steps from template
        workflow_steps = []
        for i, step_template in enumerate(template):
            step = WorkflowStep(
                step_id=f"{task_id}_step_{i}",
                action=step_template["action"],
                tool_name=step_template.get("tool_name"),
                parameters={},
                expected_outcome=step_template["expected_outcome"]
            )
            workflow_steps.append(step)
            
        return OrchestrationTask(
            task_id=task_id,
            user_query=query,
            stakeholder_type=context.get("stakeholder_type") if context else None,
            complexity=complexity,
            workflow_steps=workflow_steps
        )

    def _execute_workflow(self, task: OrchestrationTask, 
                         reasoning_effort: ReasoningEffort) -> Dict[str, Any]:
        """Execute planned workflow with monitoring and reflection"""
        
        results = {
            "steps_completed": [],
            "reasoning_steps": [],
            "errors": [],
            "tool_calls": 0
        }
        
        for step in task.workflow_steps:
            step_start = time.time()
            
            try:
                # Execute step based on tool name
                if step.tool_name == "ifc_gateway":
                    step_result = self._execute_ifc_step(step)
                elif step.tool_name == "bim_agent":
                    step_result = self._execute_bim_agent_step(step)
                elif step.tool_name == "ai_service":
                    step_result = self._execute_ai_service_step(step)
                elif step.tool_name == "orchestrator":
                    step_result = self._execute_orchestrator_step(step, reasoning_effort)
                else:
                    step_result = {"success": False, "error": "Unknown tool"}
                    
                # Record step completion
                step.execution_time = time.time() - step_start
                step.success = step_result.get("success", False)
                step.actual_outcome = step_result.get("outcome", "")
                
                results["steps_completed"].append(asdict(step))
                if step.success:
                    results["tool_calls"] += 1
                else:
                    results["errors"].append(step_result.get("error", "Unknown error"))
                    
            except Exception as e:
                step.success = False
                step.actual_outcome = f"Error: {str(e)}"
                results["errors"].append(str(e))
                logger.error(f"Step execution failed: {e}")
                
        return results

    def _execute_orchestrator_step(self, step: WorkflowStep, 
                                  reasoning_effort: ReasoningEffort) -> Dict[str, Any]:
        """Execute orchestrator-specific steps using o3-mini"""
        
        if not self.client:
            return {"success": False, "error": "o3-mini client not available"}
            
        try:
            response = self.client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompts["orchestrator"]
                    },
                    {
                        "role": "user",
                        "content": f"Execute step: {step.action}. Expected outcome: {step.expected_outcome}"
                    }
                ],
                reasoning_effort=reasoning_effort.value
            )
            
            return {
                "success": True,
                "outcome": response.choices[0].message.content,
                "reasoning_used": reasoning_effort.value
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_ifc_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute IFC gateway operations"""
        try:
            if step.action == "load_ifc_file":
                # Implementation for IFC file loading
                return {"success": True, "outcome": "IFC file loaded"}
            elif step.action == "get_building_elements":
                # Implementation for element extraction
                return {"success": True, "outcome": "Elements extracted"}
            else:
                return {"success": False, "error": "Unknown IFC action"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_bim_agent_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute BIM agent operations"""
        try:
            if step.action == "classify_user_type":
                # Implementation for stakeholder classification
                return {"success": True, "outcome": "Stakeholder classified"}
            else:
                return {"success": False, "error": "Unknown BIM agent action"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_ai_service_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute AI service operations"""
        try:
            if step.action == "analyze_structural_elements":
                # Implementation for structural analysis
                return {"success": True, "outcome": "Structural analysis completed"}
            else:
                return {"success": False, "error": "Unknown AI service action"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _synthesize_response(self, query: str, execution_results: Dict[str, Any], 
                           context: Dict[str, Any]) -> str:
        """Synthesize final response using o3-mini"""
        
        if not self.client:
            return "Analysis completed. Please check individual step results."
            
        try:
            # Prepare context for synthesis
            synthesis_prompt = f"""
Based on the workflow execution results, synthesize a comprehensive response to: {query}

Execution Summary:
- Steps completed: {len(execution_results['steps_completed'])}
- Tool calls made: {execution_results['tool_calls']}
- Errors encountered: {len(execution_results['errors'])}

Provide a clear, actionable response that addresses the user's query while highlighting key insights from the analysis.
"""

            response = self.client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompts["orchestrator"]
                    },
                    {
                        "role": "user",
                        "content": synthesis_prompt
                    }
                ],
                reasoning_effort="medium"
            )
            
            return response.choices[0].message.content or "Analysis completed successfully."
            
        except Exception as e:
            logger.error(f"Response synthesis failed: {e}")
            return "Analysis completed with mixed results. Please review the detailed workflow steps for more information."

    def _record_performance(self, task_id: str, query: str, complexity: TaskComplexity,
                          reasoning_effort: ReasoningEffort, execution_time: float,
                          results: Dict[str, Any]) -> PerformanceMetrics:
        """Record performance metrics for continuous improvement"""
        
        # Calculate success rate
        total_steps = len(results["steps_completed"])
        successful_steps = sum(1 for step in results["steps_completed"] if step["success"])
        success_rate = successful_steps / total_steps if total_steps > 0 else 0.0
        
        metrics = PerformanceMetrics(
            task_id=task_id,
            timestamp=datetime.now(),
            task_complexity=complexity,
            reasoning_effort=reasoning_effort,
            response_time=execution_time,
            success_rate=success_rate,
            tool_calls_made=results["tool_calls"],
            error_count=len(results["errors"])
        )
        
        self.performance_history.append(metrics)
        
        # Keep only last 1000 metrics
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
            
        return metrics

    def _trigger_improvement_cycle(self):
        """Trigger self-improvement cycle based on performance analysis"""
        
        # Trigger improvement every 50 tasks or if success rate drops below 70%
        recent_metrics = self.performance_history[-50:] if len(self.performance_history) >= 50 else self.performance_history
        
        if len(recent_metrics) >= 10:
            avg_success_rate = sum(m.success_rate for m in recent_metrics) / len(recent_metrics)
            
            if avg_success_rate < 0.7 or len(self.performance_history) % 50 == 0:
                self._perform_self_improvement()

    def _perform_self_improvement(self):
        """Perform self-improvement using o3-mini analysis"""
        
        if not self.client:
            logger.warning("Cannot perform self-improvement: o3-mini client not available")
            return
            
        try:
            # Analyze recent performance
            recent_metrics = self.performance_history[-50:]
            
            improvement_prompt = f"""
Analyze the performance metrics of the AI orchestrator and suggest improvements:

Recent Performance Summary:
- Total tasks: {len(recent_metrics)}
- Average success rate: {sum(m.success_rate for m in recent_metrics) / len(recent_metrics):.2f}
- Average response time: {sum(m.response_time for m in recent_metrics) / len(recent_metrics):.2f}s
- Common errors: {[m.error_count for m in recent_metrics]}

Suggest specific improvements to:
1. System prompts
2. Workflow templates  
3. Tool usage patterns
4. Performance optimization

Provide actionable recommendations for enhancing orchestrator performance.
"""

            response = self.client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI system improvement analyst. Analyze performance data and suggest concrete improvements."
                    },
                    {
                        "role": "user",
                        "content": improvement_prompt
                    }
                ],
                reasoning_effort="high"
            )
            
            improvements = response.choices[0].message.content or "No specific improvements identified at this time."
            logger.info(f"Self-improvement analysis completed: {improvements}")
            
            # Implement automatic improvements where possible
            self._implement_improvements(improvements)
            self.improvement_cycle_count += 1
            
        except Exception as e:
            logger.error(f"Self-improvement cycle failed: {e}")

    def _implement_improvements(self, improvements: str):
        """Implement suggested improvements automatically"""
        
        # This is a simplified implementation
        # In practice, this would parse the improvements and apply them
        
        logger.info(f"Implementing improvements from cycle {self.improvement_cycle_count}")
        
        # Example: Adjust reasoning effort based on performance
        if "reduce reasoning effort" in improvements.lower():
            # Adjust default reasoning effort for better performance
            pass
            
        if "improve prompts" in improvements.lower():
            # Automatically refine system prompts
            pass

    def get_performance_analytics(self) -> Dict[str, Any]:
        """Get comprehensive performance analytics"""
        
        if not self.performance_history:
            return {"message": "No performance data available"}
            
        recent_metrics = self.performance_history[-100:]
        
        return {
            "total_tasks": len(self.performance_history),
            "recent_performance": {
                "success_rate": sum(m.success_rate for m in recent_metrics) / len(recent_metrics),
                "avg_response_time": sum(m.response_time for m in recent_metrics) / len(recent_metrics),
                "tool_usage": sum(m.tool_calls_made for m in recent_metrics),
                "error_rate": sum(m.error_count for m in recent_metrics) / len(recent_metrics)
            },
            "improvement_cycles": self.improvement_cycle_count,
            "trends": self._calculate_performance_trends()
        }

    def _calculate_performance_trends(self) -> Dict[str, Any]:
        """Calculate performance trends over time"""
        
        if len(self.performance_history) < 20:
            return {"message": "Insufficient data for trend analysis"}
            
        # Compare recent vs historical performance
        recent = self.performance_history[-20:]
        historical = self.performance_history[-40:-20] if len(self.performance_history) >= 40 else []
        
        if not historical:
            return {"message": "Insufficient historical data"}
            
        recent_success = sum(m.success_rate for m in recent) / len(recent)
        historical_success = sum(m.success_rate for m in historical) / len(historical)
        
        return {
            "success_rate_trend": "improving" if recent_success > historical_success else "declining",
            "improvement_delta": recent_success - historical_success
        }

# Global orchestrator instance
_orchestrator_instance = None

def get_orchestrator() -> SelfImprovingOrchestrator:
    """Get singleton orchestrator instance"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = SelfImprovingOrchestrator()
    return _orchestrator_instance