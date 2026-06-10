# Painéis — modules/*/panels.py

## 📌 Visão Geral

Os painéis de interface (UI) do add-on estão distribuídos nos módulos de domínio dentro de `modules/`. Cada módulo contém seu próprio `panels.py` com os painéis, UILists e layouts relevantes àquele domínio.

| Módulo | Responsabilidade |
|--------|------------------|
| `modules/dictionary/panels.py` | Painel bSDD + UILists de classes |
| `modules/decomposition/panels.py` | Painel de decomposição + UILists |
| `modules/catalog/panels.py` | Painel de catálogo + UILists |
| `modules/connections/panels.py` | Painel de conexões |
| `modules/props/panels.py` | Painel de propriedades |
| `modules/settings/panels.py` | Painéis de configurações e informações |

---

## 🎨 Funções Auxiliares

### `_label_multiline(context, text, parent)`
Quebra texto longo em múltiplas linhas na interface.

```python
def _label_multiline(context, text, parent):
    chars = int(context.region.width / 8)
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)
```

### `get_product_attribute(context, index, attribute)`
Obtém um atributo específico de um produto por índice.

---

## 🖼️ Painéis

### Categorias

Os painéis estão organizados em **4 categorias** na sidebar do Blender:

| Categoria | Painéis |
|-----------|---------|
| `O&G-Dictionary` | Panel_Connect, Panel_Settings |
| `O&G-Occurrence` | Panel_Decompositions, Panel_Connect_Elements, Panel_Properties |
| `O&G-Catalog` | Panel_Catalog |
| `O&G-Info` | Panel_Info |

### 🔐 Autenticação

Todos os painéis verificam `auth.is_authenticated()` antes de desenhar conteúdo editor:

```python
from ... import auth

class Panel_Connect(bpy.types.Panel):
    def draw(self, context):
        layout = self.layout
        if not auth.is_authenticated():
            layout.label(text="Login necess\u00e1rio")
            return
        # ... conte\u00fado normal
```

---

### Panel_Connect — Subsea Classes (`modules/dictionary/panels.py`)

| Propriedade | Valor |
|-------------|-------|
| **bl_idname** | `VIEW3D_PT_og_connect` |
| **bl_category** | `O&G-Dictionary` |
| **bl_order** | 0 |
| **Modo** | Object Mode |
| **Padrão** | Fechado |

**Funcionalidades:**
1. Botão "get classes from bSDD" → operador `bsdd.get_class`
2. Lista de classes com `BIM_UL_classes`
3. Botões "Get Class Information" / "Get Class Properties"
4. Informações da classe ativa (definição, propriedades)
5. Botão "Add Properties" para criar pset templates
6. Export IDS

---

### Panel_Decompositions — Decomposição do Projeto (`modules/decomposition/panels.py`)

| Propriedade | Valor |
|-------------|-------|
| **bl_idname** | `VIEW3D_PT_og_decompositions` |
| **bl_category** | `O&G-Occurrence` |
| **bl_order** | 0 |

**Funcionalidades:**
1. Carrega decomposição IFC do projeto
2. Árvore hierárquica desenhada via `tree.draw_tree()`
3. Seleção de elementos individuais ou com filhos
4. Move elementos entre containers (nest/aggregate)
5. Reordenação de elementos

---

### Panel_Connect_Elements — Conexões (`modules/connections/panels.py`)

| Propriedade | Valor |
|-------------|-------|
| **bl_idname** | `VIEW3D_PT_connect_elements` |
| **bl_category** | `O&G-Occurrence` |

**Funcionalidades:**
1. Lista de conexões do objeto ativo
2. Seleção de objetos para conectar (eyedropper)
3. Criar/remover conexões IFC

---

### Panel_Catalog — Catálogo de Tipos (`modules/catalog/panels.py`)

| Propriedade | Valor |
|-------------|-------|
| **bl_idname** | `VIEW3D_PT_og_catalog` |
| **bl_category** | `O&G-Catalog` |

**Funcionalidades:**
1. Lista de tipos de produtos IFC (`BIM_UL_products`)
2. Seleção de tipo / instâncias
3. Visualização de camadas (`BIM_UL_layers`)
4. Relatório HTML de camadas

---

### Panel_Properties — Propriedades (`modules/props/panels.py`)

| Propriedade | Valor |
|-------------|-------|
| **bl_idname** | `VIEW3D_PT_og_properties` |
| **bl_category** | `O&G-Occurrence` |

**Funcionalidades:**
1. Exibe property sets do objeto ativo
2. Edição de valores (single, list, enum, table)
3. Seção de documentos IFC com edição
4. Geração de gráficos matplotlib
5. Toggle tabela / inversão de eixos

---

### Panel_Settings — Configurações de Dicionário (`modules/settings/panels.py`)

| Propriedade | Valor |
|-------------|-------|
| **bl_idname** | `VIEW3D_PT_og_settings` |
| **bl_category** | `O&G-Info` |

**Funcionalidades:**
1. Seleção de dicionário bSDD
2. Configurações de endpoint

---

### Panel_Info — Informações (`modules/settings/panels.py`)

| Propriedade | Valor |
|-------------|-------|
| **bl_idname** | `VIEW3D_PT_og_info` |
| **bl_category** | `O&G-Info` |

**Funcionalidades:**
1. Versão do add-on
2. Informações gerais

---

## 📋 UIList Classes

| Classe | Uso |
|--------|-----|
| `BIM_UL_ifc_properties` | Propriedades IFC |
| `BIM_UL_property_class` | Classes de propriedade |
| `BIM_UL_classes` | Classes bSDD (com indentação hierárquica) |
| `BIM_UL_class_prop` | Propriedades de classe |
| `BIM_UL_decomposition` | Decomposição IFC |
| `BIM_UL_tree` | Árvore genérica |
| `BIM_UL_products` | Produtos/tipos |
| `BIM_UL_layers` | Camadas de produto |

### Padrão de UIList
```python
class BIM_UL_classes(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Indenta\u00e7\u00e3o baseada em level_index
        # \u00cdcone de expans\u00e3o se has_children
        # Nome do item
```

---

## 🔄 Fluxo de Interação

```
Usuário clica "get classes from bSDD"
        |
        v
Operador "bsdd.get_class" executado
        |
        v
Conecta ao servidor bSDD
        |
        v
ifc_utils.build_classes() constrói hierarquia
        |
        v
tree.refresh_classes() filtra para classes_shown
        |
        v
Panel redesenhado (draw())
        |
        v
Lista atualizada via BIM_UL_classes
```

---

## 💡 Padrões de Código

### Criar Layout com Box
```python
box = layout.box()
row = box.row(align=True)
row.label(text="T\u00edtulo", icon='INFO')
```

### Template List
```python
self.layout.template_list(
    "BIM_UL_classes",
    "",
    props,
    "classes_shown",
    props,
    "active_class_index",
    rows=10
)
```

### Operador com Propriedade
```python
op = row.operator("bsdd.get_class_info", text="Info")
op.uri = active_class.uri
```

---

## 🔗 Integração com Outros Módulos

- **`modules/og_properties.py`**: Define `OG_Properties` (og_props) e callbacks usados nos painéis
- **`modules/*/properties.py`**: PropertyGroups de domínio referenciadas pelas UILists
- **`modules/*/operators.py`**: Operadores chamados pelos botões dos painéis (mesmo domínio)
- **`data/tree`**: Fornece `draw_tree()`, `refresh_*()` para árvores
- **`data/ifc_utils`**: Funções de utilidade IFC
- **`auth`**: Verifica autenticação antes de exibir conteúdo protegido
