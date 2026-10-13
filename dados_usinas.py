lista_uhe = []
lista_ute = []

usina_h1 = {
    "Nome": "Santa Branca",
    "Vinicial":254.2,
    "Vmax": 439.,
    "Vmin": 131.,
    "Prod": 0.1314,
    "Engol": 339.21,
    "Afl": [
        [173.4, 84.5],
        [191.28, 104.72],
        [213.58, 128.04]
    ]
}
lista_uhe.append(usina_h1)

# usina_h2 = {
#     "Nome": "UHE_2",
#     "Vmax": 200.,
#     "Vmin": 40.,
#     "Prod": 0.85,
#     "Engol": 100.,
#     "Afl": [
#         [46,38],
#         [30,28],
#         [30,22]
#     ]
# }
# lista_uhe.append(usina_h2)

usina_t1 = {
    "Nome": "Santa Luz",
    "Cap": 12.,
    "Custo": 581.48*720
}
lista_ute.append(usina_t1)

usina_t2 = {
    "Nome": "Baliza",
    "Cap": 18.,
    "Custo": 917.12*720
}
lista_ute.append(usina_t2)

info_geral = {
    "Custo_def": 8291*720,
    "Carga": [50,50.,50],
    "Nr_Disc": 3,  # volumes iniciais
    "Nr_Est": 3,  # meses
    "Nr_Cen": 2,  # otimista e pessimista
    "Num_UHE": len(lista_uhe),
    "Num_UTE": len(lista_ute),
    "Otimizador": "cvxopt"
}

sistema = {  # Dicionário de um dicionario e de listas de dicionários
    "Geral": info_geral,
    "UHE": lista_uhe,
    "UTE": lista_ute
}

if __name__ == "__main__":  # Só printará se eu rodar dados_usinas.py diretamente, se só importar dados_usinas não há print
    print(len(lista_uhe))
    print(sistema["UTE"])
    print(sistema["UTE"][0])
    print(sistema["UTE"][0]["Nome"])
    print(sistema["Geral"]["Custo_def"])
