import FreeSimpleGUI as sg
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import principal as pr
import analisador as analise

plt.style.use("ggplot")

# =========================
# FUNÇÕES DE VALIDAÇÃO
# =========================
def validar_float(valor, nome):
    if valor.strip() == "":
        sg.popup_error(f"O campo '{nome}' está vazio.")
        return None
    try:
        v = float(valor)
        if v < 0:
            sg.popup_error(f"O campo '{nome}' não pode ser negativo.")
            return None
        return v
    except ValueError:
        sg.popup_error(f"O campo '{nome}' tem de ser um número.")
        return None

def validar_int(valor, nome):
    if valor.strip() == "":
        sg.popup_error(f"O campo '{nome}' está vazio.")
        return None
    try:
        v = int(valor)
        if v < 0:
            sg.popup_error(f"O campo '{nome}' não pode ser negativo.")
            return None
        return v
    except ValueError:
        sg.popup_error(f"O campo '{nome}' tem de ser um número inteiro.")
        return None

# =========================
# FUNÇÕES DE DESENHO (COM PROTEÇÃO 🛡️)
# =========================

def plot_fila_tempo(hist_fila, titulo):
    # --- VERIFICAÇÃO DE SEGURANÇA ---
    if not hist_fila or len(hist_fila) < 2:
        sg.popup_ok(f"Dados insuficientes para gerar o gráfico: {titulo}\n\n(Tente aumentar o tempo de simulação)", title="Aviso de Box")
        return
    # --------------------------------
    
    tempos, valores = zip(*hist_fila)
    plt.figure(titulo, figsize=(8, 5))


    plt.step(tempos, valores, where="post")
    plt.xlabel("Tempo (min)")
    plt.ylabel("Número de Doentes")
    plt.title(titulo)
    plt.show()

def plot_ocupacao_tempo(hist_ocupa):
    # --- VERIFICAÇÃO DE SEGURANÇA ---
    if not hist_ocupa or len(hist_ocupa) < 2:
        sg.popup_ok("Dados insuficientes para gerar o gráfico de ocupação.", title="Aviso de Box")
        return
    # --------------------------------

    tempos, valores = zip(*hist_ocupa)
    plt.figure("Taxa de Ocupação", figsize=(8, 5))
    plt.plot(tempos, valores)
    plt.fill_between(tempos, valores, alpha=0.3)
    plt.ylim(0, 105)
    plt.ylabel("Percentagem")
    plt.title("Evolução da Taxa de Ocupação")
    plt.show()

def plot_distribuicao_tempo(hist_fila, titulo):
    # --- VERIFICAÇÃO DE SEGURANÇA 1 ---
    if not hist_fila or len(hist_fila) < 2:
        sg.popup_ok(f"Dados insuficientes para a distribuição: {titulo}", title="Aviso de Box")
        return
    # ----------------------------------

    tempos, valores = zip(*hist_fila)
    dist = {}

    for i in range(len(tempos) - 1):
        dt = tempos[i + 1] - tempos[i]
        v = valores[i]
        
        if v in dist:
            dist[v] += dt
        else:
            dist[v] = dt

    # --- VERIFICAÇÃO DE SEGURANÇA 2 ---
    if not dist:
        sg.popup_ok(f"Não houve variação suficiente na fila para mostrar: {titulo}", title="Aviso de Box")
        return
    # ----------------------------------

    plt.figure(titulo, figsize=(7, 7))
    plt.pie(
        dist.values(),
        labels=[f"{k} doentes" for k in dist.keys()],
        autopct="%1.1f%%"
    )
    plt.title(titulo)
    plt.show()

# =========================
# MENU DE GRÁFICOS
# =========================

