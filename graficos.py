import FreeSimpleGUI as sg
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np

# Configuração global de estilo para melhor leitura
plt.style.use("ggplot")
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'lines.linewidth': 2.5
})

# =========================
# FUNÇÕES DE DESENHO
# =========================
def plot_fila_tempo(hist_fila, titulo):
    if not hist_fila or len(hist_fila) < 2:
        sg.popup_ok(f"Dados insuficientes para gerar o gráfico: {titulo}\n\n(Tente aumentar o tempo de simulação)", title="Aviso")
        return
    
    tempos, valores = zip(*hist_fila)
    
    plt.figure(titulo, figsize=(10, 6))
    
    # Plot do tipo degrau (step) com preenchimento leve por baixo
    plt.step(tempos, valores, where="post", color="#1f77b4", linewidth=2)
    plt.fill_between(tempos, valores, step="post", alpha=0.2, color="#1f77b4")
    
    plt.xlabel("Tempo de Simulação (min)")
    plt.ylabel("N.º de Doentes em Espera")
    plt.title(titulo, fontweight='bold')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

def plot_ocupacao_tempo(hist_ocupa):
    if not hist_ocupa or len(hist_ocupa) < 2:
        sg.popup_ok("Dados insuficientes para gerar o gráfico de ocupação.", title="Aviso")
        return

    tempos, valores = zip(*hist_ocupa)
    
    plt.figure("Taxa de Ocupação", figsize=(10, 6))
    
    plt.plot(tempos, valores, color="#2ca02c", linewidth=2)
    plt.fill_between(tempos, valores, alpha=0.3, color="#2ca02c")
    
    plt.ylim(0, 105) # Margem pequena acima de 100%
    plt.xlabel("Tempo de Simulação (min)")
    plt.ylabel("Ocupação dos Médicos (%)")
    plt.title("Evolução da Taxa de Ocupação", fontweight='bold')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Adicionar linha de referência nos 100%
    plt.axhline(y=100, color='r', linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    plt.show()

def plot_distribuicao_tempo(hist_fila, titulo):
    if not hist_fila or len(hist_fila) < 2:
        sg.popup_ok(f"Dados insuficientes para a distribuição: {titulo}", title="Aviso")
        return

    tempos, valores = zip(*hist_fila)
    dist = {}

    # Calcular quanto tempo a fila teve X pessoas
    for i in range(len(tempos) - 1):
        dt = tempos[i + 1] - tempos[i]
        v = valores[i]
        
        if v in dist:
            dist[v] += dt
        else:
            dist[v] = dt

    if not dist:
        sg.popup_ok(f"Não houve variação suficiente na fila para mostrar: {titulo}", title="Aviso")
        return

    # Ordenar as chaves (0 pessoas, 1 pessoa, 2 pessoas...) para o gráfico ficar lógico
    chaves_ordenadas = sorted(dist.keys())
    valores_ordenados = [dist[k] for k in chaves_ordenadas]
    labels = [f"{k} doentes" for k in chaves_ordenadas]

    # Criar figura
    fig, ax = plt.subplots(figsize=(10, 7), num=titulo)
    
    # Usar colormap viridis para distinção clara
    colors = plt.cm.viridis(np.linspace(0, 1, len(chaves_ordenadas)))

    # Gráfico circular com legenda lateral para não sobrepor texto
    wedges, texts, autotexts = ax.pie(
        valores_ordenados, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors, 
        pctdistance=0.85, # Percentagem mais para a ponta
        textprops=dict(color="black")
    )

    # Melhorar a legibilidade das percentagens
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
        autotext.set_color('white')

    ax.legend(wedges, labels,
              title="Tamanho da Fila",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.title(titulo, fontweight='bold')
    plt.tight_layout()
    plt.show()

# =========================
# MENU DE GRÁFICOS
# =========================
def menu_graficos(res):
    layout = [
        [sg.Text("Totais", font=("Arial", 11, "bold"))],
        [sg.Button("Fila Total", size=(20, 1))],
        [sg.Button("Ocupação Total", size=(20, 1))],
        [sg.Button("Distribuição Total", size=(20, 1))],
        [sg.HorizontalSeparator()],
        [sg.Text("Por Especialidade", font=("Arial", 11, "bold"))],
    ]
    
    # Criar botões dinamicamente
    for esp in res["hist_fila_esp"]:
        layout.append([sg.Button(f"Fila - {esp}", size=(25, 1))])
        layout.append([sg.Button(f"Distribuição - {esp}", size=(25, 1))])
    
    layout.append([sg.HorizontalSeparator()])
    layout.append([sg.Button("Fechar", button_color=("white", "firebrick"), size=(20, 1))])

    win = sg.Window("Menu de Gráficos", layout, modal=True, element_justification='center')
    ativo = True
    
    while ativo:
        event, _ = win.read()
        if event in (sg.WIN_CLOSED, "Fechar"):
            ativo = False
        elif event == "Fila Total":
            plot_fila_tempo(res["hist_fila"], "Evolução da Fila Total")
        elif event == "Ocupação Total":
            plot_ocupacao_tempo(res["hist_ocupa"])
        elif event == "Distribuição Total":
            plot_distribuicao_tempo(res["hist_fila"], "Distribuição do Tempo de Espera (Global)")
        elif event and event.startswith("Fila - "):
            esp = event.replace("Fila - ", "")
            plot_fila_tempo(res["hist_fila_esp"][esp], f"Evolução da Fila - {esp}")
        elif event and event.startswith("Distribuição - "):
            esp = event.replace("Distribuição - ", "")
            plot_distribuicao_tempo(res["hist_fila_esp"][esp], f"Distribuição - {esp}")
            
    win.close()