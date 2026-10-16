lista_uhe = []
lista_ute = []

# usina_paraibuna = {
#     "Nome": "Paraibuna",
#     "ID": 1,
#     "Jusante": 2,
#     "Vinicial":3110.33,
#     "Vmax": 4732.,
#     "Vmin": 2096.,
#     "Prod": 0.26,
#     "Engol": 317.9,
#     "Afl": [
#         [154.71648, 74.18304],
#         [168.03936, 92.76768],
#         [188.77536, 110.67840]
#     ]
#     # "Afl": [
#     #     [360.28800, 182.16576],
#     #     [401.52672, 178.74432],
#     #     [350.23104, 171.90144],
#     #     [262.54368, 138.87936],
#     #     [195.02208, 115.18848],
#     #     [181.02528, 94.08960],
#     #     [150.20640, 88.87968],
#     #     [131.75136, 81.75168],
#     #     [154.71648, 74.18304],
#     #     [168.03936, 92.76768],
#     #     [188.77536, 110.67840],
#     #     [269.20512, 132.06240]
#     # ]

# }
# lista_uhe.append(usina_paraibuna)


usina_santabranca = {
    "Nome": "Santa Branca",
    "ID": 2,
    "Jusante": None, 
    "Vinicial":256.1,
    "Vmax": 439.,
    "Vmin": 131.,
    "Prod": 0.1314,
    "Engol": 339.21,
    "Afl": [
        [176.80032, 84.11040],   
        [191.28960, 104.84640],  
        [213.60672, 128.07072],
    ]
    # "Afl": [
    #     [409.38048, 209.38176],  
    #     [457.85088, 208.50048],  
    #     [399.99744, 194.14080],  
    #     [299.35008, 158.13792],  
    #     [223.11936, 131.31072],  
    #     [211.22208, 104.82048],  
    #     [171.14976, 101.99520],  
    #     [149.37696, 93.54528],   
    #     [176.80032, 84.11040],   
    #     [191.28960, 104.84640],  
    #     [213.60672, 128.07072],  
    #     [306.19296, 149.16960]   
    # ]
}
lista_uhe.append(usina_santabranca)


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
    #"Carga": [50.,50.,50.,50.,50.,50.,50.,50.,50.,50.,50.,50.],
    "Carga": [80.,80.,80.],
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
