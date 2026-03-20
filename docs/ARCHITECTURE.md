# 🏗️ Arquitetura - Oil & Gas Tools

## Visão Geral

O Oil & Gas Tools é um **add-on Blender modular** que segue o padrão **MVC (Model-View-Controller)** adaptado para Blender.

```
┌──────────────────────────────────────────────────┐
│            BLENDER (Host)                        │
├──────────────────────────────────────────────────┤
│  Panels (UI)           → panels.py               │
│  Properties (Data)     → properties.py           │
│  Operators (Logic)     → operators.py            │
│  Data Layer            → data.py                 │
└─────────────────────┬────────────────────────────┘
                      │
                      ▼
        ┌──────────────────────────┐
        │  External Services       │
        ├──────────────────────────┤
        │ • bSDD                   │
        │ • ifcopenshell           │
        │ • matplotlib, scipy      │
        └──────────────────────────┘
```

## Camadas Principais

### 1. **UI Layer** (panels.py)
Renderiza painéis na viewport com botões, listas e controles. Interage com o usuário através da interface do Blender.

### 2. **Properties Layer** (properties.py)
Define a estrutura de dados usando PropertyGroups do Blender. Armazena estado da aplicação e sincroniza com UI.

### 3. **Operators Layer** (operators.py)
Implementa a lógica de negócio: extração IFC, construção de hierarquias, processamento de dados.

### 4. **Data Layer** (data.py)
Gerencia sincronização entre camadas, callbacks, eventos e integração com bSDD.

## Fluxo de Dados

### Exemplo: Carregar Classes do bSDD

```
Usuário clica botão → Operador executa → Dados carregados
      (UI)                (Logic)         (Properties)
                            │
                            ▼
                    data.refresh() atualiza
                            │
                            ▼
                    Panel redesenha
```

## Estrutura de Dados

```
context.scene.og_props
├── classes: todas as classes (incluso ocultas)
├── classes_shown: apenas visíveis
├── types: todos os tipos
├── types_show: tipos visíveis
└── flags: status de carregamento
```

## Padrões de Design

| Padrão | Arquivo | Uso |
|--------|---------|-----|
| PropertyGroup | properties.py | Dados sincronizados com UI |
| Operator | operators.py | Lógica + undo/redo |
| Panel | panels.py | Interface visual |
| Callback | data.py | Reage a mudanças |

## Fluxo de Inicialização

```
1. Usuário ativa add-on
2. __init__.py carrega módulos
3. Registra classes e PropertyGroups
4. Painel aparece na View3D
5. Pronto para usar
```

## Dependências Entre Módulos

```
__init__.py (registro)
    ↓
properties.py ← operators.py ← panels.py
    ↓            ↓
  data.py (sincronização)
    ↓
External APIs (ifcopenshell, bSDD, etc)
```

## Para Mais Detalhes

- **[Desenvolvimento](DEVELOPMENT.md)** - Como setup e contribuir
- **[Módulos](guides/)** - Documentação completa por arquivo
- **[Glossário](reference/GLOSSARY.md)** - Termos e FAQ

### 1. **Initialization Layer** (`__init__.py`)

**Responsabilidades:**
- Definir metadados do add-on
- Registrar classes com Blender
- Gerenciar ciclo de vida (register/unregister)

**Fluxo:**
```
Blender inicia add-on
    │
    ▼
__init__.py executa
    │
    ├─ Define bl_info
    ├─ Importa módulos
    ├─ Registra classes (register_class)
    ├─ Adiciona handlers
    └─ Anexa PropertyGroups à Scene
```

### 2. **UI Layer** (`panels.py`)

**Responsabilidades:**
- Renderizar painéis na viewport
- Criar componentes visuais
- Gerenciar interações do usuário

**Padrão:**
```python
class PanelName(bpy.types.Panel):
    def draw_header(self, context):
        # Ícone e label

    def draw(self, context):
        # Layout completo
        props = context.scene.og_props
        layout.template_list(...)
        layout.operator(...)
```

### 3. **Properties Layer** (`properties.py`)

**Responsabilidades:**
- Definir estrutura de dados
- Gerenciar callbacks de mudança
- Armazenar estado da aplicação

**Padrão:**
```python
class PropertyGroup(bpy.types.PropertyGroup):
    campo1: StringProperty(...)
    campo2: IntProperty(...)
    
    def callback(self, context):
        # Reagir a mudanças
```

### 4. **Operators Layer** (`operators.py`)

