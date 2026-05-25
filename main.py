import os
import numpy as np
import matplotlib.pyplot as plt
import csv

#1 - DEFINIÇÃO DA T-NORMA E T-CONORMA DE DOMBI 

def t_norma_dombi(x, y):
    """Calcula a t-norma de Dombi"""
    x = np.clip(x, 1e-15, 1.0)
    y = np.clip(y, 1e-15, 1.0)
    
    # Condições de contorno explícitas para garantir rigor matemático
    mask_x0 = (x <= 1e-14)
    mask_y0 = (y <= 1e-14)
    
    termo_x = ((1.0 - x) / x) ** 2
    termo_y = ((1.0 - y) / y) ** 2
    
    resultado = 1.0 / (1.0 + np.sqrt(termo_x + termo_y))
    
    # Onde x ou y for 0, a t-norma deve ser estritamente 0
    resultado = np.where(mask_x0 | mask_y0, 0.0, resultado)
    return resultado

def t_conorma_dombi(x, y):
    """Calcula a t-conorma (S-norma) de Dombi via Dualidade de De Morgan."""
    x = np.clip(x, 0.0, 1.0 - 1e-15)
    y = np.clip(y, 0.0, 1.0 - 1e-15)
    
    mask_x1 = (x >= (1.0 - 1e-14))
    mask_y1 = (y >= (1.0 - 1e-14))
    
    termo_x = (x / (1.0 - x)) ** 2
    termo_y = (y / (1.0 - y)) ** 2
    
    resultado = 1.0 - (1.0 / (1.0 + np.sqrt(termo_x + termo_y)))
    
    # Onde x ou y for 1, a t-conorma deve ser estritamente 1
    resultado = np.where(mask_x1 | mask_y1, 1.0, resultado)
    return resultado

#2 - FUNÇÕES DE PERTINÊNCIA PARAMÉTRICAS

def triangular(x, a, b, c):
    """Retorna o grau de pertinência para um número fuzzy triangular."""
    cond1 = (x > a) & (x <= b)
    cond2 = (x > b) & (x < c)
    
    res = np.zeros_like(x, dtype=float)
    res[cond1] = (x[cond1] - a) / (b - a)
    res[cond2] = (c - x[cond2]) / (c - b)
    return res

def trapezoidal(x, a, b, c, d):
    """Retorna o grau de pertinência para um número fuzzy trapezoidal."""
    cond1 = (x > a) & (x < b)
    cond2 = (x >= b) & (x <= c)
    cond3 = (x > c) & (x < d)
    
    res = np.zeros_like(x, dtype=float)
    res[cond1] = (x[cond1] - a) / (b - a)
    res[cond2] = 1.0
    res[cond3] = (d - x[cond3]) / (d - c)
    return res

#Dicionários globais de partições conforme especificações do documento do projeto
def f_pertinencia_vento(x):
    return {
        'B':  trapezoidal(x, 0, 0, 5, 8),
        'M':  triangular(x, 6, 10, 14),
        'MA': triangular(x, 12, 16, 20),
        'A':  triangular(x, 18, 21.5, 25),
        'AL': trapezoidal(x, 22, 30, 1e5, 1e5)
    }

def f_pertinencia_vibracao(x):
    return {
        'B':  trapezoidal(x, 0, 0, 1, 2),
        'M':  triangular(x, 1.5, 2.75, 4),
        'MA': triangular(x, 3.5, 4.75, 6),
        'A':  triangular(x, 5.5, 6.75, 8),
        'AL': trapezoidal(x, 7.5, 9.5, 1e5, 1e5)
    }

def f_pertinencia_umidade(x):
    return {
        'MB': trapezoidal(x, 0, 0, 10, 30),
        'B':  triangular(x, 20, 35, 50),
        'MO': triangular(x, 40, 55, 70),
        'A':  triangular(x, 60, 75, 90),
        'AL': trapezoidal(x, 80, 90, 100, 100)
    }

def f_pertinencia_saida(x):
    return {
        'MB': trapezoidal(x, 0, 0, 10, 20),
        'B':  triangular(x, 15, 30, 45),
        'MO': triangular(x, 40, 52.5, 65),
        'A':  triangular(x, 60, 72.5, 85),
        'AL': trapezoidal(x, 80, 90, 100, 100)
    }

#3 - BASE DE REGRAS

