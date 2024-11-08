import pandas as pd

df = pd.read_excel("C:/Users/luiz.borato/Desktop/teste distancia.xlsx")

df = df[['Instrutor(es)', 'Nome Comercial', 'Distancia']]

resultado = df.groupby(['Instrutor(es)', 'Nome Comercial'])['Distancia'].agg(['mean', 'max']).reset_index()

resultado.columns = ['Instrutor', 'Nome Comercial', 'Distância Média', 'Distância Máxima']

resultado.to_excel("distancias_por_instrutor_e_curso.xlsx", index=False)

print("Planilha salva como 'distancias_por_instrutor_e_curso.xlsx'")