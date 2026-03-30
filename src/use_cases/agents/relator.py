"""Nó do agente relator: consolida achados e emite o parecer técnico final."""

from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from domain.entities.auditoria import ParecerTecnico
from use_cases.agents.prompts import PROMPT_AGENTE_RELATOR
from use_cases.state import AuditoriaState


class AgenteRelatorNode:
    """Nó responsável por consolidar os achados e gerar o documento final."""

    def __init__(self, llm: BaseChatModel) -> None:
        self.llm_chain = llm.with_structured_output(ParecerTecnico)

    def __call__(self, state: AuditoriaState) -> dict[str, Any]:
        edital = state.get("edital")
        achados = state.get("achados", [])

        if not edital:
            return {"erros": ["Agente Relator falhou: Nenhum edital no Estado."]}

        # Formata os achados para o LLM ler
        achados_texto = "\n".join(
            [
                f"- {a.artigo_lei} ({a.status_conformidade}): {a.justificativa}"
                for a in achados
            ]
        )

        contexto_humano = (
            f"ID do Documento: {edital.id_documento}\n"
            f"Objeto: {edital.objeto_licitacao}\n\n"
            f"ACHADOS DOS ESPECIALISTAS:\n{achados_texto if achados else 'Nenhum achado apontado.'}\n\n"
            "Gere o Parecer Técnico estruturado."
        )

        messages = [
            SystemMessage(content=PROMPT_AGENTE_RELATOR),
            HumanMessage(content=contexto_humano),
        ]

        try:
            parecer_final: ParecerTecnico = self.llm_chain.invoke(messages)
            # Atualiza a mochila com o parecer pronto
            return {"parecer_final": parecer_final}
        except Exception as e:
            return {"erros": [f"Erro na execução do Relator: {str(e)}"]}
