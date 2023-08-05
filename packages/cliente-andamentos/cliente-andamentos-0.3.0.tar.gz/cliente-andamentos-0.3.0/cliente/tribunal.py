#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cliente import BaseAPI


class Tribunais(BaseAPI):

    def __init__(self, token, url=BaseAPI.URL_DEFAULT):
        super(Tribunais, self).__init__(token, url)
        self.tribunais = None

    def _obtem_dados(self):
        resposta = self.executa_tribunal()
        self.valida_resposta(resposta)
        return resposta.json()['tribunais_suportados']

    def _tribunal_por_sigla(self, sigla):
        s = sigla.lower()
        for n, t in self.tribunais.items():
            if s == t['sigla']:
                return n
        return None

    def obtem(self, tribunal):
        if not self.tribunais:
            self.tribunais = self._obtem_dados()
        n = self._tribunal_por_sigla(tribunal) or tribunal
        t = self.tribunais.get(n, None)
        if t:
            return Tribunal(n, t)
        raise KeyError('Este tribunal não é suportado')

    def suportado(self, tribunal):
        try:
            self.obtem(tribunal)
        except KeyError:
            return False
        return True


class Tribunal(object):

    def __init__(self, tribunal_numero, tribunal_info):
        self.numero = tribunal_numero
        self.suporta_oab = tribunal_info['suporta_oab']
        self.sigla = tribunal_info['sigla']
        self.estados = tribunal_info['estados']
        self.nome = tribunal_info['nome']
