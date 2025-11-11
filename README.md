# Sistema de Monitoramento Flask - Documentação Técnica

---

Aplicação hospedada no Render:
 https://socf-so-cloud-cei8.onrender.com/

## ÍNDICE

1. Visão Geral do Projeto
2. Arquitetura da Aplicação
3. Análise Detalhada do Código
4. Estrutura de Diretórios
5. Fluxo de Execução
6. Tecnologias e Bibliotecas
7. Padrões e Convenções
8. Funcionalidades Implementadas

---

## VISÃO GERAL DO PROJETO

Este projeto implementa uma aplicação web usando Flask que fornece monitoramento em tempo real de métricas do sistema operacional e do processo da aplicação. A aplicação expõe informações através de uma interface web e endpoints de API RESTful.

### Objetivo Principal

Criar um sistema de monitoramento leve que permite visualizar e consultar métricas do sistema como uso de CPU, consumo de memória, identificador de processo e informações do ambiente de execução.

### Características Técnicas

- Arquitetura monolítica baseada em Flask
- Coleta de métricas usando psutil
- Renderização server-side com Jinja2
- API RESTful para integração
- Suporte multiplataforma (Windows, Linux, macOS)

---

## ARQUITETURA DA APLICAÇÃO

### Camadas da Aplicação

A aplicação é estruturada em três camadas principais:

CAMADA DE COLETA DE DADOS
- Função xget_system_info()
- Responsável por interagir com o sistema operacional
- Coleta métricas em tempo real usando psutil
- Processa e formata os dados coletados

CAMADA DE APRESENTAÇÃO
- Rotas Flask (@xapp.route)
- Gerencia requisições HTTP
- Renderiza templates HTML
- Retorna dados em formato JSON

CAMADA DE VISUALIZAÇÃO
- Template HTML (index.html)
- Interface visual para o usuário
- Renderização dinâmica com Jinja2

### Padrão Arquitetural

O projeto segue um padrão MVC simplificado:

MODEL: Função xget_system_info() que obtém dados do sistema
VIEW: Template HTML que apresenta os dados
CONTROLLER: Rotas Flask que coordenam Model e View

---

## ANÁLISE DETALHADA DO CÓDIGO

### Importações e Dependências

```python
import os
```
PROPÓSITO: Fornece funções para interagir com o sistema operacional
USO NO CÓDIGO: Obter o PID do processo atual através de os.getpid()
TIPO: Biblioteca padrão do Python

```python
import platform
```
PROPÓSITO: Acessa dados sobre a plataforma de hardware e sistema operacional
USO NO CÓDIGO: Detectar o nome do sistema operacional (Windows, Linux, Darwin)
TIPO: Biblioteca padrão do Python

```python
import psutil
```
PROPÓSITO: Biblioteca para recuperar informações sobre processos e utilização do sistema
USO NO CÓDIGO: Coletar métricas de CPU, memória e informações de processos
TIPO: Biblioteca externa (precisa ser instalada)
FUNCIONALIDADES USADAS:
- psutil.Process(): Cria objeto representando um processo
- memory_info(): Retorna informações sobre uso de memória
- cpu_percent(): Retorna percentual de uso de CPU

```python
from flask import Flask, jsonify, render_template
```
PROPÓSITO: Framework web para Python
COMPONENTES IMPORTADOS:
- Flask: Classe principal para criar a aplicação web
- jsonify: Converte dicionários Python para formato JSON
- render_template: Renderiza templates HTML com dados dinâmicos

```python
try:
    import distro
except:
    pass
```
PROPÓSITO: Detectar a distribuição Linux específica (Ubuntu, Fedora, etc.)
TRATAMENTO DE ERRO: Usa try-except porque esta biblioteca só funciona em Linux
COMPORTAMENTO: Se falhar, o código continua funcionando normalmente

---

### Inicialização da Aplicação

```python
xapp = Flask(__name__)
```

ANÁLISE DETALHADA:

Flask(__name__)
- Cria uma instância da aplicação Flask
- __name__ é passado para que o Flask saiba onde procurar recursos (templates, arquivos estáticos)
- Quando executado diretamente, __name__ será '__main__'
- Quando importado, __name__ será o nome do módulo

