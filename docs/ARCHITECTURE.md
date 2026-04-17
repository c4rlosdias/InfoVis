# 🏗️ Arquitetura - Oil & Gas Tools

## Visão Geral

O Oil & Gas Tools é um **add-on Blender modular** organizado por **domínio funcional**. Cada domínio (dictionary, decomposition, catalog, connections, props) possui seus próprios operadores, painéis e propriedades dentro de uma pasta dedicada em `modules/`.

```
┌───────────────────────────────────────────────────────┐
│                  BLENDER (Host)                       │
├───────────────────────────────────────────────────────┤
│  modules/                                             │
│  ├── common/       → utilitários compartilhados       │
│  ├── dictionary/   → operadores, painéis, propriedades│
│  ├── decomposition/→ operadores, painéis, propriedades│
│  ├── catalog/      → operadores, painéis, propriedades│
│  ├── connections/  → operadores, painéis              │
│  ├── props/        → operadores, painéis, propriedades│
│  ├── settings/     → painéis                          │
│  └── og_properties.py → OG_Properties + callbacks     │
│  Data Layer        → data/                            │
│  Auth              → auth.py                          │
│  Preferences       → __init__.py                      │
└──────────────────────┬────────────────────────────────┘
                       │
                       ▼
         ┌──────────────────────────┐
         │  External Services       │
         ├──────────────────────────┤
         │ • bSDD (HTTP REST)       │
         │ • ifcopenshell / bonsai  │
         │ • matplotlib, scipy      │
         │ • CDE API (mock)         │
         └──────────────────────────┘
```

## Organização por Domínio

Cada módulo de domínio dentro de `modules/` segue a mesma estrutura:

```
modules/<domínio>/
├── __init__.py      # (vazio)
├── operators.py     # Operadores (lógica de negócio)
├── panels.py        # Painéis e UILists (interface)
└── properties.py    # PropertyGroups (dados)
```

### 1. **Dictionary** (`modules/dictionary/`)
Integração com bSDD: carregamento de classes, propriedades, exportação IDS.

### 2. **Decomposition** (`modules/decomposition/`)
Hierarquia IFC: decomposição de elementos, árvore CDE, reordenação.

### 3. **Catalog** (`modules/catalog/`)
Catálogo de tipos de produto: carregamento, seleção, camadas.

### 4. **Connections** (`modules/connections/`)
Conexões entre elementos IFC: criar, remover, visualizar.

### 5. **Props** (`modules/props/`)
Propriedades do objeto selecionado: edição, gráficos, documentos.

### 6. **Settings** (`modules/settings/`)
Painéis de configuração (dicionário bSDD) e informações do addon.

### 7. **Common** (`modules/common/`)
Utilitários compartilhados: expand/contract tree, Columns, ErrorMessage.

### 8. **OG_Properties** (`modules/og_properties.py`)
PropertyGroup central que agrega todas as propriedades da aplicação + callbacks de atualização.

## Camadas de Suporte

### **Data Layer** (`data/`)
Gerencia sincronização entre camadas, callbacks, eventos e integração com bSDD. Dividido em: `bsdd.py` (cliente bSDD), `catalog.py` (importação IFC), `cde.py` (API CDE), `tree.py` (árvore e refresh) e `ifc_utils.py` (utilidades IFC).

### **Auth Layer** (`auth.py`)
Autenticação por senha pré-estabelecida (SHA-256 + salt). Controla visibilidade de funcionalidades de edição nos painéis.

### **Addon Preferences** (`__init__.py`)
Preferências do addon com configurações de CDE, modo debug e autenticação via tela de preferências do Blender.

## Fluxo de Dados

### Exemplo: Carregar Classes do bSDD

```
Usuário clica botão → Operador executa → Dados carregados
      (UI)                (Logic)         (Properties)
   modules/*/panels   modules/*/operators   modules/og_properties
                            │
                            ▼
                    data/tree.py refresh() atualiza
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
├── elements_containers: decomposição completa
├── containers_show: decomposição visível
├── elements_tree: árvore CDE
├── prop_metadata: propriedades do objeto selecionado
├── documents: documentos associados
└── flags: status de carregamento
```

## Padrões de Design

