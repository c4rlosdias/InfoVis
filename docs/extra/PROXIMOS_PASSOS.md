# Proximos Passos

## Objetivo

Este documento lista as acoes mais uteis para manter a documentacao do InfoVis consistente com a evolucao do add-on.

## Prioridade imediata

1. validar no Blender o fluxo descrito em `README.md` e `docs/DEVELOPMENT.md`
2. revisar se os paineis e operadores documentados ainda correspondem ao comportamento atual
3. atualizar exemplos quando houver mudanca de interface, nomenclatura ou fluxo de release

## Curto prazo

### 1. Adicionar evidencia visual

- incluir screenshots dos paineis principais do add-on
- registrar o fluxo de instalacao pelo zip gerado em `releases/`
- mostrar um exemplo com `Example/C3388.8_UN-31.ifc`

### 2. Refinar onboarding tecnico

- adicionar um roteiro curto de primeira contribuicao
- documentar convencoes de registro em `modules/__init__.py`
- incluir exemplos pequenos de extensao de `OG_Properties`

### 3. Melhorar rastreabilidade

- relacionar mudancas de versao em `bl_info` com alteracoes documentais relevantes
- registrar, no release process, quando bibliotecas embarcadas forem alteradas

## Medio prazo

### 1. Publicacao web

Se a equipe quiser navegacao web, uma opcao simples e publicar a pasta `docs/` com MkDocs.

Passos basicos:

```bash
pip install mkdocs mkdocs-material
mkdocs new infovis-docs
```

Depois, copiar ou referenciar os documentos principais:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/guides/*.md`
- `docs/reference/GLOSSARY.md`

### 2. Validacao automatica de markdown

- adicionar verificacao de links internos
- validar existencia de arquivos referenciados
- padronizar nomenclatura de titulos e secoes principais

## Longo prazo

- manter changelog documental por versao do add-on
- separar guias de usuario e guias de manutencao se a base crescer
- gerar material de demonstracao para novos integrantes da equipe

## Checklist de manutencao

- [ ] mudou a estrutura de pastas do add-on
- [ ] mudou o processo de build ou release
- [ ] mudou o nome exibido em `bl_info`
- [ ] mudou o fluxo de instalacao no Blender
- [ ] mudou a composicao de `OG_Properties`
- [ ] mudou a organizacao de operadores, paineis ou `PropertyGroup`s

Se qualquer item acima ocorrer, revise pelo menos:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`

## Referencias principais

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/reference/GLOSSARY.md`
