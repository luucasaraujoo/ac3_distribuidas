import requests as req
class IdInvalida(Exception):
    pass
'''
A primeira coisa a fazer é ir ao site http://www.omdbapi.com/
e clicar no link API key.

Cadastre-se, abra o e-mail e valide sua chave. Depois, você
poderá acessar o OMDb.
'''

'coloque aqui a sua chave de acesso à api'
api_key = '43f686ce'

'''
Antes de fazer qualquer função, vamos experimentar
consultar o OMDb pelo navegador.

Digite, por exemplo, a seguinte URL no Firefox:
    http://www.omdbapi.com/?s=star%20wars&apikey={SUA-CHAVE-VEM-AQUI}

Observe que vemos uma lista de 10 filmes, mas há mais resultados.

Para ver a página 2, acesse
    http://www.omdbapi.com/?s=star%20wars&page=2&apikey={SUA-CHAVE-VEM-AQUI}
'''


'''
Observe que nas URLs acima, estamos passando parâmetros.
Na URL http://www.omdbapi.com/?s=star%20wars&page=2&apikey={SUA-CHAVE-VEM-AQUI}
definimos 3 parâmetros:
 * s=star wars
 * page=2
 * apikey={SUA-CHAVE-VEM-AQUI}
'''

'''
QUESTÃO 1
Olhando para os resultados da consulta
http://www.omdbapi.com/?s=star%20wars&apikey={SUA-CHAVE-VEM-AQUI},
quantos filmes foram encontrados para o termo "star wars"?

Resposta: 10

QUESTÃO 2
Consultando a documentação em www.omdbapi.com, você
pode aprender a filtrar os resultados da sua busca,
ficando apenas com filmes, eliminando jogos e séries.

Como fazer isso?

Se você fizer essa consulta, quantos filmes
existem para a busca star wars?

Resposta:

QUESTÃO 3:
E se ao invés de filmes você quiser só jogos,
quantos existem?

Resposta:

'''




'''
Vou te deixar dois exemplos de como acessar a URL. Nesse exemplo,
eu estou retornando o dicionário inteiro.
'''

def busca_por_id(film_id):
    url = "http://www.omdbapi.com/?apikey={}&i={}".format(api_key, film_id)
    retorno = req.get(url).json()
    return retorno

def busca_por_texto(texto_buscar):
    url = "http://www.omdbapi.com/?apikey={}&s={}".format(api_key, texto_buscar)
    retorno = req.get(url).json()
    return retorno

'''
Experimente! chame d1=busca_por_texto('star wars') e examine o
dicionário d1 retornado.
'''

'''
Agora, faça uma função busca_qtd_total que retorna quantos
itens (pode ser filme, jogo, série ou o que for) batem com
uma determinada busca.
'''
def busca_qtd_total(texto_buscar):
    json = busca_por_texto(texto_buscar)
    return json['totalResults']

'''
Faça uma função busca_qtd_filmes que retorna quantos
filmes batem com uma determinada busca.
'''
def busca_qtd_filmes(texto_buscar):
    url= url = "http://www.omdbapi.com/?apikey={}&type=movie&s={}".format(api_key,texto_buscar)
    retorno = req.get(url).json()
    return retorno['totalResults']
'''
Faça uma função busca_qtd_jogos que retorna quantos
jogos batem com uma determinada busca.
'''
def busca_qtd_jogos(texto_buscar):
    url= url = "http://www.omdbapi.com/?apikey={}&type=game&s={}".format(api_key,texto_buscar)
    retorno = req.get(url).json()
    return retorno['totalResults']

'''
Agora, vamos aprender a ver os detalhes de um filme.

Por exemplo, na lista de filmes podemos ver que o filme
star wars original (de 1977) tem id 'tt0076759'

Acessando a URL
http://www.omdbapi.com/?i=tt0076759&apikey={SUA-CHAVE-VEM-AQUI}
podemos ver mais detalhes.

Observe que agora não temos mais o parâmetro 's=star%20wars'
mas sim i=tt0076759. Mudou o nome da "variável", não só
o valor.
'''

