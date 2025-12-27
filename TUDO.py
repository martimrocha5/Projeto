import FreeSimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import manipulacao1 as mani # Ficheiro com enqueue, dequeue, etc. 

# ==========================================
# 1. LÓGICA DA SIMULAÇÃO (O "MOTOR")
# ==========================================
def simula(n_medicos, taxa_h, t_medio_cons, t_simulacao, dist_tipo):
    """Executa a simulação com base nos parâmetros da interface[cite: 11, 36]."""
    
    # Conversão: doentes/hora para doentes/minuto [cite: 36]
    taxa_chegada_min = taxa_h / 60 
    
    tempo_atual = 0.0
    contadorDoentes = 1
    chegadas_saidas = [] # Fila de eventos [cite: 74]
    fila_espera = []     # Fila de doentes (queue) [cite: 76, 77]
    
    # Geração da lista de médicos conforme parâmetro num_doctors [cite: 36, 79]
    medicos = [[f"m{i}", False, None, 0.0, 0.0] for i in range(n_medicos)]
    
    chegadas_d = {} # Registo de chegada para calcular tempo na clínica [cite: 83, 41]
    
    # Listas para guardar dados dos gráficos e estatísticas [cite: 14, 50]
    historico_fila = []      # 
    historico_ocupacao = []  # [cite: 52]
    tempos_espera = []       # [cite: 39]
    tempos_consulta = []     # [cite: 40]
    tempos_na_clinica = []   # [cite: 41]

    # Geração das chegadas iniciais usando distribuição de Poisson [cite: 12, 27, 85]
    tempo_aux = 0.0
    while tempo_aux < t_simulacao:
        doente_id = "d" + str(contadorDoentes)
        contadorDoentes += 1
        chegadas_d[doente_id] = tempo_aux
        chegadas_saidas = mani.enqueue(chegadas_saidas, (tempo_aux, "chegada", doente_id))
        tempo_aux += mani.gera_intervalo_tempo_chegada(taxa_chegada_min)
    
    doentes_atendidos = 0

    # Processamento dos eventos (Tratamento de eventos) [cite: 96, 98]
    while chegadas_saidas != []:
        evento, chegadas_saidas = mani.dequeue(chegadas_saidas)
        tempo_atual = mani.e_tempo(evento) 
        id_doente = mani.e_doente(evento)

        # Registo de estado para os gráficos [cite: 14, 50]
        historico_fila.append((tempo_atual, len(fila_espera)))
        medicos_ocupados = sum(1 for m in medicos if mani.m_ocupado(m))
        historico_ocupacao.append((tempo_atual, (medicos_ocupados / n_medicos) * 100))

        if mani.e_tipo(evento) == "chegada":
            medico_livre = mani.procuraMedico(medicos)
            if medico_livre:
                tempos_espera.append(0) # Atendimento imediato [cite: 28]
                medico_livre = mani.mOcupa(medico_livre) 
                medico_livre = mani.mInicioConsulta(medico_livre, tempo_atual)
                medico_livre = mani.mDoenteCorrente(medico_livre, id_doente) 
                
                # Tempo de consulta aleatório (Exponencial, Normal ou Uniforme) [cite: 13, 30]
                t_cons = mani.gera_tempo_consulta() 
                tempos_consulta.append(t_cons)
                chegadas_saidas = mani.enqueue(chegadas_saidas, (tempo_atual + t_cons, "saída", id_doente))
            else:
                fila_espera.append((id_doente, tempo_atual)) # Vai para a fila de espera [cite: 29]
        
        elif mani.e_tipo(evento) == "saída":
            doentes_atendidos += 1
            # Cálculo do tempo médio na clínica [cite: 41, 47]
            tempos_na_clinica.append(tempo_atual - chegadas_d[id_doente])
            
            # Libertar o médico que terminou a consulta [cite: 122, 126]
            for i in range(len(medicos)):
                if mani.m_doente_corrente(medicos[i]) == id_doente:
                    medicos[i] = mani.mOcupa(medicos[i]) # Médico fica livre [cite: 129]
                    medicos[i] = mani.mDoenteCorrente(medicos[i], None)
                    # Incrementa tempo total de ocupação [cite: 131, 132]
                    medicos[i] = mani.mTempoOcupado(medicos[i], mani.m_total_tempo_ocupado(medicos[i]) + (tempo_atual - mani.m_inicio_ultima_consulta(medicos[i])))
                    
                    # Se houver doentes à espera, ocupa o médico imediatamente [cite: 138, 139]
                    if fila_espera != []:
                        (prox_id, t_cheg), fila_espera = mani.dequeue(fila_espera)
                        tempos_espera.append(tempo_atual - t_cheg) # Tempo médio de espera [cite: 39]
                        medicos[i] = mani.mOcupa(medicos[i]) 
                        medicos[i] = mani.mInicioConsulta(medicos[i], tempo_atual)
                        medicos[i] = mani.mDoenteCorrente(medicos[i], prox_id)
                        t_cons = mani.gera_tempo_consulta()
                        tempos_consulta.append(t_cons)
                        chegadas_saidas = mani.enqueue(chegadas_saidas, (tempo_atual + t_cons, "saída", prox_id))
                    break

    # Retorna dicionário com todos os indicadores esperados [cite: 37, 38]
    return {
        "total_atendidos": doentes_atendidos, # [cite: 44]
        "media_espera": np.mean(tempos_espera) if tempos_espera else 0, # [cite: 39]
        "media_consulta": np.mean(tempos_consulta) if tempos_consulta else 0, # [cite: 40]
        "media_clinica": np.mean(tempos_na_clinica) if tempos_na_clinica else 0, # [cite: 41]
        "hist_fila": historico_fila, # 
        "hist_ocupa": historico_ocupacao # [cite: 52]
    }

