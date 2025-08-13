import mysql.connector
from datetime import date
import os

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Jppm2006",
    database="trackergastos-app"
)
cursor = mydb.cursor()

def clear():
    os.system("cls")

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
                print(f"\nTotal do dia: R$ {totalDiaStr}\n"
                      f"---------------------------------")
                totalMes += totalDia
            totalMesStr = converterInteiroString(totalMes)
            totalAno += totalMes
        print(f"\nTotal de {mes}: R$ {totalMesStr}\n"
              f"---------------------------------")
        totalAnoStr = converterInteiroString(totalAno)
    print(f"\nTotal de {ano}: R$ {totalAnoStr}")
    input("\n<ENTER TO EXIT>")

def listarPorData(tabela,coluna): #Mudar nome para numerar por data
    pesquisa = ()
    i = 1
    while len(pesquisa) == 0:
        data = input("Digite a data (dd/mm/aaaa): ")
        data = converterData(data)
        sql = f"SELECT * FROM {tabela} WHERE {coluna} = '{data}'"
        cursor.execute(sql)
        pesquisa = cursor.fetchall()
        if len(pesquisa) == 0:
            print("No records found for this date.")
    for item in pesquisa:
        valorStr = converterInteiroString(item[3])
        print(f"{i}- {item[1]}: R$ {valorStr}")
        i+=1
    return pesquisa,data

def listarPorTipo(): #Mudar nome para numerar por tipo
    pesquisa = ()
    i = 1
    tipo = ""


    while len(pesquisa) == 0:
        print("Filter by Type")
        print("---------------------------------")
        print("Select the group of the record:")
        print("1- Expenses")
        print("2- Earnings")
        print("---------------------------------")
        opcaoGrupo = input("> ")

        while opcaoGrupo not in ["1", "2"]:
            print("Select a valid option!")
            opcaoGrupo = input("> ")

        if opcaoGrupo == "1":
            tabela = "expenses"
            coluna = "expense_type"
            print("Filter by Type - Expenses")
            print("---------------------------------")
            print(f"Select the type of expense:")
            print("1- Alimentação")
            print("2- Transporte")
            print("3- Outros")
            print("---------------------------------")
            opcaotipo = input("> ")

            while opcaotipo not in ["1", "2", "3"]:
                print("Select a valid option!")
                opcaotipo = input("> ")

            if opcaotipo == "1":
                tipo = "Alimentação"
            elif opcaotipo == "2":
                tipo = "Transporte"
            elif opcaotipo == "3":
                tipo = input("Qual é o tipo de gasto?")

        elif opcaoGrupo == "2":
            tabela = "earnings"
            coluna = "earning_type"
            print("Filter by Type - Earnings")
            print("---------------------------------")
            print(f"Select the type of earning:")
            print("1- Salário")
            print("2- Investimento")
            print("3- Outros")
            print("---------------------------------")
            opcaotipo = input("> ")
            while opcaotipo not in ["1", "2", "3"]:
                print("Select a valid option!")
                opcaotipo = input("> ")
            if opcaotipo == "1":
                tipo = "Salário"
            elif opcaotipo == "2":
                tipo = "Investimento"
            elif opcaotipo == "3":
                tipo = input("Qual é o tipo de ganho?")

        sql = f"SELECT * FROM {tabela} WHERE {coluna} = '{tipo}'"
        cursor.execute(sql)
        pesquisa = cursor.fetchall()
        if len(pesquisa) == 0:
            print("No records found for this type.")
    totalpesquisa = 0
    print(f"\nRecords for {tipo}:\n")
    for item in pesquisa:
        valorStr = converterInteiroString(item[3])
        print(f"{i}- {item[1]}: R$ {valorStr}")
        totalpesquisa += item[3]
        i+=1
    print(f"Total for this type: R$ {converterInteiroString(totalpesquisa)}")
    input("\n<ENTER TO EXIT>")
    return pesquisa,tipo

