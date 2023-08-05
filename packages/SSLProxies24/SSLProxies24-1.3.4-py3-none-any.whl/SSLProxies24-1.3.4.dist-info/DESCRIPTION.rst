SSLProxies24Feed
================

|Build Status| |Codacy Badge| |codecov| |Maintainability|

SSL Proxies é um site onde é postado diariamente uma listagem de Proxys
para serem utilizados, claro que nem todos funcionam perfeitamente,
pensando nisso fiz esse pequeno código para possibilitar duas coisas.

-  Obter os Proxys postados (diretamente do Feed)
-  Testar um a um e só capturar os que realmente funcionam.

Como funciona?
==============

    | A requisição é feita no site `SSL Proxies`_, para ser mais exato,
      em seu feed, onde é capturado o XML e então formatado para a
      captura dos Proxys postados.
    | O que define um Proxy como válido? Bem, se a requisição feita com
      ele obteve sucesso. (dãh)

Requisitos:
^^^^^^^^^^^

-  Python >=3.6
-  Conexão com Internet moderada. (a velocidade de sua conexão
   influência na avaliação do Proxy)

Como Utilizar
^^^^^^^^^^^^^

-  | Coloque a pasta **SSLProxies24** em seu projeto e siga o script
     abaixo:
   | \`\`\`python

   .. rubric:: !/usr/bin/env python
      :name: usrbinenv-python

   .. rubric:: -*- coding: utf-8 -*-
      :name: coding-utf-8---

Autor: rique\_dev (rique_dev@hotmail.com)
=========================================

| from SSLProxies24.Feed import Feed
| from SSLProxies24.Check import CheckProxy

Recupera a listagem
===================

prx = Feed().PROXY\_LIST

Inicia classe
=============

chk = CheckProxy()

Começa validação
================

chk.validatelist(prx)

A partir de agora os Proxys já estão sendo validados dentro de uma Thread, para obter os dados você poderá utilizar:
====================================================================================================================

Contagem de sucesso:
====================

print(str(chk.getsucesscount()))

Contagem de Falhas:
===================

print(str(chk.getfailcount())))

Total de Proxys (geral)
=======================

print(str(chk.getproxycount()))

Listagem de Proxys já avaliados e liberados com sucesso
=======================================================

| print(chk.getproxylist())
| \`\`\`

Agradecimentos
~~~~~~~~~~~~~~

`SSL Proxies`_ por disponibilizar o serviço e o Feed.

Este projeto está sob licença **MIT**.
''''''''''''''''''''''''''''''''''''''

É isso pessoal, até a proxima 😆


Gráfico Coverage
----------------

|Coverage|

.. _SSL Proxies: http://www.sslproxies24.top/

.. |Build Status| image:: https://travis-ci.org/riquedev/SSLProxies24Feed.svg?branch=master
   :target: https://travis-ci.org/riquedev/SSLProxies24Feed
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/94104d284aa5420ca0d422defb0abd49
   :target: https://www.codacy.com/app/rique_dev/SSLProxies24Feed?utm_source=github.com&utm_medium=referral&utm_content=riquedev/SSLProxies24Feed&utm_campaign=Badge_Grade
.. |codecov| image:: https://codecov.io/gh/riquedev/SSLProxies24Feed/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/riquedev/SSLProxies24Feed
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/550fedf5d605a680f698/maintainability
   :target: https://codeclimate.com/repos/59bd9395ede9d502700015c6/maintainability
.. |Coverage| image:: https://codecov.io/gh/riquedev/SSLProxies24Feed/branch/master/graphs/commits.svg

