from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class BMIState(TypedDict):
    weight: float
    height: float
    bmi: float
    category:str


def calculate_bmi(state: BMIState):
    weight = state["weight"]
    height = state["height"]

    bmi = weight / (height ** 2)

    return {
        "weight": weight,
        "height": height,
        "bmi": round(bmi, 2)
    }

def label_bmi(state: BMIState) -> BMIState:
    bmi = state["bmi"]

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return {
        **state,
        "category": category
    } 


# Define your graph
graph = StateGraph(BMIState)

# Add node to your graph
graph.add_node("calculate_bmi", calculate_bmi)
graph.add_node('label_bmi',label_bmi)


# Add edges to your graph
graph.add_edge(START, "calculate_bmi")
graph.add_edge("calculate_bmi", "label_bmi")
graph.add_edge("label_bmi", END)

# Compile the graph
workflow = graph.compile()

# Run the graph
result = workflow.invoke({
    "weight": 90,
    "height": 1.75,
    "bmi": 0
})

print(result)

png_data = workflow.get_graph().draw_mermaid_png()

with open("bmi_graph.png", "wb") as f:
    f.write(png_data)

print("Graph saved as bmi_graph.png")