# ==========================================
# 2. INTERFACE GRÁFICA (FreeSimpleGUI)
# ==========================================
def interface_clinica():
    """Implementa a interface gráfica pedida[cite: 55, 56]."""
    sg.theme('Default1')

    # Layout para alteração de parâmetros [cite: 58, 36]
    layout = [
        [sg.Text("Simulação de Clínica Médica", font=("Helvetica", 14, "bold"))],
        [sg.Text("Nº Médicos:"), sg.Input("3", key="-MEDICOS-", size=(8,1))],
        [sg.Text("Taxa Chegada (doentes/h):"), sg.Input("10", key="-TAXA-", size=(8,1))],
        [sg.Text("Tempo Consulta Médio (min):"), sg.Input("15", key="-CONSULTA-", size=(8,1))],
        [sg.Text("Duração Simulação (min):"), sg.Input("480", key="-DURACAO-", size=(8,1))],
        [sg.Text("Distribuição:"), sg.Combo(["exponential", "normal", "uniform"], "exponential", key="-DIST-")],
        [sg.Button("Executar Simulação"), sg.Button("Sair")], # [cite: 57]
        [sg.HorizontalSeparator()],
        [sg.Text("Resultados Estatísticos:", font=("Helvetica", 11, "bold"))],
        [sg.Multiline(size=(45, 6), key="-OUT-", disabled=True)],
        [sg.Button("Gráfico Fila"), sg.Button("Gráfico Ocupação")] # [cite: 59]
    ]

    window = sg.Window("Projeto Clínica - ATP", layout)
    resultados_atuais = None

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Sair"): break

        if event == "Executar Simulação":
            try:
                # Chama a função simula com os valores da interface [cite: 57, 58]
                res = simula(
                    int(values["-MEDICOS-"]),
                    float(values["-TAXA-"]),
                    float(values["-CONSULTA-"]),
                    float(values["-DURACAO-"]),
                    values["-DIST-"]
                )
                resultados_atuais = res
                
                # Exibe os indicadores no ecrã [cite: 38-44]
                texto = (f"Doentes Atendidos: {res['total_atendidos']}\n"
                         f"Espera Média: {res['media_espera']:.2f} min\n"
                         f"Tempo Médio Consulta: {res['media_consulta']:.2f} min\n"
                         f"Permanência Média: {res['media_clinica']:.2f} min")
                window["-OUT-"].update(texto)
                sg.popup("Simulação Concluída!")
            except Exception as e:
                sg.popup_error(f"Erro nos parâmetros: {e}")

        # Visualização dos gráficos pedidos [cite: 59, 51, 52]
        if event == "Gráfico Fila" and resultados_atuais:
            t, v = zip(*resultados_atuais["hist_fila"])
            plt.figure("Evolução da Fila")
            plt.step(t, v, where='post')
            plt.xlabel("Tempo (min)")
            plt.ylabel("Nº Doentes")
            plt.show()

        if event == "Gráfico Ocupação" and resultados_atuais:
            t, v = zip(*resultados_atuais["hist_ocupa"])
            plt.figure("Taxa de Ocupação")
            plt.plot(t, v, color='red')
            plt.xlabel("Tempo (min)")
            plt.ylabel("% Ocupação")
            plt.show()

    window.close()

if __name__ == "__main__":
    interface_clinica()