| Padrão | Local | Uso |
|--------|-------|-----|
| Domain Module | modules/<domínio>/ | Agrupa operators + panels + properties por funcionalidade |
| PropertyGroup | modules/<domínio>/properties.py | Dados sincronizados com UI |
| Operator | modules/<domínio>/operators.py | Lógica + undo/redo |
| Panel | modules/<domínio>/panels.py | Interface visual |
| Central Registry | modules/__init__.py | get_classes() retorna todas as classes na ordem correta |
| Callback | data/tree.py | Reage a mudanças |
| Auth Guard | auth.py | Controle de acesso por senha |
| AddonPreferences | __init__.py | Configurações do addon |

## Fluxo de Inicialização

```
1. Usuário ativa add-on
2. __init__.py importa modules.get_classes() e modules.og_properties.OG_Properties
3. modules/__init__.py importa todos os submódulos de domínio
4. Registra classes na ordem: PropertyGroups → OG_Properties → Operators → Panels
5. Registra msgbus subscriber para mudança de objeto ativo
6. Painéis aparecem na View3D (abas O&G-Dictionary, O&G-Occurrence, O&G-Catalog, O&G-Info)
7. Pronto para usar
```

## Dependências Entre Módulos

```
__init__.py (registro + auth + preferences)
    ↓
modules/__init__.py → get_classes()
    ↓
modules/<domínio>/properties.py  (PropertyGroups - sem dependências externas)
    ↓
modules/og_properties.py  (importa PropertyGroups de todos os domínios + data/bsdd, data/cde)
    ↓
modules/<domínio>/operators.py  (importa data/, common/operators)
    ↓
modules/<domínio>/panels.py  (importa data/, auth)
    ↓
data/ (sincronização, bSDD, IFC utils)
    ↓
External APIs (ifcopenshell, bonsai, bSDD REST, matplotlib, scipy)
```

## Estrutura de Arquivos

```
oil-gas-addon/
├── __init__.py              # Registro, preferences, auth operators
├── auth.py                  # Autenticação por senha (SHA-256)
├── modules/                 # Módulos organizados por domínio
│   ├── __init__.py          # get_classes() - registro centralizado
│   ├── og_properties.py     # OG_Properties + callbacks
│   ├── common/              # Utilitários compartilhados
│   │   ├── __init__.py
│   │   └── operators.py     # expand/contract tree, Columns, ErrorMessage
│   ├── dictionary/          # Integração bSDD
│   │   ├── __init__.py
│   │   ├── operators.py     # 11 operadores bSDD + IDS
│   │   ├── panels.py        # Panel_Connect, UILists
│   │   └── properties.py    # Ifc_properties, Class_info, Class_prop_info
│   ├── decomposition/       # Decomposição IFC
│   │   ├── __init__.py
│   │   ├── operators.py     # 5 operadores decomposição
│   │   ├── panels.py        # Panel_Decompositions, UILists
│   │   └── properties.py    # Container
│   ├── catalog/             # Catálogo de tipos
│   │   ├── __init__.py
│   │   ├── operators.py     # 4 operadores catálogo
│   │   ├── panels.py        # Panel_Catalog, UILists
│   │   └── properties.py    # Class_type, Layer
│   ├── connections/         # Conexões entre elementos
│   │   ├── __init__.py
│   │   ├── operators.py     # 3 operadores conexão
│   │   └── panels.py        # Panel_Connect_Elements
│   ├── props/               # Propriedades do objeto
│   │   ├── __init__.py
│   │   ├── operators.py     # 10 operadores propriedades/gráficos
│   │   ├── panels.py        # Panel_Properties
│   │   └── properties.py    # Enumeration_values, Property_info, Documents, Pset_info
│   └── settings/            # Configurações e info
│       ├── __init__.py
│       └── panels.py        # Panel_Settings, Panel_Info
├── data/                    # Camada de dados (compartilhada)
│   ├── __init__.py
│   ├── bsdd.py              # Cliente REST bSDD
│   ├── catalog.py           # Import IFC, Catalog, PropTempl
│   ├── cde.py               # API CDE (mock)
│   ├── tree.py              # Árvore, refresh, callbacks
│   └── ifc_utils.py         # Utilidades IFC, propriedades, conexões
├── resources/               # Dados estáticos (JSON)
├── libs/                    # Dependências embarcadas (Windows)
└── files/                   # Arquivos IFC de teste
```

## Para Mais Detalhes

- **[Desenvolvimento](DEVELOPMENT.md)** - Como setup e contribuir
- **[Módulos](guides/)** - Documentação completa por arquivo
- **[Glossário](reference/GLOSSARY.md)** - Termos e FAQ

### 1. **Initialization Layer** (`__init__.py`)

