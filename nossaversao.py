import heapq
import random
import numpy as np
import matplotlib as mlt
import manipulacao1 as mani


# Parâmetros da aplicação

NUM_MEDICOS = 3
TAXA_CHEGADA = 10 / 60
TEMPO_MEDIO_CONSULTA = 15
TEMPO_SIMULACAO = 8 * 60
DISTRIBUICAO_TEMPO_CONSULTA = "exponential"

CHEGADA = "chegada"
SAIDA = "saída"

def simula():
    tempo_atual = 0.0
    contadorDoentes = 1
    chegadas_saidas = [] 
    fila_espera = [] 
    
    medicos = [[f"m{i}", False, None, 0.0, 0.0] for i in range(NUM_MEDICOS)]
    
    chegadas_d = {}       # Regista quando o doente chegou à clínica
    ent_consulta_d = {}   # Regista quando o doente entrou no consultório
    saida_d = {}          # Regista quando o doente saiu da clínica
    
    # Listas para guardar dados estatísticos
    historico_fila = []      # Evolução da fila 
    historico_ocupacao = []  # Evolução da ocupação 
    tempos_espera = []       # Diferença entre ent_consulta_d e chegadas_d 
    tempos_consulta = []     # Duração real de cada consulta 
    tempos_na_clinica = []   # Diferença entre saida_d e chegadas_d 

    # Geração das chegadas (Processo de Poisson) 
    tempo_aux = 0.0
    while tempo_aux < TEMPO_SIMULACAO:
        doente_id = "d" + str(contadorDoentes)
        contadorDoentes += 1
        chegadas_d[doente_id] = tempo_aux
        chegadas_saidas = mani.enqueue(chegadas_saidas, (tempo_aux, CHEGADA, doente_id))
        tempo_aux += mani.gera_intervalo_tempo_chegada(TAXA_CHEGADA)
    
    doentes_atendidos = 0

    while chegadas_saidas != []:
        evento, chegadas_saidas = mani.dequeue(chegadas_saidas)
        tempo_atual = mani.e_tempo(evento) 
        id_doente = mani.e_doente(evento)

        # Registo de estado para gráficos
        historico_fila.append((tempo_atual, len(fila_espera)))
        medicos_ocupados = sum(1 for m in medicos if mani.m_ocupado(m))
        historico_ocupacao.append((tempo_atual, (medicos_ocupados / NUM_MEDICOS) * 100))

        if mani.e_tipo(evento) == CHEGADA:
            medico_livre = mani.procuraMedico(medicos)
            if medico_livre:
                # Caso sem fila: o tempo de espera é zero
                tempos_espera.append(0)
                ent_consulta_d[id_doente] = tempo_atual
                
                medico_livre = mani.mOcupa(medico_livre) 
                medico_livre = mani.mInicioConsulta(medico_livre, tempo_atual)
                medico_livre = mani.mDoenteCorrente(medico_livre, id_doente) 
                
                t_cons = mani.gera_tempo_consulta()
                tempos_consulta.append(t_cons)
                chegadas_saidas = mani.enqueue(chegadas_saidas, (tempo_atual + t_cons, SAIDA, id_doente))
            else:
                fila_espera.append((id_doente, tempo_atual)) # Entra na queue 
        
        elif mani.e_tipo(evento) == SAIDA:
            doentes_atendidos += 1
            
            # --- REGISTO DA SAÍDA ---
            saida_d[id_doente] = tempo_atual
            # Cálculo: Tempo na Clínica = Momento da Saída - Momento da Chegada 
            tempos_na_clinica.append(saida_d[id_doente] - chegadas_d[id_doente])
            
            # Libertar médico e processar fila
            medico = None
            for m in medicos:
                if mani.m_doente_corrente(m) == id_doente:
                    m = mani.mOcupa(m) # Fica livre 
                    m = mani.mDoenteCorrente(m, None)
                    m = mani.mTempoOcupado(m, mani.m_total_tempo_ocupado(m) + (tempo_atual - mani.m_inicio_ultima_consulta(m)))
                    medico = m
                    break

            if fila_espera != []:
                (prox_doente_id, t_chegada_fila), fila_espera = mani.dequeue(fila_espera)
                
                tempos_espera.append(tempo_atual - t_chegada_fila)
                ent_consulta_d[prox_doente_id] = tempo_atual
                
                medico = mani.mOcupa(medico) 
                medico = mani.mInicioConsulta(medico, tempo_atual)
                medico = mani.mDoenteCorrente(medico, prox_doente_id)
                
                t_cons = mani.gera_tempo_consulta()
                tempos_consulta.append(t_cons)
                chegadas_saidas = mani.enqueue(chegadas_saidas, (tempo_atual + t_cons, SAIDA, prox_doente_id))

    stats = {
        "media_espera": np.mean(tempos_espera) if tempos_espera else 0,
        "media_consulta": np.mean(tempos_consulta) if tempos_consulta else 0,
        "media_clinica": np.mean(tempos_na_clinica) if tempos_na_clinica else 0,
        "total_atendidos": doentes_atendidos,
        "hist_fila": historico_fila,
        "hist_ocupa": historico_ocupacao
    }
    
    print(f"Doentes atendidos: {doentes_atendidos}")
    print(chegadas_d)
    print(ent_consulta_d)
    print(saida_d)

    return stats


if __name__ == "__main__":
    simula()