# Operadores - modules/*/operators.py

## 📌 Visão Geral

Os operadores estão distribuídos por domínio funcional dentro de `modules/`. Cada domínio possui seu próprio `operators.py` com a lógica de negócio específica.

| Módulo | Responsabilidade |
|--------|------------------|
| `modules/common/operators.py` | Utilitários compartilhados |
| `modules/dictionary/operators.py` | Operadores bSDD |
| `modules/decomposition/operators.py` | Decomposição IFC |
| `modules/catalog/operators.py` | Catálogo de tipos |
| `modules/connections/operators.py` | Conexões IFC |
| `modules/props/operators.py` | Propriedades e gráficos |

Todas as classes são registradas centralmente em `modules/__init__.py` via `get_classes()`.

---

## 🔧 Módulo: modules/common/operators.py

Funções e operadores utilitários compartilhados por todos os módulos.

### Funções

| Função | Descrição |
|--------|-----------|
| `reorder_element(context, index, chg)` | Reordena elementos IFC aninhados |
| `_open_in_browser(url)` | Abre URL no navegador (cross-platform) |
| `get_options(self, context)` | Callback para `dynamic_items` em EnumProperty |

### Operadores

| Classe | bl_idname | Descrição |
|--------|-----------|-----------|
| `Operator_expand_tree` | `element.expand_tree` | Expande nó da árvore |
| `Operator_contract_tree` | `element.contract_tree` | Contrai nó da árvore |
| `ErrorMessage` | `og.error_message` | Popup de mensagem de erro |

### PropertyGroup

- **`Columns`** — `name` (StringProperty) + `selected` (BoolProperty) — para seleção de colunas em gráficos

---

## 🌐 Módulo: modules/dictionary/operators.py

Operadores de integração com o bSDD (buildingSMART Data Dictionary).

### Operadores

| Classe | bl_idname | Descrição |
|--------|-----------|-----------|
| `Operator_clear_properties` | `object.clear_prop` | Limpa propriedades do objeto |
| `Operator_assign_all` | `object.assign_all` | Seleciona todas as propriedades |
| `Operator_unassign_all` | `object.unassign_all` | Desmarca todas as propriedades |
| `Operator_get_properties` | `bsdd.get_prop` | Busca propriedades do bSDD |
| `Operator_uri` | `object.uri` | Abre URI no navegador |
| `Operator_get_classes` | `bsdd.get_class` | Busca classes do bSDD |
| `Operator_add_properties` | `object.add_prop` | Adiciona pset templates do bSDD |
| `Operator_get_prop_info` | `property.get_prop_info` | Busca metadados de propriedade |
| `Operator_get_class_info` | `bsdd.get_class_info` | Busca metadados de classe |
| `Operator_get_class_prop` | `bsdd.get_class_prop` | Busca propriedades de classe |
| `Operator_export_ids` | `ids.export` | Exporta arquivo IDS (XML) |

### Dependências
- `tqdm` — barras de progresso
- `ifctester.ids` — validação IDS
- `data.bsdd` — cliente bSDD
- `data.catalog` — templates de propriedade
- `data.ifc_utils` — construção de hierarquias

---

## 🏗️ Módulo: modules/decomposition/operators.py

Operadores para decomposição de projetos IFC.

### Operadores

| Classe | bl_idname | Descrição |
|--------|-----------|-----------|
| `Operator_decomposition_load` | `decomposition.load` | Carrega árvore de decomposição IFC |
| `Operator_decomposition_select_element` | `decomposition.select_element` | Seleciona elemento individual |
| `Operator_decomposition_select_components` | `decomposition.select_components` | Seleciona elemento + filhos recursivamente |
| `Operator_decomposition_move` | `decomposition.move` | Move elemento para novo pai (nest/aggregate) |
| `Operator_decomposition_chg_order` | `decomposition.chg_order` | Reordena elementos |

### Dependências
- `data.tree` — `load_contained_elements_by_decomposition()`, `refresh_tree()`

---

## 📦 Módulo: modules/catalog/operators.py

Operadores para o catálogo de tipos de produtos IFC.

### Operadores

| Classe | bl_idname | Descrição |
|--------|-----------|-----------|
| `Operator_load_products` | `catag.load_products` | Carrega produtos IFC agrupados por ElementType |
| `Operator_catalog_select_type` | `catag.select_type` | Seleciona objeto de tipo |
| `Operator_catalog_select_elements` | `catag.select_elements` | Seleciona todas as instâncias de um tipo |
| `Operator_catalog_show_layers` | `catag.show_layers` | Gera relatório HTML de camadas |
| `Operator_catalog_select_layer` | `catag.select_layer` | Seleciona objeto de uma camada |

