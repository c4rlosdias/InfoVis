# 🏗️ Arquitetura - Oil & Gas Tools

## Visão Geral

O Oil & Gas Tools é um **add-on Blender modular** que segue o padrão **MVC (Model-View-Controller)** adaptado para Blender. A partir da versão 0.1.2 a base de código foi reorganizada em **pacotes Python** (packages), substituindo os arquivos monolíticos originais por módulos menores e mais focados.

```
┌───────────────────────────────────────────────────────┐
│                  BLENDER (Host)                       │
├───────────────────────────────────────────────────────┤
│  Panels (UI)           → panels/                      │
│  Properties (Data)     → properties/                  │
│  Operators (Logic)     → operators/                   │
│  Data Layer            → data/                        │
│  Auth                  → auth.py                      │
│  Preferences           → __init__.py                  │
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

## Camadas Principais

### 1. **UI Layer** (`panels/`)
Renderiza painéis na viewport com botões, listas e controles. Interage com o usuário através da interface do Blender. Usa `auth.is_authenticated()` para controlar visibilidade de funcionalidades de edição.

### 2. **Properties Layer** (`properties/`)
Define a estrutura de dados usando PropertyGroups do Blender. Armazena estado da aplicação e sincroniza com UI. Dividido em `types.py` (PropertyGroups individuais) e `main.py` (OG_Properties + callbacks).

### 3. **Operators Layer** (`operators/`)
Implementa a lógica de negócio: extração IFC, construção de hierarquias, processamento de dados. Dividido por domínio: `dictionary.py`, `decomposition.py`, `catalog.py`, `connections.py`, `properties.py` e `common.py`.

### 4. **Data Layer** (`data/`)
Gerencia sincronização entre camadas, callbacks, eventos y integração com bSDD. Dividido em: `bsdd.py` (cliente bSDD), `catalog.py` (importação IFC), `cde.py` (API CDE), `tree.py` (árvore e refresh) e `ifc_utils.py` (utilidades IFC).

### 5. **Auth Layer** (`auth.py`)
Autenticação por senha pré-estabelecida (SHA-256 + salt). Controla visibilidade de funcionalidades de edição nos painéis.

### 6. **Addon Preferences** (`__init__.py`)
Preferências do addon com configurações de CDE, modo debug e autenticação via tela de preferências do Blender.

## Fluxo de Dados

### Exemplo: Carregar Classes do bSDD

```
Usuário clica botão → Operador executa → Dados carregados
      (UI)                (Logic)         (Properties)
       panels/         operators/         properties/
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

| Padrão | Módulo | Uso |
|--------|--------|-----|
| PropertyGroup | properties/ | Dados sincronizados com UI |
| Operator | operators/ | Lógica + undo/redo |
| Panel | panels/ | Interface visual |
| Callback | data/tree.py | Reage a mudanças |
| Auth Guard | auth.py | Controle de acesso por senha |
| AddonPreferences | __init__.py | Configurações do addon |

## Fluxo de Inicialização

```
1. Usuário ativa add-on
2. __init__.py carrega módulos (operators/, panels/, properties/, data/)
3. Registra classes, PropertyGroups e AddonPreferences
4. Registra msgbus subscriber para mudança de objeto ativo
5. Painéis aparecem na View3D (abas O&G-Dictionary, O&G-Occurrence, O&G-Catalog, O&G-Info)
6. Pronto para usar
```

## Dependências Entre Módulos

```
__init__.py (registro + auth + preferences)
    ↓
properties/ ← operators/ ← panels/
    ↓            ↓
  data/ (sincronização, bSDD, IFC utils)
    ↓
External APIs (ifcopenshell, bonsai, bSDD REST, matplotlib, scipy)
```

## Estrutura de Arquivos

```
oil-gas-addon/
├── __init__.py              # Registro, preferences, auth operators
├── auth.py                  # Autenticação por senha (SHA-256)
├── data/                    # Camada de dados
│   ├── __init__.py          # Re-exporta submódulos
│   ├── bsdd.py              # Cliente REST bSDD
│   ├── catalog.py           # Import IFC, Catalog, PropTempl
│   ├── cde.py               # API CDE (mock)
│   ├── tree.py              # Árvore, refresh, callbacks
│   └── ifc_utils.py         # Utilidades IFC, propriedades, conexões
├── properties/              # Estrutura de dados
│   ├── __init__.py          # Re-exporta submódulos
│   ├── types.py             # PropertyGroups individuais
│   └── main.py              # OG_Properties + callbacks
├── operators/               # Lógica de negócio
│   ├── __init__.py          # Re-exporta submódulos
│   ├── common.py            # Utilitários compartilhados
│   ├── dictionary.py        # Operadores bSDD
│   ├── decomposition.py     # Decomposição de elementos
│   ├── catalog.py           # Catálogo de tipos
│   ├── connections.py       # Conexões IFC
│   └── properties.py        # Propriedades e gráficos
├── panels/                  # Interface do usuário
│   ├── __init__.py          # Re-exporta submódulos
│   └── main.py              # Todos os painéis e UILists
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
- Registrar classes com Blender
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
    ├─ Importa pacotes (operators/, panels/, properties/, data/)
    ├─ Importa auth.py
    ├─ Registra classes (register_class)
    ├─ Registra msgbus subscriber (call_back)
    └─ Anexa OG_Properties à Scene
```

### 2. **UI Layer** (`panels/`)

**Módulos:**
- `panels/main.py` — Todos os painéis e UILists

**Responsabilidades:**
- Renderizar painéis na viewport (7 painéis em 4 abas)
- Criar componentes visuais (árvores, listas, botões)
- Usar `auth.is_authenticated()` para controlar visibilidade
- Gerenciar interações do usuário

