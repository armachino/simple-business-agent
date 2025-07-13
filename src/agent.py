from langgraph.graph import StateGraph, START, END
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import RegexParser

from src.models import InputState, BusinessState, OutputState

from dotenv import load_dotenv
load_dotenv()


class Agent:
    x=1
    def __init__(self, model):
        self.model = model
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a smart business analysis assistant that evaluates daily business metrics "
                    "and generates short actionable insights.\n\n"
                    "Here is a description of the business data you will analyze:\n"
                    "- Profit (float): Calculated profit for the day (sales - cost).\n"
                    "- Sales Change (%) (float): Percentage change in sales compared to the previous day.\n"
                    "- Cost Change (%) (float): Percentage change in cost compared to the previous day.\n"
                    "- CAC Increase (%) (float): Percentage increase in Customer Acquisition Cost compared to the previous day.\n"
                    "- CAC Increase Significantly (bool): Indicates if the CAC has increased significantly (more than 20%).\n"
                    "- Status (str): Indicates whether the business made a 'profit' or a 'loss' today.\n\n"
                    "Please analyze the provided data and respond in this format:\n"
                    "1. ALERT: Describe any concerning patterns or anomalies (e.g., high CAC increase, negative profit). "
                    "If there is nothing critical, say 'No alerts'.\n"
                    "2. RECOMMENDATION: Provide clear, practical business advice to improve performance.\n\n"
                    "Be concise, direct, and business-oriented.\n\n"
                    "Examples of recommendations:\n"
                    '- "Reduce costs if profit is negative"\n'
                    '- "Review marketing campaigns if CAC increased significantly"\n'
                    '- "Consider increasing advertising budget if sales are growing"\n\n'
                    "For example, warn if CAC increased, and suggest increasing marketing budget if sales grew.",
                ),
                (
                    "user",
                    "Today's business data:\n"
                    "- Profit: {profit}\n"
                    "- Sales Change (%): {sales_change_percent}\n"
                    "- Cost Change (%): {cost_change_percent}\n"
                    "- CAC Increase (%): {cac_increase_percent}\n"
                    "- CAC Increase Significantly: {is_cac_increased_significantly}\n"
                    "- Status: {status}",
                ),
            ]
        )
        builder = StateGraph(
            BusinessState, input_schema=InputState, output_schema=OutputState
        )
        # Define the nodes
        # ****The <input_node> is not necessary for the implementation but is included because of the task requirements.****
        # builder.add_node("input_node", self.input_node)
        builder.add_node("processing_node", self.processing_node)  # type: ignore
        builder.add_node("recommendation_node", self.recommendation_node)
        # Define the edges
        # builder.add_edge(START, "input_node")
        # builder.add_edge("input_node", "processing_node")
        builder.add_edge(START, "processing_node")
        builder.add_edge("processing_node", "recommendation_node")
        builder.add_edge("processing_node", END)
        self._graph = builder.compile()

    @property
    def graph(self):
        return self._graph

    # def input_node(self, input_state: InputState) -> InputState:
    #     """Initializes the input state for the graph.
    #     *******The <input_node> is not necessary for the implementation but is included because of the task requirements.****
    #     Args:
    #         input_state (InputState): The input state containing today's and previous day's business data.
    #     """
    #     return input_state

    def processing_node(self, state: InputState) -> BusinessState:
        """
        Processes the input state to compute key business metrics and generate actionable outputs.

        Args:
            state (InputState): The input state containing today's and previous day's business data.

        Returns:
                OutputState: Contains user-facing summary information with status, alerts, and recommendations.
        """
        today = state.today
        prev = state.previous_day

        # Calculate today's profit
        profit = today.sales - today.cost

        # Calculate % change in sales and cost
        sales_change_percent = (
            ((today.sales - prev.sales) / prev.sales) * 100 if prev.sales != 0 else 0
        )
        cost_change_percent = (
            ((today.cost - prev.cost) / prev.cost) * 100 if prev.cost != 0 else 0
        )

        # Calculate CAC (Customer Acquisition Cost)
        today_cac = (
            today.cost / today.number_of_customers
            if today.number_of_customers != 0
            else 0
        )
        prev_cac = (
            prev.cost / prev.number_of_customers if prev.number_of_customers != 0 else 0
        )

        cac_increase_percent = (
            ((today_cac - prev_cac) / prev_cac) * 100 if prev_cac != 0 else 0
        )
        is_cac_increased_significantly = cac_increase_percent > 20
        businessState = BusinessState(
            profit=profit,
            sales_change_percent=sales_change_percent,
            cost_change_percent=cost_change_percent,
            cac_increase_percent=cac_increase_percent,
            is_cac_increased_significantly=is_cac_increased_significantly,
        )
        print(businessState)
        return businessState

    def recommendation_node(self, state: BusinessState) -> OutputState:
        """
        Generates recommendations based on the business state.

        Args:
            state (BusinessState): The current business state containing calculated metrics.

        Returns:
            OutputState: Contains user-facing summary information with status, alerts, and recommendations.
        """
        profit = state.profit

        # Determine status
        status = "profit" if profit >= 0 else "loss"

        prompt = self.prompt_template.format_messages(
            profit=state.profit,
            sales_change_percent=state.sales_change_percent,
            cost_change_percent=state.cost_change_percent,
            cac_increase_percent=state.cac_increase_percent,
            is_cac_increased_significantly=state.is_cac_increased_significantly,
            status=status,
        )

        response = self.model.invoke(prompt)
        print(response.content)
        response = response.content.strip()
        # Parse the response using RegexParser for extracting alerts and recommendations
        parser = RegexParser(
            regex=r"1\.\s*ALERT:\s*(.*?)\s*2\.\s*RECOMMENDATION:\s*(.*)",
            output_keys=["alert", "recommendation"],
        )
        parsed = parser.parse(response)

        return OutputState(
            status=status,
            alerts_warnings=parsed["alert"],
            recommendation=parsed["recommendation"],
        )