def menu_graficos(res):

    layout = [
        [sg.Text("Totais", font=("Arial", 11, "bold"))],
        [sg.Button("Fila Total")],
        [sg.Button("Ocupação Total")],
        [sg.Button("Distribuição Total")],
        [sg.HorizontalSeparator()],
        [sg.Text("Por Especialidade", font=("Arial", 11, "bold"))],
    ]

    for esp in res["hist_fila_esp"]:
        layout.append([sg.Button(f"Fila - {esp}")])
        layout.append([sg.Button(f"Distribuição - {esp}")])

    layout.append([sg.Button("Fechar")])

    win = sg.Window("Menu de Gráficos", layout, modal=True, size=(380, 520))

    ativo = True
    while ativo:
        event, _ = win.read()

        if event in (sg.WIN_CLOSED, "-SAIR-"):
            ativo = False

        elif event == "Fila Total":
            plot_fila_tempo(res["hist_fila"], "Fila Total")

        elif event == "Ocupação Total":
            plot_ocupacao_tempo(res["hist_ocupa"])

        elif event == "Distribuição Total":
            plot_distribuicao_tempo(res["hist_fila"], "Distribuição Total")

        elif event.startswith("Fila - "):
            esp = event.replace("Fila - ", "")
            plot_fila_tempo(res["hist_fila_esp"][esp], f"Fila - {esp}")

        elif event.startswith("Distribuição - "):
            esp = event.replace("Distribuição - ", "")
            plot_distribuicao_tempo(res["hist_fila_esp"][esp], f"Distribuição - {esp}")

    win.close()

# =========================
# JANELA DE ANÁLISE
# =========================

