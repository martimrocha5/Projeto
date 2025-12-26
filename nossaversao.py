import heapq
import random
import numpy as np
import matplotlib as mlt
import manipulacao1 as mani
import PySimpleGUI as sg


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
    
    chegadas = {} 
    tempo_atual = tempo_atual + mani.gera_intervalo_tempo_chegada(TAXA_CHEGADA)
    while tempo_atual < TEMPO_SIMULACAO:
        doente_id = "d" + str(contadorDoentes)
        contadorDoentes += 1
        chegadas[doente_id] = tempo_atual
        chegadas_saidas = mani.enqueue(chegadas_saidas, (tempo_atual, CHEGADA, doente_id))
        tempo_atual = tempo_atual + mani.gera_intervalo_tempo_chegada(TAXA_CHEGADA)
    
    doentes_atendidos = 0

    while chegadas_saidas != []:
        evento, chegadas_saidas = mani.dequeue(chegadas_saidas)
        print(mani.e_tipo(evento), evento)
        tempo_atual = mani.e_tempo(evento)

        if mani.e_tipo(evento) == CHEGADA:
            medico_livre = mani.procuraMedico(medicos)
            if medico_livre:
                medico_livre = mani.mOcupa(medico_livre) 
                medico_livre = mani.mInicioConsulta(medico_livre, tempo_atual)
                tempo_consulta = mani.gera_tempo_consulta()
                medico_livre = mani.mDoenteCorrente(medico_livre, mani.e_doente(evento)) 
                chegadas_saidas = mani.enqueue(chegadas_saidas, (tempo_atual + tempo_consulta, SAIDA, mani.e_doente(evento)))
            else:
                fila_espera.append((evento[2], tempo_atual)) 
                print(f"Fila de Espera({len(fila_espera)}): ", fila_espera)
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
            
            medico = medicos[i-1]

            if fila_espera != []: # se há doentes à espera vou ocupar o médico que ficou livre...
                ev, fila_espera = mani.dequeue(fila_espera)
                prox_doente, tchegada = ev
                medico = mani.mOcupa(medico)
                medico = mani.mInicioConsulta(medico, tempo_atual)
                medico = mani.mDoenteCorrente(medico, prox_doente)
                tempo_consulta = mani.gera_tempo_consulta()
                chegadas_saidas = mani.enqueue(chegadas_saidas, (tempo_atual + tempo_consulta, SAIDA, prox_doente))

    print(f"Doentes atendidos: {doentes_atendidos}")

if __name__ == "__main__":
    simula()