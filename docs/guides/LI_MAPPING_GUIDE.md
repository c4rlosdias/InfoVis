# Guia Detalhado do LI Mapping

Este guia documenta todas as opcoes do painel `LI Mapping`, localizado em
`InfoVis-Catalog > LI Mapping`, e explica como elas afetam o arquivo
`resources/li_mapping.json` e a exportacao da Lista de Itens (LI) em Excel.

## Para que serve

O `LI Mapping` define como cada coluna da Lista de Itens deve ser preenchida a
partir do modelo IFC. O painel permite editar o mapeamento sem abrir o JSON
manualmente, usando campos guiados para atributos IFC, propriedades de Psets,
quantidades, hierarquia espacial, cadeia de montagem e valores calculados.

O fluxo principal e:

1. Abrir um modelo IFC no Blender/Bonsai.
2. Acessar `InfoVis-Catalog > LI Mapping`.
3. Clicar em `Load` para carregar `resources/li_mapping.json`.
4. Revisar ou editar as colunas da LI.
5. Clicar em `Save` para gravar o JSON.
6. Clicar em `Export LI` para gerar o `.xlsx`.

Importante: `Export LI` le o arquivo salvo em `resources/li_mapping.json`.
Se voce alterou algo na interface, clique em `Save` antes de exportar.

## Arquivo usado

O painel edita este arquivo:

```text
resources/li_mapping.json
```

Estrutura principal:

```json
{
  "$schema_version": "1.0",
  "description": "",
  "reference_sheet": "teste",
  "source_types": {},
  "columns": [],
  "subsea_flexible_classes": {},
  "description_templates": {},
  "quantity_by_class": {}
}
```

Chaves reservadas:

| Chave | Uso |
|-------|-----|
| `$schema_version` | Versao do formato do mapeamento |
| `description` | Descricao geral do mapeamento |
| `reference_sheet` | Nome da planilha ou referencia usada como base |
| `source_types` | Dicionario explicativo dos tipos de origem; nao e editado pela UI |
| `columns` | Lista ordenada das colunas exportadas |

Qualquer outra chave de primeiro nivel que seja um objeto JSON e tratada como
`Tabela de apoio`, por exemplo `subsea_flexible_classes`,
`description_templates` e `quantity_by_class`.

## Botoes do painel

| Botao | O que faz |
|-------|-----------|
| `Load` | Carrega `resources/li_mapping.json` para a interface e limpa o estado anterior |
| `Save` | Salva cabecalho, colunas e tabelas de apoio de volta no JSON |
| `Export LI` | Abre seletor de arquivo e exporta a LI para `.xlsx` |
| `Add Column` | Cria uma coluna chamada `Nova Coluna`, com origem `manual` |
| `Remove Column` | Remove a coluna selecionada |
| `Usar esta propriedade` | Copia o Pset e a propriedade escolhidos no seletor bSDD para a coluna |
| `Add Field` | Adiciona um campo extra no objeto `source` da coluna selecionada |
| `Remove Field` | Remove o campo extra selecionado |
| `Add Row` | Adiciona uma linha na tabela de apoio selecionada |
| `Remove Row` | Remove a linha selecionada da tabela de apoio |

Nao ha botao para criar uma nova tabela de apoio vazia. Pela interface, voce
edita as tabelas ja existentes no JSON. Para criar uma tabela inteiramente nova,
adicione-a manualmente em `resources/li_mapping.json`, clique em `Load`, edite
as linhas se necessario e depois clique em `Save`.

## Cabecalho do mapeamento

Depois de clicar em `Load`, o painel mostra tres campos gerais.

| Campo na UI | Chave no JSON | Descricao |
|-------------|---------------|-----------|
| `Schema` | `$schema_version` | Versao do schema do mapeamento |
| `Planilha` | `reference_sheet` | Identificador da planilha de referencia |
| `Descricao` | `description` | Observacao geral sobre o mapeamento |

## Lista de colunas

A lista central mostra todas as colunas configuradas em `columns`.

Cada item da lista exibe:

| Campo exibido | Origem |
|---------------|--------|
| nome da coluna | `column` |
| tipo de origem | `source_type` |

