#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: rique_dev (rique_dev@hotmail.com)

import gc
import threading
import time
import requests


class CheckProxy:
    # Listagem de Proxys (funcional)
    __goodList: list = []

    # Listagem de Proxis (geral)
    __proxylist: list = []

    # Timeout setado
    __timeout: int = 15

    # Sleeptime setado
    __sleeptime: int = 5

    # Contagem de Proxys ( aceitos )
    __count: int = 0

    # Total de conexões que resultaram em sucesso
    __sucess: int = 0

    # Total de conexões que resultaram em falha
    __fail: int = 0
    th: threading.Thread

    def __init__(self):
        # Ativa o Garbage Collector
        gc.enable()

    # Valida a lista de proxys passados

    def validatelist(self, proxyList: list, timeout: int = 15, sleeptime: int = 5):
        # Listagem de Proxys
        self.__proxylist = proxyList

        # Timeout escolhido
        self.__timeout = timeout

        # Sleep de conexão
        self.__sleeptime = sleeptime

        # Thread de validação
        self.th = threading.Thread(target=self.__validate, daemon=True)
        self.th.start()

    # Validação da listagem (Thread)

    def __validate(self):

        # Avaliando um proxy por vez

        for proxy in self.__proxylist:
            # Prepara dict de proxy
            prx = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
            try:
                # Tenta conexão
                r = requests.get('https://www.youtube.com/', proxies=prx, timeout=self.__timeout,
                                 headers={'Cache-Control': 'no-cache'})
                r.close()
            except Exception:
                self.__fail += 1
                # Aguarda um tempo para tentar uma nova conexão
                time.sleep(self.__sleeptime)
                continue
            else:
                self.__sucess += 1
                self.__goodList.append(proxy)
                # print('Proxy ' + proxy + ' foi aceito.')

        self.__count = len(self.__goodList)

    def join(self):
        self.th.join()

    def getproxylist(self) -> list:
        return self.__goodList

    def getsucesscount(self) -> int:
        return self.__sucess

    def getfailcount(self) -> int:
        return self.__fail

    def getproxycount(self) -> int:
        return len(self.__proxylist)
