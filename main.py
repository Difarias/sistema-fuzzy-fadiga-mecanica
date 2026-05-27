# main.py
import os
import numpy as np
import csv
from core import funcoes_fuzzy as fuzzy
from core import graficos as graficos

# CONFIGURAÇÃO DE PASTAS DE SAÍDA
PASTA_RAIZ = "imagens_geradas"
PASTA_PERTINENCIAS = os.path.join(PASTA_RAIZ, "imagens_pertinencias")
PASTA_COLETAS = os.path.join(PASTA_RAIZ, "imagens_coletas")

os.makedirs(PASTA_PERTINENCIAS, exist_ok=True)
os.makedirs(PASTA_COLETAS, exist_ok=True)

# Controladores booleanos para os gráficos de pertinência
_plotou_vento = False
_plotou_vibracao = False
_plotou_umidade = False
_plotou_saida = False

REGRAS = [
    ('B',  'MB', 'B',  'MB'), ('B',  'B',  'B',  'MB'), ('B',  'MO', 'B',  'B'),  
    ('B',  'A',  'B',  'B'),  ('B',  'AL', 'B',  'MO'), ('M',  'MB', 'B',  'B'),  
    ('M',  'B',  'B',  'B'),  ('M',  'MO', 'M',  'MO'), ('M',  'A',  'M',  'MO'), 
    ('M',  'AL', 'M',  'A'),  ('MA', 'MB', 'M',  'MO'), ('MA', 'B',  'M',  'MO'), 
    ('MA', 'MO', 'MA', 'A'),  ('MA', 'A',  'MA', 'A'),  ('MA', 'AL', 'MA', 'AL'), 
    ('A',  'MB', 'M',  'MO'), ('A',  'B',  'MA', 'A'),  ('A',  'MO', 'MA', 'A'),  
    ('A',  'A',  'A',  'AL'), ('A',  'AL', 'A',  'AL'), ('AL', 'MB', 'MA', 'A'),  
    ('AL', 'B',  'MA', 'A'),  ('AL', 'MO', 'A',  'AL'), ('AL', 'A',  'A',  'AL'), 
    ('AL', 'AL', 'AL', 'AL'), ('B',  'AL', 'AL', 'AL'), ('M',  'A',  'AL', 'AL'), 
    ('MA', 'B',  'AL', 'AL'), ('A',  'MB', 'AL', 'AL'), ('B',  'MO', 'MA', 'MO')  
]

def inferencia_fuzzy(v_val, u_val, t_val):
    """Executa o motor Fuzzy e gerencia a criação sob demanda dos gráficos de pertinência."""
    global _plotou_vento, _plotou_vibracao, _plotou_umidade, _plotou_saida
    
    # Aciona os plots das bibliotecas apenas uma única vez na primeira execução
    if not _plotou_vento:
        graficos.plotar_pertinencia_vento(PASTA_PERTINENCIAS); _plotou_vento = True
    if not _plotou_vibracao:
        graficos.plotar_pertinencia_vibracao(PASTA_PERTINENCIAS); _plotou_vibracao = True
    if not _plotou_umidade:
        graficos.plotar_pertinencia_umidade(PASTA_PERTINENCIAS); _plotou_umidade = True
    if not _plotou_saida:
        graficos.plotar_pertinencia_saida(PASTA_PERTINENCIAS); _plotou_saida = True

    y_dominio = np.linspace(0, 100, 1000)
    
    mu_v = {k: v[0] for k, v in fuzzy.f_pertinencia_vento(np.array([v_val])).items()}
    mu_u = {k: v[0] for k, v in fuzzy.f_pertinencia_umidade(np.array([u_val])).items()}
    mu_t = {k: v[0] for k, v in fuzzy.f_pertinencia_vibracao(np.array([t_val])).items()}
    
    mu_saida_discreta = fuzzy.f_pertinencia_saida(y_dominio)
    agregado = np.zeros_like(y_dominio)
    regras_ativas = []
    
    for idx, (r_vento, r_umidade, r_vib, r_saida) in enumerate(REGRAS, start=1):
        g_v = mu_v[r_vento]; g_u = mu_u[r_umidade]; g_t = mu_t[r_vib]
        grau_disparo = fuzzy.t_norma_dombi(fuzzy.t_norma_dombi(g_v, g_u), g_t)
        
        if grau_disparo > 0:
            regras_ativas.append(f"R{idx}(w={grau_disparo:.4f})")
            funcao_implicada = fuzzy.t_norma_dombi(grau_disparo, mu_saida_discreta[r_saida])
            agregado = fuzzy.t_conorma_dombi(agregado, funcao_implicada)
            
    soma_areas = np.sum(agregado)
    if soma_areas == 0:
        return 50.0, regras_ativas, agregado
        
    centro_gravidade = np.sum(y_dominio * agregado) / soma_areas
    return centro_gravidade, regras_ativas, agregado

# EXECUÇÃO DO PROJETO
coletas = [
    (1, 5.2, 18, 0.8), (2, 7.5, 35, 1.9), (3, 10.8, 42, 3.2),
    (4, 13.6, 58, 4.5), (5, 15.4, 67, 5.1), (6, 18.9, 74, 6.4),
    (7, 21.7, 83, 7.2), (8, 24.5, 91, 8.3), (9, 27.8, 96, 9.1),
    (10, 12.4, 49, 3.8), (11, 16.7, 62, 5.7), (12, 22.9, 88, 7.9)
]

print("=" * 130)
print(f"{'PPGMC - UESC: SISTEMA DE INFERÊNCIA FUZZY MODULAR':^130}")
print("=" * 130)
print(f"{'Coleta':<8} | {'Vento (m/s)':<12} | {'Umidade (%)':<12} | {'Vibr. (mm/s)':<13} | {'Risco Fadiga (%)':<18} | {'Ação Operacional':<20} | {'Regras Ativas':<30}")
print("-" * 130)

# Dicionário temporário para guardar os dados agregados para os gráficos posteriores
dados_graficos_coletas = {}

with open('resultados_fadiga_fuzzy.csv', mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor = csv.writer(arquivo_csv, delimiter=';') 
    escritor.writerow(['Coleta', 'Vento (m/s)', 'Umidade (%)', 'Vibracao (mm/s)', 'Risco Fadiga (%)', 'Acao Operacional', 'Regras Ativas'])

    for id_c, v, u, t in coletas:
        risco, regras_ativas, curva_agregada = inferencia_fuzzy(v, u, t)
        
        # Guardamos na memória para plotar depois
        dados_graficos_coletas[id_c] = (v, u, t, risco, curva_agregada)
        
        decisao = "REDUZIR ROTAÇÃO" if risco > 50.0 else "MANTER MÁXIMA"
        regras_str = ", ".join(regras_ativas)    
        
        print(f"{id_c:^8} | {v:^12.1f} | {u:^12.1f} | {t:^13.1f} | {risco:^18f} | {decisao:<20} | {regras_str}")
        escritor.writerow([id_c, v, u, t, risco, decisao, regras_str])

print("=" * 130)

# Gerando os perfis visuais de coletas específicas utilizando a biblioteca criada
for id_alvo in range(1, 13):
    if id_alvo in dados_graficos_coletas:
        v, u, t, risco, curva = dados_graficos_coletas[id_alvo]
        graficos.plotar_perfil_coleta(id_alvo, v, u, t, risco, curva, PASTA_COLETAS)