A ordem da lista e a ordem da exportacao. A primeira coluna da lista vira a
primeira coluna do Excel.

## Campos comuns de uma coluna

Ao selecionar uma coluna, o painel exibe campos comuns antes do bloco
`Source guiado`.

| Campo na UI | Chave no JSON | Uso |
|-------------|---------------|-----|
| `Coluna` | `column` | Nome da coluna no Excel |
| `Origem` | `source_type` | Estrategia usada para preencher a coluna |
| `Editavel` | `editable` | Indica se a coluna pode ser editada depois; atualmente e metadado da LI |
| `Notas` | `notes` | Observacoes para quem mantem o mapeamento |

Exemplo:

```json
{
  "column": "Qtde",
  "source_type": "ifc_quantity",
  "source": {
    "mapping_table": "quantity_by_class",
    "quantity_mode": "mapping"
  },
  "editable": true,
  "notes": "Soma comprimento para classes lineares; conta ocorrencias nas demais."
}
```

## Como a exportacao cria linhas

Ao exportar, o InfoVis percorre os `IfcTypeProduct` do modelo IFC atual.

Regras importantes:

- cada linha exportada representa um `IfcTypeProduct` que possui pelo menos uma
  ocorrencia;
- a maioria dos valores e lida da primeira ocorrencia daquele tipo e, se nao
  houver valor, do proprio tipo IFC;
- colunas de quantidade podem considerar todas as ocorrencias do tipo;
- a exportacao usa a ordem das colunas no JSON;
- se nenhuma linha puder ser gerada, o operador mostra aviso de que nao ha
  linhas de LI para o modelo atual.

## Tipos de origem

O campo `Origem` controla quais campos aparecem em `Source guiado` e como o
valor sera resolvido.

| Origem | Uso |
|--------|-----|
| `ifc_attribute` | Le atributo direto da ocorrencia ou do tipo IFC |
| `ifc_property` | Le uma propriedade dentro de um Pset |
| `ifc_quantity` | Calcula quantidade por contagem, comprimento ou tabela |
| `ifc_class` | Le uma classe/chave IFC e traduz por tabela de apoio |
| `spatial` | Busca valor em ancestral da hierarquia espacial |
| `aggregation_parent` | Busca valor em pai/avo da cadeia de montagem |
| `computed` | Calcula valor por metodo ou template |
| `manual` | Coluna manual ou Pset customizado opcional |
| `not_applicable` | Coluna sem correspondencia IFC; exporta vazio |

## Origem: ifc_attribute

Use `ifc_attribute` para ler atributos diretos de entidades IFC.

Campos exibidos:

| Campo na UI | Chave em `source` | Uso na exportacao |
|-------------|-------------------|-------------------|
| `Classe` | `ifc_class` | Metadado salvo no JSON; o exportador atual nao filtra por esse campo |
| `Atributo` | `attribute` | Atributo principal a ler |
| `Fallback` | `fallback_attribute` | Atributo alternativo se o principal vier vazio |
| `Format` | `format` | Metadado salvo no JSON; o exportador atual nao aplica formatacao |

Como resolve:

1. tenta ler `attribute` na ocorrencia;
2. se vazio, tenta ler `attribute` no tipo IFC;
3. se vazio e houver `fallback_attribute`, repete a busca pelo fallback;
4. se `attribute` for `is_a`, retorna a classe IFC normalizada, sem prefixo
   `Ifc` e sem sufixo `Type`.

Exemplos de atributos:

| Atributo | Resultado esperado |
|----------|--------------------|
| `Name` | nome da ocorrencia ou tipo |
| `Description` | descricao |
| `Tag` | tag IFC |
| `ObjectType` | tipo de objeto definido no IFC |
| `GlobalId` | identificador global IFC |
| `is_a` | classe IFC normalizada |

Exemplo JSON:

```json
{
  "column": "Name",
  "source_type": "ifc_attribute",
  "source": {
    "attribute": "Name",
    "fallback_attribute": "Tag"
  },
  "editable": true,
  "notes": ""
}
```

## Origem: ifc_property

