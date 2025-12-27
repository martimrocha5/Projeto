import FreeSimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import manipulacao1 as mani  # Certifica-te que o ficheiro manipulacao1.py está na mesma pasta


# ==========================================
# 1. MOTOR DE SIMULAÇÃO
# ==========================================
def simula(n_medicos, taxa_h, t_medio_cons, t_simulacao, dist_tipo):
    # Conversão da taxa horária para taxa por minuto
    taxa_min = taxa_h / 60 
    
    tempo_atual = 0.0
    contadorDoentes = 1
    eventos = []      
    fila_espera = []  
    
    # Inicialização da lista de médicos conforme parâmetro
    medicos = [[f"m{i}", False, None, 0.0, 0.0] for i in range(n_medicos)]
    
    chegadas_registo = {}
    historico_fila = []      
    historico_ocupacao = []  
    tempos_espera = []       
    tempos_na_clinica = []   

    # Geração das chegadas de doentes (Processo de Poisson)
    t_aux = 0.0
    while t_aux < t_simulacao:
        d_id = f"d{contadorDoentes}"
        contadorDoentes += 1
        chegadas_registo[d_id] = t_aux
        eventos = mani.enqueue(eventos, (t_aux, "chegada", d_id))
        t_aux += mani.gera_intervalo_tempo_chegada(taxa_min)
    
    atendidos = 0

    # Ciclo de tratamento de eventos (Simulação de Eventos Discretos)
    while eventos:
        ev, eventos = mani.dequeue(eventos)
        tempo_atual = mani.e_tempo(ev)
        d_id = mani.e_doente(ev)

        # Registo de dados para análise posterior
        historico_fila.append((tempo_atual, len(fila_espera)))
        ocupados = sum(1 for m in medicos if mani.m_ocupado(m))
        historico_ocupacao.append((tempo_atual, (ocupados / n_medicos) * 100))

        if mani.e_tipo(ev) == "chegada":
            medico = mani.procuraMedico(medicos)
            if medico:
                tempos_espera.append(0)
                medico = mani.mOcupa(medico)
                medico = mani.mInicioConsulta(medico, tempo_atual)
                medico = mani.mDoenteCorrente(medico, d_id)
                t_cons = mani.gera_tempo_consulta()
                eventos = mani.enqueue(eventos, (tempo_atual + t_cons, "saída", d_id))
            else:
                fila_espera.append((d_id, tempo_atual))
        
        elif mani.e_tipo(ev) == "saída":
            atendidos += 1
            tempos_na_clinica.append(tempo_atual - chegadas_registo[d_id])
            
            for i in range(len(medicos)):
                if mani.m_doente_corrente(medicos[i]) == d_id:
                    medicos[i] = mani.mOcupa(medicos[i]) 
                    medicos[i] = mani.mDoenteCorrente(medicos[i], None)
                    medicos[i] = mani.mTempoOcupado(medicos[i], mani.m_total_tempo_ocupado(medicos[i]) + (tempo_atual - mani.m_inicio_ultima_consulta(medicos[i])))
                    
                    if fila_espera:
                        (prox_id, t_ch), fila_espera = mani.dequeue(fila_espera)
                        tempos_espera.append(tempo_atual - t_ch)
                        medicos[i] = mani.mOcupa(medicos[i])
                        medicos[i] = mani.mInicioConsulta(medicos[i], tempo_atual)
                        medicos[i] = mani.mDoenteCorrente(medicos[i], prox_id)
                        t_cons = mani.gera_tempo_consulta()
                        eventos = mani.enqueue(eventos, (tempo_atual + t_cons, "saída", prox_id))
                    break

    return {
        "atendidos": atendidos,
        "espera": np.mean(tempos_espera) if tempos_espera else 0,
        "permanencia": np.mean(tempos_na_clinica) if tempos_na_clinica else 0,
        "fila_hist": historico_fila,
        "ocupa_hist": historico_ocupacao
    }

