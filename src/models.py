from pydantic import BaseModel
from typing_extensions import Literal

class DayBusinessData(BaseModel):
    """
    Represents business data for a single day.

    Attributes:
        sales (float): Total sales for the day.
        cost (float): Total cost incurred for the day.
        number_of_customers (int): Number of customers for the day.
    """

    sales: float
    cost: float
    number_of_customers: int


class InputState(BaseModel):
    """
    Input state for the graph, containing today's and previous day's business data.

    Attributes:
        today (DayBusinessData): Business data for today.
        previous_day (DayBusinessData): Business data for the previous day.
    """

    today: DayBusinessData
    previous_day: DayBusinessData


class BusinessState(BaseModel):
    """
    Intermediate computed state used within the graph for analysis and monitoring.

    Attributes:
        profit (float): Calculated profit for the day (sales - cost).
        sales_change_percent (float): Percentage change in sales compared to the previous day.
        cost_change_percent (float): Percentage change in cost compared to the previous day.
        cac_increase_percent (float): Percentage increase in Customer Acquisition Cost (CAC) compared to the previous day.
        is_cac_increased_significantly (bool): Indicates if the CAC has increased significantly (more than 20%).
    """

    profit: float
    sales_change_percent: float
    cost_change_percent: float
    cac_increase_percent: float
    is_cac_increased_significantly: bool


class OutputState(BaseModel):
    """
    Final structured output state containing high-level insights and recommendations.

    Attributes:
        status (Literal["loss", "profit"]): Indicates whether the day ended in profit or loss.
        alerts_warnings (str): Alerts or warnings generated based on business metrics.
        recommendation (str): Suggested actions or recommendations based on the day's performance.
    """

    status: Literal["loss", "profit"]
    alerts_warnings: str
    recommendation: str

