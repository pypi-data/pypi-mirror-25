#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: rique_dev (rique_dev@hotmail.com)

import gc
import re

import requests
from defusedxml import ElementTree


class Feed:
    # Fonte
    __URL = 'http://www.sslproxies24.top/feeds/posts/default'

    # Proxys Capturados
    PROXY_LIST = []

    # Result Count
    COUNT = 0

    # Remove caracteres desnecessários para identificação da Tag
    def __cleartag(self):
        return str(self.elemen.tag[str(self.elemen.tag).index('}') + 1:]).strip()

    # Pega tudo que tiver formato de Proxy dentro do HTML. [IP:PORT]
    @classmethod
    def __clearhtml(self, content):
        return re.findall('\d+\.\d+\.\d+\.\d+\:\d+', content)

    def __init__(self):
        gc.enable()
        # Lista temporária
        tmpList = []

        # Requisição   (stream)
        self.response = requests.get(self.__URL, stream=True)

        # GZip, Deflate.
        self.response.raw.decode_content = True

        # Events mdh
        self.events = ElementTree.iterparse(self.response.raw)

        # Percorrendo elementos...
        for self.event, self.elemen in self.events:

            # Limpa Tag
            tag = self.__cleartag()

            # Buscamos apenas esta.
            if tag == 'entry':

                # Hora de listar os proxys.
                for proxy in self.__clearhtml(list(self.elemen)[6].text):
                    # Adiciona a lista temporária
                    tmpList.append(proxy.strip())

        # Remove duplicatas
        self.PROXY_LIST = list(set(tmpList))

        # Contagem
        self.COUNT = len(self.PROXY_LIST)

        # Deleta lista temporária
        del tmpList
