# Relatório do Projeto: Simulação de uma Clínica Médica

## 1. Identificação do Projeto

**Unidade Curricular:** Algoritmos e Técnicas de Programação
**Curso:** Licenciatura em Engenharia Biomédica (2.º ano)
**Instituição:** Universidade do Minho – Escola de Engenharia
**Projeto laboratorial coordenado por:** José Carlos Ramalho, Luís Filipe Cunha

**Autores:**
Bárbara Jacques (a109722)
Esmeralda Rodrigues Freitas (a109932)
Martim Rocha (a112252)

**Data:** 29 de dezembro de 2025

---

## 2. Introdução

No âmbito da Unidade Curricular de **Algoritmos e Técnicas de Programação**, foi proposto o desenvolvimento de uma aplicação em Python com o objetivo de **simular o funcionamento de uma clínica médica**. O sistema desenvolvido permite modelar o processo de atendimento de doentes, considerando a chegada aleatória, a gestão de filas de espera e a ocupação de médicos.

A aplicação recorre a conceitos fundamentais abordados ao longo da unidade curricular, nomeadamente **manipulação de estruturas de dados**, **programação modular**, **uso de distribuições probabilísticas** e **desenvolvimento de interfaces de interação com o utilizador**. O objetivo principal é analisar o desempenho da clínica em diferentes cenários, através da recolha de métricas e da visualização gráfica dos resultados.

---

## 3. Objetivos do Sistema

Os principais objetivos do sistema desenvolvido são:

* Simular a chegada de doentes a uma clínica médica;
* Modelar o atendimento médico com recursos limitados;
* Gerir filas de espera de forma dinâmica;
* Recolher métricas relevantes sobre o funcionamento do sistema;
* Permitir a análise estatística dos resultados obtidos;
* Disponibilizar interfaces de interação intuitivas para o utilizador.

---

## 4. Descrição Geral do Funcionamento

A simulação desenvolvida segue uma abordagem de **eventos discretos**, em que o sistema evolui ao longo do tempo através da ocorrência de eventos específicos. Os principais eventos considerados são:

* Chegada de um doente à clínica;
* Início de consulta, caso exista médico disponível;
* Entrada do doente em fila de espera, caso todos os médicos estejam ocupados;
* Término da consulta e libertação do médico.

Os tempos entre chegadas de doentes são gerados de forma aleatória segundo uma **distribuição de Poisson**, enquanto a duração das consultas é obtida a partir de distribuições estatísticas configuráveis.

---

## 5. Parâmetros de Configuração

Antes da execução da simulação, o utilizador pode definir diversos parâmetros que influenciam o comportamento do sistema, nomeadamente:

* Taxa média de chegada de doentes;
* Número de médicos disponíveis;
* Tipo de distribuição utilizada para o tempo de consulta;
* Tempo médio de consulta;
* Duração total da simulação.

A possibilidade de alterar estes parâmetros permite analisar diferentes cenários de funcionamento da clínica.

---

## 6. Resultados e Métricas de Desempenho

Durante a execução da simulação, são recolhidas várias métricas relevantes, nomeadamente:

* Tempo médio de espera dos doentes;
* Tempo médio de consulta;
* Tempo médio total de permanência na clínica;
* Tamanho médio e máximo da fila de espera;
* Percentagem de ocupação dos médicos;
* Número total de doentes atendidos.

Estes indicadores permitem avaliar quantitativamente a eficiência do sistema simulado.

---

## 7. Interfaces do Sistema

### 7.1 Command Line Interface (CLI)

A aplicação disponibiliza uma **Interface de Linha de Comando (CLI)** que permite ao utilizador interagir com o sistema através de menus textuais. Esta interface possibilita a configuração da simulação, a execução do modelo e a visualização dos resultados estatísticos de forma simples e direta.

O utilizador pode, através desta interface, iniciar a simulação, alterar parâmetros e consultar métricas finais.

### 7.2 Graphical User Interface (GUI)

Para além do CLI, foi desenvolvida uma **Interface Gráfica do Utilizador (GUI)** utilizando a biblioteca **PySimpleGUI**. Esta interface permite uma interação mais intuitiva, recorrendo a botões, campos de texto e janelas.

A GUI encontra-se organizada em diferentes janelas, permitindo:

