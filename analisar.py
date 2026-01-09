import json

def carregar_e_validar(caminho):
    """Carrega o JSON e devolve a lista de pessoas."""
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados


def estatisticas_idades(lista):
    """Cálculo de média, mínima e máxima das idades."""
    soma = 0
    contagem = 0
    min_idade = 999
    max_idade = -1

    for p in lista:
        idade = p["idade"]
        soma += idade
        contagem += 1

        if idade < min_idade:
            min_idade = idade
        if idade > max_idade:
            max_idade = idade

    return {
        "media": soma / contagem if contagem > 0 else 0,
        "min": min_idade,
        "max": max_idade,
        "total": contagem
    }


def distribuicao_distritos(lista):
    """Frequência de distritos."""
    res = {}

    for p in lista:
        d = p["morada"]["distrito"]
        if d in res:
            res[d] += 1
        else:
            res[d] = 1

    return res


def distribuicao_fumadores(lista):
    """Contagem de fumadores e não fumadores."""
    res = {"Fumador": 0, "Não Fumador": 0}

    for p in lista:
        if p["atributos"]["fumador"]:
            res["Fumador"] += 1
        else:
            res["Não Fumador"] += 1

    return res


def distribuicao_desportos(lista):
    """Frequência de desportos."""
    res = {}

    for p in lista:
        for d in p["desportos"]:
            if d in res:
                res[d] += 1
            else:
                res[d] = 1

    return res


def top_profissoes(lista, n=10):
    """Top profissões mais frequentes."""
    res = {}

    for p in lista:
        prof = p["profissao"]
        if prof in res:
            res[prof] += 1
        else:
            res[prof] = 1

    return sorted(res.items(), key=lambda x: x[1], reverse=True)[:n]


def distribuir_faixas_etarias(lista):
    """Distribuição por faixas etárias."""
    res = {"0-17": 0, "18-30": 0, "31-50": 0, "51-70": 0, "71+": 0}

    for p in lista:
        i = p["idade"]

        if i < 18:
            res["0-17"] += 1
        elif i < 31:
            res["18-30"] += 1
        elif i < 51:
            res["31-50"] += 1
        elif i < 71:
            res["51-70"] += 1
        else:
            res["71+"] += 1

    return res
