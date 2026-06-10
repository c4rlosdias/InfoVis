# Sumario Executivo

## Resumo

InfoVis e um add-on para Blender voltado a visualizacao e enriquecimento de informacoes IFC. O projeto combina navegacao de dados de objetos, consulta a bSDD, estrutura de decomposicao, catalogo de tipos, conexoes entre elementos e inspecao de propriedades.

## Informacoes essenciais

| Aspecto | Descricao |
|---------|-----------|
| Nome do add-on | InfoVis |
| Versao atual no codigo | 0.1.2 |
| Ambiente alvo | Blender 5.0+ |
| Linguagem | Python |
| Estrutura | Modular, baseada em `modules/` e `data/` |
| Distribuicao | Zip instalavel gerado em `releases/` |

## O que o projeto entrega

- leitura e organizacao de informacoes IFC
- consulta e apoio a classificacao com bSDD
- navegacao em hierarquias e arvores de decomposicao
- selecao de tipos e camadas de catalogo
- inspecao de propriedades, documentos e atributos associados
- suporte a visualizacao complementar com bibliotecas cientificas

## Estrutura executiva

O projeto se organiza em quatro blocos principais:

1. `__init__.py`
Responsavel pelo registro do add-on, preferencias, autenticacao, ciclo de vida e carregamento de dependencias.

2. `modules/`
Contem operadores, paineis, `PropertyGroup`s e o agregador central `OG_Properties`.

3. `data/`
Contem a logica de apoio para bSDD, catalogo, CDE, arvore e utilitarios IFC.

4. `resources/` e bibliotecas embarcadas
Reunem dados estaticos e dependencias empacotadas para execucao, especialmente no Windows.

## Valor tecnico

- separacao clara entre UI Blender e logica de suporte
- uso de `PropertyGroup`s para persistencia e sincronizacao de estado
- empacotamento de dependencias para reduzir atrito de instalacao
- arquitetura que permite evolucao por dominio funcional

## Riscos e atencoes

- o comportamento depende do ambiente Blender e das versoes de Python embarcadas
- alteracoes em `modules/__init__.py`, `OG_Properties` ou scripts de build impactam diretamente a operacao do add-on
- a documentacao precisa acompanhar qualquer mudanca em estrutura, registro de classes ou fluxo de instalacao

## Indicacoes para decisao

Para manutencao e evolucao do projeto, os documentos prioritarios sao:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/guides/`

Para acompanhamento executivo, este arquivo deve permanecer curto e focado em objetivo, estrutura, valor e risco, sem duplicar o detalhamento tecnico dos demais documentos.
