import os
from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()
MODEL = "gemini-3.5-flash-lite"
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


class PerfilUsuario(BaseModel):
    nome: str = Field(description="Nome do usuário")
    idade: int = Field(ge=0, le=120, description="Idade do usuário, entre 0 e 120")
    habilidades: list[str] = Field(description="Habilidades do usuário")
    status: Literal["ativo", "inativo", "pendente"] = Field(description="Status do usuário")

    # TODO: declare os campos do perfil com type hints e Field(description=...):
    #   nome (str), idade (int, entre 0 e 120: dica, Field(ge=0, le=120)), habilidades (list[str]),
    #   status (Literal["ativo", "inativo", "pendente"])
    ...


TEXTO = (
    "Oi, sou a Marina Souza, tenho 29 anos e trabalho com Python, SQL e Power BI. "
    "Minha conta ainda esta aguardando aprovacao do time."
)


def extrair_perfil(texto: str) -> PerfilUsuario:
    response = client.models.generate_content(
        model=MODEL,
        contents=f"Extraia o perfil do usuario do texto abaixo.\n\n{texto}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",

            response_schema=PerfilUsuario,
            # TODO: passe a classe PerfilUsuario em response_schema
        ),
    )
    # response.parsed ja vem como instancia de PerfilUsuario
    return response.parsed


if __name__ == "__main__":
    perfil = extrair_perfil(TEXTO)  
    print(perfil.model_dump_json(indent=2)) 
    print(perfil.model_json_schema())
    # TODO: imprima o JSON Schema gerado pelo Pydantic com PerfilUsuario.model_json_schema()