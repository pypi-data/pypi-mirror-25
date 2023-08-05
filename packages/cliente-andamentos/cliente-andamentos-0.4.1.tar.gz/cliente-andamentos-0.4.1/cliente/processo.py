#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import arrow

from cliente import BaseAPI
from cliente.exceptions import AndamentoSemData


class ToDictMixin:
    """Adiciona capacidade de um pedaço da informação do processo
    ser convertido para um dicionário.

    Attributes:
        fields_to_dict tuple(str): Campos que serão adicionados ao dicionário.
    """

    fields_to_dict = ()

    def __iter__(self):
        for field in self.fields_to_dict:
            value = getattr(self, field)
            if isinstance(value, list):
                value = self._normaliza_lista(value)
            yield field, value

    def _normaliza_lista(self, values):
        result = []
        for v in values:
            if isinstance(v, ToDictMixin):
                v = dict(v)
            result.append(v)
        return result


class Parte(ToDictMixin):
    """Parte de um Processo."""

    fields_to_dict = ('nome', 'designacao', 'advogados')

    def __init__(self, dados):
        self.nome = dados['nome']
        self.designacao = dados['designacao']
        self.advogados = [Advogado(d) for d in dados['advogados']]


class Advogado(ToDictMixin):
    """Advogado de uma Parte."""

    fields_to_dict = ('nome', 'oab')

    def __init__(self, dados):
        self.nome = dados['nome']
        self.oab = dados['oab']


class Andamento(ToDictMixin):
    """Andamento de um Processo."""

    fields_to_dict = ('id', 'texto', 'complemento', 'anexos', 'data')

    def __init__(self, dados):
        self.id = dados['id']
        self.texto = re.sub(r'\s{2,}', ' ', dados['texto'])
        self.complemento = dados['complemento']
        self.anexos = [Anexo(d) for d in dados['anexos']]
        data = dados.get('data')
        if not data:
            raise AndamentoSemData()
        self.data = arrow.get(data).datetime


class Anexo(ToDictMixin):
    """Anexo de um andamento."""

    fields_to_dict = ('id', 'nome_arquivo', 'corrompido', 'meta')
    URL_DOWNLOAD = ('http://anexos.sij-andamentos.justicafacil.com.br'
                    '.s3-website-us-east-1.amazonaws.com/')

    def __init__(self, dados):
        self.id = dados['id']
        self.nome_arquivo = dados['nome_arquivo']
        self.corrompido = dados['corrompido']
        self.meta = dados['meta']

    def url(self):
        """URL para download do anexo"""
        return self.URL_DOWNLOAD + self.nome_arquivo


