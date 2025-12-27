import FreeSimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np
import principal as pr

# Configuração para Matplotlib não bloquear a execução
plt.style.use('ggplot')

def criar_interface():
    sg.theme('LightBlue2')
    
    layout = [
        [sg.Text("🏥 Simulação de Clínica Médica", font=("Helvetica", 18, "bold"))],
        [sg.Frame("Parâmetros", [
            [sg.Text("Número de Médicos:"), sg.Push(), sg.InputText("3", key="-MEDICOS-", size=(10,1))],
            [sg.Text("Taxa de Chegada (doentes/h):"), sg.Push(), sg.InputText("10", key="-TAXA-", size=(10,1))],
            [sg.Text("Tempo Médio Consulta (min):"), sg.Push(), sg.InputText("15", key="-TEMPO-", size=(10,1))],
            [sg.Text("Duração Simulação (min):"), sg.Push(), sg.InputText("480", key="-DURACAO-", size=(10,1))],
            [sg.Text("Distribuição:"), sg.Push(), 
             sg.Combo(["exponential", "normal", "uniform"], default_value="exponential", key="-DIST-", size=(10,1))]
        ])],
        [sg.Button("Executar Simulação", size=(20,1), button_color=('white', '#B81C21')), sg.Button("Sair", size=(10,1))],
        [sg.HorizontalSeparator()],
        [sg.Text("Resultados:", font=("Helvetica", 12, "bold"))],
        [sg.Multiline(size=(50, 6), key="-OUTPUT-", font=("Consolas", 10), disabled=True)]
    ]

    window = sg.Window("Engenharia Biomédica - Simulação", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Sair"):
            break
        
        if event == "Executar Simulação":
            try:
                # Validar inputs básicos
                if int(values["-MEDICOS-"]) <= 0: raise ValueError("Nº médicos deve ser > 0")

                # Correr a simulação
                res = pr.simula(
                    n_medicos=int(values["-MEDICOS-"]),
                    taxa_chegada=float(values["-TAXA-"]),
                    tempo_medio=float(values["-TEMPO-"]),
                    tempo_simulacao=float(values["-DURACAO-"]),
                    distribuicao=values["-DIST-"]
                )
                
                # Mostrar resultados
                out = f"📊 RESULTADOS FINAIS:\n"
                out += f"-"*30 + "\n"
                out += f"Doentes atendidos:   {res['total_atendidos']}\n"
                out += f"Tempo médio espera:  {res['media_espera']:.2f} min\n"
                out += f"Tempo médio clínica: {res['media_clinica']:.2f} min"
                window["-OUTPUT-"].update(out)
                
                # Gerar gráficos se houver dados
                if res["hist_fila"]:
                    gerar_graficos(res["hist_fila"], res["hist_ocupa"])
                else:
                    sg.popup("Simulação correu, mas não gerou dados suficientes para gráficos.")
                
            except ValueError as ve:
                 sg.popup_error(f"Erro nos valores: Verifica se são números.\nDetalhe: {ve}")
            except Exception as e:
                sg.popup_error(f"Erro inesperado: {e}")

    window.close()

def gerar_graficos(hist_fila, hist_ocupa):
    if not hist_fila or len(hist_fila) < 2:
        return

    # Função auxiliar para só mostrar % se a fatia for relevante (> 4%)
    def filter_autopct(pct):
        return f'{pct:.1f}%' if pct > 4 else ''

    fig, axs = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle('Dashboard de Simulação - Clínica Médica', fontsize=16)

    # === LINHA 1: FILA ===
    tempos_f, valores_f = zip(*hist_fila)
    
    # 1.1 Step
    axs[0, 0].step(tempos_f, valores_f, where='post', color='tab:blue')
    axs[0, 0].set_title("Evolução Temporal")
    axs[0, 0].set_ylabel("Pessoas na Fila")
    axs[0, 0].grid(True, alpha=0.3)

    # 1.2 Barras
    axs[0, 1].bar(tempos_f, valores_f, width=1.0, color='tab:blue', alpha=0.6)
    axs[0, 1].set_title("Eventos de Fila")

    # 1.3 Pie Chart (Fila) - CORRIGIDO
    dist_fila = {}
    for i in range(len(tempos_f) - 1):
        delta_t = tempos_f[i+1] - tempos_f[i]
        val = valores_f[i]
        dist_fila[val] = dist_fila.get(val, 0) + delta_t
    
    labels_f = [f"{k} pess." for k in dist_fila.keys()]
    sizes_f = list(dist_fila.values())
    
    # Pie chart sem labels externas, com legenda
    wedges, texts, autotexts = axs[0, 2].pie(sizes_f, autopct=filter_autopct, 
                                             startangle=90, colors=plt.cm.Blues(np.linspace(0.3, 0.9, len(sizes_f))))
    axs[0, 2].set_title("% Tempo por Tamanho de Fila")
    # Legenda deslocada para não tapar o gráfico
    axs[0, 2].legend(wedges, labels_f, title="Tamanho", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # === LINHA 2: OCUPAÇÃO ===
    if hist_ocupa and len(hist_ocupa) > 1:
        tempos_o, valores_o = zip(*hist_ocupa)

        # 2.1 Linha
        axs[1, 0].plot(tempos_o, valores_o, color='tab:red')
        axs[1, 0].fill_between(tempos_o, valores_o, color='tab:red', alpha=0.1)
        axs[1, 0].set_title("Taxa de Ocupação")
        axs[1, 0].set_ylabel("% Ocupação")
        axs[1, 0].set_ylim(0, 105)
        axs[1, 0].grid(True, alpha=0.3)

        # 2.2 Barras
        axs[1, 1].bar(tempos_o, valores_o, width=1.0, color='tab:red', alpha=0.6)
        axs[1, 1].set_title("Instantes de Ocupação")

        # 2.3 Pie Chart (Ocupação) - CORRIGIDO
        dist_ocupa = {}
        for i in range(len(tempos_o) - 1):
            delta_t = tempos_o[i+1] - tempos_o[i]
            val = round(valores_o[i], 1)
            dist_ocupa[val] = dist_ocupa.get(val, 0) + delta_t

        labels_o = [f"{k}% Ocup." for k in dist_ocupa.keys()]
        sizes_o = list(dist_ocupa.values())

        wedges2, texts2, autotexts2 = axs[1, 2].pie(sizes_o, autopct=filter_autopct, 
                                                    startangle=90, colors=plt.cm.Reds(np.linspace(0.3, 0.9, len(sizes_o))))
        axs[1, 2].set_title("% Tempo por Nível de Ocupação")
        axs[1, 2].legend(wedges2, labels_o, title="Nível", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    criar_interface()