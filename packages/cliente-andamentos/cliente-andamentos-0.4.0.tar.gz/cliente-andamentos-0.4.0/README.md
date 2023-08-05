Cliente Andamentos
==================

[![PyPI version](https://badge.fury.io/py/cliente-andamentos.svg)](https://badge.fury.io/py/cliente-andamentos)

O Cliente Andamentos é uma biblioteca que faz interface com a API do *Andamentos*.


# Uso básico

Para iniciar o uso desta biblioteca é necessário baixá-la no PyPI com

    pip install cliente-andamentos

O uso de qualquer cliente da API *Andamentos* presume um cadastro prévio junto
ao sistema *Andamentos*, em que é fornecido pelo cliente, no ato do cadastro:
- Nome do sistema cliente;
- E-mail do cliente;
- URL para postback no cliente: é nesta URL que o Andamentos irá enviar um GET para
  informar que algum processo foi atualizado;
- Token do postback: Token usado para acessar a URL descrita acima.

Então o novo cliente recebe um token para acessar a API. Este token também pode
ser usado para testar se a biblioteca foi corretamente cadastrada e/ou tem
acesso à API:

```python
from cliente import BaseAPI
base = BaseAPI(token=token_recebido)
# Caso não esteja conectado, este método retornará um False
base.conectado()
# > True
```

Uma resposta True significa que a biblioteca está pronta para uso.


# Interface

O Cliente é formado pelas seguintes classes:
- BaseAPI
- Processo
- Tribunais
- Parte
- Andamento
- Anexo
- Oab

Através desses objetos é possível fazer contato com a API de uma forma
interativa. Um exemplo seria:

```python
from cliente.oab import Oab
oab = Oab('MG55000', token=algum_token)
# Salva o advogado na base de dados do Andamentos
oab.cadastra('João Doe')
```

As informações de texto adquiridas neste módulo são apresentadas sem um
encoding definido (formato unicode).

## `cliente.BaseAPI`

Classe base da API, as classes `Oab` e `Processo` herdam dela.

Em caso de algum parâmetro incorreto ser passado para os métodos das classes
derivadas desta, um erro do tipo `ParametrosIncorretos` será lançado.

### `cliente.BaseAPI.conectado()`

Retorna um booleano indicando se o objecto consegue se conectar com o servidor.


## `cliente.processo.Processo`

O `Processo` possui todos os atributos de um processo no *Andamentos*, que são:

- id
- cnj
- detalhes (dicionário de dados)
- assuntos (lista de assuntos)
- instancia
- status
- orgao_julgador
- tribunal
- comarca
- ultima_atualizacao (tipo `datetime`)
- prioritario
- ativo
- partes (lista de objetos [Parte](#parte))
- andamentos (lista de objetos [Andamento](#andamento))

A classe `Processo` deve ser construída passando-se o CNJ do processo e o token de autenticação.

```python
from cliente.processo import Processo
processo = Processo(cnj='0000001-00.2017.1.00.0000', token='5a2283201f71da415748eadf2a2202caabae485f')
```

Caso haja algum problema no servidor ou nos parâmetros passados, será lançada a
[exceção adequada à situação](#excecoes).

Quando se tenta acessar algum atributo, mas nenhum processo foi carregado
ainda, o método lança uma exceção `Processo.NaoCarregado`.


### `cliente.processo.Processo.cadastra()`

Método que cadastra um processo no *Andamentos*. Um processo demora alguns instantes para 
cadastrar o processo. O sistema irá retornar um *postback* para cada processo
encontrado com o CNJ passado.

O método retorna um `created` indicando se algum processo foi criado depois
dessa operação. Mesmo que não seja criado, o processo é enfileirado caso esse
método seja executado.

```python
from cliente.processo import Processo
processo = Processo(cnj='0000001-00.2017.1.00.0000', token='5a2283201f71da415748eadf2a2202caabae485f')
processo.cadastra()
# > True
```

### `cliente.processo.Processo.carrega_ativo(numero_andamentos)`

Carrega o processo ativo para a instância invocadora. Um processo ativo é o
último processo que recebeu uma atualização do tribunal.

`numero_andamentos` indica quantos dos últimos andamentos serão carregados.
padrão é 100, um parâmetro pode ser passado caso se queira pegar um número
diferente.

```python
from cliente.processo import Processo
processo = Processo(cnj='0000001-00.2017.1.00.0000', token='5a2283201f71da415748eadf2a2202caabae485f')
processo.carrega_ativo()

processo.ativo
# > True
```

Lança uma exceção do tipo `Processo.NaoCadastrado` caso nenhum processo seja encontrado.

Este método retorna `self` e permite encadeamento de métodos.


### `cliente.processo.Processo.favorita()`

Define processo como prioritário. Um processo prioritário é atualizado de hora em hora.


### `cliente.processo.Processo.desfavorita()`

Retira status de prioritário de um processo. Um processo com status não
prioritário é atualizado todos os dias.

```python
from cliente.processo import Processo
processo = Processo(cnj='0000001-00.2017.1.00.0000', token='5a2283201f71da415748eadf2a2202caabae485f')
processo.favorita()
Processo.carrega_ativo()
Processo.prioritario
# > True
processo.desfavorita()
Processo.carrega_ativo()
Processo.prioritario
# > False
```


### `cliente.processo.Processo.remove()`

Remove totalmente o processo com o CNJ passado. Este método faz exatamente o
mesmo que `cliente.processo.Processos.remove()`.

```python
from cliente.processo import Processo
processo = Processo(cnj='0000001-00.2017.1.00.0000', token='5a2283201f71da415748eadf2a2202caabae485f')
processo.remove()
# > True
```

Caso o processo não exista este método retornará `False`.


## `cliente.processo.Parte`

Um objeto do tipo `Parte` possui os seguintes atributos:
- nome
- designacao
- advogados (lista de objetos do tipo [Advogado](#advogado))


## `cliente.processo.Advogado`

Um objeto do tipo `Advogado` possui os seguintes atributos:
- nome
- oab


## `cliente.processo.Andamento`

Um objeto do tipo `Andamento` possui os seguintes atributos:
- id
- processo_id
- texto
- data (objeto do tipo `datetime`)
- complemento
- anexos (lista de objetos do tipo [Anexo](#anexo))


## `cliente.processo.Anexo`

Um objeto do tipo `Anexo` possui os seguintes atributos:
- id
- andamento_id
- nome_arquivo
- corrompido
- meta (metadados do anexo)


## `cliente.processo.Processos`

Classe utilizada para lidar com mais de um processo ao mesmo tempo. Esta classe
representa uma lista de objetos do tipo `Processo`.

Sua instanciação é igual à da classe `Processo`.


### `cliente.processo.Processos.carrega(cnj, inicio, fim, numero_andamentos)`

Método que busca todos os processos com um determinado CNJ e retorna
`self`. Caso não exista nenhum processo com o CNJ buscado, a lista 
interna da classe permanece vazia.

`inicio` e `fim` são datas que limitam o período de busca dos processos com
base no último andamento atualizado. Caso nenhum valor seja passado, serão
buscados todos os processos.

`numero_andamentos` indica quantos dos últimos andamentos serão carregados.
padrão é 100, um parâmetro pode ser passado caso se queira pegar um número
diferente.


```python
from cliente.processo import Processos
processos = Processos('0000001-00.2017.1.00.0000', token='5a2283201f71da415748eadf2a2202caabae485f')
processos.carrega()
processos[0]
# > <Processo instance at ... >
```


### `cliente.processo.Processos.remove()`

Remove totalmente o processo com o CNJ passado. Este método faz exatamente o
mesmo que `cliente.processo.Processo.remove()`.

```python
from cliente.processo import Processos
processo = Processos(cnj='0000001-00.2017.1.00.0000', token='5a2283201f71da415748eadf2a2202caabae485f')
processo.remove()
# > True
```

Caso o processo não exista este método retornará `False`.


## `cliente.oab.Oab`

Os objetos do tipo `Oab` representam os clientes advogados cadastrados no
sistema. Uma `Oab` pode fazer busca por processos associados àquele registro
ou verificar os processos cadastrados para aquela OAB, por exemplo.

Este objeto possui os seguintes atributos:
- id
- nome
- uf
- oab
- processos

### `cliente.oab.Oab.carrega()`

Método que carrega um advogado com base em seu registro da OAB. Esse registro é
na forma UF + Número OAB, por exemplo MG15001.

Lança uma exceção do tipo `Oab.NaoCadastrado` caso nenhum processo seja encontrado.

```python
from cliente.oab import Oab
advogado = Oab(registro='SP11234', token='5a2283201f71da415748eadf2a2202caabae485f')
advogado.carrega()
advogado.nome
# > João Doe
advogado.registro
# > SP11234
```

O registro de advogado é carregado apenas com base no registro da OAB, de forma
que se o nome estiver incorreto -- ou mesmo vazio -- ele será sobrescrito.

Este método retorna `self` e permite encadeamento de métodos.


### `cliente.oab.Oab.cadastra()`

Método que cadastra um advogado com base no nome e no registro da OAB passados
para o construtor.

É necessário passar tanto o registro quanto o nome do advogado.

```python
from cliente.oab import Oab
advogado = Oab(registro='SP11234', token='5a2283201f71da415748eadf2a2202caabae485f')
advogado.cadastra(nome='João Doe')
advogado.carrega()
advogado.nome
# > João Doe
advogado.processos
# > []
```

Este método retorna `self` e permite encadeamento de métodos.


### `cliente.oab.Oab.busca_processos()`

Enfileira todos os processos encontrados para aquela OAB.

```python
from cliente.oab import Oab
advogado = Oab(registro='SP11234', token='5a2283201f71da415748eadf2a2202caabae485f')
advogado.carrega().busca_processos()
```


## `cliente.tribunal.Tribunais`

Os objetos do tipo `Tribunais` são usados para se obter as informações dos
tribunais suportados. Através deste objeto é possível reaver objetos do tipo
`Tribunal` com as features de um tribunal específico.

Este objeto também utiliza o token de acesso à API.


### `cliente.tribunal.Tribunais.suportado(tribunal)`

Retorna `True` caso o tribunal seja suportado e `False` caso contrário.
`tribunal` é uma string com a sigla do tribunal ou com o número do mesmo.

```python
from cliente.tribunal import Tribunais
tribunais = Tribunais(token='5a2283201f71da415748eadf2a2202caabae485f')
tribunais.suportado('algum_nao_suportado')
# > False
tribunais.suportado('tjrs')
# > True
```


### `cliente.tribunal.Tribunais.obtem(tribunal)`

Retorna um objeto `Tribunal` referente ao atributo `tribunal` que é uma string
que pode ser o número do tribunal ou a sigla do mesmo.

```python
from cliente.tribunal import Tribunais
tribunais = Tribunais(token='5a2283201f71da415748eadf2a2202caabae485f')
tribunais.obtem('trt4')
# <cliente.tribunal.Tribunal at 0x7f5ed4207fd0>
```


## `cliente.tribunal.Tribunal`

Os objetos do tipo `Tribunal` são usados para obter os dados de um tribunal.
Este objeto só deve ser gerado através do `Tribunais.obtem()`.

Este objeto possui os seguintes atributos:
- numero
- suporta_oab
- sigla
- estados
- nome

```python
from cliente.tribunal import Tribunais
tribunais = Tribunais(token='5a2283201f71da415748eadf2a2202caabae485f')
tribunal = tribunais.obtem('trt4')
print(tribunal.estados)
# > ["PR", "RS", "SC"]
print(tribunal.nome)
# > TRF da 4a Região
tribunal = tribunais.obtem('nome_invalido')
# > KeyError: Este tribunal não é suportado
```


# Exceções

## `cliente.exceptions.ParametrosIncorretos`

Exceção lançada quando os parâmetros passados na requisição não estão corretos.
Exceção relativa ao status HTTP 400.


## `cliente.exceptions.TribunalNaoSuportado`

Exceção lançada quando se tenta cadastrar um processo cujo tribunal não é
suportado pela API.

## `Processo.NaoCadastrado` e `Oab.NaoCadastrado`

Exceção lançada *de dentro da classe* quando o elemento buscado não foi
cadastrado. Exceção relativa ao status  HTTP 404.


## `Processo.NaoCarregado` e `Oab.NaoCarregado`

Exceção lançada quando o processo, ou a OAB, ainda não foi carregado. Para que
este erro não seja lançado, basta buscas as informações antes de tentar acessar
os atributos, por exemplo `Processo.carrega_ativo()`, `Oab.carrega()`, etc.


# Alterando a URL de conexão

Quando criando uma conexão com a API, seja através de `Processo` ou de `Oab`, a
URL padrão de conexão é

    https://andamentos.justicafacil.com.br

Caso se queira acessar a API em uma URL diferente, basta passar como parâmetro
no construtor do objeto. Veja o exemplo:

```python
from cliente.oab import Oab
oab = andamentos.Oab('MG55000', token=algum_token, url='http://localhost:8000')
# Salva o advogado em uma API que roda em localhost
oab.cadastra('João Doe')
```


# Resposta da API

Quando um cliente se registra no sistema *Andamentos*, o mesmo deve fornecer uma
URL e um token para postback. Esses dados serão utilizados para que o sistema
informe ao cliente quando houver alguma atualização dos processos.

O sistema responde com uma requisição GET para a URL fornecida (usando o token,
também fornecido, conforme descrito acima) e com o CNJ do processo atualizado
como um parâmetro na *query string*.

O *Andamentos* interpreta qualquer código de status igual ou maior que 200 e
menor que 300 como um status de sucesso. 410 significa que o processo recebido
pelo cliente não é mais utilizado pelo mesmo, e deve ser removido. Qualquer
outro status de código fará com que o *Andamentos* tente reenviar a notificação.

**Atenção**: retornar um status 410 ao postback do *Andamentos* fará com que
aquele processo seja **removido**, pois está informando à API que aquele
recurso não existe mais.