**Responsabilidades:**
- Definir metadados do add-on (`bl_info`)
- Importar `modules.get_classes()` para obter todas as classes
- Gerenciar ciclo de vida (register/unregister)
- Definir `OilGasAddonPreferences` (CDE URL, token, debug, auth)
- Definir operadores de autenticação (`OG_OT_Login`, `OG_OT_Logout`)
- Registrar msgbus subscriber para callback de objeto ativo

**Fluxo:**
```
Blender inicia add-on
    │
    ▼
__init__.py executa
    │
    ├─ Define bl_info
    ├─ Importa modules.get_classes() e modules.og_properties.OG_Properties
    ├─ Importa auth.py e data/
    ├─ Monta lista: [Preferences, Login, Logout] + get_classes()
    ├─ Registra classes (register_class)
    ├─ Registra msgbus subscriber (call_back)
    └─ Anexa OG_Properties à Scene
```

### 2. **Modules Registry** (`modules/__init__.py`)

**Responsabilidades:**
- Importar todos os submódulos de domínio
- Definir `get_classes()` que retorna todas as classes na ordem correta de registro
- Garantir que PropertyGroups são registrados antes de OG_Properties

### 3. **Domain Modules** (`modules/<domínio>/`)

Cada domínio possui até 3 arquivos:

| Arquivo | Conteúdo |
|---------|----------|
| `operators.py` | Operadores (bpy.types.Operator) — lógica de negócio |
| `panels.py` | Painéis (bpy.types.Panel) e UILists — interface |
| `properties.py` | PropertyGroups (bpy.types.PropertyGroup) — dados |

**Painéis por domínio:**
| Domínio | Painel | Aba |
|---------|--------|-----|
| dictionary | `Panel_Connect` | O&G-Dictionary |
| decomposition | `Panel_Decompositions` | O&G-Occurrence |
| connections | `Panel_Connect_Elements` | O&G-Occurrence |
| props | `Panel_Properties` | O&G-Occurrence |
| catalog | `Panel_Catalog` | O&G-Catalog |
| settings | `Panel_Settings`, `Panel_Info` | O&G-Info |

### 4. **Data Layer** (`data/`)

**Módulos:**
| Módulo | Descrição |
|--------|-----------|
| `bsdd.py` | Cliente REST para bSDD (classe `bSDD`) |
| `catalog.py` | Import_ifc, Catalog, PropTempl |
| `cde.py` | CDE_Api (mock/placeholder) |
| `tree.py` | draw_tree(), refresh_*(), callbacks, decomposição |
| `ifc_utils.py` | Propriedades IFC, unidades, conexões, build_classes/products |

**Responsabilidades:**
- Sincronizar dados entre camadas
- Gerenciar eventos e callbacks (msgbus)
- Integrar com bSDD via HTTP REST
- Manipular propriedades e conexões IFC

### 5. **Auth Layer** (`auth.py`)

**Responsabilidades:**
- Autenticação por senha pré-estabelecida
- Hash SHA-256 com salt fixo
- Funções: `login()`, `logout()`, `is_authenticated()`
- Controlada via preferências do addon

---

## 🔄 Fluxos de Dados

### Fluxo 1: Carregar Classes do bSDD

```
Usuário clica "get classes from bSDD" (modules/dictionary/panels.py)
        │
        ▼
Operador bsdd.get_class (modules/dictionary/operators.py)
        │
        ├─ Conecta ao servidor bSDD (data/bsdd.py)
        ├─ Faz requisição HTTP
        ├─ Recebe dados JSON
        │
        ▼
build_classes() constrói hierarquia (data/ifc_utils.py)
        │
        ├─ Itera sobre classes recursivamente
        ├─ Cria items em props.classes
        ├─ Define relações parent-child
        │
        ▼
refresh_classes() filtra visíveis (data/tree.py)
        │
        ├─ Limpa props.classes_shown
        ├─ Copia items não-ocultos
        │
        ▼
Panel desenha nova lista (modules/dictionary/panels.py)
        │
        ▼
Usuário vê resultado
```

### Fluxo 2: Selecionar Objeto e Carregar Propriedades

```
Usuário seleciona objeto no viewport
        │
        ▼
msgbus subscriber dispara (data/tree.py)
        │
        ▼
call_back() → bpy.ops.props.load_properties()
        │
        ▼
Operator_props_load (modules/props/operators.py)
        │
        ├─ Extrai objeto IFC selecionado
        ├─ Carrega propriedades com ifcopenshell
        │
        ▼
refresh_props() atualiza metadata (data/ifc_utils.py)
        │
        ▼
Panel exibe propriedades (modules/props/panels.py)
        │
        ▼
Usuário vê informações do objeto
```