xapp
- Convenção de nomenclatura usada no projeto (prefixo 'x')
- Poderia ser apenas 'app', mas o desenvolvedor optou por usar 'xapp'
- Esta variável representa toda a aplicação web

---

### Função de Coleta de Métricas

```python
def xget_system_info():
    """Coleta informações do sistema"""
```

PROPÓSITO: Centralizar a lógica de coleta de métricas do sistema
TIPO DE RETORNO: Dicionário contendo todas as métricas
QUANDO É CHAMADA: Sempre que uma rota precisa dos dados do sistema

#### Análise Linha por Linha

```python
xprocess = psutil.Process(os.getpid())
```
FUNCIONAMENTO:
- os.getpid() retorna o PID (Process ID) do processo Python atual
- psutil.Process() cria um objeto que representa esse processo específico
- Este objeto permite consultar informações sobre o processo

POR QUE É NECESSÁRIO:
- Para obter métricas específicas do processo da aplicação Flask
- Sem isso, não conseguiríamos saber quanto de CPU/memória a aplicação está usando

```python
xpid = os.getpid()
```
FUNCIONAMENTO:
- Armazena o PID do processo atual em uma variável
- PID é um número único que identifica cada processo no sistema operacional

UTILIDADE:
- Útil para identificar o processo em ferramentas de monitoramento
- Permite encontrar o processo no gerenciador de tarefas
- Necessário para debugging e troubleshooting

```python
xmemory_mb = xprocess.memory_info().rss / (1024 * 1024)
```
ANÁLISE TÉCNICA:

xprocess.memory_info()
- Retorna um objeto com várias métricas de memória
- Inclui RSS, VMS, shared, text, data, lib, etc.

.rss (Resident Set Size)
- Memória física (RAM) atualmente usada pelo processo
- Não inclui memória swapped para disco
- É a métrica mais relevante para uso real de memória

/ (1024 * 1024)
- Conversão de bytes para megabytes
- 1024 bytes = 1 kilobyte
- 1024 kilobytes = 1 megabyte
- Resultado final em MB é mais legível para humanos

```python
xcpu_percent = xprocess.cpu_percent(interval=0.1)
```
ANÁLISE TÉCNICA:

cpu_percent()
- Calcula o percentual de uso de CPU do processo
- Retorna um número entre 0.0 e 100.0 (ou mais em sistemas multi-core)

interval=0.1
- Período de amostragem em segundos
- A função espera 0.1 segundo para calcular a média
- Sem interval, a primeira chamada sempre retorna 0.0

POR QUE 0.1 SEGUNDO:
- Balanço entre precisão e performance
- Intervalo muito curto: dados imprecisos
- Intervalo muito longo: aplicação fica lenta

COMPORTAMENTO EM MULTI-CORE:
- Em um sistema com 4 cores, pode retornar até 400%
- 100% = um core totalmente utilizado

```python
xos_name = platform.system()
```
FUNCIONAMENTO:
- Retorna o nome do sistema operacional
- Valores possíveis: 'Windows', 'Linux', 'Darwin' (macOS), 'Java'

USO:
- Identificar em qual plataforma a aplicação está rodando
- Útil para logs e debugging

```python
try:
    import distro
    xdistro_name = distro.name()
    xos_info = f"{xos_name} ({xdistro_name})"
except:
    xos_info = xos_name
```
ANÁLISE DO BLOCO TRY-EXCEPT:

BLOCO TRY:
- Tenta importar a biblioteca distro
- distro.name() retorna o nome da distribuição Linux (ex: "Ubuntu 22.04")
- Cria string formatada combinando SO e distribuição

BLOCO EXCEPT:
- Captura qualquer exceção (ImportError, AttributeError, etc.)
- Se falhar, usa apenas o nome do SO sem a distribuição
- Garante que o código funcione em Windows e macOS

POR QUE É NECESSÁRIO:
- distro só funciona em sistemas Linux
- Em Windows/macOS, distro.name() causaria erro
- O try-except torna o código robusto e multiplataforma

