# Guia de Utilizacao do AddOn InfoVis

Este guia descreve o uso do AddOn InfoVis no Blender, com foco nas telas
disponiveis na sidebar da Viewport 3D. Ele e voltado a quem precisa inspecionar,
classificar, editar e exportar informacoes de modelos IFC.

## Visao geral

O InfoVis organiza suas ferramentas em abas da sidebar do Blender:

| Aba | Painel | Uso principal |
|-----|--------|---------------|
| `InfoVis-Dictionary` | `Subsea Classes` | Consultar dicionarios bSDD, classes, propriedades e exportar IDS |
| `InfoVis-Occurrence` | `Decompositions` | Navegar pela decomposicao IFC e exportar a arvore |
| `InfoVis-Occurrence` | `Properties` | Ler e editar propriedades, documentos e graficos de CSV |
| `InfoVis-Occurrence` | `Constructive Type` | Ver o tipo construtivo do objeto ativo e suas camadas |
| `InfoVis-Occurrence` | `Connect Elements` | Visualizar, criar e remover conexoes IFC |
| `InfoVis-Catalog` | `Catalog` | Carregar tipos de produto, quantidades e relatorios de camadas |
| `InfoVis-Catalog` | `LI Mapping` | Configurar mapeamento e exportar Lista de Itens (LI) |
| `InfoVis-Analisys` | `Analisys` | Colorir objetos por propriedades ou faixas de valores |
| `InfoVis-Settings` | `Settings` | Configurar labels IFC e vistas de decomposicao |

Abra a sidebar com `N` na Viewport 3D e procure as abas `InfoVis-*`.

## Pre-requisitos

Antes de usar os paineis que leem IFC, carregue um modelo IFC no Blender pelo
fluxo do Bonsai/BlenderBIM. O AddOn depende do modelo ativo retornado pelo Bonsai.

Requisitos principais:

- Blender 5.0 ou superior.
- AddOn `InfoVis` instalado e habilitado.
- Modelo IFC aberto quando a acao depender de elementos, tipos, propriedades ou
  conexoes.
- Acesso a internet quando for consultar o bSDD.
- Permissao de editor autenticada para alterar propriedades, documentos,
  conexoes, agregacoes e ordem de elementos.

## Instalar e habilitar

1. Gere ou obtenha o arquivo `.zip` de release do InfoVis.
2. No Blender, acesse `Edit > Preferences > Add-ons`.
3. Clique em `Install from Disk`.
4. Selecione o `.zip` do AddOn.
5. Habilite `InfoVis`.
6. Abra ou importe o arquivo IFC que sera analisado.
7. Na Viewport 3D, pressione `N` e acesse as abas `InfoVis-*`.

## Autenticacao de editor

Algumas acoes aparecem ou ficam editaveis apenas depois do login de editor.

Para autenticar:

1. Acesse `Edit > Preferences > Add-ons`.
2. Encontre o AddOn `InfoVis`.
3. Em `Autenticacao para status de editor`, informe a senha configurada para o
   projeto.
4. Clique em `Login`.

Enquanto autenticado, o AddOn libera acoes como editar valores IFC, editar
documentos, criar/remover conexoes, mover elementos na decomposicao e alterar a
ordem de elementos. Use `Logout` para encerrar a sessao do Blender.

## Fluxo rapido recomendado

1. Carregue o IFC no Blender/Bonsai.
2. Abra `InfoVis-Settings > Settings` e clique em `Load` em
   `Decomposition views`.
3. Abra `InfoVis-Occurrence > Decompositions`, escolha o `Tree Type` e navegue
   pela arvore.
4. Selecione um elemento na arvore ou na Viewport.
5. Abra `InfoVis-Occurrence > Properties` e clique em `Load properties`.
6. Use `InfoVis-Catalog > Catalog` para carregar tipos e exportar quantidades,
   se necessario.
7. Use `InfoVis-Analisys > Analisys` para colorir a viewport por propriedade,
   valor exato ou faixa numerica.

