import copy  # permite criar cópias profundas (deep copies) de objetos compostos
import sys
from urllib import parse  # manipulação de URLs
import requests  # usado para fazer requisições HTTP


def request(url):
    headers = {"User-Agent":"",
               "Cookie":""}
    try:
        response = requests.get(url, headers=headers)
        html = response.text
        return html
    except:
        pass


def is_vulnerable(html):
    errors = ["mysql_fetch_array()",
              "You have an error in your SQL syntax",
              "SQL0104 - Sinal &1 não válido. Sinais válidos: &2",
              "SQL0113 - Nome &1 não permitido.",
              "SQL0114 - A base de dados relacional &1 não é a mesma que o servidor &2 actual",
              "SQL0204 - MYSYSCONF não localizado",
              "SQL0208 - Coluna ORDER BY não está na tabela de resultados",
              "SQL0900 - O processo da aplicação não está num estado ligado",
              "SQL0901 - Erro de Sistema de SQL",
              "SQL5001 - Qualificador de coluna ou tabela &2 não definido.",
              "SQL5016 - Nome de objecto &1 não válido para convenção de nomenclatura",
              "SQL7008 - &1 em &2 não válido para a operação. O código de razão é 3"
              ]
    for error in errors:
        if error in html:
            return True


if __name__ == "__main__":
    url = sys.argv[1]
    url_parsed = parse.urlsplit(url)
    # Converte os parâmetros de query (após o ? na URL) para um dicionário onde cada chave é um nome de parâmetro:
    params = parse.parse_qs(url_parsed.query)
    for param in params.keys():
        query = copy.deepcopy(params)
        # Tenta injetar os caracteres ' e " em cada parâmetro da URL, para verificar se há vulnerabilidade:
        for c in "'\"":
            query[param][0] = c
            new_params = parse.urlencode(query, doseq=True)
            url_final = url_parsed._replace(query=new_params)
            url_final = url_final.geturl()
            html = request(url_final)
            if html:
                if is_vulnerable(html):
                    print("[ + ] {} parameter is vulnerable".format(param))
                    quit()

    print("NOT VULNERABLE")