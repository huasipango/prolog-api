from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

from prologpy.solver import Solver

class PrologTest(BaseModel):
    rules_text: str
    query_text: str

app = FastAPI()

def run_query(rules_text, query_text):
    """Interpret the entered rules and query and display the results in the
    solutions text box """

    try:
        solver = Solver(rules_text)
    except Exception as e:
        error = "Error processing prolog rules." + str(e)
        return

    # Attempt to find the solutions and handle any exceptions gracefully
    try:
        solutions = solver.find_solutions(query_text)
    except Exception as e:
        error = "Error processing prolog query." + str(e)
        return

    # If our query returns a boolean, we simply display a 'Yes' or a 'No'
    # depending on its value
    if isinstance(solutions, bool):
        solutions_display = "Yes." if solutions else "No."

    # Our solver returned a map, so we display the variable name to value mappings
    elif isinstance(solutions, dict):
        solutions_display = "\n".join("{} = {}".format(variable, value[0] if len(value) == 1 else value)for variable, value in solutions.items())
    else:
        # We know we have no matching solutions in this instance so we provide
        # relevant feedback
        solutions_display = "No solutions found."
    return solutions_display

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/prolog")
def read_root(prolog_test: PrologTest):
    return run_query(prolog_test.rules_text, prolog_test.query_text)
