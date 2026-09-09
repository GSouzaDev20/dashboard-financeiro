from database import *


def calcular_disponivel_variavel(receitas, despesas_fixas, investimento):
    #Calcula o valor disponível para gastos variados após considerar receitas, despesas fixas e investimento
    total_receitas = sum(receitas)
    total_despesas_fixas = sum(despesas_fixas)
    total_despesas = total_despesas_fixas + investimento
    return total_receitas - total_despesas

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