Use `ifc_property` para ler uma propriedade de um Pset.

Campos exibidos:

| Campo na UI | Chave em `source` | Uso na exportacao |
|-------------|-------------------|-------------------|
| `Classe` | `ifc_class` | Metadado salvo no JSON; o exportador atual nao filtra por esse campo |
| `Pset` | `pset` | Nome tecnico do property set |
| `Property` | `property` | Nome tecnico da propriedade |
| `Allowed Values` | `allowed_values` | Metadado salvo no JSON; o exportador atual nao valida valores |

Como resolve:

1. procura o Pset na ocorrencia;
2. se nao encontrar valor, procura o Pset no tipo IFC;
3. retorna o primeiro valor nao vazio;
4. se nao encontrar, exporta vazio.

Exemplo JSON:

```json
{
  "column": "Comprimento Nominal",
  "source_type": "ifc_property",
  "source": {
    "pset": "Pset_FlexiblePipeSegment",
    "property": "NominalLength"
  },
  "editable": true,
  "notes": ""
}
```

## Origem: manual

Use `manual` para colunas que a LI precisa ter, mas que podem nao existir no
modelo IFC padrao. A UI e a resolucao sao as mesmas de `ifc_property`.

Campos exibidos:

| Campo na UI | Chave em `source` | Uso |
|-------------|-------------------|-----|
| `Classe` | `ifc_class` | Metadado salvo no JSON |
| `Pset` | `pset` | Pset customizado ou futuro |
| `Property` | `property` | Propriedade customizada ou futura |
| `Allowed Values` | `allowed_values` | Metadado para controle de valores esperados |

Comportamento:

- se o Pset/propriedade existir no IFC, o valor e exportado;
- se nao existir, a coluna sai vazia para preenchimento posterior;
- esse tipo e adequado para campos de aquisicao, suprimentos, status ou
  revisoes que ainda nao estejam modelados.

Exemplo JSON:

```json
{
  "column": "Observacao",
  "source_type": "manual",
  "source": {
    "pset": "Pset_LI_Extra",
    "property": "Observation"
  },
  "editable": true,
  "notes": "Campo de preenchimento manual se nao existir no IFC."
}
```

## Seletor bSDD para ifc_property e manual

Quando a origem e `ifc_property` ou `manual`, aparece a area
`Escolher do dicionario bSDD`.

Campos:

| Campo | Opcoes |
|-------|--------|
| `Discipline` | `Flexible Pipes` ou `Rigid Pipes` |
| `Element` | classes do dicionario selecionado, vindas de `resources/subsea_*_completo.json` |
| `Property set` | Psets associados ao elemento selecionado |
| `Property` | propriedades associadas ao Pset selecionado |

Botao:

| Botao | Resultado |
|-------|-----------|
| `Usar esta propriedade` | define `source_type` como `ifc_property`, copia `Property set` para `source.pset` e `Property` para `source.property` |

Se o nome da coluna estiver vazio ou como `Nova Coluna`, o botao tambem troca o
nome da coluna para o nome da propriedade escolhida.

O seletor usa os arquivos:

```text
resources/subsea_flexible_pipes_2.1_completo.json
resources/subsea_rigid_pipes_1.0_completo.json
```

## Origem: spatial

Use `spatial` para buscar informacoes na hierarquia espacial ou de decomposicao.

Campos exibidos:

| Campo na UI | Chave em `source` | Uso |
|-------------|-------------------|-----|
| `Nivel (classe IFC)` | `level` | Classe IFC do ancestral a procurar, como `IfcSite` ou `IfcBuilding` |
| `Atributo` | `attribute` | Atributo a ler do ancestral encontrado |

Como resolve:

1. monta uma cadeia de ancestrais a partir da ocorrencia;
2. percorre relacoes `ContainedInStructure`, `Decomposes` e `Nests`;
3. procura o primeiro ancestral cuja classe seja igual a `level`;
4. retorna o atributo configurado nesse ancestral;
5. se nao encontrar, exporta vazio.

Campos extras uteis:

