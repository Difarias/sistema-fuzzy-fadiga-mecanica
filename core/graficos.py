# graficos.py
import os
import numpy as np
import matplotlib.pyplot as plt
import core.funcoes_fuzzy as fuzzy

# Configuração de estilo global para os plots
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

def plotar_pertinencia_vento(caminho_pasta):
    x_dom = np.linspace(0, 35, 1000)
    termos = fuzzy.f_pertinencia_vento(x_dom)
    plt.figure(figsize=(7, 4))
    for termo, mu in termos.items():
        if termo == 'AL':
            mu = fuzzy.trapezoidal(x_dom, 22, 30, 35, 35)
        plt.plot(x_dom, mu, label=termo, linewidth=2)
    plt.title('Funções de Pertinência: Velocidade do Vento', fontsize=11, fontweight='bold')
    plt.xlabel('m/s')
    plt.ylabel('Grau ($\mu$)')
    plt.xlim(0, 35)
    plt.ylim(0, 1.05)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(os.path.join(caminho_pasta, "pertinencia_vento.png"), dpi=300)
    plt.close()

def plotar_pertinencia_vibracao(caminho_pasta):
    x_dom = np.linspace(0, 10, 1000)
    termos = fuzzy.f_pertinencia_vibracao(x_dom)
    plt.figure(figsize=(7, 4))
    for termo, mu in termos.items():
        if termo == 'AL':
            mu = fuzzy.trapezoidal(x_dom, 7.5, 9.5, 10, 10)
        plt.plot(x_dom, mu, label=termo, linewidth=2)
    plt.title('Funções de Pertinência: Vibração da Torre', fontsize=11, fontweight='bold')
    plt.xlabel('mm/s RMS')
    plt.ylabel('Grau ($\mu$)')
    plt.xlim(0, 10)
    plt.ylim(0, 1.05)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(os.path.join(caminho_pasta, "pertinencia_vibracao.png"), dpi=300)
    plt.close()

def plotar_pertinencia_umidade(caminho_pasta):
    x_dom = np.linspace(0, 100, 1000)
    termos = fuzzy.f_pertinencia_umidade(x_dom)
    plt.figure(figsize=(7, 4))
    for termo, mu in termos.items():
        plt.plot(x_dom, mu, label=termo, linewidth=2)
    plt.title('Funções de Pertinência: Umidade Relativa', fontsize=11, fontweight='bold')
    plt.xlabel('%')
    plt.ylabel('Grau ($\mu$)')
    plt.xlim(0, 100)
    plt.ylim(0, 1.05)
    plt.legend(loc='center right')
    plt.tight_layout()
    plt.savefig(os.path.join(caminho_pasta, "pertinencia_umidade.png"), dpi=300)
    plt.close()

def plotar_pertinencia_saida(caminho_pasta):
    x_dom = np.linspace(0, 100, 1000)
    termos = fuzzy.f_pertinencia_saida(x_dom)
    plt.figure(figsize=(7, 4))
    for termo, mu in termos.items():
        plt.plot(x_dom, mu, label=termo, linewidth=2)
    plt.title('Funções de Pertinência: Risco de Fadiga (Saída)', fontsize=11, fontweight='bold')
    plt.xlabel('%')
    plt.ylabel('Grau ($\mu$)')
    plt.xlim(0, 100)
    plt.ylim(0, 1.05)
    plt.legend(loc='center right')
    plt.tight_layout()
    plt.savefig(os.path.join(caminho_pasta, "pertinencia_saida.png"), dpi=300)
    plt.close()

def plotar_perfil_coleta(id_coleta, v_val, u_val, t_val, risco_final, agregado, caminho_pasta):
    y_dominio = np.linspace(0, 100, 1000)
    mu_saida_discreta = fuzzy.f_pertinencia_saida(y_dominio)
    
    plt.figure(figsize=(10, 5))
    for termo, mu in mu_saida_discreta.items():
        plt.plot(y_dominio, mu, ':', color='gray', alpha=0.5)
        plt.text(np.argmax(mu)*0.1, 1.01, termo, fontsize=9, color='gray', ha='center')
        
    plt.fill_between(y_dominio, 0, agregado, color='#4A90E2', alpha=0.3, label='Superfície Combinada (Dombi)')
    plt.plot(y_dominio, agregado, color='#1F4E79', linewidth=2, label='Fronteira Agregada $S_D$')
    plt.axvline(x=50.0, color='black', linestyle='--', alpha=0.7, label='Limiar de Decisão (50%)')
    
    cor_resultado = '#D9534F' if risco_final > 50.0 else '#5CB85C'
    plt.axvline(x=risco_final, color=cor_resultado, linestyle='-', linewidth=3, label=f'Risco Calculado: {risco_final:.2f}%')
    
    plt.title(f'PPGMC - Perfil de Inferência Fuzzy (Coleta {id_coleta})\nInputs: Vento={v_val}m/s | Umidade={u_val}% | Vibração={t_val}mm/s', fontsize=12, fontweight='bold', pad=15)
    plt.xlabel('Risco de Fadiga Mecânica (%)', fontsize=11)
    plt.ylabel('Grau de Pertinência ($\mu$)', fontsize=11)
    plt.xlim(0, 100)
    plt.ylim(0, 1.1)
    plt.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')
    plt.tight_layout()

    plt.savefig(os.path.join(caminho_pasta, f"coleta_{id_coleta}.png"), dpi=300, bbox_inches='tight')
    plt.close()