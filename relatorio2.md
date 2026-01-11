import os

# Nome do ficheiro a ser criado
nome_ficheiro = "Relatorio_Final_Clinica.md"

# Conteúdo do relatório
# Nota: Já inseri as imagens nos locais corretos (src="nome_do_ficheiro.ext")
conteudo = r"""
# Relatório do Projeto: Simulação de uma Clínica Médica

## Autores

Bárbara Jacques, a109722  
Esmeralda Freitas, a109932  
Martim Rocha, a112252

## Data de Execução

7 de Novembro de 2025 a 11 de Janeiro de 2026

## Enquadramento Institucional

**Instituição:** Universidade do Minho – Escola de Engenharia  
**Curso:** Licenciatura em Engenharia Biomédica (2.º ano)  
**Unidade Curricular:** Algoritmos e Técnicas de Programação  
**Projeto laboratorial idealizado e coordenado por:** José Carlos Ramalho e Luís Filipe Cunha

## Visão Geral do Projeto

No âmbito da unidade curricular de Algoritmos e Técnicas de Programação, foi proposto o desenvolvimento de uma aplicação em Python destinada à **simulação do funcionamento de uma clínica médica**. O objetivo principal do projeto consiste em modelar, de forma realista, o atendimento de doentes numa clínica, recorrendo a processos probabilísticos e a uma simulação de eventos discretos.

A aplicação permite analisar o impacto de diferentes parâmetros, tais como a taxa de chegada de doentes, o número de médicos disponíveis e o tempo médio de consulta, no desempenho global do sistema.

## Objetivos do Sistema

Os principais objetivos do sistema desenvolvido são:

* Simular a chegada de doentes a uma clínica médica segundo uma distribuição de Poisson;
* Simular o atendimento médico com tempos de consulta aleatórios, seguindo distribuições estatísticas apropriadas;
* Registar métricas de desempenho como tempos de espera, tamanho da fila e ocupação dos médicos;
* Gerar gráficos que representem a evolução desses indicadores ao longo do tempo;
* Permitir a variação dos parâmetros da simulação e a análise do impacto dessas alterações nos resultados.

## Descrição do Funcionamento do Sistema

O funcionamento básico da simulação segue o seguinte fluxo:

* Os doentes chegam à clínica de forma aleatória, de acordo com uma distribuição de Poisson com parâmetro λ;
* Caso exista um médico disponível, o doente é atendido de imediato;
* Caso contrário, o doente entra numa fila de espera (queue);
* O tempo de consulta é gerado aleatoriamente, seguindo uma distribuição exponencial, normal ou uniforme;
* Após o término da consulta, o doente abandona a clínica e o médico fica disponível para atender outro doente.

Todo o sistema é baseado numa **simulação de eventos discretos**, onde os principais eventos são a chegada e a saída de doentes.

## Parâmetros de Configuração

A aplicação permite configurar diversos parâmetros relevantes para a simulação, entre os quais:

* Taxa de chegada de doentes (doentes por hora);
* Número de médicos disponíveis;
* Tipo de distribuição do tempo de consulta;
* Tempo médio de consulta;
* Duração total da simulação.

Estes parâmetros podem ser alterados de modo a testar diferentes cenários e analisar o comportamento do sistema.

## Interface Gráfica

A aplicação dispõe de uma interface gráfica desenvolvida com o módulo **SimpleGUI**, permitindo executar a simulação, alterar parâmetros e visualizar gráficos.

### 1. Configuração da Simulação (Pré-Simulação)

Na fase inicial, o utilizador tem acesso a uma janela de configuração onde pode definir os principais parâmetros da simulação. Estes parâmetros são fundamentais para caracterizar o comportamento do sistema e influenciam diretamente os resultados obtidos.

<p align="center">
  <img src="pos_simulacao.jpg" alt="Interface Principal" width="600"/>
  <br>
  <em>Figura 1: Janela de configuração inicial da simulação e parâmetros.</em>
</p>

Antes de iniciar a simulação, são efetuadas validações automáticas aos dados introduzidos, garantindo que todos os campos obrigatórios se encontram preenchidos.

---

### 2. Execução da Simulação

Para fornecer feedback contínuo ao utilizador durante a execução, é apresentada uma barra de progresso que indica o estado do processamento.

<p align="center">
    <img src="barra_progresso.jpg" alt="Barra de Progresso" width="600"/>
    <br>
    <em>Figura 2: Barra de progresso durante a execução.</em>
</p>

---

### 3. Tratamento de Erros e Validação de Dados

Com o objetivo de aumentar a robustez da aplicação, foram implementados mecanismos de tratamento de erros. Sempre que o utilizador insere dados inválidos (como texto num campo numérico ou campos vazios), o sistema apresenta mensagens de aviso.

<p align="center">
    <img src="erro_vazio.png" alt="Erro Vazio" width="300"/>
    <img src="erro_inteiro.png" alt="Erro Inteiro" width="300"/>
    <br>
    <em>Figura 3: Exemplos de validação de dados (campos vazios e tipos de dados).</em>
</p>

---

### 4. Análise de Dados

Após a conclusão da simulação, o utilizador pode aceder à janela de análise de dados, onde são apresentadas estatísticas relevantes sobre os doentes atendidos, incluindo distribuição etária e perfis de risco.

<p align="center">
  <img src="analise_dados.png" alt="Análise de Dados" width="500"/>
  <br>
  <em>Figura 4: Janela de análise de dados da simulação.</em>
</p>

---

### 5. Visualização Gráfica dos Resultados

A aplicação disponibiliza um menu dedicado à visualização gráfica dos resultados obtidos.

<p align="center">
  <img src="menu_graficos.png" alt="Menu de Gráficos" width="300"/>
  <br>
  <em>Figura 5: Menu de seleção de gráficos.</em>
</p>

Após a seleção, o gráfico correspondente é gerado, facilitando a interpretação visual dos resultados, como a evolução da fila de espera.

<p align="center">
  <img src="evol_fila.png" alt="Evolução da Fila" width="600"/>
  <br>
  <em>Figura 6: Gráfico da evolução do tamanho da fila de espera ao longo do tempo.</em>
</p>

---

### 6. Persistência de Dados

O sistema permite ainda guardar os relatórios gerados em diferentes formatos.

<p align="center">
  <img src="guardar_tj.png" alt="Menu Guardar" width="300"/>
  <img src="guard_sucesso.png" alt="Sucesso" width="300"/>
  <br>
  <em>Figura 7: Funcionalidade de exportação de dados.</em>
</p>

---

## Integração de Dados Reais de Doentes

Para tornar a simulação mais realista, foi integrada a utilização de um **dataset de pessoas em formato JSON**. Em vez de trabalhar apenas com identificadores abstratos, o sistema lida com pessoas reais, caracterizadas por atributos demográficos.

### Exemplo de Estrutura do Dataset JSON

```json
{
  "nome": "Neyanne Sampaio",
  "idade": 47,
  "sexo": "feminino",
  "morada": {
    "cidade": "Ferreira do Alentejo",
    "distrito": "Beja"
  },
  "profissao": "Programador de aplicações",
  "atributos": {
    "fumador": true
  },
  "id": "p0"
}