**Responsabilidades:**
- Implementar lógica de negócio
- Manipular dados IFC
- Processar e transformar informações

**Padrão:**
```python
class MyOperator(bpy.types.Operator):
    bl_idname = "namespace.operator_name"
    bl_label = "Label"
    
    def execute(self, context):
        # Lógica principal
        return {'FINISHED'}
```

### 5. **Data Layer** (`data.py`)

**Responsabilidades:**
- Sincronizar dados entre camadas
- Gerenciar eventos e callbacks
- Integrar com bSDD

**Padrão:**
```python
def event_handler(scene):
    # Detecta mudanças
    # Dispara atualizações

def refresh_function(context):
    # Sincroniza dados
    # Filtra resultados
```

---

## 🔄 Fluxos de Dados

### Fluxo 1: Carregar Classes do bSDD

```
Usuário clica "get classes from bSDD" (panels.py)
        │
        ▼
Operador bsdd.get_class (operators.py)
        │
        ├─ Conecta ao servidor bSDD
        ├─ Faz requisição HTTP
        ├─ Recebe dados JSON
        │
        ▼
build_classes() constrói hierarquia
        │
        ├─ Itera sobre classes recursivamente
        ├─ Cria items em props.classes
        ├─ Define relações parent-child
        │
        ▼
data.py refresh() filtra visíveis
        │
        ├─ Limpa props.classes_shown
        ├─ Copia items não-ocultos
        │
        ▼
Panel desenha nova lista (panels.py)
        │
        ▼
Usuário vê resultado
```

### Fluxo 2: Selecionar Objeto e Carregar Propriedades

```
Usuário seleciona objeto no viewport
        │
        ▼
Handler depsgraph_update_post (data.py)
        │
        ▼
on_active_object_change() detecta mudança
        │
        ├─ Compara com last_active
        ├─ Atualiza last_active
        │
        ▼
bpy.ops.props.load_properties() (operators.py)
        │
        ├─ Extrai objeto IFC selecionado
        ├─ Carrega propriedades com ifcopenshell
        ├─ Processa com pandas/numpy se necessário
        │
        ▼
data.py refresh() atualiza listas
        │
        ▼
Panel exibe propriedades (panels.py)
        │
        ▼
Usuário vê informações do objeto
```

### Fluxo 3: Expandir/Contrair Hierarquia

```
Usuário clica em expand/collapse (panels.py)
        │
        ▼
set_hide_class() / set_hide_product() (operators.py)
        │
        ├─ Encontra índice do item
        ├─ Recursivamente oculta/mostra filhos
        ├─ Marca items como is_hidden
        │
        ▼
data.py refresh() atualiza visibilidade
        │
        ├─ Filtra baseado em is_hidden
        ├─ Reconstrói classes_shown
        │
        ▼
Panel redesenha com nova hierarquia (panels.py)
        │
        ▼
Usuário vê estrutura expandida/contraída
```

---

## 🗂️ Estrutura de Dados

### Dados Persistentes (na Scene)
```
context.scene.og_props (SceneProperties)
│
├── classes: CollectionProperty[Ifc_properties]
│   └── [Todas as classes, inclusive ocultas]
│
├── classes_shown: CollectionProperty[Ifc_properties]
│   └── [Classes visíveis apenas]
│
├── types: CollectionProperty[Class_type]
│   └── [Todos os tipos]
│
├── types_show: CollectionProperty[Class_type]
│   └── [Tipos visíveis apenas]
│
└── flags: BoolProperty
    ├── classes_loaded: bool
    ├── types_loaded: bool
    └── product_loaded: bool
```

### Dados em Arquivo JSON (`dados.json`)
```json
{
  "classes": [
    {
      "code": "001",
      "name": "Flexible Pipe",
      "uri": "http://bsdd.buildingsmart.org/...",
      ...
    }
  ],
  "timestamp": "2025-01-19T10:30:00",
  "version": "0.1.1"
}
```

### Dados Temporários em Memória
```python
dynamic_items = []  # Para dropdowns
last_active = None  # Objeto anterior selecionado
bSDD.data_dic = {}  # Cache de dicionários
```

---

## 🔌 Integração com Blender

### PropertyGroups
- Atreladas a `bpy.types.Scene`
- Persistem entre saves
- Atualizáveis via UI

### Operators
- Herdam de `bpy.types.Operator`
- Registrados com `register_class()`
- Acessíveis via `bpy.ops.<namespace>.<name>()`

