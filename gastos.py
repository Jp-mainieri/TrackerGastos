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
    val = (gastoRegistrado["tipo"],gastoRegistrado["data"],gastoRegistrado["valor"])
    cursor.execute(sql, val)
    mydb.commit()
    
    #gastos.append(gastoRegistrado)

def mostrarEstratoCompleto():

    sql = "SELECT * FROM expenses"
    cursor.execute(sql)
    gastos = cursor.fetchall() #()

    gastosOrganizados = {}

    for gastoInfo in gastos:

        mes = gastoInfo[2].strftime("%B")
        dia = gastoInfo[2].strftime("%d")
        ano = gastoInfo[2].strftime("%Y")

        if ano not in gastosOrganizados:
            gastosOrganizados[ano] = {}
        if mes not in gastosOrganizados[ano]:
            gastosOrganizados[ano][mes] = {}
        if dia not in gastosOrganizados[ano][mes]:
            gastosOrganizados[ano][mes][dia] = []

        gastosOrganizados[ano][mes][dia].append(gastoInfo)

    for ano, mes in gastosOrganizados.items():
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
                    totalDia += gasto[3]
                totalMes += totalDia
                totalDia = converterInteiroString(totalDia)
                print(f"\nTotal do dia: R$ {totalDia}")    

            totalAno += totalMes
            totalMes = converterInteiroString(totalMes)
            print(f"\nTotal de {mes}: R$ {totalMes}")

        totalAno = converterInteiroString(totalAno)
        print(f"\nTotal de {ano}: R$ {totalAno}")

os.system("cls")

inserirGasto()
inserirGasto()
mostrarEstratoCompleto()