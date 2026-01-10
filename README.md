# Relatório do Projeto: Simulação de uma Clínica Médica

## Autores

Barbara Jacques
Esmeralda Freitas
Martim Rocha

## Data de Execução

7 de Novembro de 2025 a 11 de Janeiro de 2026

## Enquadramento Institucional

**Instituição:** Universidade do Minho – Escola de Engenharia
**Curso:** Licenciatura em Engenharia Biomédica (2.º ano)
**Unidade Curricular:** Algoritmos e Técnicas de Programação
**Projeto laboratorial idealizado e coordenado por:** José Carlos Ramalho e Luís Filipe Cunha

## Visão Geral do Projeto

No âmbito da unidade curricular de Algoritmos e Técnicas de Programação, foi proposto o desenvolvimento de uma aplicação em Python destinada à **simulação do funcionamento de uma clínica médica**. O objetivo principal do projeto consiste em modelar, de forma realista, o atendimento de doentes numa clínica, recorrendo a processos estocásticos e a uma simulação de eventos discretos.

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

## Resultados Produzidos

Durante a execução da simulação, são recolhidos diversos indicadores de desempenho, nomeadamente:

* Tempo médio de espera dos doentes;
* Tempo médio de consulta;
* Tempo médio total de permanência na clínica;
* Tamanho médio e máximo da fila de espera;
* Percentagem de ocupação dos médicos;
* Número total de doentes atendidos.

## Gráficos Gerados

Com base nos dados recolhidos, a aplicação gera vários gráficos, entre os quais:

* Evolução do tamanho da fila de espera ao longo do tempo;
* Evolução da taxa de ocupação dos médicos ao longo da simulação;
* Relação entre a taxa de chegada de doentes e o tamanho médio da fila de espera;
* Outros gráficos adicionais considerados relevantes para a análise do sistema.

## Interface Gráfica

A aplicação dispõe de uma interface gráfica desenvolvida com o módulo **SimpleGUI**, permitindo:

* Executar a simulação;
* Alterar os parâmetros do sistema;
* Visualizar os gráficos gerados;
* (Funcionalidade extra) Visualizar graficamente a fila de espera e a ocupação dos consultórios.

A interface foi concebida de forma a facilitar a interação do utilizador com a simulação e a interpretação dos resultados obtidos.

## Tecnologias Utilizadas

* **Python** – linguagem de programação principal;
* **SimpleGUI** – desenvolvimento da interface gráfica;
* **NumPy** – geração de variáveis aleatórias e apoio ao cálculo estatístico;
* **Matplotlib** – criação de gráficos e visualizações;
* **JSON** – armazenamento e configuração de parâmetros (opcional).

## Metodologia de Simulação

O sistema utiliza uma abordagem de **simulação de eventos discretos**, mantendo uma lista ordenada de eventos futuros. Cada evento corresponde a uma chegada ou saída de um doente. O estado do sistema é atualizado à medida que os eventos são processados, permitindo calcular métricas de desempenho em tempo real.

Os médicos são modelados como recursos que podem estar ocupados ou livres, e a fila de espera é representada por uma estrutura de dados do tipo queue.

## Desafios e Soluções

Um dos principais desafios encontrados foi a correta modelação do comportamento estocástico do sistema, garantindo que as distribuições estatísticas utilizadas representassem adequadamente o funcionamento real de uma clínica médica. Outro desafio relevante foi a gestão eficiente dos eventos e a recolha consistente das métricas ao longo da simulação.

Estes desafios foram ultrapassados através de uma estruturação cuidada do código, testes com diferentes cenários e análise dos resultados obtidos.

## Conclusão

O desenvolvimento deste projeto permitiu aplicar conceitos fundamentais de programação, estatística e modelação de sistemas reais. Através da simulação da dinâmica de uma clínica médica, foi possível compreender o impacto de diferentes parâmetros no desempenho do sistema e desenvolver uma aplicação funcional, extensível e alinhada com os objetivos da unidade curricular.

Considera-se que os objetivos propostos foram alcançados com sucesso, tendo o projeto contribuído significativamente para o desenvolvimento de competências técnicas e analíticas essenciais na área da Engenharia Biomédica.
