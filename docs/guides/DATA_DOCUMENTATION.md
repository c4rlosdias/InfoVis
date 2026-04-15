# Pacote: data/

## 📌 Visão Geral

O pacote `data/` gerencia dados, callbacks, eventos e funcionalidades de integração com IFC e bSDD. Coordena sincronização entre a cena Blender e as estruturas de dados da aplicação.

O pacote é dividido em **5 submódulos**:

| Módulo | Linhas | Responsabilidade |
|--------|--------|------------------|
| `bsdd.py` | ~88 | Cliente REST bSDD |
| `catalog.py` | ~193 | Import IFC, Catalog, PropTempl |
| `cde.py` | ~118 | API CDE (mock/stub) |
| `tree.py` | ~222 | Árvore, refresh, callbacks |
| `ifc_utils.py` | ~500 | Utilidades IFC, propriedades, conexões |

**`__init__.py`** re-exporta tudo dos submódulos:
```python
from .bsdd import *
from .catalog import *
from .cde import *
from .tree import *
from .ifc_utils import *
```

---

## 🌐 Módulo: bsdd.py

### Classe `bSDD`

Cliente estático (todos `@classmethod`) para o buildingSMART Data Dictionary.

**Variáveis de classe:**
- `data_dic` — lista de dicionários disponíveis
- `data_info_prop` — informações de propriedades
- `data_class` — dados de classes
- `data_prop` — dados de propriedades
- `endpoint` — URL base da API
- `uri` — URI do dicionário ativo
- `is_loaded` — flag de carregamento

**Métodos:**

| Método | Descrição |
|--------|-----------|
| `load_dictionaries()` | Busca versões de dicionários do servidor bSDD |
| `load_classes(version, use_nested)` | Busca classes de uma versão |
| `load_properties(version)` | Busca propriedades de uma versão |
| `get_class(uri, include_properties)` | Busca uma classe específica |
| `get_class_prop(uri)` | Busca propriedades de uma classe |
| `get_property(uri)` | Busca uma propriedade individual |

**Exemplo de uso:**
```python
from data.bsdd import bSDD

if not bSDD.is_loaded:
    bSDD.load_dictionaries()

# Buscar classes de um dicionário
bSDD.load_classes(version_uri, use_nested=True)
```

---

## 📦 Módulo: catalog.py

### Classe `Import_ifc`

Importa elementos de tipo IFC para o Blender via Bonsai.

| Método | Descrição |
|--------|-----------|
| `import_type_from_ifc()` | Importa tipo de elemento |
| `import_materials()` | Importa materiais |
| `import_styles()` | Importa estilos visuais |
| `import_material_styles()` | Importa estilos de material |

### Classe `Catalog`

Lê o arquivo `resources/ifc_types.json`.

| Método | Descrição |
|--------|-----------|
| `get_ifc_type()` | Retorna tipo IFC do catálogo |

### Classe `PropTempl`

Gerencia templates de property sets IFC (`EPset_OG.ifc`).

| Método | Descrição |
|--------|-----------|
| `get_template()` | Obtém template existente |
| `get_prop()` | Obtém propriedade do template |
| `add_pset_template(metadata)` | Cria/edita pset template a partir de metadados bSDD |

**Padrão**: Todas as classes usam `@classmethod`.

---

## 📡 Módulo: cde.py

### Classe `CDE_Api`

Stub/mock da API CDE (Common Data Environment) para integração futura.

```python
cde = CDE_Api(endpoint="https://api.cde.example.com")
projects = cde.get_projects()   # HTTP real
contracts = cde.get_contracts() # Mock (dados hardcoded)
assets = cde.get_assets()       # Mock
inventory = cde.get_inventory() # Mock
```

**Status**: Placeholder para integração futura com CDE real.

---

## 🌳 Módulo: tree.py

### Funções de Callback

#### `call_back()`
Callback simples que dispara carregamento de propriedades.

```python
def call_back():
    bpy.ops.props.load_properties()
```

**Acionado por**: msgbus (mudança de objeto ativo)

#### `on_active_object_change(scene)`
Detecta quando o objeto ativo muda e atualiza propriedades.

```python
def on_active_object_change(scene):
    global last_active
    obj = bpy.context.view_layer.objects.active
    if obj != last_active:
        last_active = obj
        bpy.ops.props.load_properties()
```

**Gatilho**: `bpy.app.handlers.depsgraph_update_post`

### Funções de Refresh

Todas seguem o mesmo padrão:

```
1. Obter props = context.scene.og_props
2. Limpar coleção visível (clear())
3. Para cada item em coleção completa:
   a. Se não está oculto (is_hidden == False):
      - Criar novo item em coleção visível
      - Copiar todas as propriedades
```

| Função | Origem → Destino |
|--------|-----------------|
| `refresh_classes(context)` | `classes` → `classes_shown` |
| `refresh_products(context)` | `products` → `products_show` |
| `refresh_types(context)` | `types` → `types_show` |
| `refresh_container(context)` | `elements_containers` → `containers_show` |
| `refresh_tree(context, property)` | Genérica para qualquer par |

### Funções de Decomposição

#### `load_contained_elements_by_decomposition(container, name_props, context)`
Carrega recursivamente a decomposição IFC (spatial/nesting/grouping) em coleção Blender.

**Usa**: `ifcopenshell.api.nest`, `ifcopenshell.api.aggregate`, `ifcopenshell.api.spatial`

#### `draw_tree(layout, item, operators, attributes, property, only_children)`
Desenha uma árvore hierárquica na UI do Blender.