| Chave extra | Uso |
|-------------|-----|
| `fallback_levels` | Lista JSON de classes alternativas a procurar depois de `level` |
| `fallback_attribute` | Atributo alternativo, embora nao apareca como campo guiado nessa origem |

Exemplo JSON:

```json
{
  "column": "Site",
  "source_type": "spatial",
  "source": {
    "level": "IfcSite",
    "attribute": "Name",
    "fallback_levels": ["IfcBuilding"]
  },
  "editable": false,
  "notes": ""
}
```

## Origem: aggregation_parent

Use `aggregation_parent` para ler atributos de um ancestral na cadeia de
montagem, considerando apenas relacoes de aninhamento/decomposicao.

Campos exibidos:

| Campo na UI | Chave em `source` | Uso |
|-------------|-------------------|-----|
| `Nivel (1=pai imediato, 2=avo, ...)` | `level` | Posicao do ancestral na cadeia |
| `Atributo` | `attribute` | Atributo a ler |
| `Fallback` | `fallback_attribute` | Atributo alternativo se o principal vier vazio |

Como resolve:

1. sobe a cadeia usando `Nests` e depois `Decomposes`;
2. nao usa `ContainedInStructure` nem grupos espaciais;
3. interpreta `level=1` como pai imediato, `level=2` como avo, e assim por
   diante;
4. le `attribute` do ancestral encontrado;
5. se vazio, tenta `fallback_attribute`;
6. se nao houver ancestral naquele nivel, exporta vazio.

Exemplo JSON:

```json
{
  "column": "Pipe Line",
  "source_type": "aggregation_parent",
  "source": {
    "level": "2",
    "attribute": "Name"
  },
  "editable": false,
  "notes": "Avo na cadeia de montagem."
}
```

## Origem: ifc_class

Use `ifc_class` para derivar uma classe de negocio a partir de atributo IFC e
traduzir o valor por uma tabela de apoio.

Campos exibidos:

| Campo na UI | Chave em `source` | Uso |
|-------------|-------------------|-----|
| `Atributo` | `attribute` | Atributo usado para formar a chave da classe |
| `Mapping Table` | `mapping_table` | Nome da tabela de apoio usada para traduzir a chave |

Como resolve:

1. le `attribute` da ocorrencia;
2. se vazio, le `attribute` do tipo IFC;
3. se ainda vazio, usa a classe IFC normalizada do tipo;
4. procura esse valor na tabela de apoio indicada por `mapping_table`;
5. se encontrar, exporta o valor mapeado;
6. se nao encontrar, exporta a propria chave.

Campo extra util:

| Chave extra | Uso |
|-------------|-----|
| `fallback_attribute` | Atributo alternativo para formar a chave, embora nao apareca como campo guiado nessa origem |

Exemplo com tabela:

```json
{
  "column": "Classe",
  "source_type": "ifc_class",
  "source": {
    "attribute": "ObjectType",
    "mapping_table": "subsea_flexible_classes"
  },
  "editable": false,
  "notes": ""
}
```

Tabela de apoio correspondente:

```json
{
  "subsea_flexible_classes": {
    "FlexiblePipeSegment": "Tramo",
    "EndFitting": "Conector"
  }
}
```

## Origem: ifc_quantity

Use `ifc_quantity` para calcular a quantidade da linha da LI.

Campo exibido sempre:

| Campo na UI | Chave em `source` | Uso |
|-------------|-------------------|-----|
| `Modo` | `quantity_mode` | Estrategia de quantidade |

Opcoes de `Modo`:

| Modo na UI | Valor JSON | Resultado |
|------------|------------|-----------|
| `Mapping Table` | `mapping` | Usa uma tabela de apoio para decidir se conta ou soma comprimento |
| `Count Occurrences` | `count` | Conta ocorrencias do tipo IFC |
| `Sum Length` | `length` | Soma comprimento por `get_qtde()` |

Quando `Modo` e `Mapping Table`, aparecem tambem:

| Campo na UI | Chave em `source` | Uso |
|-------------|-------------------|-----|
| `Mapping Table` | `mapping_table` | Nome da tabela com regra por classe |
| `Selected By` | `selected_by` | Nome de uma coluna ja calculada que tambem pode selecionar a regra |