**Painéis:**
| Painel | Aba | Descrição |
|--------|-----|-----------|
| `Panel_Connect` | O&G-Dictionary | Classes bSDD |
| `Panel_Decompositions` | O&G-Occurrence | Decomposição IFC |
| `Panel_Connect_Elements` | O&G-Occurrence | Conexões entre elementos |
| `Panel_Properties` | O&G-Occurrence | Propriedades do objeto |
| `Panel_Catalog` | O&G-Catalog | Catálogo de tipos |
| `Panel_Settings` | O&G-Info | Configurações bSDD |
| `Panel_Info` | O&G-Info | Informações do addon |

### 3. **Properties Layer** (`properties/`)

**Módulos:**
- `properties/types.py` — PropertyGroups individuais (Ifc_properties, Class_info, Class_type, Container, Property_info, Pset_info, Documents, Layer, etc.)
- `properties/main.py` — OG_Properties (PropertyGroup principal) + callbacks de atualização

**Responsabilidades:**
- Definir estrutura de dados com PropertyGroups
- Gerenciar callbacks de mudança (active_class_changed, etc.)
- Armazenar estado da aplicação (~100 propriedades em OG_Properties)

### 4. **Operators Layer** (`operators/`)

**Módulos:**
| Módulo | Descrição | Operadores |
|--------|-----------|------------|
| `common.py` | Utilitários compartilhados | Operator_expand_tree, Operator_contract_tree, Columns, ErrorMessage |
| `dictionary.py` | Operações bSDD | Operator_get_classes, Operator_get_properties, Operator_export_ids, etc. |
| `decomposition.py` | Decomposição IFC | Operator_decomposition_load, Operator_decomposition_move, etc. |
| `catalog.py` | Catálogo de tipos | Operator_load_products, Operator_catalog_show_layers, etc. |
| `connections.py` | Conexões IFC | Operator_disconnect, Operator_add_connect, etc. |
| `properties.py` | Propriedades e gráficos | Operator_props_edit, Operator_props_graph, etc. |

**Responsabilidades:**
- Implementar lógica de negócio
- Manipular dados IFC via ifcopenshell
- Processar e transformar informações
- Gerar gráficos (matplotlib) e HTML

### 5. **Data Layer** (`data/`)

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

### 6. **Auth Layer** (`auth.py`)

**Responsabilidades:**
- Autenticação por senha pré-estabelecida
- Hash SHA-256 com salt fixo
- Funções: `login()`, `logout()`, `is_authenticated()`
- Controlada via preferências do addon

---

## 🔄 Fluxos de Dados

### Fluxo 1: Carregar Classes do bSDD

```
Usuário clica "get classes from bSDD" (panels/main.py)
        │
        ▼
Operador bsdd.get_class (operators/dictionary.py)
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
Panel desenha nova lista (panels/main.py)
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
Operator_props_load (operators/properties.py)
        │
        ├─ Extrai objeto IFC selecionado
        ├─ Carrega propriedades com ifcopenshell
        │
        ▼
refresh_props() atualiza metadata (data/ifc_utils.py)
        │
        ▼
Panel exibe propriedades (panels/main.py)
        │
        ▼
Usuário vê informações do objeto
```

### Fluxo 3: Expandir/Contrair Hierarquia

```
Usuário clica em expand/collapse (panels/main.py)
        │
        ▼
Operator_expand_tree / Operator_contract_tree (operators/common.py)
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
Panel redesenha com nova hierarquia (panels/main.py)
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
    ├─ importa: operators/, panels/, properties/, data/, auth.py
    ├─ registra: todas as classes
    ├─ define: OilGasAddonPreferences, OG_OT_Login, OG_OT_Logout
    └─ annexa: OG_Properties à Scene

operators/
    ├─ common.py     → importa: data/tree.py (refresh_tree)
    ├─ dictionary.py → importa: data/bsdd.py, data/catalog.py, data/ifc_utils.py, data/tree.py
    ├─ decomposition.py → importa: data/tree.py, operators/common.py
    ├─ catalog.py    → importa: data/catalog.py, data/ifc_utils.py, data/tree.py, operators/common.py
    ├─ connections.py → importa: data/ifc_utils.py
    └─ properties.py → importa: data/ifc_utils.py, operators/common.py

panels/
    └─ main.py       → importa: data/tree.py, data/ifc_utils.py, auth.py

properties/
    ├─ types.py      → standalone PropertyGroups
    └─ main.py       → importa: data/bsdd.py, data/cde.py, properties/types.py

data/
    ├─ bsdd.py       → standalone (requests, ifcopenshell)
    ├─ catalog.py    → importa: data/bsdd.py
    ├─ cde.py        → standalone (requests)
    ├─ tree.py       → standalone (bpy, ifcopenshell, bonsai)
    └─ ifc_utils.py  → standalone (ifcopenshell, numpy, pandas, bonsai)
```

---

## 🚀 Fluxo de Inicialização

```
1. Usuário ativa add-on em Blender
   │
2. __init__.py executa:
   ├─ Define bl_info (versão 0.1.2, Blender 5.0)
   ├─ Adiciona libs/ ao sys.path (ou pip install em Linux/Mac)
   ├─ Importa pacotes (operators/, panels/, properties/, data/)
   ├─ Importa auth.py
   └─ Chama register()
   
3. register() executa:
   ├─ Registra todas as classes (PropertyGroups, Operators, Panels, Preferences)
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
Usuário clica botão em Panel (panels/main.py)
    │
    ▼
Operador disparado (operators/*.py)
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
Panel draw() chamado automaticamente
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