F-STRING:
- f"{xos_name} ({xdistro_name})"
- Sintaxe moderna do Python (3.6+) para formatação de strings
- Resultado: "Linux (Ubuntu 22.04)" ou "Windows" ou "Darwin"

```python
return {
    "pid": xpid,
    "memoria_mb": round(xmemory_mb, 2),
    "cpu_percent": xcpu_percent,
    "sistema_operacional": xos_info
}
```
ESTRUTURA DE RETORNO:

Tipo: Dicionário Python (equivalente a JSON)

Campos:
- pid: Inteiro (número do processo)
- memoria_mb: Float arredondado para 2 casas decimais
- cpu_percent: Float (pode ter várias casas decimais)
- sistema_operacional: String (nome do SO e distribuição)

round(xmemory_mb, 2):
- Arredonda o valor de memória para 2 casas decimais
- Exemplo: 45.6789123 vira 45.68
- Torna o valor mais legível

POR QUE USAR DICIONÁRIO:
- Fácil conversão para JSON
- Auto-documentado (nomes das chaves)
- Flexível para adicionar novos campos

---

### Rotas da Aplicação

#### Rota 1: Página Principal

```python
@xapp.route('/')
def xhome():
    """Página principal com todas as informações"""
    xinfo = xget_system_info()
    xinfo['nome'] = 'João Otávio Andreotti'
    return render_template('index.html', info=xinfo)
```

ANÁLISE DO DECORATOR:

