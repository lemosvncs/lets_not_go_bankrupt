from tabula import read_pdf
import pandas as pd
import polars as pl


# -----------------
file = "files/528025333_7add382a-1394-44b0-8403-b228bc6eca73.pdf"
from PyPDF2 import PdfReader


reader = PdfReader(file)
texto = ""

for page in reader.pages:
    texto += page.extract_text()

# ----------------
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

class Despesa(BaseModel):
    data: str = Field(description="Data da despesa")
    valor: float = Field(description="Valor da despesa")
    descricao: str = Field(description="Descrição da despesa")

class ListaDespesas(BaseModel):
    despesas: list[Despesa] = Field(description="Lista de despesas")

ollama_model = OpenAIModel(
    model_name='llama3.2',
    provider=OpenAIProvider(base_url='http://localhost:11434/v1'),
)

contador_agent = Agent(
    ollama_model,
    deps_type=str,
    output_type=ListaDespesas,
    # output_type=BuscaPrestador,
    # tools=[get_prestador_especialidade],
    system_prompt="""
    Você é Bernardo, um contador que ama ler faturas de cartão de crédito para criar planilhas bem estruturadas.
    """,
)

contador_agent.run_sync(user_prompt=texto)



