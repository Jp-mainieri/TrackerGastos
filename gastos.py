import mysql.connector
from datetime import date
import os

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Jppm2006",
    database="projeto_integrador_fase2"
)
cursor = mydb.cursor()

#gastos = [] #Esse vai ser o banco de dados

def converterValorInteiro(valorStr):
    try:
        if "." in valorStr:
            partes = valorStr.split(".")

            if len(partes) != 2:
                return None

            reaisStr,centavosStr = partes

            if not reaisStr.isdigit() or not centavosStr.isdigit():
                return None

            if len(centavosStr) == 1:
                centavosStr += "0"
            elif len(centavosStr) > 2:
                centavosStr = centavosStr[:2]
            
            totalCentavos = reaisStr + centavosStr

        else:
            if not valorStr.isdigit():
                return None
            totalCentavos = valorStr + "00"

        valorInt = int(totalCentavos)

        return valorInt

    except:
        return None

def converterInteiroString(valorInt):
    valorStr = str(valorInt)

    centavosStr = valorStr[-2:]
    reaisStr = valorStr[:-2]
    
    valorStr = reaisStr + "." + centavosStr
    return valorStr 

def converterData(dataStr):
    partes = dataStr.split("/") #partes = [dd,mm,aaaa]
    data = date(int(partes[2]), int(partes[1]), int(partes[0]))
    return data

def inserirGasto():

    data = input("Digite a data (dd/mm/aaaa): ")

    print("Que tipo de gasto você teve?")
    print("1- Alimentação")
    print("2- Transporte")
    print("3- Outros")

    tipoEscolhido = input("Digite o número da opção: ")

    while tipoEscolhido not in ["1", "2", "3"]:
        print("Opção inválida. Por favor, escolha uma opção válida.")
        tipoEscolhido = input("Digite o número da opção: ")

    if tipoEscolhido == "1":
        tipo = "Alimentação"
    elif tipoEscolhido == "2":
        tipo = "Transporte"
    elif tipoEscolhido == "3":
        tipo = input("Qual é o tipo de gasto?")

    valor = input("Digite o valor: R$ ")
    gastoRegistrado = {
    "tipo": tipo,
    "data": converterData(data),
    "valor": converterValorInteiro(valor)
    }

    sql = "INSERT INTO expenses (expense_type, expense_date, expense_value) VALUES (%s, %s, %s)"
    val = (gastoRegistrado["tipo"],gastoRegistrado["data"],(-1) * gastoRegistrado["valor"])
    cursor.execute(sql, val)
    mydb.commit()
    
    #gastos.append(gastoRegistrado)

def inserirGanho():

    data = input("Digite a data (dd/mm/aaaa): ")

    print("Que tipo de ganho você teve?")
    print("1- Salário")
    print("2- Investimento")
    print("3- Outros")

    tipoEscolhido = input("Digite o número da opção: ")

    while tipoEscolhido not in ["1", "2", "3"]:
        print("Opção inválida. Por favor, escolha uma opção válida.")
        tipoEscolhido = input("Digite o número da opção: ")

    if tipoEscolhido == "1":
        tipo = "Salário"
    elif tipoEscolhido == "2":
        tipo = "Investimento"
    elif tipoEscolhido == "3":
        tipo = input("Qual é o tipo de gasto?")

    valor = input("Digite o valor: R$ ")
    ganhoRegistrado = {
    "tipo": tipo,
    "data": converterData(data),
    "valor": converterValorInteiro(valor)
    }

    sql = "INSERT INTO earnings (earning_type, earning_date, earning_value) VALUES (%s, %s, %s)"
    val = (ganhoRegistrado["tipo"],ganhoRegistrado["data"],ganhoRegistrado["valor"])
    cursor.execute(sql, val)
    mydb.commit()

def mostrarEstratoCompleto():

    sql = "SELECT * FROM expenses ORDER BY expense_date ASC"
    cursor.execute(sql)
    gastos = cursor.fetchall() #()

    sql = "SELECT * FROM earnings ORDER BY earning_date ASC"
    cursor.execute(sql)
    ganhos = cursor.fetchall()

    registros = ganhos + gastos

    extrato = {}

    for registro in registros:

        mes = registro[2].strftime("%B")
        dia = registro[2].strftime("%d")
        ano = registro[2].strftime("%Y")

        if ano not in extrato:
            extrato[ano] = {}
        if mes not in extrato[ano]:
            extrato[ano][mes] = {}
        if dia not in extrato[ano][mes]:
            extrato[ano][mes][dia] = []

        extrato[ano][mes][dia].append(registro)

    for ano, mes in extrato.items():
        print(f"\n=== ANO {ano} ===")
        totalAno = 0

        for mes, dias in mes.items():
            print(f"\n--- {mes} ---")
            totalMes = 0

            for dia, lista_gastos in dias.items():
                print(f"\nDia {dia}:\n")
                totalDia = 0

                for gasto in lista_gastos:
                    valorStr = converterInteiroString(gasto[3])
                    print(f"- {gasto[1]}: R$ {valorStr}")

                    totalDia += registro[3]
                    totalDiaStr = converterInteiroString(totalDia)
                    print(f"\nTotal do dia: R$ {totalDiaStr}") 
                totalMes += totalDia
            totalMesStr = converterInteiroString(totalMes)
            print(f"\nTotal de {mes}: R$ {totalMesStr}")
            totalAno += totalMes
        totalAnoStr = converterInteiroString(totalAno)
        print(f"\nTotal de {ano}: R$ {totalAnoStr}")
            
       

os.system("cls")

#inserirGasto()
#inserirGanho()
mostrarEstratoCompleto()