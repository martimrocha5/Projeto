import heapq
import random
import numpy as np

# Parâmetros da aplicação

NUM_MEDICOS = 3
TAXA_CHEGADA = 10 / 60
TEMPO_MEDIO_CONSULTA = 15
TEMPO_SIMULACAO = 8 * 60
DISTRIBUICAO_TEMPO_CONSULTA = "exponential"

CHEGADA = "chegada"
SAIDA = "saída"

# --- Modelo para o evento
# Evento = (tempo: Float, tipo: String, doente: String)

def e_tempo(e):
    return e[0]

def e_tipo(e):
    return e[1]

def e_doente(e):
    return e[2]

# --- Modelo para a Queue de Eventos
# queueEventos = [Evento]

def procuraPosQueue(q, t):
    i = 0
    while i < len(q) and t > q[i][0]:
        i = i + 1
    return i

def enqueue(q, e):
    pos = procuraPosQueue(q, e[0])
    return q[:pos] + [e] + q[pos:]

def dequeue(q):
    e = q[0]
    q = q[1:]
    return e, q

# --- Modelo para o médico
# Médico = [id: String, ocupado: Boolean, doente_corrente: String, total_tempo_ocupado: Float, inicio_ultima_consulta: Float]

def m_id(e):
    return e[0]

def m_ocupado(e):
    return e[1]

def mOcupa(m):
    m[1] = not m[1]
    return m

def m_doente_corrente(e):
    return e[2]

def mDoenteCorrente(m, d):
    m[2] = d
    return m

def m_total_tempo_ocupado(e):
    return e[3]

def mTempoOcupado(m, t):
    m[3] = t
    return m

def m_inicio_ultima_consulta(e):
    return e[4]

def mInicioConsulta(m, t):
    m[4] = t
    return m 
# ---

# --- Utilização das distribuições para gerar chegadas e durações das consultas
# ---
def gera_intervalo_tempo_chegada(lmbda):
    return np.random.exponential(1 / lmbda)

def gera_tempo_consulta():
    if DISTRIBUICAO_TEMPO_CONSULTA == "exponential":
        return np.random.exponential(TEMPO_MEDIO_CONSULTA)
    elif DISTRIBUICAO_TEMPO_CONSULTA == "normal":
        return max(0, np.random.normal(TEMPO_MEDIO_CONSULTA, 5))
    elif DISTRIBUICAO_TEMPO_CONSULTA == "uniform":
        return np.random.uniform(TEMPO_MEDIO_CONSULTA * 0.5, TEMPO_MEDIO_CONSULTA * 1.5)

# --- Funções auxiliares
# -----------------------------------------
# --- Procura o primeiro médico livre
# ---
def procuraMedico(lista):
    res = None
    i = 0
    encontrado = False
    while not encontrado and i < len(lista):
        if not lista[i][1]:
            res = lista[i]
            encontrado = True
        i = i + 1
    return res