# Módulo: panels.py

## 📌 Visão Geral

Este módulo implementa a interface do usuário (UI) do add-on dentro do Blender. Contém painéis (Panels), listas (List UI Items) e layouts para visualizar e interagir com dados IFC.

**Linhas de Código**: 766

---

## 🎨 Componentes da UI

### 1. Funções Auxiliares

#### `_label_multiline(context, text, parent)`
Quebra texto longo em múltiplas linhas na interface.

```python
def _label_multiline(context, text, parent):
    chars = int(context.region.width / 8)   # 7 pixels por caractere
    wrapper = textwrap.TextWrapper(width=chars)
    text_lines = wrapper.wrap(text=text)
    for text_line in text_lines:
        parent.label(text=text_line)
```

**Propósito**: Evitar que texto longo ultrapasse os limites do painel
**Uso**: Descrições longas, definições, informações detalhadas

#### `get_properties(ifc_obj)`
Extrai propriedades de um objeto IFC.

```python
def get_properties(ifc_obj):
    result = []
    result.append()  # [INCOMPLETO - precisa implementação]
```

**Status**: Função em desenvolvimento

#### `get_product_attribute(context, index, attribute)`
Obtém um atributo específico de um produto por índice.

```python
def get_product_attribute(context, index, attribute):
    props = context.scene.og_props 
    products = props.types_show
    for product in products:
        if product.index == index:
            result = getattr(product, attribute)
            return result
```

**Parâmetros:**
- `index`: Índice do produto na lista
- `attribute`: Nome do atributo (string)

**Retorno**: Valor do atributo ou None

---

## 🖼️ Painéis Principais

### Panel_Connect - Subsea Classes

**Informações:**
- **Nome**: "Subsea Classes"
- **ID**: `VIEW3D_PT_og_connect`
- **Tipo**: bpy.types.Panel
- **Localização**: View 3D > Sidebar > O&G Tools
- **Ordem**: 0 (primeiro painel)
- **Modo**: Object Mode
- **Padrão**: Fechado

**Layout:**

```
┌─────────────────────────────────────────┐
│ ⊕ Subsea Classes                   [+]  │
├─────────────────────────────────────────┤
│ [ Get classes from bSDD ]               │
│                                         │
│ Classes Information:              [info]│
│                                         │
│ ┌──────────────────────────────────┐   │
│ │ • Class 1                        │   │
│ │ • Class 2 (expandível)           │   │
│ │   • SubClass 2.1                 │   │
│ │ • Class 3                        │   │
│ └──────────────────────────────────┘   │
│                                         │
│ [Get Class Information] [Get Properties]│
│                                         │
│ Active Class Name      [Index: 0]       │
│                                         │
│ Class Information:              [info]  │
│ ┌──────────────────────────────────┐   │
│ │ • Definition : Lorem ipsum...    │   │
│ │                                  │   │
│ └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Código:**
```python
class Panel_Connect(bpy.types.Panel):
    bl_label        = "Subsea Classes"
    bl_idname       = "VIEW3D_PT_og_connect"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"    
    bl_category     = "O&G Tools"
    bl_order = 0
    bl_options      = {"DEFAULT_CLOSED"}
```

**Funcionalidades:**

1. **Botão "get classes from bSDD"**
   - Conecta ao bSDD (buildingSMART Data Dictionary)
   - Carrega classes disponíveis
   - Popula `props.classes`

2. **Lista de Classes**
   - Template: `BIM_UL_classes`
   - Fonte: `props.classes_shown`
   - Índice ativo: `props.active_class_index`
   - 10 linhas visíveis

3. **Botões de Ação**
   - **Get Class Information**: Carrega definição da classe
   - **Get Class Properties**: Extrai propriedades bSDD

4. **Informações da Classe Ativa**
   - Nome da classe
   - Índice na lista
   - Definição completa com quebra de linhas

---

## 📋 List UI Items (Templates)

### BIM_UL_classes
Renderiza itens da lista de classes.

**Propriedades Exibidas:**
- `name`: Nome da classe
- `level_index`: Nível hierárquico (indentação)
- `has_children`: Ícone de expansão
- `is_expanded`: Estado expandido/contraído
- `is_hidden`: Visibilidade

**Ações:**
- Click: Seleciona classe
- Shift+Click: Seleciona múltiplas
- Expand/Collapse: Mostra/oculta filhos

---

## 🔌 Operadores Conectados

### bsdd.get_class
**Label**: "get classes from bSDD"
**Ação**: Dispara carregamento de classes

### bsdd.get_class_info
**Label**: "Get Class Information"
**Parâmetro**: `uri` (URI da classe selecionada)
**Ação**: Carrega definição e propriedades

### bsdd.get_class_prop
**Label**: "Get Class Properties"
**Parâmetro**: `uri` (URI da classe selecionada)
**Ação**: Extrai lista de propriedades aplicáveis

---

## 🎛️ Propriedades Usadas

### De `context.scene.og_props`
```python
props = context.scene.og_props

