# fiap-3sio-jellyfish

# Jellyfish | Global Solution 2024 - RM 86108

## Vídeos no YouTube e links necessários
Você pode acessar o vídeo pitch [neste link](https://youtu.be/H6mgEdQeqd0) e o vídeo técnico [neste link](https://youtu.be/H6mgEdQeqd0). 
Pode acessar todos os links úteis com documentações e entregas [neste link](https://github.com/viniciuscavalcante1/fiap-3sio-jellyfish/blob/main/docs/links/links.txt). Eles também estão disponíveis abaixo.

## Visão geral
Jellyfish é uma aplicação web simples e rápida para monitoramento e preservação da vida marinha, baseado em geolocalização, coleta de dados e reports.
O projeto foi desenvolvido para o Global Solution do primeiro semestre de 2024, avaliação global da FIAP, que neste semestre, teve o tema de preservação dos oceanos. 

## Funcionalidades
- Registro de avistamentos de vida marinha com fotos e localização.
- Solicitação de resgates de animais marinhos.
- Reporte de ameaças à vida marinha, como poluição e pesca ilegal.
- Exportação de dados coletados.
- Seção de aprendizado sobre vida marinha.
- Apoio a organizações de conservação marinha.

## Tecnologias Utilizadas
- Python
- FastAPI
- PostgreSQL
- HTML5, CSS3 e Javascript
- Jinja2 Templates
- Requests
- Microsserviços
- Autenticação JWT

## Instalação
1. Clone o repositório:
    ```bash
    git clone https://github.com/viniciuscavalcante1/fiap-3sio-jellyfish
    ```
2. Navegue até o diretório do projeto:
    ```bash
    cd fiap-3sio-jellyfish
    ```
3. Instale as dependências

## Uso
1. Em uma IDE (recomendo PyCharm), execute os arquivos `main` de cada microsserviço. 
2. Acesse a aplicação em seu navegador:
    ```
    http://localhost:8001/dashboard
    ```

## Documentação
### Documentação da API
A documentação interativa da API pode ser acessada através do Swagger ou Redoc:
- Swagger: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

### Escopo, requisitos funcionais e não funcionais
O escopo e os requisitos podem ser acessados através [deste link](https://github.com/viniciuscavalcante1/fiap-3sio-jellyfish/blob/main/docs/requisitos/requisitos.md)

### Documentação BPMN
A documentação BPMN (Business Process Model and Notation) pode ser acessada através dos seguintes links:

| Documentação BPMN       | Link                                                                                          |
|--------------------------|-----------------------------------------------------------------------------------------------|
| Pasta geral              | [Pasta Geral](https://github.com/viniciuscavalcante1/fiap-3sio-jellyfish/tree/main/docs/bpmn) |
| BPMN ameaça             | [BPMN Ameaça](https://github.com/viniciuscavalcante1/fiap-3sio-jellyfish/blob/main/docs/bpmn/bpmn_ameaca.svg) |
| BPMN autenticação       | [BPMN Autenticação](https://github.com/viniciuscavalcante1/fiap-3sio-jellyfish/blob/main/docs/bpmn/bpmn_autenticacao.svg) |
| BPMN avistamentos       | [BPMN Avistamentos](https://github.com/viniciuscavalcante1/fiap-3sio-jellyfish/blob/main/docs/bpmn/bpmn_avistamentos.svg) |
| BPMN exportação         | [BPMN Exportação](https://github.com/viniciuscavalcante1/fiap-3sio-jellyfish/blob/main/docs/bpmn/bpmn_exportacao.svg) |
| BPMN resgate            | [BPMN Resgate](https://github.com/viniciuscavalcante1/fiap-3sio-jellyfish/blob/main/docs/bpmn/bpmn_resgate.svg) |

### Protótipo não funcional
O protótipo não funcional pode ser acessado via PDF através [deste link](https://github.com/viniciuscavalcante1/fiap-3sio-jellyfish/blob/main/docs/prototipo_mockup_wireframe/prototipo.pdf) ou de forma interativa no Figma através [deste link](https://www.figma.com/design/ZCzcEoNQTC5eOO8mdAsutm/Untitled?node-id=0-1&t=tzwtaxMuXtuz0gbi-1).