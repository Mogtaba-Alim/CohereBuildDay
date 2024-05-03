from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_core.pydantic_v1 import BaseModel, Field

python_repl = PythonREPL()
python_tool = Tool(
    name="python_repl"
    , description="Executes python code and returns the result. The code runs in a static sandbox without interactive mode, so print output or save output to a file."
    , func=python_repl.run
)
python_tool.name = "python_interpreter"

# from langchain_core.pydantic_v1 import BaseModel, Field
class ToolInput(BaseModel):
    code: str = Field(description="Python code to execute.")
python_tool.args_schema = ToolInput