#Mapeamento exato das 30 regras descritas no PDF 
REGRAS = [
    #(Vento, Umidade, Vibração -> Risco de Fadiga)
    ('B',  'MB', 'B',  'MB'), # R1
    ('B',  'B',  'B',  'MB'), # R2
    ('B',  'MO', 'B',  'B'),  # R3
    ('B',  'A',  'B',  'B'),  # R4
    ('B',  'AL', 'B',  'MO'), # R5
    ('M',  'MB', 'B',  'B'),  # R6
    ('M',  'B',  'B',  'B'),  # R7
    ('M',  'MO', 'M',  'MO'), # R8
    ('M',  'A',  'M',  'MO'), # R9
    ('M',  'AL', 'M',  'A'),  # R10
    ('MA', 'MB', 'M',  'MO'), # R11
    ('MA', 'B',  'M',  'MO'), # R12
    ('MA', 'MO', 'MA', 'A'),  # R13
    ('MA', 'A',  'MA', 'A'),  # R14
    ('MA', 'AL', 'MA', 'AL'), # R15
    ('A',  'MB', 'M',  'MO'), # R16
    ('A',  'B',  'MA', 'A'),  # R17
    ('A',  'MO', 'MA', 'A'),  # R18
    ('A',  'A',  'A',  'AL'), # R19
    ('A',  'AL', 'A',  'AL'), # R20
    ('AL', 'MB', 'MA', 'A'),  # R21
    ('AL', 'B',  'MA', 'A'),  # R22
    ('AL', 'MO', 'A',  'AL'), # R23
    ('AL', 'A',  'A',  'AL'), # R24
    ('AL', 'AL', 'AL', 'AL'), # R25
    ('B',  'AL', 'AL', 'AL'), # R26
    ('M',  'A',  'AL', 'AL'), # R27
    ('MA', 'B',  'AL', 'AL'), # R28
    ('A',  'MB', 'AL', 'AL'), # R29
    ('B',  'MO', 'MA', 'MO')  # R30
]

#4 - MOTOR DE INFERÊNCIA E DEFUZZIFICAÇÃO

def inferencia_fuzzy(v_val, u_val, t_val):
    """Executa Fuzzificação, Interseção, Implicação de Dombi e Agregação."""
    #Discretização do universo de discurso da saída para integração numérica (Centro de Gravidade)
    y_dominio = np.linspace(0, 100, 1000)
    
    # 1 - Fuzzificação das entradas (passando arrays unitários para reusar as funções)
    mu_v = {k: v[0] for k, v in f_pertinencia_vento(np.array([v_val])).items()}
    mu_u = {k: v[0] for k, v in f_pertinencia_umidade(np.array([u_val])).items()}
    mu_t = {k: v[0] for k, v in f_pertinencia_vibracao(np.array([t_val])).items()}
    
    #Dicionário com as funções de pertinência completas da saída discretizada
    mu_saida_discreta = f_pertinencia_saida(y_dominio)
    
    #Inicialização do vetor de agregação com zeros
    agregado = np.zeros_like(y_dominio)

    regras_ativas = [] #Lista para guardar as regras explicáveis
    
    #Avaliação da Base de Regras
    for idx, (r_vento, r_umidade, r_vib, r_saida) in enumerate(REGRAS, start=1):
        #Recupera os graus de pertinência dos antecedentes
        g_v = mu_v[r_vento]
        g_u = mu_u[r_umidade]
        g_t = mu_t[r_vib]
        
        #Interseção dos antecedentes usando Dombi associativo: T_D(T_D(V, U), T)
        grau_disparo = t_norma_dombi(t_norma_dombi(g_v, g_u), g_t)
        
        if grau_disparo > 0:
            #Salva o nome da regra e o quão forte ela disparou
            regras_ativas.append(f"R{idx}(w={grau_disparo:.4f})")

            #Implicação de Dombi estendida: T_D(Grau de Disparo, Função de Pertinência de Saída)
            funcao_implicada = t_norma_dombi(grau_disparo, mu_saida_discreta[r_saida])
            
            #Agregação via T-Conorma de Dombi
            agregado = t_conorma_dombi(agregado, funcao_implicada)
            
    #Defuzzificação pelo método do Centro de Gravidade (Centróide)
    soma_areas = np.sum(agregado)
    if soma_areas == 0:
        return 50.0, regras_ativas  #Caso default se nenhuma regra disparar (centro do universo)
        
    centro_gravidade = np.sum(y_dominio * agregado) / soma_areas
    return centro_gravidade, regras_ativas

#5 - EXECUÇÃO PARA AS COLETAS DO PROJETO

#Matriz de dados baseada na tabela de Coletas 
coletas = [
    (1, 5.2, 18, 0.8), (2, 7.5, 35, 1.9), (3, 10.8, 42, 3.2),
    (4, 13.6, 58, 4.5), (5, 15.4, 67, 5.1), (6, 18.9, 74, 6.4),
    (7, 21.7, 83, 7.2), (8, 24.5, 91, 8.3), (9, 27.8, 96, 9.1),
    (10, 12.4, 49, 3.8), (11, 16.7, 62, 5.7), (12, 22.9, 88, 7.9)
]

print("=" * 130)
print(f"{'PPGMC - UESC: SISTEMA DE INFERÊNCIA FUZZY (MAMDANI-DOMBI)':^130}")
print(f"{'CONTROLE DE FADIGA MECÂNICA EM TURBINAS EÓLICAS':^130}")
print("=" * 130)
print(f"{'Coleta':<8} | {'Vento (m/s)':<12} | {'Umidade (%)':<12} | {'Vibr. (mm/s)':<13} | {'Risco Fadiga (%)':<18} | {'Ação Operacional':<20} | {'Regras Ativas':<30}")
print("-" * 130)

