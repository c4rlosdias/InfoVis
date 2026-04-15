# Pacote: properties/

## 📌 Visão Geral

O pacote `properties/` define as **Property Groups** customizadas que armazenam dados na cena do Blender. Funcionam como "containers" para dados que precisam persistir e sincronizar com a UI.

| Módulo | Linhas | Responsabilidade |
|--------|--------|------------------|
| `types.py` | ~120 | PropertyGroups individuais |
| `main.py` | ~196 | OG_Properties + callbacks |

**`__init__.py`** re-exporta tudo:
```python
from .types import *
from .main import *
```

---

## 🏗️ Módulo: types.py

Define todas as PropertyGroups individuais usadas pelo add-on.

### 1. **Ifc_properties**

Propriedades básicas de um elemento IFC.

```python
class Ifc_properties(PropertyGroup):
    name        : StringProperty(name='name')
    code        : StringProperty(name='code')
    description : StringProperty(name='description')
    uri         : StringProperty(name="uri")
    is_selected : BoolProperty(name="is selected", default=True)
```

### 2. **Class_info**

Informações de uma classe bSDD com suporte a hierarquia.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `code` | String | Código da classe |
| `name` | String | Nome legível |
| `description` | String | Descrição detalhada |
| `uri` | String | Identificador único bSDD |
| `propertyset` | String | Conjunto de propriedades |
| `has_children` | Bool | Possui subclasses? |
| `is_hidden` | Bool | Oculta na UI? (padrão: True) |
| `is_expanded` | Bool | Expandida na UI? (padrão: True) |
| `index` | Int | Índice sequencial |
| `parent` | String | Nome da classe pai |
| `level_index` | Int | Profundidade hierárquica |
| `type` | String | Tipo IFC (ex: IfcPipeSegment) |

### 3. **Class_type**

Tipo de produto IFC.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | Int | Identificador numérico |
| `tag` | String | Tag do elemento |
| `name` | String | Nome |
| `description` | String | Descrição |
| `element_type` | String | Tipo de elemento IFC |
| `has_children`...`is_hidden` | Bool | Estado de árvore |
| `index`, `parent` | Int/String | Posição hierárquica |

### 4. **Enumeration_values**

Valores enumerados de uma propriedade IFC.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `is_enumerated` | Bool | Se é valor enumerado |
| `value_str` | String | Valor como string |
| `value_int` | Int | Valor como inteiro |
| `value_float` | Float | Valor como float |
| `value_bool` | Bool | Valor como booleano |

### 5. **Property_info**

Metadados de uma propriedade IFC individual.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | String | Nome da propriedade |
| `description` | String | Descrição |
| `value_str/int/float/bool` | Multi-tipo | Valores da propriedade |
| `unit` | String | Unidade de medida |
| `enumerations` | Collection[Enumeration_values] | Valores enumerados |
| `table_rows/table_columns` | Int | Dimensões de tabela |

### 6. **Class_prop_info**

Relacionamento classe-propriedade (metadados do bSDD).

### 7. **Documents**

Referências de documentos IFC.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `identification` | String | ID do documento |
| `location` | String | Caminho/URL |
| `name` | String | Nome do documento |

### 8. **Pset_info**

Property set com coleções aninhadas.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | String | Nome do pset |
| `is_expanded` | Bool | Expandido na UI? |
| `is_epset` | Bool | É extended pset? |
| `properties` | Collection[Property_info] | Propriedades do pset |
| `documents` | Collection[Documents] | Documentos |
| `is_doc_expanded` | Bool | Docs expandidos? |
| `graph_*` | String/Bool | Configurações de gráfico |

### 9. **Container**

Elemento espacial/decomposição para exibição em árvore.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | Int | ID do elemento IFC |
| `name` | String | Nome |
| `description` | String | Descrição |
| `type` | String | Tipo de relação |
| `has_children`...`is_hidden` | Bool | Estado de árvore |
| `level_index`, `index`, `parent` | Int/String | Hierarquia |

### 10. **Layer**

Camada de um produto.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | Int | ID |
| `name` | String | Nome |
| `description` | String | Descrição |

---

## 🔧 Módulo: main.py

### Callbacks de Atualização

