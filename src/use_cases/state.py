import operator
from typing import Annotated, TypedDict, List, Optional

from domain.entities.auditoria import AchadoAuditoria, ParecerTecnico
from domain.entities.documentos import Edital

class AuditoriaMetadata(TypedDict):
    """Metadados obrigatórios para rastreabilidade jurídica (TCERJ)."""
    run_id: str
    law_version: str
    orgao_emissor: str

class AuditoriaState(TypedDict):
    """
    Estado global do Grafo de Auditoria. 
    Representa a 'mochila' de dados que transita entre os agentes.
    """
    # 1. Entrada: O documento que está sendo analisado
    edital: Optional[Edital]
    
    # 2. Processamento: Lista agregadora de achados. 
    # O uso do 'operator.add' (Reducer) é OBRIGATÓRIO para o Parallel Fan-Out,
    # garantindo que agentes paralelos não sobrescrevam os achados uns dos outros.
    achados: Annotated[List[AchadoAuditoria], operator.add]

    # 2.5. Controle de fluxo: Lista agregadora de análises já concluídas
    # (ex.: evita que o Supervisor chame o mesmo especialista duas vezes).
    analises_concluidas: Annotated[List[str], operator.add]
    
    # 3. Saída: O parecer final consolidado pelo Agente Relator
    parecer_final: Optional[ParecerTecnico]
    
    # 4. Rastreabilidade: Obrigatório para auditoria
    metadata: AuditoriaMetadata
    
    # 5. Telemetria e Falhas: Agrega mensagens de erro de ferramentas ou falhas de RAG
    erros: Annotated[List[str], operator.add]