# Listas de dados
props.classes           # Todas as classes
props.classes_shown     # Classes visíveis (filtradas)
props.products          # Todos os produtos
props.products_show     # Produtos visíveis
props.types             # Todos os tipos
props.types_show        # Tipos visíveis

# Estados
props.active_class_index        # Classe selecionada
props.active_product_index      # Produto selecionado
props.classes_loaded            # Flag: classes carregadas?
props.class_info_loaded         # Flag: info carregada?

# Dados da classe ativa
props.class_definition          # Definição atual
props.class_prop_info           # Lista de propriedades
```

---

## 🔄 Fluxo de Interação

```
Usuário clica "get classes from bSDD"
        │
        ▼
Operador "bsdd.get_class" executado
        │
        ▼
Conecta ao servidor bSDD
        │
        ▼
Carrega classes em props.classes
        │
        ▼
build_classes() reconstrói hierarquia
        │
        ▼
refresh() filtra para classes_shown
        │
        ▼
Panel redesenhado (draw())
        │
        ▼
Lista atualizada na UI
        │
        ▼
Usuário seleciona classe
        │
        ▼
active_class_changed() callback
        │
        ▼
Clica "Get Class Information"
        │
        ▼
props.class_definition preenchido
        │
        ▼
Panel redesenhado com definição
```

---

## 💡 Padrões de Código

### Criar Layout com Box
```python
box = layout.box()
row = box.row(align=True)
row.label(text="Título", icon='INFO')
# Conteúdo dentro da box
```

### Criar Linha com Múltiplas Colunas
```python
row = layout.row()
row.label(text="Esquerda")
row.label(text="Centro")
row.label(text="Direita")
```

### Template List
```python
self.layout.template_list(
    "UI_UL_list_id",        # Template ID
    "",                     # Desenho ID
    source_object,          # Objeto com lista
    "list_property_name",   # Nome da propriedade de lista
    source_object,          # Objeto com índice ativo
    "active_index_name",    # Nome do índice ativo
    rows=10                 # Linhas visíveis
)
```

### Operador com Propriedade
```python
op = row.operator("operator.id", text="Botão")
op.propriedade_do_operador = valor
```

---

## 🎯 Boas Práticas

1. **Use multi-line labels** para textos longos
2. **Agrupe com boxes** seções relacionadas
3. **Forneça feedback visual** (ícones, cores)
4. **Use tooltips** em botões complexos
5. **Mantenha hierarquia visual** clara
6. **Teste responsividade** com janelas pequenas

---

## 🐛 Debugging de UI

### Verificar Propriedades
```python
# No console Blender
props = bpy.context.scene.og_props
print(len(props.classes))  # Número de classes
print(props.active_class_index)  # Classe selecionada
```

### Forçar Redesenho
```python
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.tag_redraw()
```

### Verificar Espaço Disponível
```python
width = context.region.width  # Largura disponível
print(f"Caracteres disponíveis: {width // 8}")
```

---

## 🔗 Integração com Outros Módulos

- **properties.py**: Define `og_props` e propriedades usadas
- **operators.py**: Implementa ações dos botões
- **data.py**: Fornece funções `refresh()`, `refresh_products()`, etc.