'''
Faça uma função nome_do_filme_por_id que recebe a id de
um filme e retorna o seu nome.
'''
def nome_do_filme_por_id(id_filme):
    json=busca_por_id(id_filme)
    return json['Title']

'''
Faça uma função ano_do_filme_por_id que recebe a id de
um filme e retorna o seu ano de lançamento.
'''
def ano_do_filme_por_id(id_filme):
    json = busca_por_id(id_filme)
    return json['Year']

'''
Peguemos vários dados de um filme de uma vez.

A ideia é receber uma id e retornar 
um dicionário com diversos dados do filme.

O dicionário deve ter as seguintes chaves:
 * ano
 * nome
 * diretor
 * genero

E os dados devem ser preenchidos baseado nos dados do site.
'''
def dicionario_do_filme_por_id(id_filme):
    filme = {}
    json = busca_por_id(id_filme)
    if json['Response'] == 'False':
       raise IdInvalida()
    else:
        filme['nome'] = json['Title']
        filme['ano']=json['Year']
        filme['genero']=json['Genre']
        filme['diretor']=json['Director']
        filme['poster']=json['Poster']
        filme['nota_rotten_tomatoes']=int(json['Ratings'][1]['Value'][:2])/100
        filme['nota_metacritic']=int(json['Ratings'][2]['Value'][:2])/100
        filme['nota_ibm']=float(json['imdbRating'])/10
        filme['nota_media']=(filme['nota_rotten_tomatoes']+filme['nota_metacritic']+ filme['nota_ibm'])/3
        print(filme['nota_media'])
        return filme
       


'''
Voltando para a busca...

Faça uma função busca_filmes que, dada uma busca, retorna
os dez primeiros items (filmes, series, jogos ou o que for)
que batem com a busca.

A sua resposta deve ser uma lista, cada filme representado por 
um dicionário. cada dicionario deve conter os campos
'nome' (valor Title da resposta) e 'ano' (valor Year da resposta).
'''
def busca_filmes(texto_buscar):
    url = "http://www.omdbapi.com/?apikey={}&s={}".format(api_key, texto_buscar)
    retorno = req.get(url).json()
    resposta = []
    for filme in retorno['Search']:
        dicio = {}
        print(filme)
        dicio['nome'] = filme['Title']
        dicio['ano'] = filme['Year']
        dicio['id'] = filme['imdbID']
       
        resposta.append(dicio.copy())
        dicio.clear()
        print(resposta)
    return resposta

'''
Faça uma função busca_filmes_grande que, dada uma busca, retorna
os VINTE primeiros filmes que batem com a busca.
'''
def busca_filmes_grande(texto_buscar):
    url = "http://www.omdbapi.com/?apikey={}&s={}".format(api_key, texto_buscar)
    url2="http://www.omdbapi.com/?apikey={}&page=2&s={}".format(api_key, texto_buscar)
    retorno = req.get(url).json()
    retorno2 = req.get(url2).json()
    resposta = []
    for filme in retorno['Search']:
        dicio = {}
        print(filme)
        dicio['nome'] = filme['Title']
        dicio['ano'] = filme['Year']
        resposta.append(dicio.copy())
        dicio.clear()
        print(resposta)
    for filme in retorno2['Search']:
        dicio = {}
        print(filme)
        dicio['nome'] = filme['Title']
        dicio['ano'] = filme['Year'][:4]
        resposta.append(dicio.copy())
        dicio.clear()
        print(resposta)
    return resposta