* Configuração dos parâmetros da simulação;
* Execução da simulação com acompanhamento visual;
* Visualização de mensagens de erro e validação de dados;
* Acesso a gráficos e estatísticas finais.

---

## 8. Base de Dados (Dataset JSON)

De forma a aumentar o realismo da simulação, foi integrado um **dataset em formato JSON**, fornecido no âmbito do projeto. Cada registo do dataset representa um potencial doente, contendo diferentes atributos demográficos e comportamentais.

### 8.1 Estrutura do Dataset

O ficheiro JSON contém uma lista de pessoas, onde cada elemento inclui informação demográfica e comportamental relevante para a análise da simulação. Um excerto simplificado da estrutura do dataset é apresentado de seguida:

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
  "desportos": ["Peteca", "Rugby de praia"],
  "atributos": {
    "fumador": true,
    "gosta_musica": true,
    "comida_favorita": "vegetariana"
  },
  "id": "p0"
}
```

### 8.2 Carregamento e Validação dos Dados

O carregamento do dataset é realizado através de uma função dedicada, responsável por ler o ficheiro JSON e devolver a lista de pessoas a utilizar na simulação:

```python
import json

def carregar_e_validar(caminho):
    """Carrega o JSON e devolve a lista de pessoas."""
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados
```

### 8.3 Cálculo de Estatísticas Demográficas

A partir da lista de pessoas carregada, são calculadas várias estatísticas que permitem caracterizar a população atendida pela clínica. Um exemplo do cálculo das estatísticas relativas à idade é apresentado de seguida:

```python
def estatisticas_idades(lista):
    soma = 0
    contagem = 0
    min_idade = 999
    max_idade = -1

    for p in lista:
        idade = p["idade"]
        soma += idade
        contagem += 1
        if idade < min_idade:
            min_idade = idade
        if idade > max_idade:
            max_idade = idade

    return {
        "media": soma / contagem if contagem > 0 else 0,
        "min": min_idade,
        "max": max_idade,
        "total": contagem
    }
```

De forma semelhante, são implementadas funções adicionais para a análise da distribuição geográfica, hábitos de saúde, prática de atividade física e perfil profissional dos doentes.

Os resultados destas análises podem ser apresentados graficamente ou exportados para ficheiros externos em formato **JSON** e **TXT**, garantindo persistência e reprodutibilidade dos resultados.

---

## 9. Tecnologias Utilizadas

* **Python** – linguagem de programação principal;
* **PySimpleGUI** – desenvolvimento da interface gráfica;
* **NumPy** – geração de variáveis aleatórias e apoio estatístico;
* **Matplotlib** – criação de gráficos;
* **JSON** – armazenamento e troca de dados.

---

## 9. Metodologia de Simulação

O sistema baseia-se numa abordagem de **simulação de eventos discretos**, onde os médicos são modelados como recursos limitados e os doentes como entidades que percorrem o sistema.

A fila de espera é representada através de uma estrutura do tipo *queue*, garantindo uma ordem de atendimento adequada. A simulação mantém o controlo do tempo atual e dos eventos futuros, permitindo uma análise detalhada do comportamento do sistema ao longo do período simulado.

---

## 10. Desafios e Soluções

Durante o desenvolvimento do projeto foram identificados vários desafios, nomeadamente:

* A correta modelação do comportamento estocástico do sistema;
* A gestão eficiente da fila de espera;
* A recolha consistente de métricas ao longo da simulação;
* A integração de dados reais com a lógica da simulação.

Estes desafios foram ultrapassados através de uma estruturação cuidada do código, desenvolvimento de funções modulares e realização de testes com diferentes cenários.

---

## 11. Conclusão

O desenvolvimento deste projeto permitiu consolidar os conhecimentos adquiridos na Unidade Curricular de **Algoritmos e Técnicas de Programação**, nomeadamente no que diz respeito à programação em Python, manipulação de dados e desenvolvimento de interfaces.

A simulação de uma clínica médica revelou-se uma aplicação prática e relevante, possibilitando a análise do impacto de diferentes parâmetros no desempenho do sistema. Conclui-se que os objetivos propostos foram atingidos, resultando numa aplicação funcional, extensível e alinhada com os requisitos definidos para o projeto.