# ==========================================
# 2. ESTUDO DE VARIAÇÃO DA TAXA
# ==========================================
def estudo_taxa_chegada(n_medicos, t_medio, t_sim, dist):
    taxas = range(10, 31, 2) 
    resultados_fila = []
    
    for t in taxas:
        res = simula(n_medicos, t, t_medio, t_sim, dist)
        media_f = np.mean([val[1] for val in res["fila_hist"]])
        resultados_fila.append(media_f)
    
    plt.figure("Estudo: Taxa de Chegada vs Fila")
    plt.plot(taxas, resultados_fila, marker='o', color='blue')
    plt.title("Relação entre Taxa de Chegada e Tamanho Médio da Fila")
    plt.xlabel("Taxa de Chegada (doentes/hora)")
    plt.ylabel("Tamanho Médio da Fila")
    plt.grid(True)
    plt.show()

# ==========================================
# 3. INTERFACE GRÁFICA (TEMA AZUL)
# ==========================================
def janela_principal():
    # Definição do tema azul para a interface
    sg.theme('DarkBlue3') 

    layout = [
        [sg.Text("Simulação de Clínica Médica", font=("Arial", 16, "bold"), text_color="white")],
        [sg.Text("Configuração do Atendimento", font=("Arial", 11, "italic"))],
        [sg.Text("Nº Médicos:"), sg.Input("3", key="-M-", size=(6,1)), 
         sg.Text("Taxa (doentes/h):"), sg.Input("10", key="-T-", size=(6,1))],
        [sg.Text("Consulta (min):"), sg.Input("15", key="-C-", size=(6,1)), 
         sg.Text("Simulação (min):"), sg.Input("480", key="-D-", size=(6,1))],
        [sg.Text("Distribuição:"), sg.Combo(["exponential", "normal", "uniform"], "exponential", key="-DIST-")],
        [sg.Button("Simular", button_color=("white", "#004C99")), 
         sg.Button("Estudo (10-30)", button_color=("white", "#004C99")), 
         sg.Button("Sair", button_color=("white", "firebrick"))],
        [sg.HorizontalSeparator()],
        [sg.Text("Estatísticas de Desempenho:", font=("Arial", 11, "bold"))],
        [sg.Multiline(size=(45, 6), key="-OUT-", disabled=True, background_color="#F0F8FF", text_color="black")],
        [sg.Button("Gráfico Fila"), sg.Button("Gráfico Ocupação")]
    ]

    window = sg.Window("Clínica Médica - Engenharia Biomédica", layout, element_justification='c')
    dados = None

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Sair"): break

        if event == "Simular":
            try:
                dados = simula(int(values["-M-"]), float(values["-T-"]), 
                               float(values["-C-"]), float(values["-D-"]), values["-DIST-"])
                txt = (f"Doentes Atendidos: {dados['atendidos']}\n"
                       f"Tempo Médio de Espera: {dados['espera']:.2f} min\n"
                       f"Tempo Médio na Clínica: {dados['permanencia']:.2f} min")
                window["-OUT-"].update(txt)
            except Exception as e: sg.popup_error(f"Erro nos dados: {e}")

        if event == "Estudo (10-30)":
            estudo_taxa_chegada(int(values["-M-"]), float(values["-C-"]), 
                                float(values["-D-"]), values["-DIST-"])

        if event == "Gráfico Fila" and dados:
            t, v = zip(*dados["fila_hist"])
            plt.figure("Evolução Temporal da Fila")
            plt.step(t, v, color="blue")
            plt.title("Evolução do Tamanho da Fila")
            plt.xlabel("Tempo (min)")
            plt.ylabel("Nº de Doentes")
            plt.show()

        if event == "Gráfico Ocupação" and dados:
            t, v = zip(*dados["ocupa_hist"])
            plt.figure("Taxa de Ocupação Médica")
            plt.plot(t, v, color='blue')
            plt.title("Evolução da Taxa de Ocupação (%)")
            plt.xlabel("Tempo (min)")
            plt.ylabel("% de Médicos Ocupados")
            plt.show()

    window.close()

if __name__ == "__main__":
    janela_principal()