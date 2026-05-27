# Sistema de Inferência Fuzzy Mamdani-Dombi para Predição de Fadiga Mecânica em Turbinas Eólicas

Este repositório contém a implementação computacional de um Sistema de Inferência Fuzzy do tipo Mamdani, integrado com os operadores matemáticos paramétricos de Dombi. Desenvolvido no escopo do Programa de Pós-Graduação em Modelagem Computacional (PPGMC) da Universidade Estadual de Santa Cruz (UESC), na disciplina Sistemas Fuzzy, o sistema visa monitorar a estabilidade operacional de aerogeradores expostos às condições ambientais severas do Nordeste brasileiro.

---

## 1. Interpretação Rápida do Sistema

Turbinas eólicas instaladas no Nordeste sofrem esforços mecânicos contínuos gerados pela ação conjunta de rajadas de vento imprevisíveis, alta umidade relativa e salinidade da maresia. Modelar essas interações dinâmicas por equações diferenciais exatas é extremamente complexo; por isso, a lógica fuzzy é uma alternativa ideal para tratar as incertezas e ambiguidades dos dados de campo.

### O que o sistema faz?
O modelo monitora continuamente três variáveis físicas (entradas nítidas):
1. Velocidade do Vento (m/s)
2. Umidade Relativa do Ar (%)
3. Vibração na Torre (mm/s)

A partir dessas grandezas, o motor de inferência estima o **Risco de Fadiga Mecânica (%)**. Este indicador determina a tomada de decisão automatizada baseada em um limiar crítico de 50%:
* **Risco > 50%**: Ativa o protocolo preventivo de **REDUZIR ROTAÇÃO** das pás para mitigar esforços estruturais.
* **Risco <= 50%**: Mantém a diretriz de **MANTER MÁXIMA** geração para priorizar a eficiência energética.

---

## 2. Estrutura do Projeto (Arquitetura Modular)

O projeto adota uma abordagem estritamente modular e orientada a componentes, separando as responsabilidades de cálculo matemático, renderização gráfica e fluxo de execução.

```bash
.
├── main.py                          # Script principal que orquestra o fluxo e gera o CSV
├── resultados_fadiga_fuzzy.csv      # Relatório final tabulado expandido
│
├── core/                            # Pasta que centraliza as bibliotecas internas do projeto
│   ├── funcoes_fuzzy.py             # Motor matemático pura (Dombi, triângulos e trapézios)
│   └── graficos.py                  # Biblioteca gráfica customizada (Matplotlib)
│
└── imagens_geradas/                 # Diretório de saídas visuais criado dinamicamente
    ├── imagens_pertinencias/        # Curvas de pertinência isoladas
    │   ├── pertinencia_vento.png
    │   ├── pertinencia_vibracao.png
    │   ├── pertinencia_umidade.png
    │   └── pertinencia_saida.png
    └── imagens_coletas/             # Perfis de inferência de todas as coletas (1 a 12)
        ├── coleta_1.png
        ├── ...
        └── coleta_12.png

```

### Divisão de Responsabilidades

* **`core/funcoes_fuzzy.py`**: Contém as equações vetorizadas em NumPy para a T-Norma e T-Conorma de Dombi (com filtros numéricos para evitar indeterminações nas bordas 0.0 e 1.0), além do mapeamento geométrico das funções trapezoidais e triangulares.
* **`core/graficos.py`**: Concentra a lógica de renderização e estilização visual das funções de pertinência e o preenchimento poligonal da área agregada pelo motor de inferência.
* **`main.py`**: Contém a base das 30 regras linguísticas, faz a leitura da matriz de coletas, invoca as operações matemáticas, imprime os dados formatados no terminal e escreve o relatório final.

---

## 3. Monitoramento Avançado e Saídas do Sistema

Ao rodar a execução do lote de dados, o sistema computa métricas profundas de comportamento do motor fuzzy, gerando saídas altamente explicáveis tanto no terminal quanto nos arquivos persistidos.

### Arquivos Gerados após a Execução

1. **`resultados_fadiga_fuzzy.csv`**: Arquivo persistido utilizando delimitador `";"` contendo os dados de entrada, o risco de fadiga calculado, a ação operacional tomada e as colunas analíticas detalhadas de ativação.
2. **`imagens_geradas/`**:
* **`imagens_pertinencias/`**: Gráficos individuais das curvas de partição de cada variável, gerados automaticamente uma única vez durante a primeira leitura.
* **`imagens_coletas/`**: Perfis visuais completos de **todas as 12 coletas históricas**, destacando de forma transparente a superfície combinada (Dombi), o limiar preventivo de 50% e a linha indicadora do risco final obtido.

---

## 4. Tecnologias Utilizadas

O ecossistema de desenvolvimento utilizou bibliotecas científicas robustas da linguagem Python:

* **Python 3.x** - Linguagem base.
* **NumPy** - Computação numérica avançada e operações matemáticas vetorizadas.
* **Matplotlib** - Renderização, preenchimento de áreas e estilização dos gráficos dos perfis.
* **CSV (Nativa)** - Gravação e persistência estruturada dos dados tabulados.
* **OS (Nativa)** - Gerenciamento automatizado de árvores de diretórios.

---

## 5. Como Executar

1. Clone o repositório:

```bash
git clone [https://github.com/Difarias/sistema-fuzzy-fadiga-mecanica](https://github.com/Difarias/sistema-fuzzy-fadiga-mecanica)
cd sistema-fuzzy-fadiga-mecanica
```

2. Instale as dependências necessárias:

```bash
pip install numpy matplotlib
```

3. Execute o script principal na raiz do projeto:

```bash
python main.py
```