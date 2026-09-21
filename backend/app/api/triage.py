from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from app.orchestrator.graph import graph

router = APIRouter(prefix="/v1/triage", tags=["SOC Triage"])

# 1. Strict Input Validation
class AlertPayload(BaseModel):
    alert_id: str
    source: str = Field(..., description="E.g., splunk, elastic, sentinel")
    raw_log: str
    severity: str

# 2. Strict Output Validation
class TriageResponse(BaseModel):
    summary: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    mitre_tactics: List[str] = []
    recommended_actions: List[str] = []
    blocked: bool = False

@router.post("/", response_model=TriageResponse)
async def run_triage(payload: AlertPayload):
    """Executes the LangGraph orchestrator against a single alert."""
    
    # Initialize the state machine
    initial_state = {
        "alert_payload": payload.model_dump_json(),
        "history": [],
        "tool_results": [],
        "blocked": False,
        "final_analysis": ""
    }
    
    try:
        # Run the LangGraph state machine asynchronously
        result_state = await graph.ainvoke(initial_state)
        
        if result_state.get("blocked"):
            return TriageResponse(
                summary=result_state.get("final_analysis", "Blocked by security policy."),
                confidence_score=1.0,
                blocked=True
            )
            
        # Parse the LLM's final string into our strict schema
        # (In production, use the LLM's JSON mode or structured outputs here)
        import json
        analysis_data = json.loads(result_state.get("final_analysis", "{}"))
        
        return TriageResponse(
            summary=analysis_data.get("summary", "Analysis completed."),
            confidence_score=analysis_data.get("confidence", 0.85),
            mitre_tactics=analysis_data.get("mitre_tactics", []),
            recommended_actions=analysis_data.get("recommended_actions", []),
            blocked=False
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestrator failure: {str(e)}")
