from cvxopt.modeling import variable, solvers, op
import dados_usinas

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

  # Atendimento à demanda
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

  resultados_gerais = {
      "Deficit": deficit[0].value()[0],
      "CMO": restricoes[num_UHE].multiplier.value[0],
      "Custo total": fob.value()[0],
      "Custo futuro": alpha[0].value()[0]
  }

  lista_resultados_uhe = []
  for i, uhe in enumerate(sistema["UHE"]):
    resultado = {
        "vf": vf[i].value()[0],
        "vt": vt[i].value()[0],
        "vv": vv[i].value()[0],
        "cma": restricoes[i].multiplier.value[0]
    }
    lista_resultados_uhe.append(resultado)

  lista_resultados_ute = []
  for i, ute in enumerate(sistema["UTE"]):
    resultado = {
        "gt": gt[i].value()[0],

    }
    lista_resultados_ute.append(resultado)

  resultados = {
      "Geral": resultados_gerais,
      "UHE": lista_resultados_uhe,
      "UTE": lista_resultados_ute
  }

  if imprime:
      print(problema.status)
      print("Custo total:", fob.value())

      for i,uhe in enumerate(sistema["UHE"]):
        print(vf.name, i, "é", vf[i].value())
        print(vt.name, i, "é", vt[i].value())
        print(vv.name, i, "é", vv[i].value())

      for i, ute in enumerate(sistema['UTE']):
        print(gt.name, i, "é", gt[i].value())

      print(deficit.name, "é", deficit[0].value())

      print(alpha.name, "é", alpha[0].value())

      for i, uhe in enumerate(sistema["UHE"]):
        # O que acontece com a FOB se eu colocar 1 hm3 a mais de agua no reservatorio
        print("O valor da água na usina", i, "é: ", restricoes[i].multiplier.value)  # o multiplier fornece o multiplicador de lagrange da restrição

      print("O custo marginal de operação é: ", restricoes[num_UHE].multiplier.value)

      print("-------------------------------------------------")

  return resultados

from itertools import product, tee
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

passo = 100/(dados_usinas.sistema["Geral"]["Nr_Disc"]-1)  # quantos estados de volume inicial queremos analisar

lista = np.arange(0,100+passo,passo) # no arange o último elemento é exclusivo

discretizacoes = product(lista, repeat = dados_usinas.num_UHE) # iterator com todas as possibilidades de combinação de 0, 50 e 100 para 2 usinas
discretizacoes = list(discretizacoes)

cortes = []

t = time.time()

for iest in np.arange(dados_usinas.sistema["Geral"]["Nr_Est"], 0, -1):  # Analogo a cada mes
  if dados_usinas.num_UHE == 1:
    plt.figure(iest)
    plt.title("Funcao de custo futuro - Estágio" + str(iest))
    plt.xlabel("Volume inicial")
    plt.ylabel("Custo total")
    eixox = []
    eixoy = []

  if dados_usinas.num_UHE == 2:
    fig = plt.figure(iest)
    ax = fig.add_subplot(111, projection='3d')
    #ax = fig.gca(projection='3d')
    ax.set_title("Funcao de custo futuro - Estágio" + str(iest))
    ax.set_xlabel('Volume inicial UHE 1')
    ax.set_ylabel('Volume inicial UHE 2')
    ax.set_zlabel('FCF ($)')
    usi_1 = np.arange(0,100+passo,passo)
    usi_2 = np.arange(0,100+passo,passo)
    usi_1, usi_2 = np.meshgrid(usi_1, usi_2)  # Todas as combinações possiveis de volume inicial nas duas usinas (um dos maiores gargalos)
    custos = np.zeros((dados_usinas.sistema["Geral"]["Nr_Disc"],dados_usinas.sistema["Geral"]["Nr_Disc"]))

  for disc in discretizacoes:  # Analogo a cada volume inicial
    VI = []
    for i, uhe in enumerate(dados_usinas.sistema["UHE"]):
      VI.append(uhe["Vmin"] + (uhe["Vmax"]-uhe["Vmin"])*disc[i]/100)  # 20 + (100-20)*0/100     depois 20 + (100-20)*50/100
    if dados_usinas.num_UHE == 1:
      eixox.append(VI[0])
    media = 0.
    media_cma = []

    for i, uhe in enumerate(dados_usinas.sistema["UHE"]):
        media_cma.append(0)

    for icen in np.arange(0, dados_usinas.sistema["Geral"]["Nr_Cen"]): # Analogo a cada cenário de afluencia
      AFL = []

      for i, uhe in enumerate(dados_usinas.sistema["UHE"]):
        AFL.append(uhe["Afl"][iest-1][icen]) # iest-1 pois a lista começa em 0 não em 1
        #print(iest, disc, VI, icen, AFL)
      #print("Iniciando:", "estágio", iest,"VI", VI, "cenário", icen,flush=True )
      resultado = despacho(dados_usinas.sistema, VI, AFL, cortes, iest+1, imprime = False)
      #print(resultado) # cada dicionario de resultado
      # a = restricoes[num_UHE].multiplier.value[0]
      # coef_a.append(a)
      media += resultado["Geral"]["Custo total"]

      for i, uhe in enumerate(resultado["UHE"]):
        media_cma[i] += uhe["cma"]
    media = media/dados_usinas.sistema["Geral"]["Nr_Cen"]

    if dados_usinas.num_UHE == 2:
      for linha in range(dados_usinas.sistema["Geral"]["Nr_Disc"]):
        for coluna in range(dados_usinas.sistema["Geral"]["Nr_Disc"]):
          if usi_1[linha][coluna] == disc[0] and usi_2[linha][coluna] == disc[1]:
            custos[linha][coluna] = media

    termo_ind = media

    for i, uhe in enumerate(resultado["UHE"]):
      media_cma[i] = - media_cma[i]/dados_usinas.sistema["Geral"]["Nr_Cen"]  # mesmo as retas sendo decrescentes os valores de cma estão positivos, isso é uma estratégia do solver
      termo_ind -= VI[i]*media_cma[i]
    corte = {
        "Estagio": iest,
        "Termo independente": termo_ind,
        "Coeficientes": media_cma
    }

    cortes.append(corte)

    if dados_usinas.num_UHE == 1:
      eixoy.append(media)

  if dados_usinas.num_UHE == 1:
    plt.plot(eixox,eixoy, marker = 'o', color = 'blue')

  if dados_usinas.num_UHE == 2:
    surf = ax.plot_surface(usi_1, usi_2, custos, cmap = cm.coolwarm)


#print("Corte", cortes)
print("Tempo decorrido na PDE", time.time() - t)
despacho(dados_usinas.sistema,[62, 150], [16, 30], cortes, 2, imprime = True)

