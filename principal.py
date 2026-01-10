import json
import numpy as np
import manipulacao as mani
import FreeSimpleGUI as sg

# ===============================
# CONSTANTES
# ===============================
CHEGADA = "chegada"
SAIDA = "saída"

# ===============================
# CARREGAR DATASET
# ===============================
with open("pessoas.json", encoding="utf-8") as f:
    PESSOAS = json.load(f)

# Especialidades (sem ortopedia)
especialidades = ["Cardiologia", "Clínica Geral", "Pneumologia"]

# ===============================
# FUNÇÃO PRINCIPAL
# ===============================
def simula(n_medicos, taxa_chegada, tempo_medio, tempo_simulacao, distribuicao, window=None):

    mani.NUM_MEDICOS = n_medicos
    mani.TAXA_CHEGADA = taxa_chegada / 60
    mani.TEMPO_MEDIO_CONSULTA = tempo_medio
    mani.TEMPO_SIMULACAO = tempo_simulacao
    mani.DISTRIBUICAO_TEMPO_CONSULTA = distribuicao

    tempo_atual = 0.0
    queueEventos = []

    fila_espera = {esp: [] for esp in especialidades}
    medicos = mani.criarMedico(n_medicos, especialidades)

    print("\n" + "=" * 40)
    print(f"CLÍNICA ABERTA - {n_medicos} MÉDICOS")
    print("=" * 40)
    for m in medicos:
        print(f"{m[0]} -> {m[5]}")
    print("-" * 40 + "\n")

    chegadas_d = {}
    ent_consulta_d = {}
    saida_d = {}

    hist_fila = []
    hist_fila_esp = {esp: [] for esp in especialidades}
    hist_ocupa = []

    contagem_especialidades = {esp: 0 for esp in especialidades}

    indice_pessoa = 0
    t_chegada_aux = mani.gera_intervalo_tempo_chegada(mani.TAXA_CHEGADA)
    contador_eventos = 0

    # ===============================
    # GERAÇÃO DE CHEGADAS
    # ===============================
    while t_chegada_aux < tempo_simulacao:
        pessoa = PESSOAS[indice_pessoa % len(PESSOAS)]
        pessoa["especialidade"] = mani.atribuir_especialidade(pessoa)

        id_unico = f"{pessoa['id']}_{indice_pessoa}"
        chegadas_d[id_unico] = t_chegada_aux

        queueEventos = mani.enqueue(
            queueEventos,
            (t_chegada_aux, CHEGADA, (id_unico, pessoa))
        )

        t_chegada_aux += mani.gera_intervalo_tempo_chegada(mani.TAXA_CHEGADA)
        indice_pessoa += 1

    doentes_atendidos = 0

    print(f"--- INÍCIO DA SIMULAÇÃO ({tempo_simulacao} min) ---\n")

    # ===============================
    # CICLO DE EVENTOS
    # ===============================
    while queueEventos:
        evento, queueEventos = mani.dequeue(queueEventos)
        tempo_atual = evento[0]

        if tempo_atual > tempo_simulacao:
            continue

        if window:
            percentagem = (tempo_atual / tempo_simulacao) * 100
            window["-PROGRESS-"].update_bar(percentagem, 100)
            window["-PROGRESS-TEXT-"].update(f"{int(percentagem)}%")
            window.refresh()

        id_unico, dados_doente = evento[2]
        ocupados = sum(1 for m in medicos if m[1])
        hist_ocupa.append((tempo_atual, (ocupados / n_medicos) * 100))

        if evento[1] == CHEGADA:
            esp = dados_doente["especialidade"]
            msg_chegada = f"\n[{round(tempo_atual,2):6} min] Chegada: {dados_doente['nome']} ({esp})"
            print(msg_chegada)
            
            if window:
                conteudo_atual = window["-OUTPUT-"].get()
                window["-OUTPUT-"].update(conteudo_atual + msg_chegada + "\n")
                window["-OUTPUT-"].Widget.see(sg.tk.END)
                window.refresh()

            medico = mani.procuraMedico(medicos, esp)

            if medico:
                msg_atend = f"            Atendimento imediato por {medico[0]}"
                print(msg_atend)
                if window:
                    conteudo_atual = window["-OUTPUT-"].get()
                    window["-OUTPUT-"].update(conteudo_atual + msg_atend + "\n")
                    window["-OUTPUT-"].Widget.see(sg.tk.END)
                    window.refresh()
                
                medico[1] = True
                medico[2] = id_unico
                medico[4] = tempo_atual
                ent_consulta_d[id_unico] = tempo_atual
                contagem_especialidades[esp] += 1

                t_cons = mani.gera_tempo_consulta(dados_doente)
                queueEventos = mani.enqueue(queueEventos, (tempo_atual + t_cons, SAIDA, (id_unico, dados_doente)))
            else:
                fila_espera[esp].append((id_unico, dados_doente, tempo_atual))
                total_fila = sum(len(f) for f in fila_espera.values())
                hist_fila.append((tempo_atual, total_fila))
                hist_fila_esp[esp].append((tempo_atual, len(fila_espera[esp])))
                msg_fila = f"            Entrou na fila de {esp} (Tamanho: {len(fila_espera[esp])})"
                print(msg_fila)
                if window:
                    conteudo_atual = window["-OUTPUT-"].get()
                    window["-OUTPUT-"].update(conteudo_atual + msg_fila + "\n")
                    window["-OUTPUT-"].Widget.see(sg.tk.END)
                    window.refresh()

        elif evento[1] == SAIDA:
            msg_saida = f"\n[{round(tempo_atual,2):6} min] Fim consulta: {dados_doente['nome']}"
            print(msg_saida)
            if window:
                conteudo_atual = window["-OUTPUT-"].get()
                window["-OUTPUT-"].update(conteudo_atual + msg_saida + "\n")
                window["-OUTPUT-"].Widget.see(sg.tk.END)
                window.refresh()
            
            doentes_atendidos += 1
            saida_d[id_unico] = tempo_atual

            medico_idx = -1
            for i, m in enumerate(medicos):
                if m[2] == id_unico:
                    m[1] = False
                    m[3] += tempo_atual - m[4]
                    m[2] = None
                    medico_idx = i

            m = medicos[medico_idx]
            esp = m[5]
            fila_esp = fila_espera[esp]

            if fila_esp:
                p_id, p_dados, t_chegada_f = fila_esp.pop(0)
                espera = tempo_atual - t_chegada_f
                msg_chamada = f"            {m[0]} chamou {p_dados['nome']} (espera: {round(espera,1)} min)"
                print(msg_chamada)
                if window:
                    conteudo_atual = window["-OUTPUT-"].get()
                    window["-OUTPUT-"].update(conteudo_atual + msg_chamada + "\n")
                    window["-OUTPUT-"].Widget.see(sg.tk.END)
                    window.refresh()

                total_fila = sum(len(f) for f in fila_espera.values())
                hist_fila.append((tempo_atual, total_fila))
                hist_fila_esp[esp].append((tempo_atual, len(fila_esp)))

                m[1] = True
                m[2] = p_id
                m[4] = tempo_atual
                ent_consulta_d[p_id] = tempo_atual
                contagem_especialidades[esp] += 1

                t_cons = mani.gera_tempo_consulta(p_dados)
                queueEventos = mani.enqueue(queueEventos, (tempo_atual + t_cons, SAIDA, (p_id, p_dados)))
        
        contador_eventos += 1

    if window:
        window["-PROGRESS-"].update_bar(100, 100)
        window["-PROGRESS-TEXT-"].update("100%")
        window.refresh()

    # ===============================
    # ESTATÍSTICAS FINAIS
    # ===============================
    esperas = [ent_consulta_d[d] - chegadas_d[d] for d in saida_d if d in ent_consulta_d]
    totais = [saida_d[d] - chegadas_d[d] for d in saida_d]

    media_espera = np.mean(esperas) if esperas else 0
    media_clinica = np.mean(totais) if totais else 0

    total_fila_final = sum(len(f) for f in fila_espera.values())

    print("\n" + "=" * 40)
    print("RELATÓRIO FINAL DA SIMULAÇÃO")
    print("=" * 40)
    print(f"Total Doentes Atendidos: {doentes_atendidos}")
    print(f"Tempo Médio de Espera: {media_espera:.2f} min")
    print(f"Tempo Médio na Clínica: {media_clinica:.2f} min")
    print(f"Doentes que ficaram à espera: {total_fila_final}")
    print("Doentes por Especialidade:")
    for esp, qtd in contagem_especialidades.items():
        print(f"   - {esp}: {qtd}")
    print("=" * 40 + "\n")

    return {
        "total_atendidos": doentes_atendidos,
        "media_espera": media_espera,
        "media_clinica": media_clinica,
        "hist_fila": hist_fila,
        "hist_fila_esp": hist_fila_esp,
        "hist_ocupa": hist_ocupa,
        "contagem_especialidades": contagem_especialidades,
        "fila_final": total_fila_final
    }

if __name__ == "__main__":
    simula(3, 10, 15, 480, "exponential")

