import manipulacao1 as mani

# Constantes para legibilidade
CHEGADA = "chegada"
SAIDA = "saída"

def simula(n_medicos, taxa_chegada, tempo_medio, tempo_simulacao, distribuicao):
    # 1. ATUALIZAR O MÓDULO DE MANIPULAÇÃO COM OS DADOS DA GUI
    # Isto garante que as funções gera_tempo_consulta usem os valores que escolheste
    mani.NUM_MEDICOS = n_medicos
    mani.TAXA_CHEGADA = taxa_chegada / 60  # converter para doentes/min
    mani.TEMPO_MEDIO_CONSULTA = tempo_medio
    mani.TEMPO_SIMULACAO = tempo_simulacao
    mani.DISTRIBUICAO_TEMPO_CONSULTA = distribuicao
    
    # Inicialização
    tempo_atual = 0.0
    contadorDoentes = 1
    queueEventos = []
    queue = [] # Fila de espera (FIFO)
   
    # Criar médicos: [id, ocupado, doente_atual, tempo_ocupado, inicio_ult_consulta]
    medicos = [[f"m{i}", False, None, 0.0, 0.0] for i in range(mani.NUM_MEDICOS)]
   
    # Estruturas para estatísticas
    chegadas_d = {}
    ent_consulta_d = {}
    saida_d = {}

    tamanho_fila = []     # Para o gráfico 1
    tempo_atual_fila = [] # Para o gráfico 1
    
    hist_ocupa = []       # Para o gráfico 2 (Novo!)
   
    # Gerar chegadas iniciais
    tempo_atual = mani.gera_intervalo_tempo_chegada(mani.TAXA_CHEGADA)
    while tempo_atual < mani.TEMPO_SIMULACAO:
        doente_id = "d" + str(contadorDoentes)
        contadorDoentes += 1
        chegadas_d[doente_id] = tempo_atual
        queueEventos = mani.enqueue(queueEventos, (tempo_atual, CHEGADA, doente_id))
        tempo_atual += mani.gera_intervalo_tempo_chegada(mani.TAXA_CHEGADA)
   
    doentes_atendidos = 0

    # CICLO DE SIMULAÇÃO
    while queueEventos != []:
        evento, queueEventos = mani.dequeue(queueEventos)
        tempo_atual = mani.e_tempo(evento)

        # Recolha de dados para o Gráfico de Ocupação
        ocupados = sum(1 for m in medicos if mani.m_ocupado(m))
        perc_ocupacao = (ocupados / n_medicos) * 100
        hist_ocupa.append((tempo_atual, perc_ocupacao))

        # Processar CHEGADA
        if mani.e_tipo(evento) == CHEGADA:
            medico_livre = mani.procuraMedico(medicos)
            
            if medico_livre:
                # O médico estava livre, atende já
                medico_livre = mani.mOcupa(medico_livre)
                medico_livre = mani.mInicioConsulta(medico_livre, tempo_atual)
                ent_consulta_d[mani.e_doente(evento)] = tempo_atual
                
                tempo_consulta = mani.gera_tempo_consulta()
                medico_livre = mani.mDoenteCorrente(medico_livre, mani.e_doente(evento))
                
                queueEventos = mani.enqueue(queueEventos, (tempo_atual + tempo_consulta, SAIDA, mani.e_doente(evento)))
            else:
                # Médicos ocupados, vai para a fila
                queue.append((mani.e_doente(evento), tempo_atual))
                tamanho_fila.append(len(queue))
                tempo_atual_fila.append(tempo_atual)

        # Processar SAÍDA
        elif mani.e_tipo(evento) == SAIDA:
            doentes_atendidos += 1
            
            # Libertar o médico que estava com este doente
            i = 0
            encontrado = False
            medico_idx = -1
            while i < len(medicos) and not encontrado:
                if mani.m_doente_corrente(medicos[i]) == mani.e_doente(evento):
                    medicos[i] = mani.mOcupa(medicos[i]) # Desocupa
                    medicos[i] = mani.mDoenteCorrente(medicos[i], None)  
                    # Contabilizar tempo de trabalho
                    duracao = tempo_atual - mani.m_inicio_ultima_consulta(medicos[i])
                    medicos[i] = mani.mTempoOcupado(medicos[i], mani.m_total_tempo_ocupado(medicos[i]) + duracao)
                    medico_idx = i
                    encontrado = True
                i += 1
            
            saida_d[mani.e_doente(evento)] = tempo_atual
            
            # Se houver alguém na fila, o médico atende logo o próximo
            if queue:
                prox_doente, t_chegada_fila = queue.pop(0) # FIFO
                
                # Registar fila (diminuiu)
                tamanho_fila.append(len(queue))
                tempo_atual_fila.append(tempo_atual)
                
                medico = medicos[medico_idx]
                medico = mani.mOcupa(medico)
                medico = mani.mInicioConsulta(medico, tempo_atual)
                ent_consulta_d[prox_doente] = tempo_atual
                medico = mani.mDoenteCorrente(medico, prox_doente)
                
                tempo_consulta = mani.gera_tempo_consulta()
                queueEventos = mani.enqueue(queueEventos, (tempo_atual + tempo_consulta, SAIDA, prox_doente))

    # --- CÁLCULO DE ESTATÍSTICAS FINAIS ---
    tempos_espera = []
    tempos_totais = []

    for doente in chegadas_d:
        if doente in ent_consulta_d and doente in saida_d:
            tempo_espera = ent_consulta_d[doente] - chegadas_d[doente]
            tempo_total = saida_d[doente] - chegadas_d[doente]
            tempos_espera.append(tempo_espera)
            tempos_totais.append(tempo_total)
    
    media_espera = sum(tempos_espera)/len(tempos_espera) if tempos_espera else 0
    media_total = sum(tempos_totais)/len(tempos_totais) if tempos_totais else 0

    return {
        "total_atendidos": doentes_atendidos,
        "media_espera": media_espera,
        "media_clinica": media_total,
        "hist_fila": list(zip(tempo_atual_fila, tamanho_fila)),
        "hist_ocupa": hist_ocupa # Agora já tem dados!
    }