### Fluxo 3: Expandir/Contrair Hierarquia

```
Usuário clica em expand/collapse (modules/<domínio>/panels.py)
        │
        ▼
Operator_expand_tree / Operator_contract_tree (modules/common/operators.py)
        │
        ├─ Encontra índice do item
        ├─ Marca items como is_hidden
        │
        ▼
refresh_tree() atualiza visibilidade (data/tree.py)
        │
        ├─ Filtra baseado em is_hidden
        ├─ Reconstrói coleção visível
        │
        ▼
Panel redesenha com nova hierarquia (modules/<domínio>/panels.py)
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

## 🔗 Dependências Detalhadas Entre Módulos

```
__init__.py
    │
    ├─ importa: modules.get_classes(), modules.og_properties.OG_Properties
    ├─ importa: data/, auth.py
    ├─ define: OilGasAddonPreferences, OG_OT_Login, OG_OT_Logout
    └─ anexa: OG_Properties à Scene

modules/__init__.py
    ├─ importa todos os submódulos de domínio
    └─ define: get_classes() com ordem de registro

modules/og_properties.py
    └─ importa PropertyGroups de: dictionary, catalog, props, decomposition
    └─ importa: data/bsdd.py, data/cde.py

modules/common/operators.py    → importa: data/tree.py (refresh_tree)
modules/dictionary/operators.py → importa: data/bsdd.py, data/catalog.py, data/ifc_utils.py, data/tree.py
modules/dictionary/panels.py   → importa: data/tree.py, data/ifc_utils.py, auth.py
modules/decomposition/operators.py → importa: data/tree.py, common/operators.py
modules/decomposition/panels.py   → importa: data/tree.py, auth.py
modules/catalog/operators.py   → importa: data/catalog.py, data/ifc_utils.py, data/tree.py, common/operators.py
modules/catalog/panels.py      → importa: data/tree.py
modules/connections/operators.py → importa: data/ifc_utils.py
modules/connections/panels.py  → importa: auth.py
modules/props/operators.py     → importa: data/ifc_utils.py, common/operators.py
modules/props/panels.py        → importa: data/ifc_utils.py, auth.py

data/
    ├─ bsdd.py       → standalone (requests, ifcopenshell)
    ├─ catalog.py    → importa: data/bsdd.py
    ├─ cde.py        → standalone (requests)
    ├─ tree.py       → standalone (bpy, ifcopenshell, bonsai)
    └─ ifc_utils.py  → standalone (ifcopenshell, numpy, pandas, bonsai)
```

---

## 🚀 Fluxo de Inicialização Detalhado

```
1. Usuário ativa add-on em Blender
   │
2. __init__.py executa:
   ├─ Define bl_info (versão 0.1.2, Blender 5.0)
   ├─ Adiciona libs/ ao sys.path (ou pip install em Linux/Mac)
   ├─ Importa modules.get_classes() e modules.og_properties.OG_Properties
   ├─ Importa auth.py e data/
   └─ Chama register()
   
3. register() executa:
   ├─ Registra classes: [Preferences, Login, Logout] + get_classes()
   ├─ get_classes() retorna PropertyGroups → OG_Properties → Operators → Panels
   ├─ Anexa OG_Properties à Scene
   ├─ Cria PointerProperties no WindowManager (add_connect_object_a/b/c)
   └─ Registra msgbus subscriber para mudança de objeto ativo
   
4. Blender pronto
   ├─ Painéis aparecem na View3D sidepanel (N)
   ├─ Abas: O&G-Dictionary, O&G-Occurrence, O&G-Catalog, O&G-Info
   └─ Preferências acessíveis em Edit > Preferences > Add-ons
```

---

## 📊 Fluxo de Execução de Um Operador

```
Usuário clica botão em Panel (modules/<domínio>/panels.py)
    │
    ▼
Operador disparado (modules/<domínio>/operators.py)
    │
    ├─ Recebe parâmetros do painel
    ├─ Executa lógica principal
    ├─ Modifica context.scene.og_props
    │
    ▼
refresh_*() chamado (data/tree.py ou data/ifc_utils.py)
    │
    ├─ Filtra dados
    ├─ Atualiza collections visíveis
    │
    ▼
Panel draw() chamado automaticamente (modules/<domínio>/panels.py)
    │
    ├─ Lê dados atualizados
    ├─ Verifica auth.is_authenticated() para funcionalidades de edição
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

