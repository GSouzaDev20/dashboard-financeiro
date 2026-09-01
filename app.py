
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def start():
    Salario = 5000
    Despesas = 500
    Valor_para_guardar = 500

    DiaRestantes = 25
    
    Saldo = Salario - Despesas - Valor_para_guardar
    Limite_diario = Saldo / DiaRestantes
    return render_template('index.html', 
                           Salario=Salario, 
                           Despesas=Despesas, 
                           Valor_para_guardar=Valor_para_guardar, 
                           Saldo=Saldo,
                           DiaRestantes=DiaRestantes,
                           Limite_diario=Limite_diario)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug=True)