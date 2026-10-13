lista_uhe = []
lista_ute = []

usina_h1 = {
    "Nome": "UHE_1",
    "Vmax": 100.,
    "Vmin": 20.,
    "Prod": 0.95,
    "Engol": 60.,
    "Afl": [
        [23,16],
        [19,14],
        [15,11]
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
    "Nome": "GT_1",
    "Cap": 15.,
    "Custo": 10.
}
lista_ute.append(usina_t1)

usina_t2 = {
    "Nome": "GT_2",
    "Cap": 10.,
    "Custo": 25.
}
lista_ute.append(usina_t2)

info_geral = {
    "Custo_def": 500.,
    "Carga": [100,100.,100],
    "Nr_Disc": 12,  # volumes iniciais
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
