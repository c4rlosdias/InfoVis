# Propriedades — modules/*/properties.py + modules/og_properties.py

## 📌 Visão Geral

As **Property Groups** customizadas estão distribuídas nos módulos de domínio dentro de `modules/`. Cada módulo define suas próprias PropertyGroups em `properties.py`, e o agregador central `OG_Properties` fica em `modules/og_properties.py`.

| Módulo | Responsabilidade |
|--------|------------------|
| `modules/dictionary/properties.py` | Ifc_properties, Class_info, Class_prop_info |
| `modules/decomposition/properties.py` | Container |
| `modules/catalog/properties.py` | Class_type, Layer |
| `modules/props/properties.py` | Enumeration_values, Property_info, Documents, Pset_info |
| `modules/og_properties.py` | OG_Properties + callbacks |

---

## 🏗️ Módulo: modules/dictionary/properties.py

Define as PropertyGroups relacionadas ao dicionário bSDD.

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

### 3. **Class_type** (`modules/catalog/properties.py`)

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

### 4. **Enumeration_values** (`modules/props/properties.py`)

Valores enumerados de uma propriedade IFC.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `is_enumerated` | Bool | Se é valor enumerado |
| `value_str` | String | Valor como string |
| `value_int` | Int | Valor como inteiro |
| `value_float` | Float | Valor como float |
| `value_bool` | Bool | Valor como booleano |

### 5. **Property_info** (`modules/props/properties.py`)

Metadados de uma propriedade IFC individual.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | String | Nome da propriedade |
| `description` | String | Descrição |
| `value_str/int/float/bool` | Multi-tipo | Valores da propriedade |
| `unit` | String | Unidade de medida |
| `enumerations` | Collection[Enumeration_values] | Valores enumerados |
| `table_rows/table_columns` | Int | Dimensões de tabela |

### 6. **Class_prop_info** (`modules/dictionary/properties.py`)

Relacionamento classe-propriedade (metadados do bSDD).

### 7. **Documents** (`modules/props/properties.py`)

Referências de documentos IFC.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `identification` | String | ID do documento |
| `location` | String | Caminho/URL |
| `name` | String | Nome do documento |

### 8. **Pset_info** (`modules/props/properties.py`)

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

### 9. **Container** (`modules/decomposition/properties.py`)

Elemento espacial/decomposição para exibição em árvore.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | Int | ID do elemento IFC |
| `name` | String | Nome |
| `description` | String | Descrição |
| `type` | String | Tipo de relação |
| `has_children`...`is_hidden` | Bool | Estado de árvore |
| `level_index`, `index`, `parent` | Int/String | Hierarquia |

### 10. **Layer** (`modules/catalog/properties.py`)

Camada de um produto.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | Int | ID |
| `name` | String | Nome |
| `description` | String | Descrição |

---

## 🔧 Módulo: modules/og_properties.py

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

No `modules/__init__.py`, a função `get_classes()` retorna todas as classes na ordem correta de dependência. No `__init__.py` (raiz):

```python
from .modules import get_classes
from .modules.og_properties import OG_Properties

classes = [Prefs, Login, Logout] + get_classes()

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

## 🔗 Integração com Outros Módulos

- **`data/`**: Usa PropertyGroups para armazenar dados carregados de IFC/bSDD
- **`modules/*/operators.py`**: Lê e modifica propriedades durante execução de operadores (mesmo domínio)
- **`modules/*/panels.py`**: Renderiza PropertyGroups na UI (template_list, labels, etc.)
- **`modules/__init__.py`**: `get_classes()` retorna todas as classes na ordem correta
- **`__init__.py`**: Registra todas as classes e configura `Scene.og_props`
