from time import time
import random
from typing import List, Callable
from langchain.agents import Tool
from loguru import logger
from pydantic import BaseModel, Field

from src.model.utils import return_with_name


class EmptyInputSchema(BaseModel):
    """Input"""
    input: str = Field(description="Anything")


class ToolConstructor:
    def __init__(self):
        self.tools = self.construct_tools(debug=True)

    def construct_tools(self, debug=False) -> List[Tool]:
        """
        Create langchain agent tools
        :param debug: bool
        :return:
        """
        # function = (Callable, Description, args_schema)
        functions_with_description = [
            (
                self.change_background_color,
                "Useful for changing the background color. Input color in hexadecimal."
            ),
            (
                self.change_message_color,
                "Useful for changing the color of messages. Input color in hexadecimal."
            ),
            (
                self.randomize_personality_sliders,
                "Useful for changing personality of bots to random",
                EmptyInputSchema
            ),
            # (
            #     self.cashback_balance,
            #     "Useful for answering questions about a user's cashback balance.",
            #     EmptyInputSchema
            # ),
            # (
            #     self.delivery_status,
            #     "Call this function when the user is interested in their delivery/package (e.g., ETA or location).",
            #     EmptyInputSchema
            # ),
            #
            # (
            #     self.wallet_linking,
            #     "Useful for linking a virtual wallet to a user's account."
            # ),
            # (
            #     self.document_status,
            #     "Checks the status of documents sent to a user."
            # ),
            # (
            #     self.refund_status,
            #     "Checks the status of a refund for the last item purchased by a user."
            # ),
        ]

        tools = [self._make_tool(*func_tuple) for func_tuple in functions_with_description]
        if debug:
            logger.debug("Functions: ")
            for tool in tools:
                logger.debug(f"{tool.name}: {tool.description}")
        return tools

    @staticmethod
    def _make_tool(function: Callable, description: str, args_schema: dict = None):
        """
        This function creates a Langchain Tool, that has pythonic function name for a langchain tool name.

        :param function:
        :param description:
        :param args_schema:
        :return:
        """
        tool_args = {
            'name': function.__name__,
            'func': function,
            'description': description
        }
        if args_schema:
            tool_args['args_schema'] = args_schema

        tool = Tool(**tool_args)
        return tool

    # ------------------ #
    #   Bot Functions:   #
    # ------------------ #
    @return_with_name
    def change_background_color(self, color_hex: str):
        return color_hex

    @return_with_name
    def change_message_color(self, color_hex: str):
        return color_hex

    @return_with_name
    def randomize_personality_sliders(self, any_input: str):
        seed = int(time() * 1000)  # Use the current system time as a seed
        random.seed(seed)
        return [random.randint(0, 3) for _ in range(8)]

    @return_with_name
    def cashback_balance(self, x):
        return "5 рублей"

    @return_with_name
    def delivery_status(self, x):
        return "Shipment is being delivered. Will come in 10 minutes (Function delivery_status was called)"

    @return_with_name
    def wallet_linking(self, x):
        return "Virtual wallet linked successfully"

    @return_with_name
    def document_status(self, x):
        return "Documents are preparing"

    @return_with_name
    def refund_status(self, x):
        return "Refund will be provided in 1 hour"
