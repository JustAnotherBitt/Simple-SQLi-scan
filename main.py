import copy  # allows you to create deep copies (deep copies) of composite objects
import sys
from urllib import parse  # URL manipulation
import requests  # for HTTP requests


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
    errors = open('errors.txt')
    print(errors)
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