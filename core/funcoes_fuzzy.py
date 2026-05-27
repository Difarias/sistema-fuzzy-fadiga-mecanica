# funcoes_fuzzy.py
import numpy as np

def t_norma_dombi(x, y):
    """Calcula a t-norma de Dombi"""
    x = np.clip(x, 1e-15, 1.0)
    y = np.clip(y, 1e-15, 1.0)
    
    mask_x0 = (x <= 1e-14)
    mask_y0 = (y <= 1e-14)
    
    termo_x = ((1.0 - x) / x) ** 2
    termo_y = ((1.0 - y) / y) ** 2
    
    resultado = 1.0 / (1.0 + np.sqrt(termo_x + termo_y))
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
    resultado = np.where(mask_x1 | mask_y1, 1.0, resultado)
    return resultado

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