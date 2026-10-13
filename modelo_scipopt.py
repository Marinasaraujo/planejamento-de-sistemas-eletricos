from pyscipopt import Model, SCIP_PARAMSETTING
import resultados

def despacho(sistema, VI, AFL, cortes, mes_futuro, imprime):

    num_UHE = len(sistema["UHE"])
    num_UTE = len(sistema["UTE"])

    modelo = Model("despacho_hidrotermico")

    # Configurações para consultar os duais (multp lagrange) do problema 
    modelo.setPresolve(SCIP_PARAMSETTING.OFF)
    modelo.setHeuristics(SCIP_PARAMSETTING.OFF)
    modelo.disablePropagation()

    # Variáveis de decisão
    vf = []
    vt = []
    vv = []
    gt = []

    # Variáveis de decisão
    for i, uhe in enumerate(sistema["UHE"]):
        vf.append(modelo.addVar(f"vf_{i}", lb= uhe["Vmin"], ub=uhe["Vmax"]))
        vt.append(modelo.addVar(f"vt_{i}", lb=0, ub=uhe["Engol"]))
        vv.append(modelo.addVar(f"vv_{i}", lb=0))

    for i, ute in enumerate(sistema["UTE"]):
        gt.append(modelo.addVar(f"gt_{i}", lb=0, ub=ute["Cap"]))

    deficit = modelo.addVar("def", lb=0)
    alpha = modelo.addVar("alpha", lb=0)

    balanco_hidrico = []
    # Balanço hídrico e atendimento à carga
    for i, uhe in enumerate(sistema["UHE"]):
        restricao = modelo.addCons(
            vf[i] == VI[i] + AFL[i] - vt[i] - vv[i],
            name=f"balanco_hidrico_{i}"
        )
        balanco_hidrico.append(restricao)

    # Atendimento à demanda
    AD = 0
    for i, uhe in enumerate(sistema['UHE']):
        AD += uhe["Prod"]*vt[i]

    for i, ute in enumerate(sistema["UTE"]):
        AD += gt[i]

    AD += deficit

    atendimento_demanda = modelo.addCons(
        AD == sistema["Geral"]["Carga"][mes_futuro-2],
        name="atendimento_demanda"
    )



    for i, reta in enumerate(cortes):
        if reta['Estagio'] == mes_futuro:
            equacao = 0
            for uhe in range(num_UHE): # para mais de uma uhe a reta vira plano ou outras superficies
                equacao += float(reta['Coeficientes'][uhe])*vf[uhe]
            equacao += float(reta['Termo independente'])
            modelo.addCons(alpha >= equacao, name=f"corte_{i}")



    # Função objetivo
    FOB = 0

    for i, ute in enumerate(sistema["UTE"]):
        FOB += float(ute["Custo"])*gt[i]

    FOB += float(sistema["Geral"]["Custo_def"])*deficit

    for i, uhe in enumerate(sistema["UHE"]):
        FOB += 0.01*vv[i]

    FOB += 1.0*alpha

    modelo.setObjective(
        FOB,
        sense="minimize"
    )

    modelo.optimize()

    if modelo.getStatus() != "optimal":
        raise RuntimeError(
            f"Não foi encontrada solução ótima. Status: {modelo.getStatus()}"
        )

    # Extração dos valores numéricos.
    variaveis = {
        "vf": [modelo.getVal(v) for v in vf],
        "vt": [modelo.getVal(v) for v in vt],
        "vv": [modelo.getVal(v) for v in vv],
        "gt": [modelo.getVal(v) for v in gt],
        "deficit": modelo.getVal(deficit),
        "alpha": modelo.getVal(alpha)
    }

    multiplicadores = {
        "CMO": modelo.getDualsolLinear(atendimento_demanda),
        "cma": [
            -modelo.getDualsolLinear(restricao)
            for restricao in balanco_hidrico
        ]
    }

    return resultados.gerar_resultados(imprime, multiplicadores, modelo.getObjVal(), variaveis)
