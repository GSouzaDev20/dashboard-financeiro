
from flask import Flask, render_template

app = Flask(__name__)

def Saldo_diario(Salario, Despesas, Valor_para_guardar):
    Saldo = Salario - Despesas - Valor_para_guardar
    return Saldo

def Limite_diario(Valor_restante, DiaRestantes):
    if DiaRestantes <= 0:
        return 0
    Limite = Valor_restante / DiaRestantes
    return Limite
def Despesas(Gastos_Mensais):
    total_despesas = sum(gasto["valor"] for gasto in Gastos_Mensais)
    return total_despesas

@app.route('/')
def start():
    Salario = 5000
    Gastos_Mensais = [
        {"descricao": "Aluguel", "valor": 1500},
        {"descricao": "Compras", "valor": 1000},
        {"descricao": "Transporte", "valor": 500},
        {"descricao": "Lazer", "valor": 300},
        {"descricao": "Outros", "valor": 200}
    ]
    Valor_para_guardar = 500

    despesas = Despesas(Gastos_Mensais)
    Valor_restante = Saldo_diario(Salario, despesas, Valor_para_guardar)

    DiaRestantes = 25
    limite_diario = Limite_diario(Valor_restante, DiaRestantes)
    return render_template('index.html', 
                           Salario=Salario, 
                           Despesas=despesas, 
                           Valor_para_guardar=Valor_para_guardar, 
                           Valor_restante=Valor_restante,
                           DiaRestantes=DiaRestantes,
                           Limite_diario=limite_diario)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug=True)