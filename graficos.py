import FreeSimpleGUI as sg
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

plt.style.use("ggplot")

# =========================
# FUNÇÕES DE DESENHO
# =========================
def plot_fila_tempo(hist_fila, titulo):
    if not hist_fila or len(hist_fila) < 2:
        sg.popup_ok(f"Dados insuficientes para gerar o gráfico: {titulo}\n\n(Tente aumentar o tempo de simulação)", title="Aviso de Box")
        return
    
    tempos, valores = zip(*hist_fila)
    plt.figure(titulo, figsize=(8, 5))
    plt.step(tempos, valores, where="post")
    plt.xlabel("Tempo (min)")
    plt.ylabel("Número de Doentes")
    plt.title(titulo)
    plt.show()

def plot_ocupacao_tempo(hist_ocupa):
    if not hist_ocupa or len(hist_ocupa) < 2:
        sg.popup_ok("Dados insuficientes para gerar o gráfico de ocupação.", title="Aviso de Box")
        return

    tempos, valores = zip(*hist_ocupa)
    plt.figure("Taxa de Ocupação", figsize=(8, 5))
    plt.plot(tempos, valores)
    plt.fill_between(tempos, valores, alpha=0.3)
    plt.ylim(0, 105)
    plt.ylabel("Percentagem")
    plt.title("Evolução da Taxa de Ocupação")
    plt.show()

def plot_distribuicao_tempo(hist_fila, titulo):
    if not hist_fila or len(hist_fila) < 2:
        sg.popup_ok(f"Dados insuficientes para a distribuição: {titulo}", title="Aviso de Box")
        return

    tempos, valores = zip(*hist_fila)
    dist = {}

    for i in range(len(tempos) - 1):
        dt = tempos[i + 1] - tempos[i]
        v = valores[i]
        
        if v in dist:
            dist[v] += dt
        else:
            dist[v] = dt

    if not dist:
        sg.popup_ok(f"Não houve variação suficiente na fila para mostrar: {titulo}", title="Aviso de Box")
        return

    plt.figure(titulo, figsize=(7, 7))
    plt.pie(dist.values(), labels=[f"{k} doentes" for k in dist.keys()], autopct="%1.1f%%")
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
        if event in (sg.WIN_CLOSED, "Fechar"):
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
