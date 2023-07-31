# BIPy - Processador BIP em Python

## Descrição
Projeto indicado pelo nosso professor Nuncio Perrella da matéra ECM245-Arquitetura e Organização de Computadores do Instituto Mauá de Tecnologia. No primeiro semestre, aprendemos sobre como é formado um processador BIP de arquitetura Havard. Analisamos a eletrônica por trás dele a partir do software Cedar Logic. A fim de melhorar o aprendizado dos futuros alunos, este projeto visa facilitar a programação neste processador via um executável em linguagem Python que simula o projeto do BIP criado no Cedar Logic, utilizado na matéria.

### BIP
BIP (Basic Instruction-set Processor) é um tipo de processador que foi utilizada nos primórdios da computação. Consiste em instruções simples (como subtração, adição, carregar, etc.), um conjunto de instruções é uma coleção de comandos em nível de máquina que um processador pode executar para realizar várias operações. Para o seu funcionamento, ele possui componentes chaves como o PC (Program Counter) e ACC (Accumulator). 

Ele possui duas memórias, uma onde se armazenam os dados e outra onde se armazenam as instruções, seguindo os preceitos da arquitetura Harvard.

É importante entendermos o funcionamento de processadores primordiais, para ampliar o nosso entendimento das máquinas atuais e o que pode ser feito para aprimorá-las.

![BIP ARQ](https://github.com/JoaoVitorBranco/BIPy/assets/81604963/8e55a893-30dc-4ac5-883f-c33a735fcc29)

## Como executar
Abra as releases, baixe o arquivo executável disponível para o seu Sistema Operacional. Extraia o arquivo, e abra o executável chamado *"BIPy.exe"*. Não editar nenhum conteúdo da pasta.

## Como testar
Para rodar a aplicação em mode de desenvolvedor, é necessário Python 3.9+, além de uma IDE para editar os arquivos. Clone o repositório para a sua máquina, e siga os seguintes passos de configuração: 

### Somente na primeira vez execute:

#### Windows

```console
python -m venv venv
```

#### Linux

```
virtualenv -p python3.10 venv
```

### Ativando a venv

#### Windows

```console
venv\Scripts\activate
```

#### Linux

```console
source venv/bin/activate
```

### Instalando os requirements

```console
pip install -e .

pip install -r requirements.txt
```

### Executar o arquivo `main.py` para inicializar o software

```console
cd src

python main.py
```

## Como utilizar
Para utilizar a nossa aplicação, você deve escrever os comandos (uma lista com todos as instruções e suas ações podem ser encontradas dentro da aba *Mais→Consulta*), dentro da **memória de programa**, e os dados na **memória de dados**. Fique atento, pois as colunas e linhas representam o lugar na memória que a informação está sendo armazenado. Desta forma, se algo for escrito na **primeira linha**, **terceira coluna**, quer dizer que esta informação está no endereço **0x002**. 

Para executar os comandos, antes de tudo, dê um *RESET*, e em seguida click no botão *STEP* para executar um comando por vez. Para executar o seu programa de forma mais automática, utilize a funcionalidade do *HALT*, que uma vez clicado, irá performar STEPs automático, a uma velocidade determinada pelo usuário (dentro da aba *Configurações→Setar Clock*).

Acima do display do acumulador, pode se encontrar um switch entre os modos de display (hexadecimal ou decimal) do acumulador, esta funcionalidade também pode ser encontrada na aba *Configurações→Alterar modo do acumulador*.

Tanto a Memória de Dados ou de Programa podem ser carregados (*Arquivos→Carregar*), salvos (*Arquivos→Salvar*) e/ou zerados (*Arquivos→Zerar Memória*) de forma independente de um ao outro. Outrossim, as memórias são mantidas pelo programa quando ele é encerrado, garantindo que nenhum progresso seja perdido.

As memórias podem ser salvas no formato **.cdm**. Além disso, a Memória de Dados pode ser carregada por meio de um arquivo **.cdm**, enquanto a Memória de Programa pode ser carragada apartir de um arquivo **.cdm** ou **.txt**. Caso opte por carregar a Memória de Programa com arquivo de texto, cada linha do arquivo deverá seguir o seguinte formato "\<nome do comando> \<valor>". Segue um exemplo de um arquivo no formato **.txt** reconhecido pelo programa:

```
LDI 001
STO 000
ADD 000
STO 001
ADD 000
STO 000
ADD 001
JUMP 003
```

A integração com arquivos **.txt** se deve ao fato do assemblador criado em Python, utilizado em aula, ler este formato.

## Atalhos dentro do programa
#### Atalhos da página principal
- *Ctrl+D*        → Abre a Memória de Dados
- *Ctrl+P*        → Abre a Memória de Programa
- *Ctrl+R*        → Reset
- *spacebar*      → Step
- *Ctrl+spacebar* → Halt
- *Ctrl+H*        → Abre o menu de configuração do clock
- *Ctrl+Shift+D*  → Altera o modo do acumulador para decimal
- *Ctrl+Shift+H*  → Altera o modo do acumulador para hexadecimal
#### Atalhos das páginas de memória
- *Ctrl+S*      → Salva a memória atual
- *Ctrl+O*      → Carrega uma nova memória
- *Ctrl+Del*    → Zera a memória atual

## Como contribuir
Caso queira contribuir com a nossa aplicação, você pode criar uma **issue** apontando bugs ou features novas, para que possamos dar a devida manutenção. Você também pode ajudar de forma ativa: crie um fork, modifique o que deseja e solicite um *pull request* para o repositório. Se acharmos pertinente, aceitaremos e creditaremos de forma devida.

## Contribuidores
- João Branco - [JoaoVitorBranco](https://github.com/JoaoVitorBranco)
- Pedro Mesquita - [pedrogjmesquita](https://github.com/pedrogjmesquita)
- Vitor Soller - [VgsStudio](https://github.com/VgsStudio)

## Agradecimentos especiais
Agradecemos as seguintes pessoas pelo apoio e contribuições no projeto:

- Prof. Nuncio Perrella - Supervisão

- Prof. Dr. Angelo Sebastião Zanini - Supervisão

- Tiago Perrella - Design

- Igor Improta - Assemblador
