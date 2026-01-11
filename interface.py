import FreeSimpleGUI as sg
import principal
import analisar
import json
from datetime import datetime
from graficos import menu_graficos

# =========================
# FUNÇÕES DE VALIDAÇÃO
# =========================
def validar_float(valor, nome, minimo=0, maximo=10000):
    if valor.strip() == "":
        sg.popup_error(f"O campo '{nome}' está vazio.")
        return None
    try:
        v = float(valor)
        if v < minimo or v > maximo:
            sg.popup_error(f"O campo '{nome}' deve estar entre {minimo} e {maximo}.")
            return None
        return v
    except ValueError:
        sg.popup_error(f"O campo '{nome}' tem de ser um número.")
        return None

def validar_int(valor, nome, minimo=0, maximo=100):
    if valor.strip() == "":
        sg.popup_error(f"O campo '{nome}' está vazio.")
        return None
    try:
        v = int(valor)
        if v < minimo or v > maximo:
            sg.popup_error(f"O campo '{nome}' deve estar entre {minimo} e {maximo}.")
            return None
        return v
    except ValueError:
        sg.popup_error(f"O campo '{nome}' tem de ser um número inteiro.")
        return None

# =========================
# JANELA DE ANÁLISE
# =========================
def abrir_janela_analise():
    try:
        dados = analisar.carregar_e_validar("pessoas.json")
        idades = analisar.estatisticas_idades(dados)
        faixas = analisar.distribuir_faixas_etarias(dados)
        fumadores = analisar.distribuicao_fumadores(dados)
        desportos = analisar.distribuicao_desportos(dados)
        distritos = analisar.distribuicao_distritos(dados)
        profs = analisar.top_profissoes(dados)

        txt_idade = f"Media: {idades['media']:.1f}\nMin: {idades['min']} | Max: {idades['max']}\n\nFaixas:\n"
        for k, v in faixas.items():
            txt_idade += f"- {k}: {v}\n"

        txt_profs = "Top Profissoes:\n"
        for k, v in profs:
            txt_profs += f"* {k}: {v}\n"

        dados_completos = {
            "Idades": {"media": idades['media'], "minimo": idades['min'], "maximo": idades['max'], "faixas": faixas},
            "Fumadores": fumadores,
            "Desportos": desportos,
            "Distritos": distritos,
            "Profissoes": [{"profissao": prof, "quantidade": qtd} for prof, qtd in profs]
        }

        layout = [
            [sg.Text("Painel de Analise de Dados", font=("Arial", 14, "bold"))],
            [sg.TabGroup([[
                sg.Tab("Idades", [[sg.Multiline(txt_idade, size=(45, 12), disabled=True, key="-TAB-IDADES-")]]),
                sg.Tab("Fumadores", [[sg.Listbox([f"{k}: {v}" for k,v in fumadores.items()], size=(45, 12), key="-TAB-FUMADORES-")]]),
                sg.Tab("Desportos", [[sg.Listbox([f"{k}: {v}" for k,v in desportos.items()], size=(45, 12), key="-TAB-DESPORTOS-")]]),
                sg.Tab("Distritos", [[sg.Listbox([f"{k}: {v}" for k,v in distritos.items()], size=(45, 12), key="-TAB-DISTRITOS-")]]),
                sg.Tab("Profissoes", [[sg.Multiline(txt_profs, size=(45, 12), disabled=True, key="-TAB-PROFS-")]])
            ]], key="-TABGROUP-")],
            [sg.Button("Guardar"), sg.Button("Fechar")]
        ]

        win = sg.Window("Estatisticas", layout, modal=True)
        analise_ativa = True
        
        while analise_ativa:
            e, values = win.read()
            if e in (sg.WIN_CLOSED, "Fechar"):
                win.close()
                analise_ativa = False
            elif e == "Guardar":
                layout_guardar = [
                    [sg.Text("Guardar relatório completo", font=("Helvetica", 12, "bold"))],
                    [sg.Button("Guardar em JSON", key="-JSON-", size=(20, 2), font=("Helvetica", 11))],
                    [sg.Button("Guardar em TXT", key="-TXT-", size=(20, 2), font=("Helvetica", 11))],
                    [sg.Button("Cancelar", key="-CANCELAR-", size=(20, 2), font=("Helvetica", 11))]
                ]
                win_guardar = sg.Window("Guardar Análise", layout_guardar, modal=True)
                guardar_ativo = True
                
                while guardar_ativo:
                    event_guardar, _ = win_guardar.read()
                    if event_guardar in (sg.WIN_CLOSED, "-CANCELAR-"):
                        win_guardar.close()
                        guardar_ativo = False
                    elif event_guardar == "-JSON-":
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"analise_completa_{timestamp}.json"
                        try:
                            with open(filename, 'w', encoding='utf-8') as f:
                                json.dump(dados_completos, f, indent=4, ensure_ascii=False)
                            sg.popup_ok(f"Análise guardada em: {filename}", title="Sucesso")
                        except Exception as ex:
                            sg.popup_error(f"Erro ao guardar JSON: {ex}", title="Erro")
                        win_guardar.close()
                        guardar_ativo = False
                        analise_ativa = False
                    elif event_guardar == "-TXT-":
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"analise_completa_{timestamp}.txt"
                        try:
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write("RELATÓRIO COMPLETO DE ANÁLISE DE DADOS\n" + "=" * 60 + f"\nData: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                                f.write(f"IDADES\n{'-' * 60}\nMédia: {idades['media']:.1f}\nMínimo: {idades['min']} | Máximo: {idades['max']}\nFaixas Etárias:\n")
                                for k, v in faixas.items():
                                    f.write(f"  - {k}: {v}\n")
                                f.write(f"\nFUMADORES\n{'-' * 60}\n")
                                for k, v in fumadores.items():
                                    f.write(f"  - {k}: {v}\n")
                                f.write(f"\nDESPORTOS\n{'-' * 60}\n")
                                for k, v in desportos.items():
                                    f.write(f"  - {k}: {v}\n")
                                f.write(f"\nDISTRITOS\n{'-' * 60}\n")
                                for k, v in distritos.items():
                                    f.write(f"  - {k}: {v}\n")
                                f.write(f"\nPROFISSÕES (TOP)\n{'-' * 60}\n")
                                for prof, qtd in profs:
                                    f.write(f"  - {prof}: {qtd}\n")
                                f.write("=" * 60 + "\n")
                            sg.popup_ok(f"Análise guardada em: {filename}", title="Sucesso")
                        except Exception as ex:
                            sg.popup_error(f"Erro ao guardar TXT: {ex}", title="Erro")
                        win_guardar.close()
                        guardar_ativo = False
                        analise_ativa = False
    except Exception as e:
        sg.popup_error(f"Erro ao carregar análise: {e}")

# =========================
# INTERFACE PRINCIPAL
# =========================
def criar_interface():
    sg.theme("LightBlue2")

    # Aumentei o size=(20,1) para size=(28,1) para caber o texto maior
    layout_config = [
        [sg.Text("Configurações", font=("Helvetica", 16, "bold"))],
        [sg.Text("Médicos:", size=(28,1), font=("Helvetica", 14)), sg.Input("3", key="-MEDICOS-", size=(10,), font=("Helvetica", 13))],
        [sg.Text("Taxa (doentes/h):", size=(28,1), font=("Helvetica", 14)), sg.Input("10", key="-TAXA-", size=(10,), font=("Helvetica", 13))],
        [sg.Text("Tempo de Consulta (min):", size=(28,1), font=("Helvetica", 14)), sg.Input("15", key="-TEMPO-", size=(10,), font=("Helvetica", 13))],
        [sg.Text("Duração da Simulação (min):", size=(28,1), font=("Helvetica", 14)), sg.Input("480", key="-DURACAO-", size=(10,), font=("Helvetica", 13))],
        [sg.Text("Distribuição:", size=(28,1), font=("Helvetica", 14)), sg.Combo(["exponential", "normal", "uniform"], default_value="exponential", key="-DIST-", readonly=True, font=("Helvetica", 13))]
    ]

    layout_botoes = [
        [sg.Button("Executar Simulação", key="-SIMULAR-", size=(18,2), font=("Helvetica", 13), button_color=("white","green")), sg.Button("Análise de Dados", key="-BT-ANALISE-", size=(18,2), font=("Helvetica", 13), button_color=("white","blue")), sg.Button("Sair", key="Sair", size=(18,2), font=("Helvetica", 13), button_color=("white","firebrick"))]
    ]

    layout_resultados = [
        [sg.Text("Resultados da Simulação", font=("Helvetica", 16, "bold"))],
        [sg.ProgressBar(100, orientation='h', size=(50, 20), key="-PROGRESS-", bar_color=("green", "#f0f0f0"))],
        [sg.Text("0%", key="-PROGRESS-TEXT-", font=("Helvetica", 10))],
        [sg.Column([[sg.Multiline(size=(150, 30), key="-OUTPUT-", disabled=True, font=("Courier New", 10), background_color="#f0f0f0")]]), sg.Column([[sg.Button("Abrir Menu de\nGráficos", key="-GRAF-", visible=False, font=("Helvetica", 11), size=(15, 3), button_color=("white", "orange"))], [sg.Button("Guardar", key="-GUARDAR-", visible=False, font=("Helvetica", 11), size=(15, 2), button_color=("white", "purple"))]], vertical_alignment="top")]
    ]

    layout = [
        [sg.Column([
            [sg.Text("Simulação de Clínica Médica", font=("Helvetica", 22, "bold"))],
            [sg.HorizontalSeparator()],
            [sg.Column(layout_config, pad=(0,15))],
            [sg.HorizontalSeparator()],
            [sg.Column(layout_botoes, justification="center")],
            [sg.HorizontalSeparator()],
            [sg.Column(layout_resultados, pad=(0,15))]
        ], justification="center", expand_x=True, expand_y=True)]
    ]

    window = sg.Window("Simulador", layout, resizable=True, finalize=True)
    window.maximize()
    
    dados = None
    app_ativa = True

    while app_ativa:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Sair"):
            app_ativa = False

        elif event == "-BT-ANALISE-":
            abrir_janela_analise()

        elif event == "-SIMULAR-":
            n_medicos = validar_int(values["-MEDICOS-"], "Médicos", minimo=1, maximo=20)
            taxa = validar_float(values["-TAXA-"], "Taxa (doentes/h)", minimo=0.1, maximo=100)
            tempo = validar_float(values["-TEMPO-"], "Tempo Consulta (min)", minimo=1, maximo=120)
            duracao = validar_float(values["-DURACAO-"], "Duração (min)", minimo=10, maximo=1440)

            if None in (n_medicos, taxa, tempo, duracao):
                continue

            window["-OUTPUT-"].update("")
            window.refresh()

            dados = principal.simula(n_medicos, taxa, tempo, duracao, values["-DIST-"], window=window)

            resumo = f"\n{'=' * 50}\nTotal de Doentes Atendidos: {dados['total_atendidos']}\nTempo Médio de Espera: {dados['media_espera']:.2f} min\nTempo Médio na Clínica: {dados['media_clinica']:.2f} min\nDoentes que ficaram à espera: {dados['fila_final']}\nDoentes por Especialidade:\n"
            for esp, qtd in dados["contagem_especialidades"].items():
                resumo += f"   - {esp}: {qtd}\n"
            resumo += "=" * 50

            conteudo_atual = window["-OUTPUT-"].get()
            window["-OUTPUT-"].update(conteudo_atual + resumo)
            window["-GRAF-"].update(visible=True)
            window["-GUARDAR-"].update(visible=True)

        elif event == "-GRAF-" and dados:
            menu_graficos(dados)

        elif event == "-GUARDAR-" and dados:
            layout_guardar = [
                [sg.Text("Escolha o formato para guardar:", font=("Helvetica", 12, "bold"))],
                [sg.Button("Guardar em JSON", key="-JSON-", size=(20, 2), font=("Helvetica", 11))],
                [sg.Button("Guardar em TXT", key="-TXT-", size=(20, 2), font=("Helvetica", 11))],
                [sg.Button("Cancelar", key="-CANCELAR-", size=(20, 2), font=("Helvetica", 11))]
            ]
            
            win_guardar = sg.Window("Guardar Resultados", layout_guardar, modal=True)
            guardar_ativo = True
            
            while guardar_ativo:
                event_guardar, _ = win_guardar.read()
                
                if event_guardar in (sg.WIN_CLOSED, "-CANCELAR-"):
                    guardar_ativo = False
                elif event_guardar == "-JSON-":
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"relatorio_{timestamp}.json"
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(dados, f, indent=4, ensure_ascii=False)
                        sg.popup_ok(f"Relatório guardado em: {filename}", title="Sucesso")
                    except Exception as e:
                        sg.popup_error(f"Erro ao guardar JSON: {e}", title="Erro")
                    guardar_ativo = False
                elif event_guardar == "-TXT-":
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"relatorio_{timestamp}.txt"
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write("RELATÓRIO DE SIMULAÇÃO DE CLÍNICA MÉDICA\n" + "=" * 50 + f"\nData: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                            f.write(f"Total de Doentes Atendidos: {dados['total_atendidos']}\n")
                            f.write(f"Tempo Médio de Espera: {dados['media_espera']:.2f} min\n")
                            f.write(f"Tempo Médio na Clínica: {dados['media_clinica']:.2f} min\n")
                            f.write(f"Doentes que ficaram à espera: {dados['fila_final']}\n\n")
                            f.write("Doentes por Especialidade:\n")
                            for esp, qtd in dados["contagem_especialidades"].items():
                                f.write(f"   - {esp}: {qtd}\n")
                            f.write("=" * 50 + "\n")
                        sg.popup_ok(f"Relatório guardado em: {filename}", title="Sucesso")
                    except Exception as e:
                        sg.popup_error(f"Erro ao guardar TXT: {e}", title="Erro")
                    guardar_ativo = False
            
            win_guardar.close()

    window.close()

if __name__ == "__main__":
    criar_interface()