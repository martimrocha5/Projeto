import heapq
import random
import numpy as np
import matplotlib as mlt
import manipulacao1 as mani
import FreeSimpleGUI as sg

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
    queueEventos = []
    queue = []
   
    medicos = [[f"m{i}", False, None, 0.0, 0.0] for i in range(NUM_MEDICOS)]
   
    chegadas_d = {}
    ent_consulta_d = {}
    saida_d = {}

    tamanho_fila=[]
    tempo_atual_fila=[]
   
    tempo_atual = tempo_atual + mani.gera_intervalo_tempo_chegada(TAXA_CHEGADA)
    while tempo_atual < TEMPO_SIMULACAO:
        doente_id = "d" + str(contadorDoentes)
        contadorDoentes += 1
        chegadas_d[doente_id] = tempo_atual
        queueEventos = mani.enqueue(queueEventos, (tempo_atual, CHEGADA, doente_id))
        tempo_atual = tempo_atual + mani.gera_intervalo_tempo_chegada(TAXA_CHEGADA)
   
    doentes_atendidos = 0

    while queueEventos != []:
        evento, queueEventos = mani.dequeue(queueEventos)
        tempo_atual = mani.e_tempo(evento)

        if mani.e_tipo(evento) == CHEGADA:
            medico_livre = mani.procuraMedico(medicos)
            if medico_livre:
                medico_livre = mani.mOcupa(medico_livre)
                medico_livre = mani.mInicioConsulta(medico_livre, tempo_atual)
                ent_consulta_d[mani.e_doente(evento)]=tempo_atual
                tempo_consulta = mani.gera_tempo_consulta()
                medico_livre = mani.mDoenteCorrente(medico_livre, mani.e_doente(evento))
                queueEventos = mani.enqueue(queueEventos, (tempo_atual + tempo_consulta, SAIDA, mani.e_doente(evento)))
               
            else:
                queue.append((evento[2], tempo_atual))
                
                tamanho_fila.append(len(queue))
                tempo_atual_fila.append(tempo_atual)
        elif evento[1] == SAIDA:
            doentes_atendidos += 1
           
            i = 0
            encontrado = False
            while i < len(medicos) and not encontrado:
                if mani.m_doente_corrente(medicos[i]) == mani.e_doente(evento):
                    medicos[i] = mani.mOcupa(medicos[i])
                    medicos[i] = mani.mDoenteCorrente(medicos[i], None)  
                    medicos[i] = mani.mTempoOcupado(medicos[i], mani.m_total_tempo_ocupado(medicos[i]) + tempo_atual - mani.m_inicio_ultima_consulta(medicos[i]))
                    encontrado = True
                i = i + 1
            saida_d[mani.e_doente(evento)]=tempo_atual
            medico = medicos[i-1]

            if queue != []:
                ev, queue = mani.dequeue(queue)
                tamanho_fila.append(len(queue))
                tempo_atual_fila.append(tempo_atual)
                prox_doente, tchegada = ev
                medico = mani.mOcupa(medico)
                medico = mani.mInicioConsulta(medico, tempo_atual)
                ent_consulta_d[prox_doente]=tempo_atual
                medico = mani.mDoenteCorrente(medico, prox_doente)
                tempo_consulta = mani.gera_tempo_consulta()
                queueEventos = mani.enqueue(queueEventos, (tempo_atual + tempo_consulta, SAIDA, prox_doente))

    print(f"Doentes atendidos: {doentes_atendidos}")
    
    tempos_espera = []
    tempos_totais = []
    soma_espera=0
    media_espera=0
    soma_total=0
    media_total=0

    for doente in chegadas_d:
        if doente in ent_consulta_d and doente in saida_d:
            tempo_espera = ent_consulta_d[doente] - chegadas_d[doente]
            tempo_total = saida_d[doente] - chegadas_d[doente]

            tempos_espera.append(tempo_espera)
            tempos_totais.append(tempo_total)
    

    for t1 in tempos_espera:
        soma_espera+=t1
    media_espera=soma_espera/len(tempos_espera)

    for t2 in tempos_totais:
        soma_total+=t2
    media_total=soma_total/len(tempos_totais)

    max_espera=max(tempos_espera)
    max_total=max(tempos_totais)

    print(tamanho_fila)
    print(tempo_atual_fila)

if __name__ == "__main__":
    simula()