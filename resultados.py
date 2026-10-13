def gerar_resultados(imprime, multiplicadores, fob, variaveis):

    resultados_gerais = {
        "Deficit": variaveis["deficit"],
        "CMO": multiplicadores["CMO"],
        "Custo total": fob,
        "Custo futuro": variaveis["alpha"]
    }

    resultados_uhe = []

    for i in range(len(variaveis["vf"])):
      resultado = {
          "vf": variaveis["vf"][i],
          "vt": variaveis["vt"][i],
          "vv": variaveis["vv"][i],
          "cma": multiplicadores["cma"][i]
          }
      
      resultados_uhe.append(resultado)

    resultados_ute = []

    for geracao in variaveis["gt"]:
        resultado = {
            "gt": geracao
        }
        resultados_ute.append(resultado)


    saida = {
        "Geral": resultados_gerais,
        "UHE": resultados_uhe,  
        "UTE": resultados_ute
    }

    if imprime:

        for nome, valor in saida["Geral"].items():
            print(f"{nome}: {valor}")

        for i, uhe in enumerate(saida["UHE"]):
            print(f"UHE {i}:")
            for nome, valor in uhe.items():
                print(f"  {nome}: {valor}")

        for i, ute in enumerate(saida["UTE"]):
            print(f"UTE {i}: gt = {ute['gt']}")

        print("-------------------------------------------------")

    return saida