import random


class JogoDeForca:
    def __init__(self):
        import requests
        url = 'https://www.ime.usp.br/~pf/dicios/br-sem-acentos.txt'
        r = requests.get(url, allow_redirects=True)
        if r.status_code == 200:
            self.content = str(r.content.decode()).split('\n')
        else:
            print("Erro: ", r.status_code)

    def novo_jogo(self, vidas=5):
        self.vidas = vidas
        self.palavra = random.choice(self.content)
        return len(self.palavra)

    def tentar_letra(self, letra):
        if self.vidas > 0:
            if letra in self.palavra:
                return [idx for idx in range(len(self.palavra)) if self.palavra[idx] == letra]
            else:
                self.vidas -= 1
                if self.vidas == 0:
                    print("Fim de jogo!")
                    return False
                else:
                    return []

    def tentar_palavra(self, palavra):
        if self.vidas > 0:
            if self.palavra == palavra:
                print("Ganhou!")
                return True
            else:
                self.vidas = 0
                print("Fim de jogo!")
                return False


def letra_tentativa(lista, letras_tentadas):
    dici = {}
    for palavra in lista:
        for letra in palavra:
            if letra not in letras_tentadas:
                if letra in dici:
                    dici[letra] += 1
                else:
                    dici[letra] = 1
    return max(dici, key=dici.get)


def filtra_palavras_por_letras(palavras, num):
    lista = []
    for palavra in palavras:
        if len(palavra) == num:
            lista.append(palavra)
    return lista


def jogador(jogo):
    letras_tentadas = []
    num = jogo.novo_jogo()
    lista = filtra_palavras_por_letras(jogo.content, num)

    while jogo.vidas > 0:
        letra = letra_tentativa(lista, letras_tentadas)
        resultado = jogo.tentar_letra(letra)

        if resultado == False:
            break
        elif len(resultado) == 0:
            lista = filtra_palavras_por_letras(lista, num)
        else:
            lista = [palavra for palavra in lista if all(palavra[idx] == letra for idx in resultado)]
        if len(lista) == 1:
            resultado_final = jogo.tentar_palavra(lista[0])
            if resultado_final:
                return True
            break
        return False
    


ganhou = 0
jogo = JogoDeForca()
for i in range(1):
    resultado = jogador(jogo)
if resultado == True:
    ganhou += 1
print(ganhou)
