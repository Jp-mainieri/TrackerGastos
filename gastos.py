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
    print("Insert Expense")
    print("----------------------------------")
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
    print("Insert Earning")
    print("----------------------------------")
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
    print("Receipt")
    print("----------------------------------")
    sql = "SELECT * FROM expenses ORDER BY expense_date ASC"
    cursor.execute(sql)
    gastos = cursor.fetchall() #()

    sql = "SELECT * FROM earnings ORDER BY earning_date ASC"
    cursor.execute(sql)
    ganhos = cursor.fetchall()

    registros = gastos + ganhos

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

            for dia, listaG in dias.items():
                print(f"\nDia {dia}:\n")
                totalDia = 0

                for item in listaG:
                    valorStr = converterInteiroString(item[3])
                    print(f"- {item[1]}: R$ {valorStr}")

                    totalDia += item[3]
                    totalDiaStr = converterInteiroString(totalDia)
                    print(f"\nTotal do dia: R$ {totalDiaStr}") 
                totalMes += totalDia
            totalMesStr = converterInteiroString(totalMes)
            print(f"\nTotal de {mes}: R$ {totalMesStr}")
            totalAno += totalMes
        totalAnoStr = converterInteiroString(totalAno)
        print(f"\nTotal de {ano}: R$ {totalAnoStr}")

def alterarGasto():
    print("Modify Expenses")
    print("---------------------------------")
    print("| Select Option                 |")
    print("---------------------------------")
    print("|1- Modify Expenses             |")
    print("|2- Modify Earnings             |")
    print("|0- Exit                        |")
    print("---------------------------------")
    menuOption = int(input("> "))
    while menuOption not in [1, 2, 0]:
        print("Select a valid option!")
        menuOption = int(input("> "))

    if menuOption == 1:
        data = input("Digite a data (dd/mm/aaaa): ")
        data = converterData(data)
        sql = f"SELECT * FROM expenses WHERE expense_date = '{data}' ORDER BY expense_date ASC"
        cursor.execute(sql)
        gastos = cursor.fetchall()
        for item in gastos:
            valorStr = converterInteiroString(item[3])
            print(f"- {item[1]}: R$ {valorStr}")

    elif menuOption == 2:
        data = input("Digite a data (dd/mm/aaaa): ")
        data = converterData(data)
        sql = f"SELECT * FROM earnings WHERE earning_date = '{data}' ORDER BY earning_date ASC"
        cursor.execute(sql)
        ganhos = cursor.fetchall()
        for item in ganhos:
            valorStr = converterInteiroString(item[3])
            print(f"- {item[1]}: R$ {valorStr}")
    input()

def excluirGasto():
    print("Delete Expenses")
    print("----------------------------------")


def clear():
    os.system("cls")

def showMenu():
    clear()
    print("Menu")
    print("---------------------------------")
    print("| Select Option                 |")
    print("---------------------------------")
    print("|1- Insert Expenses             |")
    print("|2- Insert Earnings             |")
    print("|3- Update Expenses             |")
    print("|4- Delete Expenses             |")
    print("|5- Show Receipt                |")
    print("|0- Exit                        |")
    print("---------------------------------")
def main():
    menuOption = 1
    while menuOption != 0:
        showMenu()
        menuOption = int(input("> "))
        while menuOption not in [1, 2, 3, 4, 5, 0]:
            print("Select a valid option!")
            menuOption = int(input("> "))

        clear()

        if menuOption == 1:
            inserirGasto()
        elif menuOption == 2:
            inserirGanho()
        elif menuOption == 3:
            alterarGasto()
        elif menuOption == 5:
            excluirGasto()
        elif menuOption == 4:
            mostrarEstratoCompleto()
        else:
            print("Thanks for using the program!")

if __name__ == "__main__":
    main()