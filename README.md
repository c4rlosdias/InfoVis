# InfoVis

Add-on para Blender voltado a visualizacao, inspecao e enriquecimento de informacoes IFC, com integracao a bSDD, estruturas de decomposicao, catalogo de tipos, conexoes e propriedades de objetos.

## Visao Geral

O projeto e distribuido como um add-on Python para Blender. A entrada principal fica em `__init__.py`, que registra preferencias, operadores de autenticacao, `OG_Properties` e todas as classes carregadas por `modules/get_classes()`.

Principais capacidades:

- leitura e navegacao de dados IFC
- consulta a classes e propriedades via bSDD
- visualizacao de decomposicao e arvore de elementos
- selecao de tipos e camadas de catalogo
- edicao e inspecao de propriedades e documentos
- exibicao de atributos IFC na viewport

## Requisitos

- Blender 5.0 ou superior
- Python embarcado do Blender compativel com o ambiente alvo
- Windows, Linux ou macOS

Observacoes sobre dependencias:

- no Windows, o add-on utiliza bibliotecas empacotadas em `libs311/` e `libs313/`
- em Linux e macOS, pacotes ausentes podem ser instalados no Python do Blender na inicializacao do add-on

## Instalacao

### Uso de release zipado

1. Gere ou obtenha um arquivo `.zip` do release.
2. No Blender, abra `Edit > Preferences > Add-ons`.
3. Clique em `Install from Disk`.
4. Selecione o arquivo `.zip` gerado em `releases/`.
5. Ative o add-on `InfoVis`.

### Instalacao para desenvolvimento

1. Clone ou copie este repositorio para um diretorio de trabalho.
2. Gere um pacote de release com um dos scripts abaixo:

```powershell
.\build_release.bat nome-do-release
```

```bash
./build_release.sh nome-do-release
```

3. Instale o zip gerado no Blender pelo fluxo de `Install from Disk`.

Se preferir instalar sem zip durante o desenvolvimento, copie a pasta do projeto para o diretorio de add-ons do Blender mantendo a estrutura atual e o nome do pacote consistente com `InfoVis`.

## Build de Release

Os scripts de build copiam os arquivos necessarios para `releases/InfoVis/` e geram um zip final em `releases/<nome>.zip`.

Arquivos e pastas incluidos no pacote:

- `__init__.py`
- `auth.py`
- `modules/`
- `data/`
- `libs311/`
- `libs313/`
- `resources/`

## Estrutura do Repositorio

```text
InfoVis/
|-- __init__.py
|-- auth.py
|-- build_release.bat
|-- build_release.sh
|-- data/
|-- docs/
|-- Example/
|-- libs311/
|-- libs313/
|-- modules/
|-- releases/
`-- resources/
```

### Modulos principais

- `modules/dictionary/`: integracao com bSDD e propriedades de classe
- `modules/decomposition/`: arvore de decomposicao e navegacao IFC
- `modules/catalog/`: tipos de produto e camadas
- `modules/connections/`: criacao e remocao de conexoes entre objetos
- `modules/props/`: propriedades, documentos e visualizacoes
- `modules/types/`: painel de tipos
- `modules/settings/`: informacoes do add-on e configuracoes visuais
- `modules/common/`: utilitarios compartilhados
- `modules/og_properties.py`: property group central da aplicacao

### Camadas de suporte

- `data/bsdd.py`: cliente para a API bSDD
- `data/catalog.py`: leitura de catalogo e importacao IFC
- `data/cde.py`: integracao com CDE
- `data/tree.py`: refresh de arvores e callbacks
- `data/ifc_utils.py`: funcoes auxiliares para IFC
- `resources/`: arquivos JSON de apoio

## Documentacao

Documentos principais:

- [docs/guides/GUIA_DE_UTILIZACAO.md](docs/guides/GUIA_DE_UTILIZACAO.md): uso do AddOn no Blender, paineis, fluxos e exportacoes
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): arquitetura do add-on, fluxo de inicializacao e organizacao por modulos
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md): setup, fluxo de trabalho e manutencao
- [docs/reference/GLOSSARY.md](docs/reference/GLOSSARY.md): termos recorrentes e convencoes

Guias detalhados:

- [docs/guides/LI_MAPPING_GUIDE.md](docs/guides/LI_MAPPING_GUIDE.md)
- [docs/guides/OPERATORS_DOCUMENTATION.md](docs/guides/OPERATORS_DOCUMENTATION.md)
- [docs/guides/PANELS_DOCUMENTATION.md](docs/guides/PANELS_DOCUMENTATION.md)
- [docs/guides/PROPERTIES_DOCUMENTATION.md](docs/guides/PROPERTIES_DOCUMENTATION.md)
- [docs/guides/DATA_DOCUMENTATION.md](docs/guides/DATA_DOCUMENTATION.md)

Documentos complementares:

- `docs/extra/` contem materiais de apoio gerencial e historico da documentacao

### Publicacao com MkDocs

O repositorio ja possui uma base inicial para publicacao da documentacao:

- `mkdocs.yml`
- `docs/index.md`
- `requirements-docs.txt`

Para publicar localmente:

```powershell
pip install -r requirements-docs.txt
mkdocs serve
```

Para gerar o site estatico:

```powershell
mkdocs build
```

Se o repositorio estiver hospedado no GitHub, o workflow em `.github/workflows/docs.yml` pode publicar automaticamente a documentacao via GitHub Pages.

## Fluxo de Desenvolvimento

1. Ajuste o codigo em `modules/`, `data/` ou `resources/`.
2. Reinstale ou recarregue o add-on no Blender.
3. Valide os paines e operadores afetados com um arquivo IFC de exemplo.
4. Gere um novo zip de release quando necessario.

## Arquivos de Exemplo

- `Example/C3388.8_UN-31.ifc`: arquivo IFC para testes manuais
- `graphic.html` e `layers.html`: artefatos auxiliares para visualizacao

## Observacoes

- `requirements.txt` lista dependencias Python do projeto, mas o empacotamento para Blender depende tambem das bibliotecas embarcadas em `libs311/` e `libs313/`.
- O nome exibido no Blender e definido em `bl_info` dentro de `__init__.py`.