Como resolve em `mapping`:

1. busca a tabela indicada em `mapping_table`;
2. calcula uma chave de classe pelo `ObjectType` da ocorrencia ou classe IFC;
3. tambem le o valor da coluna indicada por `selected_by`, se existir;
4. procura regra na tabela nesta ordem: chave de classe, valor selecionado,
   `_default`;
5. se a regra tiver `quantity` igual a `Length`, soma comprimento;
6. caso contrario, conta ocorrencias.

Regra de comprimento atual:

- para `IfcPipeSegmentType`, soma `NominalLength` das ocorrencias no Pset
  `OGSubPset_FlexiblePipeSegmentOccurence`;
- para outros tipos, `get_qtde()` retorna contagem de ocorrencias.

Exemplo JSON:

```json
{
  "column": "Qtde",
  "source_type": "ifc_quantity",
  "source": {
    "mapping_table": "quantity_by_class",
    "quantity_mode": "mapping",
    "selected_by": "Classe"
  },
  "editable": true,
  "notes": ""
}
```

Tabela de apoio:

```json
{
  "quantity_by_class": {
    "FlexiblePipeSegment": {
      "qto": "Qto_FlexiblePipeSegment",
      "quantity": "Length"
    },
    "_default": {
      "qto": "BaseQuantities",
      "quantity": "Count"
    }
  }
}
```

## Origem: computed

Use `computed` para valores calculados. O comportamento depende do campo
`Method` ou da combinacao `Template Table` + `Selected By`.

Campos exibidos:

| Campo na UI | Chave em `source` | Uso |
|-------------|-------------------|-----|
| `Selected By` | `selected_by` | Nome de coluna ja calculada usada para escolher template |
| `Template Table` | `template_table` | Nome da tabela de apoio com templates |
| `Derived From` | `derived_from` | Nome de coluna base para alguns metodos |
| `Method` | `method` | Metodo especial de calculo |
| `Format` | `format` | Metadado salvo no JSON; o exportador atual nao aplica formatacao |

### Method: quantity_unit_symbol

Deriva a unidade de uma coluna de quantidade.

Campos esperados:

| Campo | Valor |
|-------|-------|
| `Method` | `quantity_unit_symbol` |
| `Derived From` | nome da coluna de quantidade, por exemplo `Qtde` |

Como resolve:

1. le o valor ja calculado em `derived_from`;
2. se estiver vazio, exporta vazio;
3. se a coluna derivada usa `quantity_mode=count`, retorna `un`;
4. se usa `quantity_mode=length`, retorna `m`;
5. se usa `mapping`, consulta `quantity_by_class`;
6. quando possivel, tenta obter a unidade IFC real do Qto;
7. se nao conseguir ler a unidade, usa `m` para comprimento e `un` para
   contagem.

Exemplo:

```json
{
  "column": "Unidade",
  "source_type": "computed",
  "source": {
    "derived_from": "Qtde",
    "method": "quantity_unit_symbol"
  },
  "editable": false,
  "notes": ""
}
```

### Method: spatial_name_part

Extrai uma informacao do `Name` da ocorrencia ou de um ancestral que contenha
um separador.

Campos esperados:

| Campo | Uso |
|-------|-----|
| `Method` | `spatial_name_part` |
| `separator` | campo extra; separador usado no `Name`; padrao `/` |
| `part_index` | campo extra opcional; indice da parte apos `split` |

Comportamento:

- procura primeiro na ocorrencia;
- depois procura nos ancestrais por `ContainedInStructure`, `Decomposes` e
  `Nests`;
- se encontrar um `Name` com o separador e nao houver `part_index`, retorna o
  nome inteiro;
- se houver `part_index`, retorna somente a parte indicada.

Exemplo:

```json
{
  "column": "space",
  "source_type": "computed",
  "source": {
    "method": "spatial_name_part",
    "separator": "/",
    "part_index": 0
  },
  "editable": false,
  "notes": ""
}
```

### Template Table + Selected By

Quando `method` nao e um metodo especial, o computed pode renderizar um template
de texto.

