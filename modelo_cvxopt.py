from cvxopt.modeling import variable, solvers, op
import resultados

solvers.options["glpk"] = {"msg_lev": "GLP_MSG_OFF"}

def despacho(sistema, VI, AFL, cortes, mes_futuro, imprime):

  num_UHE = len(sistema["UHE"])
  num_UTE = len(sistema["UTE"])

  # Definição das variaveis de decisão e quantas teremos de cada
  vf = variable(num_UHE, "Volume final da usina")
  vt = variable(num_UHE, "Volume turbinado da usina")
  vv = variable(num_UHE, "Volume vertido da usina")
  gt = variable(num_UTE, "Geração na usina termica")
  deficit = variable(1, "Deficit de energia")
  alpha = variable(1, "Custo Futuro")

  # Definição da função objetivo
  fob = 0

  for i, ute in enumerate(sistema["UTE"]):
      fob += ute["Custo"]*gt[i]

  fob += sistema["Geral"]["Custo_def"]*deficit[0]

  for i, uhe in enumerate(sistema["UHE"]):
      fob += 0.01*vv[i]

  fob += 1.0*alpha[0]

  # Definição das restrições

  restricoes = []

  # Balanço Hidrico
  for i, uhe in enumerate(sistema["UHE"]):
    restricoes.append(vf[i] == float(VI[i]) + float(AFL[i]) - vt[i] - vv[i]) # Faltam as discretizações

  # Atendimento à demanda -> Fornece CMO
  AD = 0
  for i, uhe in enumerate(sistema['UHE']):
    AD += uhe["Prod"]*vt[i]

  for i, ute in enumerate(sistema["UTE"]):
    AD += gt[i]

  AD += deficit[0]

 # O vetor carga de tamanho n acessamos de 0 a n-1
 # mes_futuro já é um mes na frente do analisado, precisamos subtrair 2 para chegar no indice da carga correspondente
  restricoes.append(AD == sistema["Geral"]["Carga"][mes_futuro-2])

  for i, uhe in enumerate(sistema['UHE']):
    restricoes.append(vf[i] >= uhe['Vmin'])
    restricoes.append(vf[i] <= uhe['Vmax'])
    restricoes.append(vt[i] >= 0)
    restricoes.append(vt[i] <= uhe['Engol'])
    restricoes.append(vv[i] >= 0)

  for i, ute in enumerate(sistema["UTE"]):
    restricoes.append(gt[i] >= 0)
    restricoes.append(gt[i] <= ute['Cap'])

  restricoes.append(deficit[0] >= 0)

  restricoes.append(alpha[0] >= 0)

  for icorte in cortes:
    # A medida que os despachos vao ocorrendo, os cortes vão sendo criados para a média dos cenários de cada VI
    # Os meses são varridos de cima para baixo. Quando eu tiver no mes 2 vou passar mes_futuro = 3
    # Como eu já fiz o despacho de todos os volumes iniciais do mes 3 já tenho todos os cortes dele e uso só os dele para ser o custo futuro em 2
    if icorte['Estagio'] == mes_futuro:
      equacao = 0
      for uhe in range(num_UHE): # para mais de uma uhe a reta vira plano ou outras superficies
        equacao += float(icorte['Coeficientes'][uhe])*vf[uhe]
      equacao += float(icorte['Termo independente'])
      restricoes.append(alpha[0] >= equacao)

  problema = op(fob, restricoes)
  problema.solve('dense', 'glpk') # dense nao usa matrizes esparças

  if problema.status != "optimal":
      raise RuntimeError(
          f"Não foi encontrada solução ótima. "
          f"Status: {problema.status}"
      )
  
  variaveis = {
      "vf": list(vf.value),
      "vt": list(vt.value),
      "vv": list(vv.value),
      "gt": list(gt.value),
      "deficit": deficit.value[0],
      "alpha": alpha.value[0]
  }

  multiplicadores = {
      "CMO": -restricoes[num_UHE].multiplier.value[0],
      "cma": [
          restricoes[i].multiplier.value[0]
          for i in range(num_UHE)
      ]
  }

  return resultados.gerar_resultados(imprime, multiplicadores, fob.value()[0], variaveis)




