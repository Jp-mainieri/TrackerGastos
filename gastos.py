gastos = {}

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
    
def inserirGasto():
    id_gasto = len(gastos)

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
    gastos[id_gasto] = {
    "tipo": tipo,
    "date": input("Digite a data (dd/mm/aaaa): "),
    "valor": converterValorInteiro(valor)
    }
    print(gastos)
    
inserirGasto()
inserirGasto()
inserirGasto()