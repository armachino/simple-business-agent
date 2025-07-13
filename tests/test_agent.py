
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.models import InputState, OutputState, BusinessState  
from src.agent import Agent  


def test_agent(model):
    input_state_dict = {
        "today": {"sales": 1000.0, "cost": 1200.0, "number_of_customers": 30},
        "previous_day": {"sales": 900.0, "cost": 1000.0, "number_of_customers": 40},
    }

    # Parse the dictionary into the Pydantic model for validation
    input_state = InputState.model_validate(input_state_dict)

    agent = Agent(model)
    # Proccesing node test
    processing_node_res: BusinessState = agent.processing_node(input_state)
    assert round(processing_node_res.profit, 2) == -200.0, (
        "Profit should be -200.0 (1000 - 1200)"
    )
    assert round(processing_node_res.sales_change_percent, 2) == 11.11, (
        "Sales change should be 11.11% ((1000 - 900) / 900 * 100)"
    )
    assert round(processing_node_res.cost_change_percent, 2) == 20.0, (
        "Cost change should be 20.0% ((1200 - 1000) / 1000 * 100)"
    )
    assert round(processing_node_res.cac_increase_percent, 2) == 60.0, (
        "CAC increase should be 60.0% ((40 - 25) / 25 * 100)"
    )
    assert processing_node_res.is_cac_increased_significantly

    print("✅ processing_node test passed.")
    print("Output:", processing_node_res)
    # Reccommendation node test
    output_res: OutputState = agent.recommendation_node(processing_node_res)
    assert output_res.status == "loss", (
        "Status should be 'loss' since profit is negative"
    )
    assert "alerts_warnings" in output_res.model_fields_set
    assert "recommendation" in output_res.model_fields_set
    print("✅ recommendation_node test passed.")