def alterarGasto():
    print("Update Records")
    print("---------------------------------")
    print("| Select Option                 |")
    print("---------------------------------")
    print("|1- Modify Expenses             |")
    print("|2- Delete Expenses             |")
    print("---------------------------------")
    print("|3- Modify Earnings             |")
    print("|4- Delete Earnings             |")
    print("---------------------------------")
    print("|0- Exit                        |")
    print("---------------------------------")
    menuOption = int(input("> "))
    while menuOption not in [1, 2, 3, 4, 0]:
        print("Select a valid option!")
        menuOption = int(input("> "))

    if menuOption == 1:
        lista,data = listarPorData("expenses", "expense_date")
        print("Escolha o gasto que você deseja alterar:")
        id = int(input("> "))

        while not 1 <= id <= len(lista):
            print("Escolha um número válido:")
            id = int(input("> "))

        item = lista[id-1]
        print("Insira o valor do gasto atualizado:")
        valor = -1* converterValorInteiro(input("> "))
        sql = f"UPDATE expenses SET expense_value = {valor} WHERE id = {item[0]}"
        cursor.execute(sql)
        mydb.commit()
        print("Atualizado com sucesso")

    elif menuOption == 2:
        lista,data = listarPorData("expenses", "expense_date")
        print("Escolha o gasto que você deseja excluir:")
        id = int(input("> "))
        while not 1 <= id <= len(lista):
            print("Escolha um número válido:")
            id = int(input("> "))

        item = lista[id-1]
        sql = f"DELETE FROM expenses WHERE id = {item[0]}"
        cursor.execute(sql)
        mydb.commit()
        print("Excluido com sucesso")
    elif menuOption == 3:
        lista,data = listarPorData("earnings", "earning_date")
        print("Escolha o ganho que você deseja alterar:")
        id = int(input("> "))
        while not 1 <= id <= len(lista):
            print("Escolha um número válido:")
            id = int(input("> "))

        item = lista[id-1]
        print("Insira o valor do ganho atualizado:")
        valor = converterValorInteiro(input("> "))
        sql = f"UPDATE earnings SET earning_value = {valor} WHERE id = {item[0]}"
        cursor.execute(sql)
        mydb.commit()
        print("Atualizado com sucesso")

    elif menuOption == 4:
        lista,data = listarPorData("earnings", "earning_date")
        print("Escolha o ganho que você deseja excluir:")
        id = int(input("> "))
        while not 1 <= id <= len(lista):
            print("Escolha um número válido:")
            id = int(input("> "))

        item = lista[id-1]
        sql = f"DELETE FROM earnings WHERE id = {item[0]}"
        cursor.execute(sql)
        mydb.commit()
        print("Excluido com sucesso")
    input("\n<ENTER TO EXIT>")

def mostrarEstatisticas():
    print("Statistics")
    print("---------------------------------")
    print("| Select Option                 |")
    print("---------------------------------")
    print("|1- Filters                     |")
    print("|2- Analytics (X)               |")
    print("|3- (X)                         |")
    print("---------------------------------")
    print("|0- Exit                        |")
    print("---------------------------------")

    menuOption = int(input("> "))
    while menuOption not in [1, 2, 0]:
        print("Select a valid option!")
        menuOption = int(input("> "))

    clear()

    if menuOption == 1:
        print("Filters")
        print("---------------------------------")
        print("| Select Option                 |")
        print("---------------------------------")
        print("|1- By Date                     |")
        print("|2- By Type                     |")
        print("|3- By Value  (X)               |")
        print("---------------------------------")
        print("|0- Exit                        |")
        print("---------------------------------")

        filterOption = int(input("> "))
        while filterOption not in [1, 2, 3, 0]:
            print("Select a valid option!")
            filterOption = int(input("> "))

        if filterOption == 1:
            listarPorData("expenses", "expense_date")
            listarPorData("earnings", "earning_date")
        elif filterOption == 2:
            listarPorTipo()
            pass
        elif filterOption == 3:
            # Implementar filtro por valor
            pass


def showMenu():
    clear()
    print("Menu")
    print("---------------------------------")
    print("| Select Option                 |")
    print("---------------------------------")
    print("|1- Insert Expenses             |")
    print("|2- Insert Earnings             |")
    print("|3- Update Records              |")
    print("|4- Show Receipt                |")
    print("|5- Show Statistics             |")
    print("---------------------------------")
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
        elif menuOption == 4:
            mostrarEstratoCompleto()
        elif menuOption == 5:
            mostrarEstatisticas()
        else:
            print("Thanks for using the program!")

if __name__ == "__main__":
    main()