@xapp.route('/')
- Decorator que registra a função como manipulador de rota
- '/' indica a raiz do site (http://localhost:5000/)
- Método HTTP padrão: GET

FUNCIONAMENTO DA FUNÇÃO:

xinfo = xget_system_info()
- Chama a função de coleta de métricas
- Retorna dicionário com todas as informações

xinfo['nome'] = 'João Otávio Andreotti'
- Adiciona campo 'nome' ao dicionário existente
- Mutação do dicionário (modifica o objeto original)
- Este campo não está na função xget_system_info() original

return render_template('index.html', info=xinfo)
- render_template(): Função do Flask para renderizar HTML
- 'index.html': Nome do arquivo de template (procura em /templates)
- info=xinfo: Passa o dicionário para o template com nome 'info'

FLUXO COMPLETO:
1. Usuário acessa http://localhost:5000/
2. Flask chama a função xhome()
3. xhome() coleta métricas do sistema
4. Adiciona nome do desenvolvedor
5. Renderiza template HTML com os dados
6. Retorna HTML formatado para o navegador

#### Rota 2: Informações do Desenvolvedor

```python
@xapp.route('/info')
def xinfo_route():
    """Rota que retorna apenas o nome dos integrantes em JSON"""
    return jsonify({
        "nome": "João Otávio Andreotti"
    })
```

ANÁLISE:

@xapp.route('/info')
- Endpoint: http://localhost:5000/info
- Rota simples e específica

jsonify({...})
- Converte dicionário Python para resposta JSON
- Define Content-Type: application/json automaticamente
- Trata serialização de tipos Python para JSON

POR QUE ESTA ROTA EXISTE:
- Fornece identificação do desenvolvedor
- Útil para APIs que precisam saber quem mantém o serviço
- Endpoint leve para health checks
- Não requer coleta de métricas (mais rápido)

RESPOSTA HTTP:
- Status: 200 OK
- Content-Type: application/json
- Body: {"nome": "João Otávio Andreotti"}

#### Rota 3: Métricas Completas

```python
@xapp.route('/metricas')
def xmetricas():
    """Rota que retorna todas as métricas em JSON"""
    xinfo = xget_system_info()
    xinfo['nome'] = 'João Otávio Andreotti'
    return jsonify(xinfo)
```

ANÁLISE:

Diferença da rota '/':
- Esta retorna JSON em vez de HTML
- Útil para integração com outras aplicações
- Pode ser consumida por scripts, dashboards, monitoramento

PROCESSO:
1. Coleta métricas do sistema
2. Adiciona nome do desenvolvedor
3. Converte tudo para JSON
4. Retorna resposta JSON

USO PRÁTICO:
- Sistemas de monitoramento podem fazer polling desta rota
- Scripts podem processar os dados programaticamente
- Dashboards podem exibir as métricas em tempo real

EXEMPLO DE RESPOSTA:
```
{
  "pid": 12345,
  "memoria_mb": 45.67,
  "cpu_percent": 2.5,
  "sistema_operacional": "Linux (Ubuntu 22.04)",
  "nome": "João Otávio Andreotti"
}
```

---

### Inicialização do Servidor

```python
APP = xapp
```

PROPÓSITO:
- Cria uma referência alternativa para a aplicação Flask
- Convenção WSGI (Web Server Gateway Interface)
- Alguns servidores de produção procuram por variável 'APP' ou 'application'

POR QUE É ÚTIL:
- Compatibilidade com diferentes servidores (Gunicorn, uWSGI)
- Permite usar tanto 'xapp' quanto 'APP' para referenciar a aplicação

```python
if __name__ == '__main__':
    xapp.run(debug=True, host='0.0.0.0', port=5000)
```

ANÁLISE COMPLETA:

if __name__ == '__main__':
- Verifica se o script está sendo executado diretamente
- Se importado como módulo, este bloco não executa
- Padrão comum em Python para código executável

xapp.run()
- Inicia o servidor de desenvolvimento do Flask
- Aguarda requisições HTTP

PARÂMETROS:

debug=True
- Ativa modo de debug
- Recarrega automaticamente quando o código muda
- Mostra mensagens de erro detalhadas no navegador
- NUNCA use em produção (expõe informações sensíveis)

host='0.0.0.0'
- Aceita conexões de qualquer interface de rede
- '0.0.0.0' = todas as interfaces (localhost, IP local, etc.)
- Permite acesso de outros computadores na rede
- Alternativa: '127.0.0.1' (apenas localhost)

port=5000
- Define a porta onde o servidor escutará
- Padrão do Flask
- URL de acesso: http://localhost:5000

MODO DEBUG - RECURSOS:
- Reloader: Reinicia automaticamente ao detectar mudanças
- Debugger: Interface web para debug de exceções
- Logs detalhados no terminal

---

## ESTRUTURA DE DIRETÓRIOS

```
projeto/
│
├── app.py
│   └── Arquivo principal com toda a lógica da aplicação
│       - Importações de bibliotecas
│       - Inicialização do Flask
│       - Função de coleta de métricas
│       - Definição das rotas
│       - Configuração do servidor
│
├── templates/
│   └── index.html
│       └── Template HTML para a interface web
│           - Estrutura HTML
│           - CSS embutido para estilização
│           - Tags Jinja2 para dados dinâmicos
│
└── (outros arquivos possíveis)
    ├── requirements.txt (lista de dependências)
    ├── .gitignore (arquivos ignorados pelo Git)
    └── README.md (documentação)
```

### Por Que Esta Estrutura

PASTA templates/:
- Convenção do Flask
- Flask procura templates automaticamente nesta pasta
- Usar outro nome requer configuração adicional

ARQUIVO app.py:
- Nome comum para aplicação Flask principal
- Poderia ter qualquer nome
- Facilita identificação do ponto de entrada

SEPARAÇÃO DE CONCERNS:
- Lógica Python em .py
- Apresentação em .html
- Facilita manutenção e testes

---

## FLUXO DE EXECUÇÃO

### Inicialização da Aplicação

PASSO 1: Execução do Script
- Usuário executa: python app.py
- Python interpreta o arquivo linha por linha

PASSO 2: Importações
- Carrega os módulos necessários (os, platform, psutil, Flask)
- Valida se todas as dependências estão instaladas

PASSO 3: Criação da Aplicação
- Flask(__name__) instancia a aplicação
- Registra as rotas com os decorators

PASSO 4: Início do Servidor
- xapp.run() inicia o servidor HTTP
- Servidor fica aguardando requisições na porta 5000

### Processamento de Requisições

REQUISIÇÃO PARA '/'

1. Cliente faz requisição GET para http://localhost:5000/
2. Flask identifica a rota '/' e chama xhome()
3. xhome() executa xget_system_info()
4. xget_system_info() coleta métricas:
   - Obtém PID do processo
   - Consulta uso de memória
   - Calcula uso de CPU
   - Detecta sistema operacional
5. Função retorna dicionário com métricas
6. xhome() adiciona campo 'nome'
7. render_template() processa index.html com os dados
8. Jinja2 substitui {{}} pelos valores reais
9. HTML final é retornado ao cliente
10. Navegador renderiza a página

REQUISIÇÃO PARA '/info'

1. Cliente faz requisição GET para http://localhost:5000/info
2. Flask identifica a rota '/info' e chama xinfo_route()
3. xinfo_route() cria dicionário simples com nome
4. jsonify() converte para JSON
5. JSON é retornado ao cliente
6. Cliente recebe {"nome": "João Otávio Andreotti"}

REQUISIÇÃO PARA '/metricas'

1. Cliente faz requisição GET para http://localhost:5000/metricas
2. Flask identifica a rota '/metricas' e chama xmetricas()
3. xmetricas() executa xget_system_info()
4. Adiciona campo 'nome' ao dicionário
5. jsonify() converte tudo para JSON
6. JSON com todas as métricas é retornado
7. Cliente recebe JSON completo

---

## TECNOLOGIAS E BIBLIOTECAS

### Flask

TIPO: Microframework web para Python
VERSÃO MÍNIMA: 2.0

CARACTERÍSTICAS:
- Leve e minimalista
- Fácil de aprender
- Flexível e extensível
- Baseado em Werkzeug (WSGI) e Jinja2 (templates)

USO NO PROJETO:
- Gerenciamento de rotas HTTP
- Renderização de templates
- Serialização JSON
- Servidor de desenvolvimento

COMPONENTES UTILIZADOS:
- Flask: Classe principal da aplicação
- @app.route: Decorator para definir rotas
- render_template: Renderização de HTML
- jsonify: Conversão para JSON

### psutil

TIPO: Biblioteca para informações de sistema e processos
VERSÃO MÍNIMA: 5.0

CARACTERÍSTICAS:
- Cross-platform (Windows, Linux, macOS)
- Acesso a informações de processos
- Métricas de CPU, memória, disco, rede
- Usado por ferramentas de monitoramento profissionais

USO NO PROJETO:
- psutil.Process(): Objeto representando processo
- memory_info().rss: Uso de memória física
- cpu_percent(): Percentual de uso de CPU

ALTERNATIVAS:
- os.popen() com comandos do sistema (menos portável)
- /proc filesystem no Linux (não funciona em Windows)
- wmi no Windows (não funciona em Linux)

### platform

TIPO: Módulo built-in do Python
VERSÃO: Incluso no Python

CARACTERÍSTICAS:
- Informações sobre hardware e SO
- Não requer instalação
- Cross-platform

USO NO PROJETO:
- platform.system(): Nome do sistema operacional

FUNÇÕES DISPONÍVEIS:
- system(): 'Windows', 'Linux', 'Darwin'
- release(): Versão do SO
- machine(): Arquitetura (x86_64, ARM, etc.)
- processor(): Informações do processador

### distro

TIPO: Biblioteca para detectar distribuição Linux
VERSÃO MÍNIMA: 1.5

CARACTERÍSTICAS:
- Específica para Linux
- Detecta Ubuntu, Fedora, Debian, etc.
- Substitui platform.linux_distribution() (removido no Python 3.8)

USO NO PROJETO:
- distro.name(): Nome da distribuição
- Usado dentro de try-except (opcional)

POR QUE É OPCIONAL:
- Não funciona em Windows/macOS
- Aplicação funciona sem ela
- Apenas adiciona informação extra no Linux

---

## PADRÕES E CONVENÇÕES

### Nomenclatura com Prefixo 'x'

OBSERVAÇÃO: Todas as variáveis e funções usam prefixo 'x'

EXEMPLOS:
- xapp (em vez de app)
- xget_system_info (em vez de get_system_info)
- xhome (em vez de home)
- xprocess, xpid, xmemory_mb, etc.

POSSÍVEIS RAZÕES:
- Convenção pessoal do desenvolvedor
- Evitar conflitos com palavras reservadas
- Padronização do código
- Identificação visual

IMPACTO:
- Funcionalidade não é afetada
- Torna o código único e identificável
- Pode dificultar leitura para outros desenvolvedores

### Estrutura de Rotas

PADRÃO RESTful IMPLEMENTADO:

GET /
- Retorna interface visual (HTML)
- Para consumo humano

GET /info
- Retorna identificação básica (JSON)
- Endpoint leve

GET /metricas
- Retorna dados completos (JSON)
- Para consumo programático

SEPARAÇÃO DE RESPONSABILIDADES:
- Uma rota para humanos (HTML)
- Duas rotas para máquinas (JSON)
- Dados separados por finalidade

### Tratamento de Erros

ABORDAGEM ATUAL:

try-except para distro
- Único tratamento de erro explícito
- Permite código multiplataforma

SEM TRATAMENTO EXPLÍCITO:
- Erros de psutil não são tratados
- Erros de renderização não são tratados
- Flask mostra página de erro padrão em debug

MELHORIAS POSSÍVEIS:
- Adicionar error handlers do Flask
- Validar se psutil está disponível
- Tratar exceções em xget_system_info()

### Configuração

MODO DEBUG:

debug=True
- Apropriado para desenvolvimento
- NUNCA usar em produção

SEGURANÇA:
- Expõe código-fonte em erros
- Permite execução de código arbitrário
- Desativa proteções do Werkzeug

HOST E PORTA:

host='0.0.0.0'
- Permite acesso externo
- Necessário para containers Docker
- Cuidado em redes públicas

port=5000
- Porta padrão do Flask
- Pode conflitar com outros serviços
- Pode ser alterada conforme necessidade

---

## FUNCIONALIDADES IMPLEMENTADAS

### Monitoramento de Processo

MÉTRICA: Process ID (PID)
- Identifica unicamente o processo
- Útil para ferramentas de sistema
- Muda a cada execução

COLETA: os.getpid()
- Função do módulo os
- Retorna inteiro
- Sempre disponível

### Monitoramento de Memória

MÉTRICA: Uso de memória em MB
- RSS (Resident Set Size)
- Memória física em uso
- Não inclui swap

COLETA: psutil.Process().memory_info().rss
- Em bytes
- Convertido para MB
- Arredondado para 2 decimais

INTERPRETAÇÃO:
- Valor baixo: Aplicação leve
- Valor crescente: Possível memory leak
- Valor estável: Comportamento normal

### Monitoramento de CPU

MÉTRICA: Percentual de uso de CPU
- Média durante 0.1 segundo
- Pode exceder 100% em multi-core
- Varia constantemente

COLETA: psutil.Process().cpu_percent(interval=0.1)
- Bloqueia por 0.1 segundo
- Retorna float
- Específico do processo

INTERPRETAÇÃO:
- 0-10%: Uso baixo (ocioso)
- 10-50%: Uso moderado
- 50-100%: Uso intenso
- >100%: Múltiplos cores sendo usados

### Detecção de Sistema Operacional

MÉTRICA: Nome do SO e distribuição
- Sistema base (Windows, Linux, Darwin)
- Distribuição Linux (se aplicável)
- Versão (em alguns casos)

COLETA: platform.system() + distro.name()
- Multiplataforma
- Robusto
- Informativo

EXEMPLOS DE RETORNO:
- "Windows"
- "Linux (Ubuntu 22.04)"
- "Darwin"
- "Linux (Fedora 38)"

### Interface Web

TECNOLOGIA: HTML + CSS + Jinja2
- Server-side rendering
- Sem JavaScript necessário
- Responsivo via CSS

FUNCIONALIDADE:
- Exibe todas as métricas
- Atualiza a cada reload
- Design simples e limpo

### API RESTful

ENDPOINTS JSON:
- /info: Identificação
- /metricas: Dados completos

FORMATO: JSON
- Fácil de processar
- Padrão web
- Compatível com qualquer linguagem

USO PRÁTICO:
- Integração com dashboards
- Monitoramento automatizado
- Scripts de coleta de dados