## InfoVis-Dictionary: Subsea Classes

Use este painel para consultar dicionarios bSDD e transformar propriedades do
dicionario em templates/artefatos de especificacao.

### Carregar classes do bSDD

1. Em `Select Dictionary`, escolha o dicionario:
   - `Subsea Flexible Pipes v2.1`
   - `Subsea Rigid Pipelines v1.0`
2. Clique em `get classes from bSDD`.
3. Navegue pela lista de classes.
4. Use o icone de URL para abrir a classe no navegador.

Com uma classe selecionada:

- `Get Class Information` carrega definicao, descricao, data de versao, tipo de
  classe e classe IFC relacionada.
- `Get Class Properties` lista as propriedades associadas a classe.
- `Export IDS file` exporta um arquivo `.ids` com requisitos derivados das
  classes e propriedades carregadas.

### Carregar propriedades do bSDD

1. Escolha o dicionario.
2. Clique em `get properties from bSDD`.
3. Marque ou desmarque propriedades na lista.
4. Use `Assing all`, `Unassign all` ou `Clear` para controlar a selecao.
5. Selecione uma propriedade e clique em `Get Property Information` para ver
   metadados, unidades e classes relacionadas.
6. Clique em `Add selected properties` para gerar/adicionar templates de Pset a
   partir das propriedades selecionadas.

## InfoVis-Occurrence: Decompositions

O painel `Decompositions` mostra a arvore de decomposicao do IFC conforme a
vista configurada.

### Configurar vistas de decomposicao

As vistas sao lidas de `resources/decomposition_view.json`. Elas definem:

- `id` e `label` da vista.
- classe raiz IFC, como `IfcProject`, `IfcProjectOrder` ou `IfcInventory`.
- relacoes IFC percorridas, como `IfcRelAggregates`, `IfcRelNests`,
  `IfcRelContainedInSpatialStructure` e `IfcRelAssignsToGroup`.

Para editar pelo Blender:

1. Acesse `InfoVis-Settings > Settings`.
2. Em `Decomposition views`, clique em `Load`.
3. Edite, adicione, duplique ou remova vistas e relacoes.
4. Clique em `Save` para gravar em `resources/decomposition_view.json`.
5. Use `Defaults` para carregar a configuracao padrao na interface antes de
   salvar.

### Navegar pela arvore

1. Em `InfoVis-Occurrence > Decompositions`, escolha o `Tree Type`.
2. A troca do `Tree Type` recarrega a arvore automaticamente.
3. Use `Expand all` para abrir todos os nos.
4. Use `Collapse children` para recolher os filhos.
5. Clique em um item da lista para selecionar o objeto correspondente na
   Viewport.
6. Use o icone de selecao de componentes para selecionar um elemento e seus
   filhos.

### Exportar decomposicao

Clique em `Export` e escolha um caminho de arquivo. O AddOn gera um `.xlsx` com:

- nivel hierarquico;
- ID IFC;
- nome;
- tipo IFC;
- `ObjectType`;
- ID e nome do pai;
- indicacao de filhos.

Se nada for exportado, carregue uma vista de decomposicao antes de clicar em
`Export`.

### Editar agregacoes e ordem

Depois de autenticar como editor, o painel mostra:

- `change aggregations`: habilita mover elementos para outro pai.
- `aggregation type`: escolhe entre `Nests` e `Aggregations`.
- `change order`: habilita setas para reordenar elementos folha.

Depois de mover ou reordenar, salve o IFC pelo fluxo normal do Bonsai/Blender
para preservar as alteracoes no arquivo.

## InfoVis-Occurrence: Properties

O painel `Properties` trabalha sobre o objeto ativo da Viewport.

1. Selecione um objeto IFC.
2. Clique em `Load properties`.
3. Revise `Occurence Properties` e `Inherited Type Properties`.
4. Use `Show property description` para alternar entre nomes tecnicos e
   descricoes.
5. Expanda/recolha Psets pelo icone triangular.

Quando autenticado:

