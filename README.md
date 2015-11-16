# EdisonGram
### Versão 1.0

EdisonGram - Código-fonte do programa Python criado para demonstração do bot de monitoramento com Telegram implementado em Intel Edison.

### Dependências
* Python 2.7 - Normalmente instalado por padrão no Poky Linux da Intel Edison

* Python-PIP - Pode ser instalado com o seguinte comando:

```sh
# opkg install python-pip
```

* OpenCV - Pode ser instalado com o seguinte comando:
```sh
# opkg install python-opencv
```

* MRAA - Já vem instalado por padrão no Poky Linux da Intel Edison.

* UPM - Já vem instalado por padrão no Poky Linux da Intel Edison.

* Biblioteca Telegram para Python - Orignal de [Telegram-Leandro] - Pode ser instalada pelo Python-PIP:
```sh
# pip install python-telegram-bot
```

### Estrutura de aplicação:
- Telegram - Faz a conexão com o sistema Telegram usando Token de autenticação para Bot.
- OpenCV - Biblioteca de visão computacional - Tira foto, reconhecimento facial, detecção de intruso, filtros, etc.
- ThingSpeak - Envia dados para 
- UPM  - [link-upm] - Biblioteca para integração de acesso e configuração a periféricos da Intel numa abstração alto-nível - Facilita MUITO mexer com os sensores e componentes do Kit Grove! Funciona integrado com MRAA.
- MRAA - [link-mraa] - Biblioteca para interface baixo-nível com componentes de I/Os, sensores e demais periférios da Intel.


### Tutorial para Criação de um Bot Telegram 
Para obter a sua chave de Bot Telegram, siga o tutorial mostrado em [telegram-bot].


### Desenvolvimento

Quer contribuir? Ótimo!

Copie o repositório, teste o código com seus Tokens, e me notifique de possíveis alterações e sugestões. 

Receberei feedback com o maior zelo possível!


Não tenha medo de testar/modificar a aplicação como bem quiser.

Iniciar a aplicação:
```sh
$ python edisonGram.py
```

### Todos

 - Testar com Intel Galileo - Bigger Linux Image
 - Adicionar mais comandos
 - Testes com Processamento de Linguagem Natural?
 - Aceito sugestões!

License
----

MIT


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [telegram-leandro]: <https://github.com/leandrotoledo/python-telegram-botr>
   [thingspeak]: <https://thingspeak.com>
   [@andremlcurvello]: <http://twitter.com/andremlcurvello>
   [link-upm]: <http://iotdk.intel.com/docs/master/upm/>
   [link-mraa]: <https://github.com/intel-iot-devkit/mraa
   [telegram-bot]: <https://core.telegram.org/bots>


