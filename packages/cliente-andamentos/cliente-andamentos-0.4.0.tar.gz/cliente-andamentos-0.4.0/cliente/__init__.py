#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from cliente.exceptions import (
    ErroInesperadoServidor,
    NaoCadastrado,
    NaoCarregado,
    ParametrosIncorretos,
    StatusCodeNaoTratado,
    TimeoutServidor,
    TribunalNaoSuportado,
)


class BaseAPI(object):
    """Implementa interface básica com a API do SIJ-Andamentos

    Esta classe implementa chamadas à API e tratamento de dados. Esta não é uma
    classe fim e deve ser utilizada apenas através das classes "filha".
    """
    URL_DEFAULT = 'https://andamentos.justicafacil.com.br/'
    PATH_PROCESSO = 'api/v1/processos/'
    PATH_OAB = 'api/v1/oabs/'
    PATH_TRIBUNAL = 'api/v1/tribunais/'

    NaoCadastrado = NaoCadastrado
    NaoCarregado = NaoCarregado

    def __init__(self, token, url=URL_DEFAULT):
        self.token = token
        self.headers = {'Authorization': 'Token ' + token}
        self.url = url if url.endswith('/') else url + '/'

    def conectado(self):
        resposta = self._executa('auth/postback/')
        if resposta.status_code == 200:
            return True
        return False

    def _executa(self, path, method='get', params={}, data={}):
        dominio = self.url + path
        dominio = dominio if dominio.endswith('/') else dominio + '/'
        executa = getattr(requests, method)
        resposta = executa(
            dominio,
            data=data,
            params=params,
            headers=self.headers
        )
        return resposta

    def executa_processo(self, cnj=None, method='get', params={}, data={}):
        path = self.PATH_PROCESSO + cnj + '/' if cnj else self.PATH_PROCESSO
        resposta = self._executa(path, method, params=params, data=data)
        return resposta

    def executa_oab(self, registro=None, method='get', params={}, data={}):
        path = self.PATH_OAB + registro + '/' if registro else self.PATH_OAB
        resposta = self._executa(path, method, params=params, data=data)
        return resposta

    def executa_tribunal(self):
        resposta = self._executa(self.PATH_TRIBUNAL, 'get')
        return resposta

    def valida_resposta(self, resposta):
        """Valida um argumento do tipo `requests.resposta` vindo da API

        Valida uma resposta do tipo `requests.resposta` quanto ao status HTTP
        e retorna um booleano "created", indicando se algum recurso foi criado.
        """
        if resposta.status_code == 404:
            raise self.NaoCadastrado(response=resposta)
        elif resposta.status_code == 400:
            raise ParametrosIncorretos(response=resposta)
        elif resposta.status_code == 501:
            raise TribunalNaoSuportado(response=resposta)
        elif resposta.status_code == 502:
            raise ErroInesperadoServidor(response=resposta)
        elif resposta.status_code == 504:
            raise TimeoutServidor(response=resposta)
        elif resposta.status_code == 201:
            return True
        elif resposta.status_code == 200:
            return False
        elif resposta.status_code == 204:
            return None
        raise StatusCodeNaoTratado(response=resposta)
