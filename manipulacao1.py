import numpy as np
import json

# ===============================
# PARÂMETROS DA SIMULAÇÃO
# ===============================
NUM_MEDICOS = 3
TAXA_CHEGADA = 10 / 60
TEMPO_MEDIO_CONSULTA = 15
TEMPO_SIMULACAO = 8 * 60
DISTRIBUICAO_TEMPO_CONSULTA = "exponential"

CHEGADA = "chegada"
SAIDA = "saida"

# ===============================
# CARREGAR DATASET
# ===============================
with open("pessoas.json", encoding="utf-8") as f:
    PESSOAS = json.load(f)

# ===============================
# EVENTOS
# ===============================
def e_tempo(e):
    return e[0]

def e_tipo(e):
    return e[1]

def e_doente(e):
    return e[2]

# ===============================
# FILA DE EVENTOS
# ===============================
def procuraPosQueue(q, t):
    i = 0
    while i < len(q) and t > q[i][0]:
        i += 1
    return i

def enqueue(q, e):
    pos = procuraPosQueue(q, e[0])
    return q[:pos] + [e] + q[pos:]

def dequeue(q):
    return q[0], q[1:]

# ===============================
# MODELO DE MÉDICO
# ===============================
def m_ocupa(m):
    m[1] = not m[1]
    return m

def m_doente_corrente(m):
    return m[2]

def mDoenteCorrente(m, d):
    m[2] = d
    return m

def mTempoOcupado(m, t):
    m[3] = t
    return m

def m_inicio_ultima_consulta(m):
    return m[4]

def mInicioConsulta(m, t):
    m[4] = t
    return m

# ===============================
# DISTRIBUIÇÕES
# ===============================
def gera_intervalo_tempo_chegada(lmbda):
    return np.random.exponential(1 / lmbda)

def gera_tempo_consulta(doente):
    if DISTRIBUICAO_TEMPO_CONSULTA == "exponential":
        tempo = np.random.exponential(TEMPO_MEDIO_CONSULTA)
    elif DISTRIBUICAO_TEMPO_CONSULTA == "normal":
        tempo = max(0, np.random.normal(TEMPO_MEDIO_CONSULTA, 5))
    elif DISTRIBUICAO_TEMPO_CONSULTA == "uniform":
        tempo = np.random.uniform(
            TEMPO_MEDIO_CONSULTA * 0.5,
            TEMPO_MEDIO_CONSULTA * 1.5
        )

    # ajuste por idade
    idade = doente["idade"]
    if idade < 18:
        tempo *= 0.8
    elif idade > 65:
        tempo *= 1.3

    return tempo

# ===============================
# PROCURAR MÉDICO LIVRE
# ===============================
def procuraMedico(lista):
    for m in lista:
        if not m[1]:
            return m
    return None