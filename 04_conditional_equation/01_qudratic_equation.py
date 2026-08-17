from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal


class QuadEquation(TypedDict, total=False):
    a: int
    b: int
    c: int

    equation: str
    discriminant: float
    result: str


graph = StateGraph(QuadEquation)


# 1. Show quadratic equation
def show_equation(state: QuadEquation):
    equation = f'{state["a"]}x^2 + {state["b"]}x + {state["c"]} = 0'

    return {
        "equation": equation
    }


# 2. Calculate discriminant
def calculate_discriminant(state: QuadEquation):
    discriminant = state["b"] ** 2 - (4 * state["a"] * state["c"])

    return {
        "discriminant": discriminant
    }


# 3. Calculate real roots
def real_roots(state: QuadEquation):

    root1 = (
        -state["b"] + state["discriminant"] ** 0.5
    ) / (2 * state["a"])

    root2 = (
        -state["b"] - state["discriminant"] ** 0.5
    ) / (2 * state["a"])

    result = f"The roots are {root1} and {root2}"

    return {
        "result": result
    }


# 4. Calculate repeated root
def repeated_roots(state: QuadEquation):

    root = -state["b"] / (2 * state["a"])

    result = f"The repeated root is {root}"

    return {
        "result": result
    }


# 5. No real roots
def no_real_roots(state: QuadEquation):

    result = "No real roots"

    return {
        "result": result
    }


# 6. Check discriminant condition
def check_condition(
    state: QuadEquation
) -> Literal["real_roots", "repeated_roots", "no_real_roots"]:

    if state["discriminant"] > 0:
        return "real_roots"

    elif state["discriminant"] == 0:
        return "repeated_roots"

    else:
        return "no_real_roots"


# Add nodes
graph.add_node("show_equation", show_equation)
graph.add_node("calculate_discriminant", calculate_discriminant)
graph.add_node("real_roots", real_roots)
graph.add_node("repeated_roots", repeated_roots)
graph.add_node("no_real_roots", no_real_roots)


# Normal edges
graph.add_edge(START, "show_equation")
graph.add_edge("show_equation", "calculate_discriminant")


# Conditional edges
graph.add_conditional_edges(
    "calculate_discriminant",
    check_condition,
    {
        "real_roots": "real_roots",
        "repeated_roots": "repeated_roots",
        "no_real_roots": "no_real_roots"
    }
)


# End edges
graph.add_edge("real_roots", END)
graph.add_edge("repeated_roots", END)
graph.add_edge("no_real_roots", END)


# Compile
workflow = graph.compile()


# Initial state
initial_state = {
    "a": 2,
    "b": 4,
    "c": 2
}


# Run
result = workflow.invoke(initial_state)

print(result)