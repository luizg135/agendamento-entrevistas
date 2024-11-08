import pandas as pd
from ortools.linear_solver import pywraplp

municipios_sem_atendimento = pd.read_excel('C:/Users/luiz.borato/Desktop/Calculo.xlsx')
coordenadas_municipios = pd.read_excel('C:/Users/luiz.borato/Desktop/Coordenadas1.xlsx')
distancias_municipios = pd.read_excel('C:/Users/luiz.borato/Desktop/Distancia.xlsx')

municipios_sem_atendimento['Município'] = municipios_sem_atendimento['Município'].str.strip()
distancias_municipios['Origem'] = distancias_municipios['Origem'].str.strip()
distancias_municipios['Destino'] = distancias_municipios['Destino'].str.strip()

cursos_unicos = municipios_sem_atendimento['Nome Comercial'].unique()

distancias_municipios_pivot = distancias_municipios.pivot_table(index='Origem', columns='Destino', values='Distância')

def solve_set_cover(municipios_sem_atendimento_list, distancias_municipios_pivot, max_distance=100):

    solver = pywraplp.Solver.CreateSolver('SCIP')

    municipios_base = distancias_municipios_pivot.index.tolist()
    num_municipios_base = len(municipios_base)

    x = [solver.IntVar(0, 1, f'x_{i}') for i in range(num_municipios_base)]

    for municipio in municipios_sem_atendimento_list:
        if municipio not in distancias_municipios_pivot.index:
            print(f'Município {municipio} não encontrado, ignorando...')
            continue
        solver.Add(
            solver.Sum(x[j] for j in range(num_municipios_base) 
                       if municipio in distancias_municipios_pivot.index and
                       distancias_municipios_pivot.at[municipio, municipios_base[j]] <= max_distance) >= 1
        )

    solver.Minimize(solver.Sum(x))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solução ótima encontrada!')

        municipios_selecionados = [municipios_base[i] for i in range(num_municipios_base) if x[i].solution_value() == 1]
        return municipios_selecionados
    else:
        print('Nenhuma solução encontrada.')
        return None

def melhores_municipios_por_curso(municipios_sem_atendimento, distancias_municipios_pivot, cursos_unicos):
    resultados_cursos = {}

    for curso in cursos_unicos:
        print(f"Resolvendo para o curso: {curso}")

        municipios_curso = municipios_sem_atendimento[municipios_sem_atendimento['Nome Comercial'] == curso]
        municipios_sem_atendimento_list = municipios_curso['Município'].unique()

        melhores_municipios = solve_set_cover(municipios_sem_atendimento_list, distancias_municipios_pivot)

        if melhores_municipios:
            resultados_cursos[curso] = melhores_municipios

    return resultados_cursos

resultados = melhores_municipios_por_curso(municipios_sem_atendimento, distancias_municipios_pivot, cursos_unicos)

resultados_df = pd.DataFrame([
    {'Curso': curso, 'Melhor Município': municipio}
    for curso, municipios in resultados.items()
    for municipio in municipios
])

output_file = 'C:/Users/luiz.borato/Desktop/melhores_municipios_por_curso_v2.xlsx'
resultados_df.to_excel(output_file, index=False)

print(f"Resultados salvos em {output_file}")