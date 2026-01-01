import json

def carregar_e_validar(caminho):
    """Carrega o JSON e valida os dados básicos."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        # Filtra apenas dicionários que contenham a chave 'id'
        return [p for p in dados if isinstance(p, dict) and "id" in p]
    except Exception:
        return []

def estatisticas_idades(lista):
    """Cálculo de média, mín e máx."""
    soma, contagem = 0, 0
    min_idade, max_idade = 999, -1
    
    for p in lista:
        if "idade" in p:
            idade = p["idade"]
            soma += idade
            contagem += 1
            if idade < min_idade: min_idade = idade
            if idade > max_idade: max_idade = idade
            
    return {
        "media": soma / contagem if contagem > 0 else 0,
        "min": min_idade, "max": max_idade, "total": contagem
    }

def distribuicao_distritos(lista):
    """Frequência de distritos na raiz da morada."""
    res = {}
    for p in lista:
        if "morada" in p and "distrito" in p["morada"]:
            d = p["morada"]["distrito"]
            res[d] = res.get(d, 0) + 1
    return res

def distribuicao_fumadores(lista):
    """Contagem booleana dentro da chave 'atributos'."""
    res = {"Fumador": 0, "Não Fumador": 0}
    for p in lista:
        # Acede à sub-chave conforme a estrutura do teu JSON
        if "atributos" in p:
            if p["atributos"]["fumador"]:
                res["Fumador"] += 1
            else:
                res["Não Fumador"] += 1
    return res

def distribuicao_desportos(lista):
    """Frequência de itens numa lista dentro de 'atributos'."""
    res = {}
    for p in lista:
        if "desportos" in p:
            para_contar = p["desportos"]
            for item in para_contar:
                res[item] = res.get(item, 0) + 1
    return res

def top_profissoes(lista, n=10):
    """Frequência e ordenação por lambda."""
    res = {}
    for p in lista:
        prof = p.get("profissao", "N/A")
        res[prof] = res.get(prof, 0) + 1
    # Ordena a lista de tuplos pelo valor (contagem)
    return sorted(res.items(), key=lambda x: x[1], reverse=True)[:n]

def distribuir_faixas_etarias(lista):
    """Contagem por categorias fixas."""
    res = {"0-17": 0, "18-30": 0, "31-50": 0, "51-70": 0, "71+": 0}
    for p in lista:
        if "idade" in p:
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