### Panels
- Herdam de `bpy.types.Panel`
- Renderizados em regiões específicas
- Atualizados automaticamente

### Handlers
- Registrados em `bpy.app.handlers`
- Chamados durante eventos da cena
- Exemplo: `depsgraph_update_post`

---

## 🧪 Padrões de Design

### 1. Property Group Pattern
```python
class MyPropertyGroup(PropertyGroup):
    value: StringProperty(
        name="Value",
        update=callback_function
    )
```

**Vantagem**: Dados sincronizados com UI automaticamente

### 2. Operator Pattern
```python
class MyOperator(bpy.types.Operator):
    bl_idname = "my.operator"
    
    def execute(self, context):
        return {'FINISHED'}
    
    def undo_push(self):
        # Para undo/redo
```

**Vantagem**: Integração com sistema de undo/redo do Blender

### 3. Panel Pattern
```python
class MyPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        # Desenhar elementos
```

**Vantagem**: Aparecem corretamente na UI

### 4. Callback Pattern
```python
def on_property_change(self, context):
    # Reagir a mudanças
    refresh(context)
```

**Vantagem**: Sincronização automática

---

## 🔗 Dependências Entre Módulos

```
__init__.py
    │
    ├─ importa: operators.py, panels.py, properties.py
    ├─ registra: todas as classes
    └─ annexa: PropertyGroups à Scene

operators.py
    ├─ importa: data.py (funções refresh)
    ├─ usa: ifcopenshell, matplotlib, scipy, pandas
    ├─ popula: props.classes, props.types
    └─ chama: data.refresh()

panels.py
    ├─ importa: operators.py (operadores para botões)
    ├─ lê: properties.py (PropertyGroups)
    └─ renderiza: dados de properties

properties.py
    ├─ define: PropertyGroups
    ├─ callbacks: para sincronização
    └─ usado por: panels.py, operators.py

data.py
    ├─ gerencia: eventos e sincronização
    ├─ implementa: refresh functions
    ├─ integra: bSDD
    └─ manipula: properties.py
```

---

## 🚀 Fluxo de Inicialização

```
1. Usuário ativa add-on em Blender
   │
2. __init__.py executa:
   ├─ Define bl_info
   ├─ Importa módulos
   └─ Chama register()
   
3. register() executa:
   ├─ Registra classes (register_class)
   ├─ Anexa PropertyGroups
   └─ Registra handlers
   
4. Blender pronto
   └─ Painel aparece na View3D
   └─ Pronto para usar
```

---

## 📊 Fluxo de Execução de Um Operador

```
Usuário clica botão em Panel (panels.py)
    │
    ▼
Operador disparado (operators.py)
    │
    ├─ Recebe parâmetros do painel
    ├─ Executa lógica principal
    ├─ Modifica context.scene.og_props
    │
    ▼
data.refresh() chamado
    │
    ├─ Filtra dados
    ├─ Atualiza collections
    │
    ▼
Panel render() chamado automaticamente
    │
    ├─ Lê dados atualizados
    ├─ Desenha novamente
    │
    ▼
Usuário vê resultado
```

---

## ⚙️ Configurações e Constantes

### Em `__init__.py`
```python
bl_info = {
    "name": "Oil&Gas Tools",
    "version": (0, 1, 1),
    "blender": (5, 0, 0),
    ...
}
```

### Em `requirements.txt`
```
ifcopenshell==0.8.1
numpy==2.2.4
matplotlib==3.10.5
...
```

### Em `resources/` (dados estáticos)
```
ifc_types.json
FlexiblePipeStructure.json
HangOffCollarType.json
TopBendStiffenerType.json
BendRestrictorType.ttl
units.json
```

---

## 🔐 Segurança e Validação

### Validação IFC
- Verificar se arquivo é válido com `ifcopenshell`
- Testar conformidade com IDS
- Validar estrutura esperada

### Tratamento de Erros
- Try-except em operações de arquivo
- Feedback ao usuário via UI
- Log em console

### Sincronização de Dados
- Evitar loops infinitos de callbacks
- Usar flags para prevenir reprocessamento
- Limpar dados antigos antes de carregar novos

---

## 📚 Recursos Externos

- **Blender Python API**: https://docs.blender.org/api/current/
- **ifcopenshell Docs**: http://docs.ifcopenshell.org/
- **buildingSMART**: https://www.buildingsmart.org/
- **Matplotlib**: https://matplotlib.org/
- **Pandas**: https://pandas.pydata.org/
- **SciPy**: https://scipy.org/

