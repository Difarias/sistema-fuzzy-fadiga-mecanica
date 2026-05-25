
# Sistema de Inferência Fuzzy Mamdani-Dombi para Predição de Fadiga Mecânica em Turbinas Eólicas

Este repositório contém a implementação computacional de um Sistema de Inferência Fuzzy (SIF) do tipo Mamdani, integrado com os operadores matemáticos paramétricos de Dombi. Desenvolvido no escopo do Programa de Pós-Graduação em Modelagem Computacional (PPGMC) da Universidade Estadual de Santa Cruz (UESC), o sistema visa monitorar a estabilidade operacional de aerogeradores expostos às condições ambientais severas do Nordeste brasileiro.

---

## 1. Interpretação Rápida do Sistema

Turbinas eólicas instaladas no Nordeste sofrem esforços mecânicos contínuos gerados pela ação conjunta de rajadas de vento imprevisíveis, alta umidade relativa e salinidade da maresia. Modelar essas interações dinâmicas por equações diferenciais exatas é extremamente complexo; por isso, a lógica fuzzy é uma alternativa ideal para tratar as incertezas e ambiguidades dos dados de campo.

### O que o sistema faz?
O modelo monitora continuamente três variáveis físicas (entradas nítidas):
1. Velocidade do Vento (m/s)
2. Umidade Relativa do Ar (%)
3. Vibração na Torre (mm/s)

A partir dessas grandezas, o motor de inferência estima o Risco de Fadiga Mecânica (%). Este indicador determina a tomada de decisão automatizada baseada em um limiar crítico de 50%:
* Risco > 50%: Ativa o protocolo preventivo de REDUZIR ROTAÇÃO das pás para mitigar esforços estruturais.
* Risco <= 50%: Mantém a diretriz de MANTER MÁXIMA geração para priorizar a eficiência energética.


---

## 2. Estrutura do Projeto e Arquivos Gerados

O projeto foi construído sob uma abordagem puramente modular dentro de um único script principal estruturado.

### Arquitetura do Código
* Operadores de Dombi: Funções vetorizadas com NumPy que calculam a T-Norma e a T-Conorma (via Dualidade de De Morgan), aplicando técnicas de clipping e filtros booleanos para evitar indeterminações numéricas ou divisões por zero nas condições de contorno (0.0 e 1.0).
* Funções de Pertinência Paramétricas: Modelagem geométrica utilizando funções Trapezoidais nas extremidades (para garantir saturação física e pertinência total nas condições mínimas/máximas) e Triangulares nas partições intermediárias.
* Base de Regras: Mapeamento matricial exato das 30 regras de inferência linguísticas que cruzam as condições ambientais.
* Motor de Inferência e Defuzzificação: Fuzzificação das entradas, cálculo do grau de disparo encadeado, implicação não linear e defuzzificação baseada no método numérico do Centro de Gravidade (Centróide) com alta resolução (discretização do universo em 1000 pontos).

### Arquivos e Diretórios Gerados após a Execução

Ao rodar o arquivo principal, o sistema processa automaticamente em lote um conjunto histórico de 12 coletas e gera as seguintes saídas:

```bash
.
├── main.py                  # Script principal com a inteligência do sistema
├── resultados_fadiga_fuzzy.csv    # Relatório de dados tabulados em formato CSV
└── imagens_geradas/               # Pasta criada dinamicamente para os gráficos
    ├── coleta_1.png               # Perfil de inferência para cenário de Risco Baixo
    ├── coleta_3.png               # Perfil de inferência para cenário de Transição Crítica
    └── coleta_9.png               # Perfil de inferência para cenário de Risco Alto

```

* resultados_fadiga_fuzzy.csv: Arquivo persistido utilizando delimitador ";" contendo os dados de entrada das coletas, o risco de fadiga calculado com precisão de ponto flutuante, a ação operacional tomada e a string explicável descrevendo quais regras foram ativadas e o peso de disparo de cada uma.
* imagens_geradas/: Gráficos de alta resolução gerados pelo Matplotlib. Eles destacam de forma transparente a superfície combinada (área agregada por Dombi), o limiar preventivo de 50% e a linha indicadora do risco final obtido, servindo como uma ferramenta visual de suporte à decisão da engenharia de manutenção.

---

## 3. Tecnologias Utilizadas

O ecossistema de desenvolvimento foi focado em bibliotecas científicas robustas da linguagem Python:

* Python 3.x - Linguagem base.
* NumPy - Para computação numérica avançada, operações matemáticas vetorizadas e manipulação de matrizes de pertinência.
* Matplotlib - Para renderização e estilização dos gráficos dos perfis de inferência fuzzy.
* CSV (Nativa) - Para gravação e persistência dos dados tabulados.
* OS (Nativa) - Para gerenciamento automatizado de diretórios no sistema operacional.

---

## 4. Como Executar e Personalizar a Visualização

1. Clone o repositório:
```bash
git clone https://github.com/Difarias/sistema-fuzzy-fadiga-mecanica
cd sistema-fuzzy-fadiga-mecanica
```


2. Instale as dependências necessárias:
```bash
pip install numpy matplotlib
```


3. Execute o script:
```bash
python main.py
```



### Visualizando outras coletas

Por padrão, o script vem configurado para exportar e exibir os gráficos de três coletas específicas (1, 3 e 9). Caso você queira inspecionar visualmente o perfil de inferência de qualquer outra coleta presente no histórico (de 1 a 12), basta localizar o final do arquivo de código e alterar o número do identificador na função de visualização.

Por exemplo, para analisar a coleta 9, a linha correspondente deve ser configurada da seguinte forma:

```python
visualizar_inferencia_coleta(id_coleta=9)

```

Modifique o valor de `id_coleta` para o número correspondente à medição desejada e execute o script novamente para gerar o novo gráfico na pasta de imagens.