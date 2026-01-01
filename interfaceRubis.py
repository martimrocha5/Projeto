# =========================
# IMPORTS
# =========================
import FreeSimpleGUI as sg
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import principal as pr

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

    win = sg.Window("Menu de Gráficos", layout, modal=True)

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

        [sg.Button("Executar Simulação"), sg.Button("Sair")],
        [sg.Text("Resultados:")],
        [sg.Multiline(size=(60, 10), key="-OUTPUT-", disabled=True)],
        [sg.Button("Abrir Menu de Gráficos", key="-GRAF-", visible=False)]
    ]

    window = sg.Window("Simulador", layout)

    dados = None
    running = True

    while running:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Sair"):
            running = False

        elif event == "Executar Simulação":
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

        elif event == "-GRAF-":
            if dados is not None:
                menu_graficos(dados)

    window.close()

# =========================
# PONTO DE ENTRADA
# =========================

if __name__ == "__main__":
    criar_interface()