Campos esperados:

| Campo | Uso |
|-------|-----|
| `Selected By` | nome da coluna usada como chave, por exemplo `Classe` |
| `Template Table` | nome da tabela de apoio, por exemplo `description_templates` |

Como resolve:

1. le o valor ja calculado da coluna `selected_by`;
2. usa esse valor para escolher um template na tabela;
3. se nao encontrar, usa `_default`;
4. substitui placeholders no template;
5. exporta o texto final.

Placeholders aceitos:

| Placeholder | Resultado |
|-------------|-----------|
| `{attr.Name}` | atributo direto da ocorrencia ou tipo |
| `{attr.Tag}` | tag da ocorrencia ou tipo |
| `{Pset_Nome.Propriedade}` | valor de propriedade em Pset da ocorrencia ou tipo |

Exemplo:

```json
{
  "column": "Descricao",
  "source_type": "computed",
  "source": {
    "selected_by": "Classe",
    "template_table": "description_templates"
  },
  "editable": true,
  "notes": ""
}
```

Tabela de apoio:

```json
{
  "description_templates": {
    "Tramo": "Tramo {attr.Tag}; comprimento {Pset_FlexiblePipeSegment.NominalLength} m",
    "_default": "{attr.Description}"
  }
}
```

## Origem: not_applicable

Use `not_applicable` para colunas de controle que devem existir na LI, mas nao
tem origem no IFC.

Campos guiados:

- nenhum campo de `Source guiado` e exibido;
- e possivel registrar metadados em `Campos extras`, mas a exportacao sempre
  retorna vazio para essa origem.

Exemplo:

```json
{
  "column": "Status",
  "source_type": "not_applicable",
  "source": null,
  "editable": true,
  "notes": "Campo de controle da planilha."
}
```

## Campos extras

`Campos extras` permite adicionar pares `Chave` / `Valor` ao objeto `source` da
coluna selecionada.

Use para:

- chaves suportadas pelo exportador mas nao expostas como campo guiado;
- parametros especificos de metodos `computed`;
- listas, objetos ou valores escalares que precisam ser salvos no JSON.

Regras:

- se `Valor` for JSON valido, ele sera salvo como JSON;
- se nao for JSON valido, ele sera salvo como texto;
- campos extras sao adicionados depois dos campos guiados e podem sobrescrever
  uma chave guiada com o mesmo nome;
- chaves vazias sao ignoradas ao salvar.

Exemplos:

| Chave | Valor | Uso |
|-------|-------|-----|
| `separator` | `/` | separador para `spatial_name_part` |
| `part_index` | `0` | indice da parte extraida pelo metodo |
| `fallback_levels` | `["IfcBuilding", "IfcSite"]` | niveis espaciais alternativos |
| `fallback_attribute` | `Tag` | atributo alternativo em origens que nao exibem esse campo |
| `allowed_values` | `["A", "B", "C"]` | lista de valores esperados |

## Tabelas de apoio

A area `Tabelas de apoio` edita objetos de primeiro nivel do JSON que nao sejam
chaves reservadas.

Campos de uma tabela:

| Campo na UI | Chave no JSON | Uso |
|-------------|---------------|-----|
| `Tabela` | nome da chave de primeiro nivel | Nome usado por `mapping_table` ou `template_table` |
| `Comentario` | `_comment` | Comentario salvo dentro da tabela |

Campos de uma linha:

| Campo na UI | JSON | Uso |
|-------------|------|-----|
| `Chave` | chave do objeto | Valor usado para lookup |
| `Valor` | valor da chave | Pode ser texto, numero, lista ou objeto JSON |

Exemplo de tabela simples:

```json
{
  "subsea_flexible_classes": {
    "FlexiblePipeSegment": "Tramo",
    "EndFitting": "Conector"
  }
}
```

Exemplo de tabela com objetos:

```json
{
  "quantity_by_class": {
    "FlexiblePipeSegment": {
      "qto": "Qto_FlexiblePipeSegment",
      "quantity": "Length"
    },
    "_default": {
      "qto": "BaseQuantities",
      "quantity": "Count"
    }
  }
}
```