def abrir_janela_analise():
    try:
        dados = analise.carregar_e_validar("pessoas.json")

        idades = analise.estatisticas_idades(dados)
        faixas = analise.distribuir_faixas_etarias(dados)
        fumadores = analise.distribuicao_fumadores(dados)
        desportos = analise.distribuicao_desportos(dados)
        distritos = analise.distribuicao_distritos(dados)
        profs = analise.top_profissoes(dados)

        txt_idade = (
            f"Media: {idades['media']:.1f}\n"
            f"Min: {idades['min']} | Max: {idades['max']}\n\nFaixas:\n"
        )
        for k, v in faixas.items():
            txt_idade += f"- {k}: {v}\n"

        txt_profs = "Top Profissoes:\n"
        for k, v in profs:
            txt_profs += f"* {k}: {v}\n"

        layout = [
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

        win = sg.Window("Estatisticas", layout, modal=True)

        ativo = True
        while ativo:
            e, _ = win.read()
            if e in (sg.WIN_CLOSED, "Fechar"):
                ativo = False

        win.close()
    except Exception as e:
        sg.popup_error(f"Erro ao carregar análise: {e}")

# =========================
# INTERFACE PRINCIPAL
# =========================

def criar_interface():

    sg.theme("LightBlue2")

    layout_config = [
        [sg.Text("Configurações", font=("Helvetica", 16, "bold"))],

        [sg.Text("Médicos:", size=(20,1), font=("Helvetica", 14)),
         sg.Input("3", key="-MEDICOS-", size=(10,), font=("Helvetica", 13))],

        [sg.Text("Taxa (doentes/h):", size=(20,1), font=("Helvetica", 14)),
         sg.Input("10", key="-TAXA-", size=(10,), font=("Helvetica", 13))],

        [sg.Text("Tempo de Consulta (min):", size=(20,1), font=("Helvetica", 14)),
         sg.Input("15", key="-TEMPO-", size=(10,), font=("Helvetica", 13))],

        [sg.Text("Duração da Simulação (min):", size=(20,1), font=("Helvetica", 14)),
         sg.Input("480", key="-DURACAO-", size=(10,), font=("Helvetica", 13))],

        [sg.Text("Distribuição:", size=(20,1), font=("Helvetica", 14)),
         sg.Combo(
             ["exponential", "normal", "uniform"],
             default_value="exponential",
             key="-DIST-",
             readonly=True,
             font=("Helvetica", 13)
         )]
    ]

    layout_botoes = [
        [
            sg.Button("Executar Simulação", key="-SIMULAR-", size=(18,2),
                      font=("Helvetica", 13), button_color=("white","green")),

            sg.Button("Análise de Dados", key="-BT-ANALISE-", size=(18,2),
                      font=("Helvetica", 13), button_color=("white","blue")),

            sg.Button("Sair", key="Sair", size=(18,2),
                      font=("Helvetica", 13), button_color=("white","firebrick"))
        ]
    ]

    layout_resultados = [
        [sg.Text("Resultados da Simulação", font=("Helvetica", 16, "bold"))],
        [sg.ProgressBar(100, orientation='h', size=(50, 20), key="-PROGRESS-", 
                       bar_color=("green", "#f0f0f0"))],
        [sg.Text("0%", key="-PROGRESS-TEXT-", font=("Helvetica", 10))],
        [
            sg.Column([
                [sg.Multiline(
                    size=(150, 30),
                    key="-OUTPUT-",
                    disabled=True,
                    font=("Courier New", 10),
                    background_color="#f0f0f0"
                )]
            ]),
            sg.Column([
                [sg.Button("Abrir Menu de\nGráficos", key="-GRAF-", visible=False,
                          font=("Helvetica", 11), size=(15, 3),
                          button_color=("white", "orange"))],
                [sg.Text(" " * 20)]
            ], vertical_alignment="top")
        ]
    ]

    layout = [
        [sg.Column([
            [sg.Text("Simulação de Clínica Médica",
                     font=("Helvetica", 22, "bold"))],

            [sg.HorizontalSeparator()],

            [sg.Column(layout_config, pad=(0,15))],

            [sg.HorizontalSeparator()],

            [sg.Column(layout_botoes, justification="center")],

            [sg.HorizontalSeparator()],

            [sg.Column(layout_resultados, pad=(0,15))]
        ],
        justification="center",
        expand_x=True,
        expand_y=True)]
    ]

    window = sg.Window(
        "Simulador",
        layout,
        resizable=True,
        finalize=True
    )

    window.maximize()

    dados = None

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Sair"):
            break

        elif event == "-BT-ANALISE-":
            abrir_janela_analise()

        elif event == "-SIMULAR-":

            n_medicos = validar_int(values["-MEDICOS-"], "Médicos")
            taxa = validar_float(values["-TAXA-"], "Taxa (doentes/h)")
            tempo = validar_float(values["-TEMPO-"], "Tempo Consulta (min)")
            duracao = validar_float(values["-DURACAO-"], "Duração (min)")

            if None in (n_medicos, taxa, tempo, duracao):
                continue

            # Limpar output anterior
            window["-OUTPUT-"].update("")
            window.refresh()

            def adicionar_evento(msg):
                """Callback para adicionar eventos ao output"""
                conteudo_atual = window["-OUTPUT-"].get()
                window["-OUTPUT-"].update(conteudo_atual + msg)
                # Fazer scroll para o final
                window["-OUTPUT-"].Widget.see(sg.tk.END)
                window.refresh()

            def atualizar_progresso(percentagem):
                """Callback para atualizar barra de progresso"""
                window["-PROGRESS-"].update_bar(percentagem, 100)
                window["-PROGRESS-TEXT-"].update(f"{int(percentagem)}%")
                window.refresh()

            dados = pr.simula(
                n_medicos,
                taxa,
                tempo,
                duracao,
                values["-DIST-"],
                callback_evento=adicionar_evento,
                callback_progresso=atualizar_progresso
            )

            # Adicionar resumo final
            resumo = (
                "\n" + "=" * 50 + "\n"
                f"✅ Total de Doentes Atendidos: {dados['total_atendidos']}\n"
                f"⏱️  Tempo Médio de Espera: {dados['media_espera']:.2f} min\n"
                f"🏥 Tempo Médio na Clínica: {dados['media_clinica']:.2f} min\n"
                f"⏳ Doentes que ficaram à espera: {dados['fila_final']}\n"
                "📌 Doentes por Especialidade:\n"
            )
            
            for esp, qtd in dados["contagem_especialidades"].items():
                resumo += f"   - {esp}: {qtd}\n"
            
            resumo += "=" * 50

            conteudo_atual = window["-OUTPUT-"].get()
            window["-OUTPUT-"].update(conteudo_atual + resumo)
            window["-GRAF-"].update(visible=True)

        elif event == "-GRAF-" and dados:
            menu_graficos(dados)

    window.close()


if __name__ == "__main__":
    criar_interface()