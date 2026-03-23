from typing import Annotated, TypedDict, Union, List
from langgraph.graph import StateGraph, END
import operator

# Define the state of our multi-agent system
class AgentState(TypedDict):
    invoice_data: dict
    audit_results: str
    is_approved: bool
    messages: Annotated[List[str], operator.add]
    logs: Annotated[List[str], operator.add]

# --- Agent Definitions ---

class FinBotAgents:
    def __init__(self, model_name="gpt-4o"):
        self.model_name = model_name

    def invoicer(self, state: AgentState):
        """Creates or updates a draft invoice."""
        print("--- Invoicer Agent ---")
        invoice = state.get("invoice_data", {})
        if not invoice:
            invoice = {"amount": 5000, "vendor": "ACME Corp", "description": "Cloud Services"}
        
        return {
            "invoice_data": invoice,
            "messages": ["Invoicer: Generated draft invoice."],
            "logs": ["Invoicer processed the request."]
        }

    def auditor(self, state: AgentState):
        """Audits the invoice for fraud or errors."""
        print("--- Auditor Agent ---")
        invoice = state["invoice_data"]
        
        # Simple rule-based audit for PoC
        if invoice["amount"] > 10000:
            audit_res = "FLAGGED: High amount requires manual review."
            is_approved = False
        elif "malicious" in str(invoice).lower():
            audit_res = "FLAGGED: Potential prompt injection or malicious data."
            is_approved = False
        else:
            audit_res = "PASSED: Budget-compliant."
            is_approved = True

        return {
            "audit_results": audit_res,
            "is_approved": is_approved,
            "messages": [f"Auditor: Audit result - {audit_res}"],
            "logs": ["Auditor completed the check."]
        }

    def finalizer(self, state: AgentState):
        """Finalizes and 'approves' the invoice if audit passed."""
        print("--- Finalizer Agent ---")
        if state["is_approved"]:
            msg = "Finalizer: Invoice approved and processed."
        else:
            msg = "Finalizer: Invoice rejected based on audit."
            
        return {
            "messages": [msg],
            "logs": ["Finalizer completed the task."]
        }
