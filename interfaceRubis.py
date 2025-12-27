# =========================
# IMPORTS
# =========================
import FreeSimpleGUI as sg

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
import principal as pr

plt.style.use("ggplot")

# =========================
# FUNÇÕES AUXILIARES
# =========================
def filter_autopct(pct):
    if pct > 4:
        return f"{pct:.1f}%"
    return ""

# =========================
# GRÁFICOS
# =========================
def gerar_graficos(hist_fila, hist_ocupa):

    if len(hist_fila) < 2:
        return

    fig, axs = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle("Dashboard de Simulação - Clínica Médica", fontsize=16)

    # ---------- FILA ----------
    tempos_f, valores_f = zip(*hist_fila)

    axs[0, 0].step(tempos_f, valores_f, where="post")
    axs[0, 0].set_title("Evolução da Fila")
    axs[0, 0].set_ylabel("Pessoas")

    axs[0, 1].bar(tempos_f, valores_f, width=1)
    axs[0, 1].set_title("Eventos da Fila")

    dist_fila = {}
    for i in range(len(tempos_f) - 1):
        dt = tempos_f[i+1] - tempos_f[i]
        val = valores_f[i]
        dist_fila[val] = dist_fila.get(val, 0) + dt

    labels_f = [f"{k} pessoas" for k in dist_fila.keys()]
    sizes_f = list(dist_fila.values())

    wedges, _, _ = axs[0, 2].pie(
        sizes_f,
        autopct=filter_autopct,
        startangle=90
    )
    axs[0, 2].set_title("% Tempo por tamanho da fila")
    axs[0, 2].legend(wedges, labels_f)

    # ---------- OCUPAÇÃO ----------
    if len(hist_ocupa) > 1:
        tempos_o, valores_o = zip(*hist_ocupa)

        axs[1, 0].plot(tempos_o, valores_o)
        axs[1, 0].set_title("Taxa de Ocupação")
        axs[1, 0].set_ylabel("%")
        axs[1, 0].set_ylim(0, 100)

        axs[1, 1].bar(tempos_o, valores_o, width=1)
        axs[1, 1].set_title("Eventos de Ocupação")

        dist_ocupa = {}
        for i in range(len(tempos_o) - 1):
            dt = tempos_o[i+1] - tempos_o[i]
            val = round(valores_o[i], 1)
            dist_ocupa[val] = dist_ocupa.get(val, 0) + dt

        labels_o = [f"{k}%" for k in dist_ocupa.keys()]
        sizes_o = list(dist_ocupa.values())

        wedges2, _, _ = axs[1, 2].pie(
            sizes_o,
            autopct=filter_autopct,
            startangle=90
        )
        axs[1, 2].set_title("% Tempo por ocupação")
        axs[1, 2].legend(wedges2, labels_o)

    plt.tight_layout()
    plt.show()

# =========================
# INTERFACE
# =========================
def criar_interface():

    sg.theme("LightBlue2")

    layout = [
        [sg.Text("🏥 Simulação de Clínica Médica", font=("Helvetica", 18, "bold"))],

        [sg.Frame("Parâmetros", [
            [sg.Text("Número de Médicos:"), sg.Input("3", key="-MEDICOS-")],
            [sg.Text("Taxa de Chegada (doentes/h):"), sg.Input("10", key="-TAXA-")],
            [sg.Text("Tempo Médio Consulta (min):"), sg.Input("15", key="-TEMPO-")],
            [sg.Text("Duração Simulação (min):"), sg.Input("480", key="-DURACAO-")],
            [sg.Text("Distribuição:"),
             sg.Combo(["exponential", "normal", "uniform"],
                      default_value="exponential",
                      key="-DIST-")]
        ])],

        [sg.Button("Executar Simulação"), sg.Button("Sair")],
        [sg.HorizontalSeparator()],
        [sg.Text("Resultados:")],
        [sg.Multiline(size=(50, 6), key="-OUTPUT-", disabled=True)]
    ]

    window = sg.Window("Clínica Médica", layout)

    running = True

    while running:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Sair"):
            running = False

        elif event == "Executar Simulação":

            res = pr.simula(
                n_medicos=int(values["-MEDICOS-"]),
                taxa_chegada=float(values["-TAXA-"]),
                tempo_medio=float(values["-TEMPO-"]),
                tempo_simulacao=float(values["-DURACAO-"]),
                distribuicao=values["-DIST-"]
            )

            output = (
                "📊 RESULTADOS\n"
                "-------------------------\n"
                f"Doentes atendidos: {res['total_atendidos']}\n"
                f"Tempo médio espera: {res['media_espera']:.2f} min\n"
                f"Tempo médio clínica: {res['media_clinica']:.2f} min"
            )

            window["-OUTPUT-"].update(output)
            gerar_graficos(res["hist_fila"], res["hist_ocupa"])

    window.close()



# =========================
# PONTO DE ENTRADA
# =========================
if __name__ == "__main__":
    criar_interface()
