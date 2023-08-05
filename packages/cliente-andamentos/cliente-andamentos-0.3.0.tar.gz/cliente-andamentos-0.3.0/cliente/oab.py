#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cliente import BaseAPI


class Oab(BaseAPI):
    """Encapsula um registro de advogado buscado na API do SIJ-Andamentos.

    Todo advogado (também denominado neste sistema por Oab) buscado na API é
    representado por uma entidade desta classe.  Os atributos desta classe
    correspondem aos atributos disponíveis na API.

    Args:
        registro(`str`): Registro da OAB do advogado no tipo RS12345
        token(`str`): Token de acesso à API
        url(`str`, optional): URL da API.

    Attributes:
        id(int): ID do advogado na base de dados do SIJ-Andamentos
        uf(str): UF do regitro da OAB
        oab(str): Número do registro da OAB
        nome(str): Nome do advogado
        processos(:obj:`list` of :obj:`str`): Lista de processos relacionados a
            uma OAB
    """

    def __init__(self, registro, token, url=BaseAPI.URL_DEFAULT):
        super(Oab, self).__init__(token, url)
        self.registro = registro
        self.carregado = False
        self._id = None
        self._uf = None
        self._oab = None
        self._nome = None
        self._processos = None

    def cadastra(self, nome):
        """Cadastra um registro de Advogado na API

        Se o registro da OAB ainda não existir na API, um novo advogado é
        cadastrado.
        """
        params = {
            'nome': nome,
            'registro': self.registro,
        }
        resposta = self.executa_oab(method='put', params=params)
        return self.valida_resposta(resposta)

    def carrega(self):
        """Carrega os dados de um registro de Advogado

        Os dados de um advogado são carregados para esta instância de Oab e
        podem ser acessadas pelos seus atributos.
        """
        resposta = self.executa_oab(self.registro, 'get')
        self.valida_resposta(resposta)
        self.preenche(resposta.json())
        return self

    def busca_processos(self):
        """Busca todos os processos de um advogado na API

        Para acessar os processos de um advogado, basta usar o método
        `cliente.oab.Oab.carrega()` novamente e acessar o atributo `processos`.

        Note:
            Entre a chamada por `busca_processos()` e o `carrega()`, deve haver
            um tempo, necessário para que o sistema cadastre os novos
            processos. Esse tempo vai depender da quantidade de processos
            encontrados para o registro OAB buscado.
        """
        resposta = self.executa_oab(self.registro, 'post')
        return self.valida_resposta(resposta)

    def preenche(self, dados):
        self._id = dados['id']
        self._uf = dados['uf']
        self._oab = dados['oab']
        self._nome = dados['nome']
        self._processos = dados['processos']
        self.carregado = True

    def _check_carregado(self):
        if not self.carregado:
            raise self.NaoCarregado(
                'Utilize Oab.carrega() antes de'
                ' tentar acessar algum atributo.')

    @property
    def id(self):
        self._check_carregado()
        return self._id

    @property
    def uf(self):
        self._check_carregado()
        return self._uf

    @property
    def oab(self):
        self._check_carregado()
        return self._oab

    @property
    def nome(self):
        self._check_carregado()
        return self._nome

    @property
    def processos(self):
        self._check_carregado()
        return self._processos