Quando editar valores complexos pela UI, escreva JSON valido no campo `Valor`.

Exemplo de `Valor` para uma linha:

```json
{"qto": "Qto_FlexiblePipeSegment", "quantity": "Length"}
```

## Tabela de campos por origem

| Origem | Campos guiados salvos em `source` |
|--------|-----------------------------------|
| `ifc_attribute` | `ifc_class`, `attribute`, `fallback_attribute`, `format` |
| `ifc_property` | `ifc_class`, `pset`, `property`, `allowed_values` |
| `manual` | `ifc_class`, `pset`, `property`, `allowed_values` |
| `spatial` | `level`, `attribute` |
| `aggregation_parent` | `level`, `attribute`, `fallback_attribute` |
| `ifc_class` | `attribute`, `mapping_table` |
| `ifc_quantity` | `quantity_mode`, `mapping_table`, `selected_by` |
| `computed` | `selected_by`, `template_table`, `derived_from`, `method`, `format` |
| `not_applicable` | nenhum campo guiado |

## Exemplo completo de coluna

```json
{
  "column": "Pipe Line",
  "source_type": "aggregation_parent",
  "source": {
    "level": "2",
    "attribute": "Name"
  },
  "editable": false,
  "notes": "Avo na cadeia de montagem."
}
```

## Exemplo completo de fluxo

Para adicionar uma coluna que leia uma propriedade do bSDD:

1. Clique em `Load`.
2. Clique em `Add Column`.
3. Em `Coluna`, informe o nome que deve aparecer no Excel.
4. Em `Origem`, selecione `IFC Property`.
5. Em `Escolher do dicionario bSDD`, escolha `Discipline`.
6. Escolha `Element`.
7. Escolha `Property set`.
8. Escolha `Property`.
9. Clique em `Usar esta propriedade`.
10. Revise `Editavel` e `Notas`.
11. Clique em `Save`.
12. Clique em `Export LI`.

## Checklist antes de exportar

- O modelo IFC esta aberto no Bonsai/Blender.
- Existem `IfcTypeProduct` com ocorrencias no modelo.
- As alteracoes do painel foram salvas com `Save`.
- Colunas que dependem de outras colunas aparecem depois das colunas base.
- `Selected By` usa exatamente o nome de uma coluna anterior.
- `Mapping Table` e `Template Table` apontam para tabelas existentes.
- Valores complexos em tabelas de apoio estao em JSON valido.
- Colunas `computed` com `quantity_unit_symbol` possuem `Derived From`.

## Solucao de problemas

| Sintoma | Verifique |
|---------|-----------|
| `Export LI` nao reflete a alteracao feita na tela | Clique em `Save` antes de exportar |
| Exportacao gera aviso de nenhuma linha | O IFC precisa ter `IfcTypeProduct` com ocorrencias |
| Coluna sai vazia | Confirme `source_type`, Pset/propriedade, atributo ou nivel configurado |
| `Selected By` nao funciona | A coluna referenciada precisa existir e ser calculada antes |
| Tabela de apoio nao e usada | Confira se `mapping_table` ou `template_table` tem o mesmo nome da tabela |
| Valor complexo virou texto | O campo `Valor` precisa ser JSON valido |
| Unidade sai `un` quando deveria sair `m` | Confira `quantity_by_class` e a regra `quantity: Length` |
| Propriedade bSDD nao aparece no seletor | Verifique `Discipline`, `Element` e se o dicionario JSON possui a propriedade |

## Observacoes de manutencao

- A UI preserva `source_types`, mas nao edita essa chave.
- `Save` remove e recria as tabelas de apoio a partir do que esta carregado na
  interface.
- `ifc_class`, `format` e `allowed_values` sao salvos em algumas origens, mas
  parte deles atua hoje como metadado; o exportador atual nao usa esses campos
  para filtrar, formatar ou validar.
- Colunas `computed` podem depender de valores ja calculados em `row_values`;
  por isso, a ordem das colunas e relevante.
- Para campos ainda nao suportados pela UI, use `Campos extras` ou edite o JSON
  diretamente.
