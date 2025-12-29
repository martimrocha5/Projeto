import json
import numpy as np
import manipulacao1 as mani

# Constantes para legibilidade
CHEGADA = "chegada"
SAIDA = "saída"

# ===============================
# CARREGAR DATASET 
# ===============================

with open("pessoas.json", encoding="utf-8") as f:
    PESSOAS = json.load(f)

def simula(n_medicos, taxa_chegada, tempo_medio, tempo_simulacao, distribuicao):
    # 1. ATUALIZAR PARÂMETROS NO MOTOR
    mani.NUM_MEDICOS = n_medicos
    mani.TAXA_CHEGADA = taxa_chegada / 60  
    mani.TEMPO_MEDIO_CONSULTA = tempo_medio
    mani.TEMPO_SIMULACAO = tempo_simulacao
    mani.DISTRIBUICAO_TEMPO_CONSULTA = distribuicao
    
    tempo_atual = 0.0
    queueEventos = []
    fila_espera = [] 

    medicos = [[f"m{i}", False, None, 0.0, 0.0] for i in range(n_medicos)]

    chegadas_d = {}
    ent_consulta_d = {}
    saida_d = {}
    
    tamanho_fila_hist = []     
    tempo_fila_hist = [] 
    hist_ocupa = []

    indice_pessoa = 0
    t_chegada_aux = mani.gera_intervalo_tempo_chegada(mani.TAXA_CHEGADA)
    
    # --- GERAÇÃO DE CHEGADAS ---
    while t_chegada_aux < tempo_simulacao:
        
        pessoa = PESSOAS[indice_pessoa % len(PESSOAS)]
        id_unico = f"{pessoa['id']}_{indice_pessoa}" 
        
        chegadas_d[id_unico] = t_chegada_aux

        queueEventos = mani.enqueue(queueEventos, (t_chegada_aux, CHEGADA, (id_unico, pessoa)))
        
        t_chegada_aux += mani.gera_intervalo_tempo_chegada(mani.TAXA_CHEGADA)
        indice_pessoa += 1

    doentes_atendidos = 0
    print(f"\n--- INÍCIO DA SIMULAÇÃO ({tempo_simulacao} min) ---")

    while queueEventos:
        evento, queueEventos = mani.dequeue(queueEventos)
        tempo_atual = evento[0]
        id_unico, dados_doente = evento[2]

        ocupados = sum(1 for m in medicos if m[1])
        hist_ocupa.append((tempo_atual, (ocupados / n_medicos) * 100))

        if evento[1] == CHEGADA:
            print(f"\n{round(tempo_atual, 2)} min | Chegada: {dados_doente['nome']} ({dados_doente['idade']} anos)")
            medico = mani.procuraMedico(medicos)
            
            if medico:
                print(f"   ✔ Médico {medico[0]} livre -> Atendimento imediato")
                medico[1] = True 
                medico[2] = id_unico
                medico[4] = tempo_atual
                ent_consulta_d[id_unico] = tempo_atual
                
                t_cons = mani.gera_tempo_consulta(dados_doente)
                print(f"Consulta prevista: {round(t_cons, 2)} min")
                
                queueEventos = mani.enqueue(queueEventos, (tempo_atual + t_cons, SAIDA, (id_unico, dados_doente)))
            else:
                fila_espera.append((id_unico, dados_doente, tempo_atual))
                print(f"Todos ocupados -> {dados_doente['nome']} entrou na fila (Tamanho: {len(fila_espera)})")
                tamanho_fila_hist.append(len(fila_espera))
                tempo_fila_hist.append(tempo_atual)

        elif evento[1] == SAIDA:
            print(f"\n{round(tempo_atual, 2)} min | Fim de consulta: {dados_doente['nome']}")
            doentes_atendidos += 1
            saida_d[id_unico] = tempo_atual
            
            medico_idx = -1
            
            for i, m in enumerate(medicos):
                if m[2] == id_unico:
                    m[1] = False
                    duracao = tempo_atual - m[4]
                    m[3] += duracao 
                    m[2] = None
                    medico_idx = i
                    

            if fila_espera:
                p_id, p_dados, t_chegada_f = fila_espera.pop(0)
                print(f"Saiu da fila: {p_dados['nome']} (esperou {round(tempo_atual - t_chegada_f, 2)} min)")
                
                tamanho_fila_hist.append(len(fila_espera))
                tempo_fila_hist.append(tempo_atual)
                
                m = medicos[medico_idx]
                m[1] = True
                m[2] = p_id
                m[4] = tempo_atual
                ent_consulta_d[p_id] = tempo_atual
                
                t_cons = mani.gera_tempo_consulta(p_dados)
                print(f"Consulta prevista: {round(t_cons, 2)} min")
                queueEventos = mani.enqueue(queueEventos, (tempo_atual + t_cons, SAIDA, (p_id, p_dados)))

    # --- ESTATÍSTICAS FINAIS ---
    esperas = [ent_consulta_d[d] - chegadas_d[d] for d in saida_d if d in ent_consulta_d]
    totais = [saida_d[d] - chegadas_d[d] for d in saida_d]

    print(f"\n{'='*40}\n   SIMULAÇÃO TERMINADA\n{'='*40}")
    print(f"Doentes Atendidos: {doentes_atendidos}")
    print(f"Média de Espera: {round(np.mean(esperas), 2) if esperas else 0} min")
    print(f"Média na Clínica: {round(np.mean(totais), 2) if totais else 0} min")

    return {
        "total_atendidos": doentes_atendidos,
        "media_espera": np.mean(esperas) if esperas else 0,
        "media_clinica": np.mean(totais) if totais else 0,
        "hist_fila": list(zip(tempo_fila_hist, tamanho_fila_hist)),
        "hist_ocupa": hist_ocupa
    }

if __name__ == "__main__":
    simula(3, 10, 15, 480, "exponential")