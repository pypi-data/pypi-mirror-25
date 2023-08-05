#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests.exceptions import HTTPError


class NaoCarregado(Exception):
    pass


class TribunalNaoSuportado(HTTPError):
    """O tribunal requisitado não é suportado pelo Andamentos.

    Em um número CNJ

        NNNNNNN-DD.AAAA.J.TR.OOOO

    os números "J" e "TR" representam o tribunal acessado para receber as
    informações do processo. Caso o tribunal não seja suportado, o Andamentos
    retorna um status code HTTP 501, e o Cliente-Andamentos lança então uma
    exceção `TribunalNaoSuportado`.

    Para obter informações dos tribunais suportados, veja `cliente.tribunal`.
    """
    pass


class ParametrosIncorretos(HTTPError):
    """Algum parâmetro está incorreto

    Esta exceção é uma representação do status code HTTP 400 e significa que
    algum dos parâmetros passados não pode ser compreendido pela API.
    """
    pass


class NaoCadastrado(HTTPError):
    """O processo ou advogado requisitados não existe na base de dados do
    Andamentos.

    O Cliente-Andamentos tentou realizar alguma ação que exige um recurso
    pré-cadastrado e este recurso não pode ser encontrado. Este erro é uma
    interface para o status code HTTP 404.
    """
    pass


class ErroInesperadoServidor(HTTPError):
    """O servidor não está funcionando corretamente

    Equivalente ao status code HTTP 502.
    """
    pass


class TimeoutServidor(HTTPError):
    """O servidor não respondeu dentro do tempo de timeout definido.

    Equivalente ao status code HTTP 504.
    """
    pass


class StatusCodeNaoTratado(HTTPError):
    """O status code HTTP retornado pela API não foi tratado. Contate os
    administradores da API.
    """
    pass


class AndamentoSemData(Exception):
    pass