- campos de propriedades ficam editaveis;
- o botao com icone de confirmacao grava o valor no IFC;
- documentos referenciados podem ser editados;
- o seletor de arquivo pode atualizar a localizacao de documentos.

### Documentos e graficos

Quando o objeto ou o Pset possui documentos referenciados:

- use o icone de abrir para acessar URL ou arquivo local;
- use o seletor de arquivo para alterar o caminho quando autenticado;
- se o documento for `.CSV`, use o botao de grafico para gerar um HTML com o
  grafico em `graphic.html`.

O dialogo de grafico permite escolher eixo X, colunas, limites, intervalos de
grade, ordenacao e interpolacao.

### Adicionar propriedade aos labels da Viewport

Em propriedades comuns do painel, o botao com icone `ADD` adiciona o campo
`Pset.Property` aos labels IFC da Viewport. A lista de campos exibidos fica em
`InfoVis-Settings > Settings`.

## InfoVis-Occurrence: Constructive Type

O painel `Constructive Type` mostra informacoes do tipo IFC relacionado ao objeto
ativo.

Com um objeto selecionado, ele exibe:

- `ElementType`;
- nome e descricao do tipo;
- documentos associados ao tipo;
- atalhos para selecionar todas as ocorrencias do tipo;
- atalho para mostrar camadas do tipo;
- atalho para selecionar o objeto de tipo.

Quando o tipo possui componentes/camadas, a lista `Layers` permite selecionar a
camada correspondente no Blender.

## InfoVis-Occurrence: Connect Elements

Use `Connect Elements` para revisar e editar relacoes IFC de conexao.

Com objetos selecionados, o painel lista as conexoes encontradas, incluindo:

- `IfcRelConnectsElements`;
- `IfcRelConnectsPorts`;
- `IfcRelConnectsWithRealizingElements`.

Quando autenticado:

1. Escolha `Connection Type`.
2. Selecione o objeto ativo desejado na Viewport.
3. Use o botao `ADD` ao lado de `Relating Element A`.
4. Selecione outro objeto e use `ADD` em `Relating Element B`.
5. Para conexoes que exigem realizador, preencha `Realizing Element`.
6. Clique em `Add Connection`.

Para remover uma conexao existente, use o icone de desconectar ao lado da
conexao listada.

## InfoVis-Catalog: Catalog

O painel `Catalog` organiza os `IfcTypeProduct` do modelo por tipo de elemento.

1. Clique em `Load type products`.
2. Navegue pela arvore de tipos.
3. Em itens folha, use:
   - o icone de selecao para selecionar todas as ocorrencias do tipo;
   - o icone de informacao para abrir o relatorio de camadas.

O relatorio de camadas e gerado em `layers.html` na raiz do projeto e aberto no
navegador.

Clique em `Export Quantities` para exportar um `.xlsx` com nome do tipo,
quantidade e unidade.

## InfoVis-Catalog: LI Mapping

O painel `LI Mapping` edita `resources/li_mapping.json` e usa esse mapeamento
para gerar uma Lista de Itens em Excel.

Para uma referencia completa de todos os campos, origens, tabelas de apoio e
regras de exportacao, consulte [Guia Detalhado do LI Mapping](LI_MAPPING_GUIDE.md).

### Carregar e salvar mapeamento

- `Load`: carrega `resources/li_mapping.json` para a interface.
- `Save`: grava as alteracoes de volta no JSON.
- `Export LI`: gera um `.xlsx` a partir do modelo IFC atual e do mapeamento.

### Editar colunas da LI

Cada coluna possui:

- `Coluna`: nome da coluna exportada.
- `Origem`: tipo de fonte, como `ifc_attribute`, `ifc_property`,
  `ifc_quantity`, `spatial`, `aggregation_parent`, `computed`, `manual` ou
  `not_applicable`.
- `Editavel`: indica se a coluna pode ser ajustada manualmente depois.
- `Notas`: observacoes para manutencao do mapeamento.

