# src/agentic_ai/core/agents/react_agent.py
from typing import Dict, Any, List
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.callbacks import get_openai_callback
from .base import BaseAgent
import time

class ReActAgent(BaseAgent):
    """ReAct pattern agent with reasoning and acting capabilities"""
    
    def __init__(self, name: str, tools: List, model: str = "gpt-3.5-turbo"):
        super().__init__(name, "ReAct agent with step-by-step reasoning")
        
        # Initialize LLM
        self.llm = ChatOpenAI(model=model, temperature=0)
        
        # Create agent
        prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(self.llm, tools, prompt)
        
        self.executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
    
    async def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute task with ReAct pattern"""
        start_time = time.time()
        
        # Prepare input
        input_text = task
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            input_text = f"Context:\n{context_str}\n\nTask: {task}"
        
        try:
            with get_openai_callback() as cb:
                result = await self.executor.ainvoke({"input": input_text})
                
                execution_result = {
                    "success": True,
                    "output": result.get("output", ""),
                    "cost": cb.total_cost,
                    "tokens": cb.total_tokens,
                    "duration": time.time() - start_time
                }
                
                self.log_execution(task, execution_result, execution_result["duration"])
                return execution_result
                
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "duration": time.time() - start_time
            }
            self.log_execution(task, error_result, error_result["duration"])
            return error_result
    
    def get_capabilities(self) -> List[str]:
        """Return agent capabilities"""
        return [
            "step_by_step_reasoning",
            "tool_usage",
            "problem_solving",
            "adaptable_execution"
        ]