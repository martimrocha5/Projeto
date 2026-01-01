# =========================
# IMPORTS
# =========================
import FreeSimpleGUI as sg
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import principal as pr
import analisador as analise

plt.style.use("ggplot")

# =========================
# FUNÇÕES DE DESENHO
# =========================

def plot_fila_tempo(hist_fila):
    tempos, valores = zip(*hist_fila)
    plt.figure("Evolução da Fila", figsize=(8, 5))
    plt.step(tempos, valores, where="post")
    plt.title("Tamanho da Fila ao Longo do Tempo")
    plt.xlabel("Tempo (min)")
    plt.ylabel("Número de Doentes")
    plt.show()

def plot_ocupacao_tempo(hist_ocupa):
    tempos, valores = zip(*hist_ocupa)
    plt.figure("Taxa de Ocupação", figsize=(8, 5))
    plt.plot(tempos, valores)
    plt.fill_between(tempos, valores, alpha=0.3)
    plt.title("Evolução da Taxa de Ocupação")
    plt.ylabel("Percentagem")
    plt.ylim(0, 105)
    plt.show()

def plot_distribuicao_tempo(hist_fila):
    tempos, valores = zip(*hist_fila)
    dist = {}

    for i in range(len(tempos) - 1):
        dt = tempos[i + 1] - tempos[i]
        val = valores[i]
        dist[val] = dist.get(val, 0) + dt

    plt.figure("Distribuição de Tempo", figsize=(7, 7))
    plt.pie(dist.values(), labels=[f"{k} doentes" for k in dist.keys()], autopct="%1.1f%%")
    plt.title("Tempo Total em Cada Estado da Fila")
    plt.show()

# =========================
# MENU DE GRÁFICOS
# =========================

def menu_graficos(res):
    layout = [
        [sg.Text("Escolha a Visualização:")],
        [sg.Button("Evolução da Fila")],
        [sg.Button("Taxa de Ocupação")],
        [sg.Button("Distribuição de Tempo")],
        [sg.Button("Fechar")]
    ]

    win = sg.Window("Menu de Gráficos", layout, size=(350,230), modal=True)

    ativo = True
    while ativo:
        event, _ = win.read()

        if event in (sg.WIN_CLOSED, "Fechar"):
            ativo = False

        elif event == "Evolução da Fila":
            plot_fila_tempo(res["hist_fila"])

        elif event == "Taxa de Ocupação":
            plot_ocupacao_tempo(res["hist_ocupa"])

        elif event == "Distribuição de Tempo":
            plot_distribuicao_tempo(res["hist_fila"])

    win.close()

# =========================
# JANELA DE ANÁLISE
# =========================
def abrir_janela_analise():
    dados = analise.carregar_e_validar("pessoas.json")
    if not dados:
        sg.popup_error("Erro: Ficheiro pessoas.json nao encontrado.")
        return

    # 1. Obter dados do analisador
    idades = analise.estatisticas_idades(dados)
    faixas = analise.distribuir_faixas_etarias(dados)
    fumadores = analise.distribuicao_fumadores(dados)
    desportos = analise.distribuicao_desportos(dados)
    distritos = analise.distribuicao_distritos(dados)
    profs = analise.top_profissoes(dados)

    # 2. Formatar textos (Sem emojis como solicitado)
    txt_idade = f"Media: {idades['media']:.1f}\nMin: {idades['min']} | Max: {idades['max']}\n\nFaixas:\n"
    for k, v in faixas.items(): txt_idade += f"- {k}: {v}\n"

    txt_profs = "Top Profissoes:\n"
    for k, v in profs: txt_profs += f"* {k}: {v}\n"

    layout_analise = [
        [sg.Text("Painel de Analise de Dados", font=("Arial", 14, "bold"))],
        [sg.TabGroup([[
            sg.Tab("Idades", [[sg.Multiline(txt_idade, size=(45, 12), disabled=True)]]),
            sg.Tab("Fumadores", [[sg.Listbox([f"{k}: {v}" for k,v in fumadores.items()], size=(45, 12))]]),
            sg.Tab("Desportos", [[sg.Listbox([f"{k}: {v}" for k,v in desportos.items()], size=(45, 12))]]),
            sg.Tab("Distritos", [[sg.Listbox([f"{k}: {v}" for k,v in distritos.items()], size=(45, 12))]]),
            sg.Tab("Profissoes", [[sg.Multiline(txt_profs, size=(45, 12), disabled=True)]])
        ]])],
        [sg.Button("Fechar")]
    ]

    win = sg.Window("Estatisticas", layout_analise, modal=True)
    while True:
        e, _ = win.read()
        if e in (sg.WIN_CLOSED, "Fechar"): break
    win.close()

# =========================
# INTERFACE PRINCIPAL
# =========================
def criar_interface():
    sg.theme("LightBlue2")

    layout = [
        [sg.Text("Simulação de Clínica Médica", font=("Helvetica", 16, "bold"))],

        [sg.Frame("Configurações", [
            [sg.Text("Médicos:"), sg.Input("3", key="-MEDICOS-", size=(10,))],
            [sg.Text("Taxa (doentes/h):"), sg.Input("10", key="-TAXA-", size=(10,))],
            [sg.Text("Tempo Consulta (min):"), sg.Input("15", key="-TEMPO-", size=(10,))],
            [sg.Text("Duração (min):"), sg.Input("480", key="-DURACAO-", size=(10,))],
            [sg.Combo(["exponential", "normal", "uniform"],
                      default_value="exponential", key="-DIST-")]
        ])],

        [sg.Button("Executar Simulacao", button_color="green", key="-SIMULAR-"), # Adicionei uma KEY para segurança
         sg.Button("Analise de Dados", key="-BT-ANALISE-", button_color="blue"), 
         sg.Button("Sair")],
        [sg.Text("Resultados:")],
        [sg.Multiline(size=(60, 10), key="-OUTPUT-", disabled=True)],
        [sg.Button("Abrir Menu de Gráficos", key="-GRAF-", visible=False)]
    ]

    window = sg.Window("Simulador", layout)
    dados = None

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Sair"):
            break
       
        if event == "-BT-ANALISE-":
            abrir_janela_analise()

        elif event == "-SIMULAR-": # Agora usa a KEY fixa, evitando erros de acento
            try:
                dados = pr.simula(
                    n_medicos=int(values["-MEDICOS-"]),
                    taxa_chegada=float(values["-TAXA-"]),
                    tempo_medio=float(values["-TEMPO-"]),
                    tempo_simulacao=float(values["-DURACAO-"]),
                    distribuicao=values["-DIST-"]
                )

                texto = (
                    f"Atendidos: {dados['total_atendidos']}\n"
                    f"Espera média: {dados['media_espera']:.2f} min\n"
                    f"Tempo total médio: {dados['media_clinica']:.2f} min"
                )

                window["-OUTPUT-"].update(texto)
                window["-GRAF-"].update(visible=True)
            except Exception as e:
                sg.popup_error(f"Erro nos parâmetros: {e}")

        elif event == "-GRAF-":
            if dados is not None:
                menu_graficos(dados)

    window.close()

if __name__ == "__main__":
    criar_interface()