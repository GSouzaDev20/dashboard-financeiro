
from flask import Flask, render_template, redirect, request
from database import buscar_gastos, salvar_gasto

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
    Gastos_Mensais = buscar_gastos()
    gastos_detalhados = buscar_gastos()
    Valor_para_guardar = 500

    despesas = Despesas(Gastos_Mensais)
    Valor_restante = Saldo_diario(Salario, despesas, Valor_para_guardar)

    DiaRestantes = 25
    limite_diario = Limite_diario(Valor_restante, DiaRestantes)
    return render_template(
        'index.html',
        Salario=Salario,
        Despesas=despesas,
        Despesas_Detalhadas=gastos_detalhados,
        Valor_para_guardar=Valor_para_guardar,
        Valor_restante=Valor_restante,
        DiaRestantes=DiaRestantes,
        Limite_diario=limite_diario,
    )


@app.route('/adicionar_gasto', methods=['POST'])
def adicionar_gasto():
    descricao = request.form['descricao']
    if not descricao:
        return "Descrição do gasto não pode ser vazia.", 400

    try:
        valor = float(request.form['valor'])
    except ValueError:
        return "Valor do gasto deve ser um número válido.", 400

    if valor <= 0:
        return "Valor do gasto deve ser maior que zero.", 400

    salvar_gasto(descricao, valor)
    return redirect('/')

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)