'''
Agora, considere novamente a sua função dicionario_do_filme_por_id.

1) Um dos campos que o servidor retorna para nós tem
a URL de um poster. Adicione o campo poster no dicionário retornado.

2) Quando usamos uma id que não existe, temos um erro.
Nesse caso, a função deverá lançar a exceção IdInvalida.
Verifique primeiro no Firefox uma consulta 'zoada'
para ter uma ideia do que fazer.

3) O servidor nos retorna várias notas diferentes.
Adicione o campo nota_rotten_tomatoes no dicionario retornado
A nota deve ser normalizada, passando a ser um valor de 0 a 1,
em vez de uma porcentagem.

4) Faça a mesma coisa do item 3, mas para o metacritic.

5) Faça a mesma coisa dos itens anteriores, mas agora
dando a média das 3 notas (rotten tomatoes, metacritic e imdb).
'''

'''
Voltemos para a busca por string.

Quando fazermos uma busca por string no omdb, temos
como resposta uma lista com 10 dicionários, cada um
representando um filme/jogo/serie.

Queremos contar quantos de cada existem.

A próxima função recebe uma string para buscar,
e devolve um dicionário, dizendo quantos de cada "tipo"
de resultado tivemos.

Por exemplo,
ao fazer conta_tipos_de_midia_para_busca('menace') devemos
receber a resposta {'movie':8,'series':2}.

Confira, acessando a URL: 
http://www.omdbapi.com/?s=menace&apikey={SUA-CHAVE-VEM-AQUI}
'''
def conta_tipos_de_midia_para_busca(texto_buscar):
    url = "http://www.omdbapi.com/?apikey={}&s={}".format(api_key, texto_buscar)
    filmes = req.get(url).json()
    lista_tipo=[]
    dic_tipo={}
    for filme in filmes['Search']:
        dic_tipo[filme['Type']]=0
    for filme in filmes['Search']:
        dic_tipo[filme['Type']]+=1
    return dic_tipo

        
    
        

'''
Outra coisa que podemos fazer com nossos 10 resultados é
descobrir qual o filme mais antigo que apareceu.

A função id_do_mais_velho faz exatamente isso:
 * Recebe um texto a buscar;
 * Retorna a id do mais velho dentre os 10 primeiros.
'''
def id_do_mais_velho(texto_buscar):
    filmes=busca_filmes(texto_buscar)
    velho=int(filmes[0]['ano'])
    id = filmes[0]['id']
    for filme in filmes:
        print('oi')
        print(filme['id'])
        if int(filme['ano']) <velho:
            velho =int(filme['ano'])
            id=filme['id']
    return id
'''
Faça uma função ids_dos_tres_primeiros, que faz uma busca
e retorna uma lista com as ids dos três primeiros produtos
encontrados.
'''
def ids_dos_tres_primeiros(texto_buscar):
    filmes=busca_filmes(texto_buscar)
    ids = []
    for filme in filmes:
        if len(ids) >=3:
            break
        else:
            ids.append(filme['id'])
    return ids

'''
Agora, podemos cruzar os dados.

A lista de 10 filmes nao contém notas, mas nós sabemos fazer outra
consulta para achar as notas.

Crie uma função mais_bem_avaliado_dos_3_primeiros, que recebe uma
string para buscar, e retorna a id do mais bem avaliado entre os
3 primeiros resultados.

Não façamos com mais resultados, para não sobrecarregar o servidor.
'''
def mais_bem_avaliado_dos_3_primeiros(texto_buscar):
   ids = ids_dos_tres_primeiros(texto_buscar)
   maior_nota = dicionario_do_filme_por_id(ids[0])['nota_media']
   id_maior= ids[0]
   for idss in ids:
    if dicionario_do_filme_por_id(idss)['nota_media'] > maior_nota:
        maior_nota=dicionario_do_filme_por_id(idss)['nota_media']
        id_maior=idss
    return id_maior

'''
A próxima função já vem pronta, mas vamos melhorar ela depois.

O que ela faz? Recebe uma id do filme e baixa um arquivo Poster.jpg
com o poster do filme.

Basicamente, ela acessa uma URL como
http://img.omdbapi.com/?apikey={SUA-CHAVE-VEM-AQUI}&i=tt0120915
'''
def baixar_poster(id_filme):
    url = "http://img.omdbapi.com/?apikey={}&i={}".format(api_key, id_filme)
    retorno = req.get(url)
    print(retorno.status_code)
    if retorno.status_code == 404:
        return 'id inválida'
    else:
        arquivo = open("Poster.jpg", "wb")
        arquivo.write(retorno.content)
        arquivo.close()
        return 'id válida'