| Callback | Descrição |
|----------|-----------|
| `update_tree_type(self, context)` | Atualiza tipo de árvore |
| `get_dictionaries(self, context)` | Carrega dicionários bSDD dinamicamente |
| `active_prop_changed(self, context)` | Limpa dados ao mudar propriedade |
| `active_class_changed(self, context)` | Reset ao mudar classe ativa |
| `active_product_changed(self, context)` | Marca produto como não carregado |
| `active_type_changed(self, context)` | Marca tipo como não carregado |
| `active_element_changed(self, context)` | Atualiza ao mudar elemento |

### Classe `OG_Properties`

PropertyGroup principal registrada em `bpy.types.Scene`. Contém ~60+ propriedades organizadas em seções:

**Seção Dictionary:**
- `dictionaries` — EnumProperty (callback: `get_dictionaries`)
- `classes`, `classes_shown` — CollectionProperty[Class_info]
- `active_class_index` — IntProperty (callback: `active_class_changed`)
- `class_definition` — StringProperty
- `class_prop_info` — CollectionProperty[Class_prop_info]
- Flags: `classes_loaded`, `class_info_loaded`, `class_prop_info_loaded`

**Seção Decomposition:**
- `elements_containers`, `containers_show` — CollectionProperty[Container]
- Configurações de ícone e tipo de árvore

**Seção Catalog:**
- `products`, `products_show` — CollectionProperty[Class_type]
- `types`, `types_show` — CollectionProperty[Class_type]
- `layers` — CollectionProperty[Layer]
- Flags de carregamento

**Seção Properties:**
- `properties` — CollectionProperty[Pset_info]
- `ifc_properties` — CollectionProperty[Ifc_properties]
- `graph_columns` — CollectionProperty[Columns]

**Seção Connections:**
- `connections` — CollectionProperty
- Seleção de tipo de conexão

---

## 🔗 Relação Entre PropertyGroups

```
scene.og_props (OG_Properties)
+-- classes: CollectionProperty[Class_info]
+-- classes_shown: CollectionProperty[Class_info]
+-- types: CollectionProperty[Class_type]
+-- types_show: CollectionProperty[Class_type]
+-- products: CollectionProperty[Class_type]
+-- products_show: CollectionProperty[Class_type]
+-- elements_containers: CollectionProperty[Container]
+-- containers_show: CollectionProperty[Container]
+-- properties: CollectionProperty[Pset_info]
|   +-- [i].properties: CollectionProperty[Property_info]
|       +-- [j].enumerations: CollectionProperty[Enumeration_values]
|   +-- [i].documents: CollectionProperty[Documents]
+-- layers: CollectionProperty[Layer]
+-- ifc_properties: CollectionProperty[Ifc_properties]
+-- class_prop_info: CollectionProperty[Class_prop_info]
+-- graph_columns: CollectionProperty[Columns]
```

---

## 🔄 Fluxo de Atualização

```
Usuário interage com UI
        |
        v
Propriedade muda (ex: active_class_index)
        |
        v
Callback disparado (active_class_changed)
        |
        v
Flags resetadas (classes_loaded = False)
        |
        v
tree.refresh_*() chamado
        |
        v
Coleção *_shown repopulada
        |
        v
Panel redesenhado com novos dados
```

---

## 📝 Registrando PropertyGroups

No `__init__.py` (raiz):

```python
from .properties import *

# Lista de classes em ordem de dependência
classes = [
    Ifc_properties, Class_info, Class_type,
    Enumeration_values, Property_info, Class_prop_info,
    Documents, Pset_info, Container, Layer,
    Columns,  # de operators/common.py
    OG_Properties,  # deve ser \u00faltimo (depende dos demais)
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.og_props = PointerProperty(type=OG_Properties)

def unregister():
    del bpy.types.Scene.og_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
```

---

## 🔗 Integração com Outros Pacotes

- **`data/`**: Usa PropertyGroups para armazenar dados carregados de IFC/bSDD
- **`operators/`**: Lê e modifica propriedades durante execução de operadores
- **`panels/`**: Renderiza PropertyGroups na UI (template_list, labels, etc.)
- **`__init__.py`**: Registra todas as classes e configura `Scene.og_props`
