from database import *

def obter_total_receitas_fixas_por_competencia(competencia):
    ocorrencias = buscar_receitas_fixas_ocorrencias_por_competencia(competencia)
    total_receitas_fixas = sum(ocorrencia['valor'] for ocorrencia in ocorrencias if ocorrencia['status'] == 'recebida')
    return total_receitas_fixas

def obter_total_receitas_variaveis_por_competencia(competencia):
    ocorrencias = buscar_receitas_variaveis_por_competencia(competencia)
    total_receitas_variaveis = sum(ocorrencia['valor'] for ocorrencia in ocorrencias)
    return total_receitas_variaveis

def obter_total_receitas_mes(competencia):
    receita_fixa = obter_total_receitas_fixas_por_competencia(competencia)
    receita_variavel = obter_total_receitas_variaveis_por_competencia(competencia)
    return receita_fixa + receita_variavel

def obter_total_despesas_fixas_por_competencia(competencia):
    ocorrencias = buscar_despesas_fixas_ocorrencias_por_competencia(competencia)
    total_despesas_fixas = sum(ocorrencia['valor'] for ocorrencia in ocorrencias if ocorrencia['status'] == 'pago')
    return total_despesas_fixas
    
def calcular_limite_diario(disponivel_variavel, dias_restantes):
    #Calcula o limite diário de gastos variáveis com base no valor disponível e no número de dias restantes
    if dias_restantes <= 0:
        return 0  # Evita divisão por zero
    return disponivel_variavel / dias_restantes

def calcular_despesas_fixas_mes(ocorrencias):
    #Calcula o total de despesas fixas a partir de uma lista de ocorrências
    return sum(ocorrencia["valor"] for ocorrencia in ocorrencias)

def obter_total_despesas_fixas(competencia):  
    ocorrencias = buscar_despesas_fixas_ocorrencias_por_competencia(competencia)
    total_despesas_fixas = calcular_despesas_fixas_mes(ocorrencias)
    return total_despesas_fixas

def calcular_despesas_variaveis_mes(ocorrencias):
    return sum(ocorrencia["valor"] for ocorrencia in ocorrencias)

def obter_total_despesas_variaveis_por_competencia(competencia):
    ocorrencias = buscar_despesas_variaveis_por_competencia(competencia)
    total_despesas_variaveis = calcular_despesas_variaveis_mes(ocorrencias)
    return total_despesas_variaveis

def obter_total_despesas_mes(competencia):
    total_fixas = obter_total_despesas_fixas(competencia)
    total_variaveis = obter_total_despesas_variaveis_por_competencia(competencia)
    return total_fixas + total_variaveis

def calcular_resultado_mes(competencia):
    total_receitas = obter_total_receitas_mes(competencia)
    total_despesas = obter_total_despesas_mes(competencia)
    return total_receitas - total_despesas

def total_despesas_fixas_pendentes_por_competencia(competencia):
    ocorrencias = buscar_despesas_fixas_ocorrencias_por_competencia(competencia)
    total_pendentes = sum(ocorrencia['valor'] for ocorrencia in ocorrencias if ocorrencia['status'] == 'pendente')
    return total_pendentes

def total_aportes_por_meta(meta_id):
    aportes = buscar_aportes_por_meta(meta_id)
    total_aportes = sum(aporte['valor'] for aporte in aportes)
    return total_aportes
def total_aportes_por_meta_e_competencia(meta_id, competencia):
    aportes = buscar_aportes_por_competencia(meta_id, competencia)
    total_aportes = sum(aporte['valor'] for aporte in aportes)
    return total_aportes

def valor_aporte_por_competencia(meta_id, competencia):
    valor_meta = buscar_valor_meta(meta_id)
    aportes = buscar_aportes_por_competencia(meta_id, competencia)
    total_aportes = sum(aporte['valor'] for aporte in aportes)
    return total_aportes + valor_meta
    