#### `move_to_assembly(parent, children, type)`
Move elementos IFC via nesting ou aggregation APIs.

---

## 🔧 Módulo: ifc_utils.py

O maior arquivo utilitário (~500 linhas). Manipula propriedades IFC, visibilidade e conexões.

### Funções de Tipo de Propriedade

| Função | Descrição |
|--------|-----------|
| `set_prop_type(prop, value)` | Setter polimórfico (str/int/float/bool) |
| `get_prop_type(prop)` | Getter polimórfico |

### Funções de Unidade

| Função | Descrição |
|--------|-----------|
| `get_unit_symbol(unit)` | Retorna símbolo da unidade IFC |
| `get_unit(ifc_obj, pset_name, prop_name)` | Resolve unidade de uma propriedade |

### Funções de Propriedade IFC

| Função | Descrição |
|--------|-----------|
| `get_property(ifc_obj, pset_name, prop_name)` | Busca/cria property set |
| `get_pset(ifc_obj, pset_name)` | Busca property set existente |
| `set_properties(props, ifc_obj, is_a, i)` | Carrega todas as propriedades (tabelas, enums, listas, docs) em coleções Blender |
| `refresh_props(context)` | Recarrega propriedades do objeto ativo |

### Funções de Visibilidade

| Função | Descrição |
|--------|-----------|
| `set_hide_class(context, index, is_hidden)` | Oculta/mostra subclasses recursivamente |
| `set_hide_product(context, index, is_hidden)` | Oculta/mostra subprodutos recursivamente |

**Algoritmo de visibilidade:**
```
Para cada classe após o índice:
  Se nível > nível do índice:
    Aplica o estado is_hidden
  Se nível <= nível do índice:
    Para (limite alcançado)
```

### Funções de Construção de Hierarquia

| Função | Descrição |
|--------|-----------|
| `build_classes(context, classe, c, level, parent, hide)` | Constrói hierarquia de classes em `props.classes` |
| `build_products(context, classe, c, level, parent, hide, children)` | Constrói hierarquia de produtos em `props.types` |

**Exemplo `build_classes`:**
```python
classe_dict = {
    "code": "001",
    "name": "Pipe",
    "descriptionPart": "Tubulação subsuperficial",
    "uri": "http://bsdd.buildingsmart.org/...",
    "classType": "IfcPipeSegment",
    "children": [...]
}
build_classes(context, classe_dict, 0, 1, "", False)
```

### Funções de Conexão

| Função | Descrição |
|--------|-----------|
| `add_connections(obj_a, obj_b, obj_c, connect_type)` | Cria relações IFC de conexão |

**Tipos de conexão suportados:**
- `IfcRelConnectsPorts`
- `IfcRelConnectsElements`
- `IfcRelConnectsWithRealizingElements`

---

## 📡 Fluxo de Eventos

```
┌─────────────────────────────────┐
│ Usuário seleciona objeto Blender│
└────────────────┬────────────────┘
                 │
    ┌────────────▼─────────────┐
    │ msgbus / Handler:        │
    │ depsgraph_update_post    │
    └────────────┬─────────────┘
                 │
    ┌────────────▼─────────────────┐
    │ tree.call_back() ou          │
    │ tree.on_active_object_change()│
    └────────────┬─────────────────┘
                 │
    ┌────────────▼──────────────────┐
    │ bpy.ops.props.load_properties()│
    │ (operators/properties.py)      │
    └────────────┬──────────────────┘
                 │
    ┌────────────▼──────────────────┐
    │ ifc_utils.refresh_props()     │
    │ (carrega dados IFC)           │
    └────────────┬──────────────────┘
                 │
    ┌────────────▼──────────────┐
    │ tree.refresh_*()          │
    │ (atualiza listas visíveis)│
    └────────────┬──────────────┘
                 │
    ┌────────────▼──────────────┐
    │ Painel redesenhado       │
    │ (props.classes_shown)    │
    └──────────────────────────┘
```

---

## 🔧 Registrando Handlers

No `__init__.py` (raiz) ao ativar o add-on:

```python
# Via msgbus (preferido)
bpy.msgbus.subscribe_rna(
    key=subscribe_to,
    owner=owner,
    args=(bpy.context,),
    notify=_data_tree.call_back,
)
```

---

## 📊 Dependências

### Integração com IfcStore e Bonsai
```python
from bonsai.bim.ifc import IfcStore
import bonsai.tool as tool
```

### Processamento de Dados
- **ifcopenshell**: Manipulação IFC
- **numpy**: Operações matriciais (usado em `ifc_utils.py`)
- **pandas**: Análise tabular (tabelas de propriedades)

---

## 📝 Boas Práticas

### 1. Sempre Limpar Antes de Popular
```python
props.classes_shown.clear()
for item in data:
    new = props.classes_shown.add()
```

### 2. Verificar Estado Antes de Processar
```python
if props.classes_loaded:
    # Usar dados
else:
    # Carregamento necessário
```

### 3. Evitar Loops de Callback
```python
self.updating = True
# ... fazer mudanças ...
self.updating = False
```

---

## 🔗 Integração com Outros Pacotes

- **`operators/`**: Usa `tree.refresh_*()` e `ifc_utils.*` para atualizar após operações
- **`panels/`**: Exibe dados de `classes_shown`, `products_show`, etc. Usa `tree.draw_tree()`
- **`properties/`**: Define as PropertyGroups manipuladas aqui
- **`__init__.py`**: Registra os handlers de eventos via msgbus usando `tree.call_back`
