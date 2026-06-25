# InfoVis

Documentacao central do add-on InfoVis para Blender.

## Visao geral

O projeto e distribuido como um add-on Python com entrada em `__init__.py`, organizacao funcional em `modules/` e camada de apoio em `data/`. Esta documentacao foi reorganizada para refletir a estrutura real do repositorio, o fluxo de instalacao no Blender e o processo atual de release.

> Ponto de entrada recomendado para manutencao: leia primeiro Arquitetura, depois Desenvolvimento e entao a referencia tecnica do dominio que sera alterado.

## O que voce encontra aqui

- arquitetura do add-on e fluxo de inicializacao
- guia de utilizacao dos paineis do AddOn no Blender
- guia de desenvolvimento e release
- referencia por operadores, paineis, propriedades e camada de dados
- glossario dos termos e componentes recorrentes
- materiais de apoio para acompanhamento e manutencao documental

## Trilhas de leitura

| Objetivo | Comece aqui | Proximo passo |
|----------|-------------|---------------|
| Usar o AddOn no Blender | [Guia de Utilizacao](guides/GUIA_DE_UTILIZACAO.md) | [Glossario](reference/GLOSSARY.md) |
| Configurar a Lista de Itens | [Guia LI Mapping](guides/LI_MAPPING_GUIDE.md) | [Guia de Utilizacao](guides/GUIA_DE_UTILIZACAO.md) |
| Entender a estrutura do add-on | [Arquitetura](ARCHITECTURE.md) | [Glossario](reference/GLOSSARY.md) |
| Implementar mudancas no codigo | [Desenvolvimento](DEVELOPMENT.md) | Guias em `guides/` |
| Revisar operadores e paineis | [Operadores](guides/OPERATORS_DOCUMENTATION.md) | [Paineis](guides/PANELS_DOCUMENTATION.md) |
| Revisar modelo de dados | [Propriedades](guides/PROPERTIES_DOCUMENTATION.md) | [Dados](guides/DATA_DOCUMENTATION.md) |
| Obter contexto executivo | [Sumario Executivo](extra/SUMARIO_EXECUTIVO.md) | [Proximos Passos](extra/PROXIMOS_PASSOS.md) |

## Comece por perfil

### Para entender o projeto

- [Arquitetura](ARCHITECTURE.md)
- [Glossario](reference/GLOSSARY.md)

### Para desenvolver

- [Desenvolvimento](DEVELOPMENT.md)
- [Operadores](guides/OPERATORS_DOCUMENTATION.md)
- [Paineis](guides/PANELS_DOCUMENTATION.md)
- [Propriedades](guides/PROPERTIES_DOCUMENTATION.md)
- [Dados](guides/DATA_DOCUMENTATION.md)

### Para instalar e validar rapidamente

1. consulte o [Guia de Utilizacao](guides/GUIA_DE_UTILIZACAO.md) para o fluxo geral de uso
2. gere um zip com `build_release.bat` ou `build_release.sh`
3. instale o add-on no Blender por `Install from Disk`
4. valide com `Example/C3388.8_UN-31.ifc`

### Para revisar documentacao

1. valide os documentos principais desta pasta
2. execute `mkdocs build --strict` na raiz do repositorio
3. revise a navegacao gerada em `site/`

### Para contexto executivo ou acompanhamento

- [Sumario Executivo](extra/SUMARIO_EXECUTIVO.md)
- [Proximos Passos](extra/PROXIMOS_PASSOS.md)
- [Documentacao Concluida](extra/DOCUMENTACAO_CONCLUIDA.md)

## Estrutura rapida

```text
InfoVis/
|-- __init__.py
|-- auth.py
|-- data/
|-- docs/
|-- modules/
|-- resources/
|-- libs311/
`-- libs313/
```

## Publicacao da documentacao

Esta pasta `docs/` pode ser publicada com MkDocs usando a configuracao em `mkdocs.yml`.

Execute os comandos a partir da raiz do repositorio.

### Ambiente local

Comandos basicos:

```powershell
pip install -r requirements-docs.txt
mkdocs serve
```

Para build estatico:

```powershell
mkdocs build
```

Se o repositorio estiver no GitHub, o workflow `.github/workflows/docs.yml` publica a documentacao automaticamente no GitHub Pages para a branch configurada.

## Checklist rapido

- `README.md` alinhado com `docs/`
- `mkdocs build --strict` sem warnings bloqueantes
- links locais resolvendo corretamente
- workflow de docs apontando para a branch ativa
