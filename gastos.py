import mysql.connector
from datetime import date

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword"
)
mycursor = mydb.cursor()
gastos = []

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
    gastos.append(gastoRegistrado)

def mostrarEstratoCompleto():

    gastosOrganizados = {}

    for gastoInfo in gastos:

        mes = gastoInfo["data"].strftime("%B")
        dia = gastoInfo["data"].strftime("%d")
        ano = gastoInfo["data"].strftime("%Y")

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
                    valorStr = converterInteiroString(gasto["valor"])
                    print(f"- {gasto['tipo']}: R$ {valorStr}")
                    totalDia += gasto["valor"]
                totalMes += totalDia
                totalDia = converterInteiroString(totalDia)
                print(f"\nTotal do dia: R$ {totalDia}")    

            totalAno += totalMes
            totalMes = converterInteiroString(totalMes)
            print(f"\nTotal de {mes}: R$ {totalMes}")

        totalAno = converterInteiroString(totalAno)
        print(f"\nTotal de {ano}: R$ {totalAno}")

inserirGasto()
inserirGasto()
mostrarEstratoCompleto()