class Processo(BaseAPI, ToDictMixin):
    """Encapsula um processo buscado na API do SIJ-Andamentos.

    Todo processo buscado na API é representado por uma entidade desta classe.
    Os atributos desta classe correspondem aos atributos disponíveis na API.

    Args:
        cnj(str): Número CNJ no tipo 0000000-00.0000.0.00.0000
        token(str): Token de acesso à API
        url(str, optional): URL da API.

    Attributes:
        id(int): ID do processo na base de dados do SIJ-Andamentos
        cnj(str): CNJ do processo
        detalhes(dict): Detalhes do processo específicos do tribunal
        assuntos(:obj:`list` of :obj:`str`): Lista de assuntos de um processo
        instancia(int): Instância do processo. Pode ser 1, 2, 3 ou 4.
        status(int): Status do processo. De acordo com
            `cliente.processo.Processo.codigo_status`
        orgao_julgador(str): Orgão julgador do processo
        ultima_atualizacao(datetime.datetime): Última atualização daquele
            processo realizada
        ativo(bool): Define se a instância do processo está ativa
        partes(:obj:`list` of :obj:`cliente.processo.Parte`): Partes de um
            processo
        andamentos(:obj:`list` of :obj:`cliente.processo.Andamento`):
            Andamentos de um processo
    """

    fields_to_dict = (
        'id',
        'cnj',
        'detalhes',
        'assuntos',
        'instancia',
        'status',
        'orgao_julgador',
        'ultima_atualizacao',
        'ativo',
        'partes',
        'andamentos',
        'comarca',
        'tribunal',
    )

    novo = 0
    cadastrado = 1
    cadastro_invalido = 2
    sigiloso = 3

    codigo_status = {
        0: 'novo',
        1: 'cadastrado',
        2: 'cadastro_invalido',
        3: 'sigiloso',
    }

    def __init__(self, cnj, token, url=BaseAPI.URL_DEFAULT):
        super(Processo, self).__init__(token, url)
        self.cnj = cnj
        self.carregado = False
        self._id = None
        self._detalhes = None
        self._assuntos = None
        self._tribunal = None
        self._comarca = None
        self._instancia = None
        self._status = None
        self._orgao_julgador = None
        self._ultima_atualizacao = None
        self._ativo = None
        self._partes = None
        self._andamentos = None

    def cadastra(self):
        """Cadastra processo na API do SIJ-Andamentos

        Inicia-se uma busca pelas instâncias do processo na API. O processo em
        questão será incluído na busca diária por andamentos.

        Note:
            **Todas** as vezes que este método for chamado, o processo será
            buscado em todas as instâncias novamente. Usar este método é
            indicado caso se queira saber se o processo está em uma nova
            instância.
        """
        resposta = self.executa_processo(self.cnj, 'post')
        return self.valida_resposta(resposta)

    def favorita(self):
        """Marca todas as instâncias deste processo (CNJ) como prioritários

        Um processo prioritário é buscado de hora em hora.
        """
        payload = {'prioritario': True}
        resposta = self.executa_processo(self.cnj, 'patch', data=payload)
        self.valida_resposta(resposta)

    def desfavorita(self):
        """Marca todas as instâncias deste processo com prioridade normal

        Um processo com prioridade normal é buscado uma vez por dia.
        """
        payload = {'prioritario': False}
        resposta = self.executa_processo(self.cnj, 'patch', data=payload)
        self.valida_resposta(resposta)

    def carrega_ativo(self, numero_andamentos=None):
        """Carrega instância ativa do processo

        Um processo pode estar em mais de uma instância. O processo ativo é o
        processo que tem o andamento mais recente.
        """
        params = {'ativo': True}
        if numero_andamentos:
            params['numero_andamentos'] = numero_andamentos
        response = self._busca_processo(params)
        self.preenche(response)
        return self

    def remove(self):
        """Remove o processo deste objeto na API."""
        resposta = self.executa_processo(self.cnj, 'delete')
        removido = True
        try:
            self.valida_resposta(resposta)
        except self.NaoCadastrado:
            removido = False
        self.carregado = False
        return removido

    def _busca_processo(self, params):
        resposta = self.executa_processo(self.cnj, 'get', params=params)
        self.valida_resposta(resposta)
        return resposta.json()[0]

    def preenche(self, dados):
        self._id = dados['id']
        self._detalhes = dados['detalhes']
        self._assuntos = dados['assuntos']
        self._instancia = dados['instancia']
        self._tribunal = dados['tribunal']
        self._comarca = dados['comarca']
        self._status = dados['status']
        self._orgao_julgador = dados['orgao_julgador']
        self._ativo = dados['ativo']
        self._partes = [Parte(d) for d in dados['partes']]
        self._andamentos = [Andamento(d) for d in dados['andamentos']]

        data = arrow.get(dados.get('ultima_atualizacao'))
        self._ultima_atualizacao = data.datetime
        self.carregado = True

    def _check_carregado(self):
        if not self.carregado:
            raise self.NaoCarregado(
                'Utilize Processo.carrega_ativo() ou '
                'Processo.carrega_processos() antes de'
                ' tentar acessar algum atributo.')

    @property
    def id(self):
        self._check_carregado()
        return self._id

    @property
    def detalhes(self):
        self._check_carregado()
        return self._detalhes

    @property
    def assuntos(self):
        self._check_carregado()
        return self._assuntos

    @property
    def instancia(self):
        self._check_carregado()
        return self._instancia

    @property
    def status(self):
        self._check_carregado()
        return self._status

    @property
    def tribunal(self):
        self._check_carregado()
        return self._tribunal

    @property
    def comarca(self):
        self._check_carregado()
        return self._comarca

    @property
    def orgao_julgador(self):
        self._check_carregado()
        return self._orgao_julgador

    @property
    def ativo(self):
        self._check_carregado()
        return self._ativo

    @property
    def partes(self):
        self._check_carregado()
        return self._partes

    @property
    def andamentos(self):
        self._check_carregado()
        return self._andamentos

    @property
    def ultima_atualizacao(self):
        self._check_carregado()
        return self._ultima_atualizacao


class Processos(BaseAPI):
    """Busca por lista de processos com mesmo número CNJ

    Busca processos na API e os armazena em uma lista de tipos
    `cliente.processo.Processo`, de forma que os elementos podem ser acessados
    através do operador de índice.

    Args:
        cnj(`str`): Número CNJ no tipo 0000000-00.0000.0.00.0000
        token(`str`): Token de acesso à API
        url(`str`, optional): URL da API.
    """

    def __init__(self, cnj, token, url=BaseAPI.URL_DEFAULT):
        super(Processos, self).__init__(token, url)
        self.cnj = cnj
        self.carregado = False
        self._lista = []

    def carrega(self, inicio=None, fim=None, numero_andamentos=None):
        """Carrega todas as instâncias de um CNJ para uma lista de
        cliente.processo.Processo

        Quando este método é chamado, é feita uma busca por todas as instâncias
        de um processo, inclusive as inativas, criando uma lista de Processo.
        """
        params = {}
        if inicio:
            params['inicio'] = inicio
        if fim:
            params['fim'] = fim
        if numero_andamentos:
            params['numero_andamentos'] = numero_andamentos
        processos = self._busca_processos(params)
        for proc in processos:
            processo = Processo(self.cnj, self.token, self.url)
            processo.preenche(proc)
            self._lista.append(processo)
        return self

    def remove(self):
        """Remove o processo deste objeto na API."""
        resposta = self.executa_processo(self.cnj, 'delete')
        removido = True
        try:
            self.valida_resposta(resposta)
        except self.NaoCadastrado:
            removido = False
        self.carregado = False
        return removido

    def _busca_processos(self, params):
        resposta = self.executa_processo(self.cnj, 'get', params=params)
        self.valida_resposta(resposta)
        return resposta.json()

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError('Os índices precisam ser inteiros, não strings')
        return self._lista[key]