### Funções

| Função | Descrição |
|--------|-----------|
| `update_predefined_types()` | Atualiza ObjectType/PredefinedType em elementos IFC em lote |

### Dependências
- `data.catalog` — `Import_ifc`, `Catalog`
- `data.ifc_utils` — `build_products()`
- `data.tree` — `refresh_products()`, `refresh_types()`

---

## 🔌 Módulo: modules/connections/operators.py

Operadores para gerenciamento de conexões IFC.

### Operadores

| Classe | bl_idname | Descrição |
|--------|-----------|-----------|
| `Operator_disconnect` | `conn.disconnect` | Remove relação de conexão IFC |
| `Operator_select_object` | `conn.select_object` | Seletor de objeto (eyedropper) |
| `Operator_add_connect` | `conn.add_connect` | Cria conexão IFC entre objetos |

### Padrão
Usa `WindowManager` pointer properties para seleção de objetos.

---

## 📊 Módulo: modules/props/operators.py

Operadores para edição de propriedades IFC e geração de gráficos.

### Operadores

| Classe | bl_idname | Descrição |
|--------|-----------|-----------|
| `Operator_props_edit` | `props.edit` | Edita valor de propriedade (single, list, enum) |
| `Operator_props_load` | `props.load_properties` | Carrega propriedades do objeto ativo |
| `Operator_props_expand` | `props.expand` | Toggle expandir/contrair pset |
| `Operator_docs_expand` | `docs.expand` | Toggle seção de documentos |
| `Operator_props_graph` | `props.graph` | Gera gráfico matplotlib de dados tabela/CSV |
| `Operator_props_invert` | `props.invert` | Inverte eixos X/Y |
| `Operator_document_edit` | `props.doc_edit` | Edita referências de documentos IFC |
| `Operator_document_load` | `props.load_doc` | File browser para caminhos de documentos |
| `Operator_document_open` | `props.open_doc` | Abre documento no navegador/OS |
| `Operator_show_table` | `props.show_table` | Toggle visibilidade de tabela |

### Bibliotecas de Análise
- **pandas**: Processamento de dados tabulares
- **matplotlib**: Geração de gráficos 2D
- **numpy**: Operações vetorizadas
- **scipy.interpolate**: Interpolação de curvas

### Padrão
Usa `invoke_props_dialog` para configuração de gráficos com seleção de colunas.

---

## 🔄 Fluxo Típico

```
1. Usuário seleciona arquivo IFC ou clica em botão
   |
2. Operador disparado (ex: bsdd.get_class)
   |
3. auth.is_authenticated() verificado (se necessário)
   |
4. Extrai dados com ifcopenshell
   |
5. Processa com pandas/numpy se necessário
   |
6. Constrói hierarquias com ifc_utils.build_classes/build_products
   |
7. Atualiza propriedades (modules/og_properties.py)
   |
8. Renderiza na UI (modules/*/panels.py)
```

---

## 📦 Estruturas de Dados

### Classe JSON esperada (bSDD)
```json
{
  "code": "001",
  "name": "Flexible Pipe",
  "descriptionPart": "Descri\u00e7\u00e3o",
  "uri": "http://bsdd.buildingsmart.org/...",
  "classType": "IfcPipeSegmentFlexible",
  "children": [
    {
      "code": "001.001",
      "name": "Tensioner"
    }
  ]
}
```

---

## 🐛 Debugging

### Imprimir Classes
```python
props = context.scene.og_props
for classe in props.classes:
    print(f"{classe.name} (level: {classe.level_index})")
```

### Inspecionar Propriedades IFC
```python
import ifcopenshell.util.element as element
element_obj = ifc_file[123]
props_dict = element.get_psets(element_obj)
```

---

## 🔗 Integração com Outros Pacotes

- **`data/`**: Fornece `bSDD`, `Catalog`, `tree`, `ifc_utils` — toda a camada de dados
- **`modules/*/properties.py`** e **`modules/og_properties.py`**: Definem `Class_info`, `Class_type`, `OG_Properties` e outras estruturas de dados
- **`modules/*/panels.py`**: Consomem dados construidos aqui para renderizar na UI
- **`__init__.py`**: Registra todos os operadores para o Blender