# Abre o arquivo CSV para gravação concorrente à execução
with open('resultados_fadiga_fuzzy.csv', mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor = csv.writer(arquivo_csv, delimiter=';') 
    
    escritor.writerow(['Coleta', 'Vento (m/s)', 'Umidade (%)', 'Vibracao (mm/s)', 'Risco Fadiga (%)', 'Acao Operacional', 'Regras Ativas'])

    for id_c, v, u, t in coletas:
        risco, regras_ativas = inferencia_fuzzy(v, u, t)
        
        #Decisão baseada no limiar de 50%
        if risco > 50.0:
            decisao = "REDUZIR ROTAÇÃO"
        else:
            decisao = "MANTER MÁXIMA"
            
        regras_str = ", ".join(regras_ativas)    
        
        #1-IMPRIME NO TERMINAL
        print(f"{id_c:^8} | {v:^12.1f} | {u:^12.1f} | {t:^13.1f} | {risco:^18f} | {decisao:<20} | {regras_str}")
        
        #2-GRAVA NO CSV 
        escritor.writerow([id_c, v, u, t, risco, decisao, regras_str])

print("=" * 130)
print("Obs: O limiar crítico para redução preventiva de rotação está calibrado em 50.00%.")
print("=" * 130)

# 7 - INSPECIONAR E PLOTAR UMA COLETA ESPECÍFICA
PASTA_IMAGENS = "imagens_geradas"
os.makedirs(PASTA_IMAGENS, exist_ok=True)

def visualizar_inferencia_coleta(id_coleta):
    dados_coleta = [c for c in coletas if c[0] == id_coleta]
    if not dados_coleta: return
    
    _, v_val, u_val, t_val = dados_coleta[0]
    y_dominio = np.linspace(0, 100, 1000)
    mu_saida_discreta = f_pertinencia_saida(y_dominio)
    
    mu_v = {k: v[0] for k, v in f_pertinencia_vento(np.array([v_val])).items()}
    mu_u = {k: v[0] for k, v in f_pertinencia_umidade(np.array([u_val])).items()}
    mu_t = {k: v[0] for k, v in f_pertinencia_vibracao(np.array([t_val])).items()}
    
    agregado = np.zeros_like(y_dominio)
    for r_vento, r_umidade, r_vib, r_saida in REGRAS:
        g_v = mu_v[r_vento]; g_u = mu_u[r_umidade]; g_t = mu_t[r_vib]
        grau_disparo = t_norma_dombi(t_norma_dombi(g_v, g_u), g_t)

        if grau_disparo > 0:
            funcao_implicada = t_norma_dombi(grau_disparo, mu_saida_discreta[r_saida])
            agregado = t_conorma_dombi(agregado, funcao_implicada)
            
    risco_final, _ = inferencia_fuzzy(v_val, u_val, t_val)
    
    #Estilização do Gráfico
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    plt.figure(figsize=(10, 5))
    
    #Curvas de referência de saída
    for termo, mu in mu_saida_discreta.items():
        plt.plot(y_dominio, mu, ':', color='gray', alpha=0.5)
        # Adiciona o nome do termo no topo de cada função para facilitar a leitura
        plt.text(np.argmax(mu)*0.1, 1.01, termo, fontsize=9, color='gray', ha='center')
        
    #Área Agregada por Dombi
    plt.fill_between(y_dominio, 0, agregado, color='#4A90E2', alpha=0.3, label='Superfície Combinada (Dombi)')
    plt.plot(y_dominio, agregado, color='#1F4E79', linewidth=2, label='Fronteira Agregada $S_D$')
    
    # Linha do Limiar Crítico de 50%
    plt.axvline(x=50.0, color='black', linestyle='--', alpha=0.7, label='Limiar de Decisão (50%)')
    
    # Linha do Resultado do Sistema
    cor_resultado = '#D9534F' if risco_final > 50.0 else '#5CB85C'
    plt.axvline(x=risco_final, color=cor_resultado, linestyle='-', linewidth=3, 
                label=f'Risco Calculado: {risco_final:.2f}%')
    
    plt.title(f'PPGMC - Perfil de Inferência Fuzzy (Coleta {id_coleta})\nInputs: Vento={v_val}m/s | Umidade={u_val}% | Vibração={t_val}mm/s', 
              fontsize=12, fontweight='bold', pad=15)
    plt.xlabel('Risco de Fadiga Mecânica (%)', fontsize=11)
    plt.ylabel('Grau de Pertinência ($\mu$)', fontsize=11)
    plt.xlim(0, 100)
    plt.ylim(0, 1.1)
    plt.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')
    plt.tight_layout()

    #Salva a imagem
    nome_arquivo = f"coleta_{id_coleta}.png"
    caminho_arquivo = os.path.join(PASTA_IMAGENS, nome_arquivo)

    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')

# Exemplo de uso: Escolher a coleta que deseja inspecionar visualmente (de 1 a 12)
# Peguei para exemplificar: Coleta 1 (Risco Baixo), Coleta 3 (Transição Crítica) e Coleta 9 (Risco Alto)
visualizar_inferencia_coleta(id_coleta=1)
visualizar_inferencia_coleta(id_coleta=3)
visualizar_inferencia_coleta(id_coleta=9)