from langchain.tools import Tool

def get_tools():

    tools = [

        Tool(
            name="Business Advisor",
            func=lambda x: x,
            description="Answers business questions"
        )

    ]

    return tools