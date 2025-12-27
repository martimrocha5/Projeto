import PySimpleGUI as sg
import matplotlib.pyplot as plt

def criar_interface():
    # Definição do Layout [cite: 36, 56]
    layout = [
        [sg.Text("Simulação de Clínica Médica", font=("Helvetica", 16))],
        [sg.Text("Número de Médicos:"), sg.InputText("3", key="-MEDICOS-")],
        [sg.Text("Taxa de Chegada (doentes/h):"), sg.InputText("10", key="-TAXA-")],
        [sg.Text("Tempo Médio Consulta (min):"), sg.InputText("15", key="-TEMPO-")],
        [sg.Text("Duração Simulação (min):"), sg.InputText("480", key="-DURACAO-")],
        [sg.Text("Distribuição:"), 
         sg.Combo(["exponential", "normal", "uniform"], default_value="exponential", key="-DIST-")],
        [sg.Button("Executar Simulação"), sg.Button("Sair")],
        [sg.HorizontalSeparator()],
        [sg.Text("Resultados:", font=("Helvetica", 12))],
        [sg.Multiline(size=(45, 5), key="-OUTPUT-", echo_stdout_stderr=False)]
    ]

    window = sg.Window("Clínica Médica - Projeto", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Sair"):
            break
        
        if event == "Executar Simulação":
            try:
                # Ler valores da interface 
                res = simula(
                    n_medicos=int(values["-MEDICOS-"]),
                    taxa_chegada=float(values["-TAXA-"]),
                    tempo_medio=float(values["-TEMPO-"]),
                    tempo_simulacao=float(values["-DURACAO-"]),
                    distribuicao=values["-DIST-"]
                )
                
                # Mostrar resultados no Multiline [cite: 39, 43, 44]
                out = f"Doentes atendidos: {res['total_atendidos']}\n"
                out += f"Tempo médio espera: {res['media_espera']:.2f} min\n"
                out += f"Tempo médio na clínica: {res['media_clinica']:.2f} min"
                window["-OUTPUT-"].update(out)
                
                # Gerar gráficos 
                gerar_graficos(res["hist_fila"], res["hist_ocupa"])
                
            except Exception as e:
                sg.popup_error(f"Erro nos parâmetros: {e}")

    window.close()

def gerar_graficos(hist_fila, hist_ocupa):
    # Gráfico da Fila [cite: 51]
    tempos_f, valores_f = zip(*hist_fila)
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.step(tempos_f, valores_f, where='post')
    plt.title("Evolução da Fila de Espera")
    plt.xlabel("Tempo (min)")
    plt.ylabel("Doentes na Fila")

    # Gráfico de Ocupação [cite: 52]
    tempos_o, valores_o = zip(*hist_ocupa)
    plt.subplot(1, 2, 2)
    plt.plot(tempos_o, valores_o, color='orange')
    plt.title("Taxa de Ocupação dos Médicos")
    plt.xlabel("Tempo (min)")
    plt.ylabel("% Ocupação")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    criar_interface()