Dependendo da origem, o painel mostra campos como classe IFC, atributo,
fallback, Pset, propriedade, tabela de apoio, metodo calculado, formato e
valores permitidos.

### Escolher propriedade do bSDD

Para origens `ifc_property` ou `manual`, use a area `Escolher do dicionario
bSDD`:

1. Selecione `Discipline`.
2. Selecione `Element`.
3. Selecione `Property set`.
4. Selecione `Property`.
5. Clique em `Usar esta propriedade`.

O AddOn copia o Pset e a propriedade para os campos reais usados na exportacao.

### Tabelas de apoio

A area `Tabelas de apoio` permite editar tabelas auxiliares usadas por fontes
como `ifc_class`, `ifc_quantity` e `computed`.

Use `Add Row` e `Remove Row` para controlar pares `Chave`/`Valor`.

## InfoVis-Analisys: Analisys

O painel `Analisys` colore objetos da Viewport com base em propriedades IFC.

1. Escolha `Discipline`.
2. Escolha `Element`.
3. Escolha `Property set`.
4. Escolha `Property`.
5. Escolha `Mode`:
   - `Distinct values`: cria uma cor por valor distinto.
   - `Exact value`: destaca um valor especifico.
   - `Numeric range`: colore objetos dentro de uma faixa numerica.
6. Clique em `Apply colors`.
7. Consulte a `Legend` e o `Status`.

Use `Reset colors` para restaurar as cores dos objetos na Viewport.

## InfoVis-Settings: Settings

O painel `Settings` concentra configuracoes visuais e de vistas.

### Labels IFC na Viewport

1. Ative ou desative `Show IFC label`.
2. Em `Fields to display`, adicione atributos IFC ou propriedades.
3. Ajuste `Display text` para controlar o nome mostrado no label.
4. Ajuste `Label offset (px)` para deslocar o label na tela.

Campos de propriedade devem seguir o formato:

```text
PsetName.PropertyName
```

Exemplo:

```text
Pset_FlexiblePipeSegment.NominalLength
```

## Arquivos gerados e editados

| Acao | Saida |
|------|-------|
| `Export IDS file` | arquivo `.ids` escolhido pelo usuario |
| `Decompositions > Export` | arquivo `.xlsx` escolhido pelo usuario |
| `Catalog > Export Quantities` | arquivo `.xlsx` escolhido pelo usuario |
| `LI Mapping > Export LI` | arquivo `.xlsx` escolhido pelo usuario |
| `Catalog > show layers` | `layers.html` na raiz do projeto |
| `Properties > graph` | `graphic.html` na raiz do projeto |
| `LI Mapping > Save` | `resources/li_mapping.json` |
| `Settings > Decomposition views > Save` | `resources/decomposition_view.json` |

## Solucao de problemas

| Sintoma | Verifique |
|---------|-----------|
| `No Ifc file loaded` | Carregue um IFC no Bonsai/Blender antes de usar o painel |
| Arvore de decomposicao vazia | Confira o `Tree Type` e a `root_ifc_class` da vista |
| bSDD nao carrega classes ou propriedades | Verifique conexao com internet e disponibilidade da API |
| Campos aparecem somente leitura | Faca login como editor nas preferencias do AddOn |
| Documento nao abre | Confirme se `Location` e uma URL valida ou um caminho existente |
| Grafico falha | O documento precisa ser CSV e o caminho precisa existir |
| Exportacao LI nao gera linhas | Confirme se o IFC possui `IfcTypeProduct` com ocorrencias |
| Labels nao mostram propriedade | Use o formato `Pset.Property` e recarregue as propriedades do objeto |

## Boas praticas

- Carregue propriedades depois de selecionar o objeto que deseja inspecionar.
- Salve o IFC no Bonsai/Blender depois de editar propriedades, conexoes ou
  decomposicoes.
- Antes de exportar LI, carregue e revise `LI Mapping`.
- Antes de exportar decomposicao, selecione a vista correta em `Tree Type`.
- Use `Reset colors` apos analises visuais para limpar a Viewport.
