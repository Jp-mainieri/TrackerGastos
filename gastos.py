gastos = {}
id_gasto = len(gastos)+1

print("Que tipo de gasto você teve?")
print("1- Alimentação")
print("2- Transporte")
print("3- Outros")

tipoEscolhido = input("Digite o número da opção: ")

while tipoEscolhido not in ["1", "2", "3"]:
    print("Opção inválida. Por favor, escolha uma opção válida.")
    tipoEscolhido = input("Digite o número da opção: ")

if tipoEscolhido == 1:
    tipo = "Alimentação"
elif tipoEscolhido == "2":
    tipo = "Transporte"
elif tipoEscolhido == "3":
    tipo = input("Qual é o tipo de gasto?")

valor = input("Digite o valor: R$ ")

def converterValorInteiro(valorStr):
    try:
        valorStr = valorStr.strip()
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
                return None
            
            totalCentavos = reaisStr + centavosStr

        else:
            if not valorStr.isdigit():
                return None
            totalCentavos = reais + "00"

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

gastos[id_gasto] = {
    "tipo": tipoEscolhido,
    "date": input("Digite a data (dd/mm/aaaa): "),
    "valor": converterValorInteiro(valor)
}

print(valor)
print(converterValorInteiro(valor))
print(converterInteiroString(converterValorInteiro(valor)))