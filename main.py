import modelo_cvxopt, modelo_scipopt, dados_usinas
from itertools import product, tee
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

passo = 100/(dados_usinas.sistema["Geral"]["Nr_Disc"]-1)  # quantos estados de volume inicial queremos analisar

lista = np.arange(0,100+passo,passo) # no arange o último elemento é exclusivo

discretizacoes = product(lista, repeat = dados_usinas.sistema["Geral"]["Num_UHE"]) # iterator com todas as possibilidades de combinação de 0, 50 e 100 para 2 usinas
discretizacoes = list(discretizacoes)

cortes = []

t = time.time()

VI_mes1 = []

for uhe in dados_usinas.sistema["UHE"]:
    VI_mes1.append(float(uhe["Vinicial"]))

# Mes
for iest in np.arange(dados_usinas.sistema["Geral"]["Nr_Est"], 0, -1):   # [3, 2, 1]
  if iest > 1 and dados_usinas.sistema["Geral"]["Num_UHE"] == 1:
    plt.figure(iest)
    plt.title("Funcao de custo futuro - Estágio" + str(iest))
    plt.xlabel("Volume inicial")
    plt.ylabel("Custo total")
    eixox = []
    eixoy = []

  if iest > 1 and dados_usinas.sistema["Geral"]["Num_UHE"] == 2:
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

  if iest == 1:
    discretizacoes_estagio = [None]  
  else:
    discretizacoes_estagio = discretizacoes

# Volume inicial
  for disc in discretizacoes_estagio:  
    if iest == 1:
      VI = VI_mes1
    else:
      VI = []
      for i, uhe in enumerate(dados_usinas.sistema["UHE"]):
        VI.append(uhe["Vmin"] + (uhe["Vmax"]-uhe["Vmin"])*disc[i]/100)  # 20 + (100-20)*0/100     depois 20 + (100-20)*50/100

    if iest > 1 and dados_usinas.sistema["Geral"]["Num_UHE"] == 1:
      eixox.append(VI[0])
    media = 0.
    media_cma = []
    for i, uhe in enumerate(dados_usinas.sistema["UHE"]):
        media_cma.append(0)

# Cenário de afluencia
    for icen in np.arange(0, dados_usinas.sistema["Geral"]["Nr_Cen"]): 
      AFL = []
      for i, uhe in enumerate(dados_usinas.sistema["UHE"]):
        AFL.append(uhe["Afl"][iest-1][icen]) # iest-1 pois a lista começa em 0 não em 1

      if dados_usinas.sistema["Geral"]["Otimizador"] == "cvxopt":
        resultado = modelo_cvxopt.despacho(dados_usinas.sistema, VI, AFL, cortes, iest+1, imprime = True)
      elif dados_usinas.sistema["Geral"]["Otimizador"] == "scipopt":  
        resultado = modelo_scipopt.despacho(dados_usinas.sistema, VI, AFL, cortes, iest+1, imprime = True)

      media += resultado["Geral"]["Custo total"]
      for i, uhe in enumerate(resultado["UHE"]):
        media_cma[i] += uhe["cma"]
    media = media/dados_usinas.sistema["Geral"]["Nr_Cen"]

    if iest > 1 and dados_usinas.sistema["Geral"]["Num_UHE"] == 2:
      for linha in range(dados_usinas.sistema["Geral"]["Nr_Disc"]):
        for coluna in range(dados_usinas.sistema["Geral"]["Nr_Disc"]):
          if usi_1[linha][coluna] == disc[0] and usi_2[linha][coluna] == disc[1]:
            custos[linha][coluna] = media

    termo_ind = media

    for i, uhe in enumerate(resultado["UHE"]):
      media_cma[i] = - media_cma[i]/dados_usinas.sistema["Geral"]["Nr_Cen"]  # mesmo as retas sendo decrescentes os valores de cma estão padronizados como positivos em ambos os solvers
      termo_ind -= VI[i]*media_cma[i]
    corte = {
        "Estagio": iest,
        "Termo independente": termo_ind,
        "Coeficientes": media_cma
    }

    cortes.append(corte)

    if iest > 1 and dados_usinas.sistema["Geral"]["Num_UHE"] == 1:
      eixoy.append(media)

  if iest > 1 and dados_usinas.sistema["Geral"]["Num_UHE"] == 1:
    plt.plot(eixox,eixoy, marker = 'o', color = 'blue')

  if iest > 1 and dados_usinas.sistema["Geral"]["Num_UHE"] == 2:
    surf = ax.plot_surface(usi_1, usi_2, custos, cmap = cm.coolwarm)

print("Tempo decorrido na PDE", time.time() - t)
#modelo_cvxopt.despacho(dados_usinas.sistema,[62, 150], [16, 30], cortes, 2, imprime = True)
plt.show()