'''
'tt0796366' é a id de star trek.
'tt1211837' é a id de doctor strange.
'naoexiste' é uma id inválida.

1) Experimente digitar as URLs, juntando as IDs acima.

2) Experimente a função, usando as ids acima.

3) Tente rodar a funcao com a id naonaonao. O que ocorreu?

4) Corrija o problema: Faça a função retornar 'id inválida' quando 
ela recebeu uma id inválida, e 'id válida' quando a id era valida.

Dica: Procure o código de status no Firefox.
Faça a chamada válida e a chamada inválida, mas antes de cada uma,
vá em ferramentas de desenvolvedor > network.

Dica 2: Procure como descobrir o código de status
com a biblioteca requests em:
http://docs.python-requests.org/en/master/user/quickstart/
'''


import unittest

class TestStringMethods(unittest.TestCase):
    def test_000_qdt_total(self):
        self.assertTrue(439 * 0.9 < int(busca_qtd_total('star wars')) < 439 * 1.1)
        self.assertTrue(283 * 0.9 < int(busca_qtd_total('star trek')) < 283 * 1.1)

    def test_001_qdt_filmes(self):
        self.assertTrue(305 * 0.9 < int(busca_qtd_filmes('star wars')) < 305 * 1.1)
        self.assertTrue(186 * 0.9 < int(busca_qtd_filmes('star trek')) < 186 * 1.1)
        self.assertTrue(111 * 0.9 < int(busca_qtd_filmes('menace')) < 1.1 * 111)
        self.assertTrue(964 * 0.9 < int(busca_qtd_filmes('future')) < 964 * 1.1)

    def test_002_qdt_jogos(self):
        self.assertTrue(96 * 0.9 < int(busca_qtd_jogos('star wars')) < 1.1 * 96)
        self.assertTrue(55 * 0.9 < int(busca_qtd_jogos('star trek')) < 1.1 * 55)
        self.assertTrue( 8 * 0.8 < int(busca_qtd_jogos('menace')) < 1.2 *  8)
        self.assertTrue(34 * 0.9 < int(busca_qtd_jogos('future')) < 1.1 * 34)

    def test_003_nome_do_filme_por_id(self):
        self.assertEqual(nome_do_filme_por_id('tt0796366'), 'Star Trek')
        self.assertEqual(nome_do_filme_por_id('tt0861739'), 'Elite Squad')

    def test_004_ano_do_filme_por_id(self):
        self.assertEqual(ano_do_filme_por_id('tt0076759'), '1977')
        self.assertEqual(ano_do_filme_por_id('tt1211837'), '2016')

    def test_005_dicionario_filme_por_id(self):
        d1 = dicionario_do_filme_por_id('tt0076759')
        self.assertTrue(type(d1) is dict)
        self.assertEqual(d1['ano'], '1977')
        self.assertEqual(d1['diretor'], 'George Lucas')
        self.assertTrue('Action' in d1['genero'])
        d2 = dicionario_do_filme_por_id('tt1211837')
        self.assertTrue(type(d2) is dict)
        self.assertEqual(d2['ano'], '2016')
        self.assertEqual(d2['nome'], 'Doctor Strange')
        self.assertTrue('Fantasy' in d2['genero'])

    def test_006_busca(self):
        resposta = busca_filmes('star wars')
        self.assertEqual(len(resposta),10)
        achei = False
        for filme in resposta:
            if int(filme['ano']) == 1977:
                achei = True
            if 'ano' not in filme:
                self.fail('Ano não encontrado')
            if 'nome' not in filme:
                self.fail('Nome não encontrado')
        if not achei:
            self.fail('Filme "A New Hope" não encontrado')
    
    def test_007_busca_grande(self):
        resposta = busca_filmes_grande('star wars')
        self.assertEqual(len(resposta), 20)
        achei = False
        for filme in resposta:
            if int(filme['ano']) == 1977:
                achei = True
            if 'ano' not in filme:
                self.fail('Ano não encontrado.')
            if 'nome' not in filme:
                self.fail('Nome não encontrado.')
        if not achei:
            self.fail('Filme "A New Hope" não encontrado.')
    
    def test_008_dicionario_filme_por_id_tem_poster(self):
        resposta = dicionario_do_filme_por_id('tt0796366')
        self.assertTrue(
        "MV5BMjE5NDQ5OTE4Ml5BMl5BanBnXkFtZTcwOTE3NDIzMw@@._V1_SX300.jpg" in
                resposta['poster'])
    
    def test_009_tenta_montar_dicionario_para_id_invalida(self):
        try:
            dicionario_do_filme_por_id('tt0796366naoao')
        except IdInvalida:
            print('Ok, você levantou a exceção desejada.')
        except:
            self.fail('Você levantou uma exceção diferente.')
        else:
            self.fail('Você não levantou exceção.')
    
    def test_010_dicionario_tem_nota_rotten_tomatoes(self):
        resposta = dicionario_do_filme_por_id('tt0796366')
        self.assertTrue(0.92 < resposta['nota_rotten_tomatoes'] < 0.96)
        resposta = dicionario_do_filme_por_id('tt0861739')
        self.assertTrue(0.51 < resposta['nota_rotten_tomatoes'] < 0.55)
    
    def test_011_dicionario_tem_nota_metacritic(self):
        resposta = dicionario_do_filme_por_id('tt0796366')
        self.assertTrue(0.8 < resposta['nota_metacritic'] < 0.84)
        resposta = dicionario_do_filme_por_id('tt0861739')
        self.assertTrue(0.3 < resposta['nota_metacritic'] < 0.35)
    
    def test_012_dicionario_tem_nota_media(self):
        resposta = dicionario_do_filme_por_id('tt0796366')
        self.assertTrue(0.81 < resposta['nota_media'] < 0.89)
        resposta = dicionario_do_filme_por_id('tt0861739')
        self.assertTrue(0.51 < resposta['nota_media'] < 0.59)

    def test_013_conta_tipos_de_midia_para_busca(self):
        d1 = conta_tipos_de_midia_para_busca('menace')
        self.assertEqual(d1, {'movie': 8, 'series': 2})
        d1 = conta_tipos_de_midia_para_busca('grim fandango')
        self.assertEqual(d1, {'game': 2})
   
    def test_014_id_do_mais_velho(self):
        self.assertEqual(id_do_mais_velho('star wars'), 'tt0076759')
        self.assertEqual(id_do_mais_velho('grim fandango'), 'tt0177822')

    def test_015_ids_dos_tres_primeiros(self):
        lista = ids_dos_tres_primeiros('star wars')
        self.assertTrue('tt0076759' in lista)
        self.assertTrue('tt0080684' in lista)
        self.assertTrue('tt0086190' in lista)

    def test_016_mais_bem_avaliado(self):
        self.assertEqual(mais_bem_avaliado_dos_3_primeiros('star wars'), 'tt0076759')

    def test_017_poster_invalida(self):
        resposta = baixar_poster('tt0796366naoao')
        self.assertEqual(resposta, 'id inválida')
        resposta = baixar_poster('bonde')
        self.assertEqual(resposta, 'id inválida')
        resposta = baixar_poster('blackkamenrider')
        self.assertEqual(resposta, 'id inválida')

    def test_018_poster_valida(self):
        resposta = baixar_poster('tt0796366')
        self.assertEqual(resposta, 'id válida')

def runTests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity = 2, failfast = True).run(suite)

if __name__ == "__main__":
    runTests()
