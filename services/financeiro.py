
def calcular_disponivel_variavel(receitas, despesas_fixas, investimento):
    #Calcula o valor disponível para gastos variados após considerar receitas, despesas fixas e investimento
    total_receitas = sum(receitas)
    total_despesas_fixas = sum(despesas_fixas)
    total_despesas = total_despesas_fixas + investimento
    return total_receitas - total_despesas