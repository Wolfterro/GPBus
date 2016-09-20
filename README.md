# GPBus
## Liste e localize as linhas de ônibus disponíveis no município do Rio de Janeiro!

### Descrição:

#### Este é um simples programa em Python que possui a função de listar e localizar as linhas de ônibus disponíveis no município do Rio de Janeiro, utilizando a API do [data.rio](http://data.rio/dataset/gps-de-onibus) para recuperar as informações dos ônibus em tempo real e utilizando a API do [Google Maps Geocoding](https://developers.google.com/maps/documentation/geocoding/intro?hl=pt-br) para fazer a geocodificação reversa, isto é, utilizar as coordenadas recebidas para mostrar uma localização exata para o usuário.

#### O programa pergunta ao usuário um modo de busca, caso o usuário não tenha utilizado nenhuma opção pela linha de comando.

#### Há dois modos disponíveis, o modo de busca pela linha do ônibus e pelo número de ordem do ônibus. Ao buscar pela linha, o programa irá listar todos os ônibus daquela linha que estão circulando. Ao buscar pelo número de ordem, o programa irá listar apenas o ônibus que possuir aquele número.

#### Abaixo está uma demonstração de busca por uma linha de ônibus específica:

![GPBus](http://i.imgur.com/8guv6Ky.gif)

### Opções:

#### Aqui estão algumas opções disponíveis e que podem ser inseridas como argumentos pela linha de comando, simplificando a busca:

    Uso: ./GPBus-RJ.py [OPÇÕES] [LINHA / ORDEM]
    -------------------------------------------
    
    -a || --ajuda       Mostra o menu de ajuda.
    -h || --help        Mostra o menu de ajuda.
    -l || --linha       Faz a busca pelos ônibus através da linha desejada.
    -o || --ordem       Faz a busca pelos ônibus através do número de ordem desejado.

### Nota:

#### Este programa faz uso da API do Google Maps para decodificar a localização exata dos ônibus. Porém, há um limite diário de 2.500 verificações (1 ônibus = 1 verificação), caso exceda este limite, você poderá ficar sem a localização exata dos ônibus, mas poderá ainda possuir a latitude e longitude dos mesmos, podendo então verificar manualmente suas localizações.

#### Caso queira possuir um controle maior do uso de verificações ou queira um limite maior, adquira uma API Key pelo seguinte endereço: [https://developers.google.com/maps/documentation/geocoding/get-api-key?hl=pt-br](https://developers.google.com/maps/documentation/geocoding/get-api-key?hl=pt-br)

#### Para utilizar a sua API Key no programa, insira a chave dentro da variável GOOGLEAPI_KEY como uma string, que se localiza logo nas primeiras linhas do código-fonte do programa.

### Requerimentos:
- Python 2.x

### Download:

#### Você poderá baixar o programa utilizando o git:

    git clone https://github.com/Wolfterro/GPBus.git
    cd GPBus/
    chmod +x GPBus-RJ.py
    ./GPBus-RJ.py

#### Você também poderá utilizar o wget para baixar o programa:

    wget "https://raw.github.com/GPBus/master/GPBus-RJ.py"
    chmod +x GPBus-RJ.py
    ./GPBus-RJ.py

#### Caso não possua o git e queira também baixar o repositório por completo, baixe através deste [Link](https://github.com/Wolfterro/GPBus/archive/master.zip) ou clique em "Clone or Download", no topo da página.
