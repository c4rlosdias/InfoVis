# Módulo: properties.py

## 📌 Visão Geral

Este módulo define as **Property Groups** customizadas que armazenam dados na cena do Blender. Funcionam como "containers" para dados que precisam persistir e sincronizar com a UI.

**Linhas de Código**: 234

---

## 🏗️ Estrutura de Property Groups

### O que é uma PropertyGroup?

Em Blender, uma `PropertyGroup` é um conjunto de propriedades que pode ser anexado a objetos da cena. Funciona como uma classe com atributos tipados que Blender gerencia automaticamente.

```python
class MinhaPropertyGroup(PropertyGroup):
    nome: StringProperty(name="Nome", default="")
    valor: IntProperty(name="Valor", default=0)
    ativo: BoolProperty(name="Ativo", default=True)
```

---

## 🔧 Funções de Callback

### `get_dictionaries(self, context)`
**Tipo**: Callback para EnumProperty

```python
def get_dictionaries(self, context):                
    if not bSDD.is_loaded:
        bSDD.load_dictionaries()
    return bSDD.data_dic
```

**Propósito**: Carrega dicionários bSDD dinamicamente
**Retorno**: Lista de tuplas (id, label, description)
**Gatilho**: Quando propriedade enum é desenhada

### `active_prop_changed(self, context)`
**Tipo**: Callback update_func

```python
def active_prop_changed(self, context):
    self.info_class_prop_loaded = False
    self.class_info.clear()
```

**Propósito**: Limpa dados quando propriedade muda
**Ação**: Reseta flags de carregamento

### `active_class_changed(self, context)`
```python
def active_class_changed(self, context):
    self.class_prop_info.clear()
    self.classes_loaded = False
    self.class_prop_info_loaded = False
```

**Propósito**: Reseta dados ao mudar classe ativa
**Ação**: Limpa inforamções relacionadas

### `active_product_changed(self, context)`
```python
def active_product_changed(self, context):
    self.product_loaded = False
```

**Propósito**: Marca dados como não carregados

### `active_type_changed(self, context)`
```python
def active_type_changed(self, context):
    self.types_loaded = False
```

**Propósito**: Marca tipos como não carregados

---

## 📊 Property Groups Principais

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

**Campos:**
- `name`: StringProperty - Nome do elemento
- `code`: StringProperty - Código identificador
- `description`: StringProperty - Descrição textual
- `uri`: StringProperty - URI/URL único
- `is_selected`: BoolProperty - Flag de seleção (padrão: True)

**Uso**: Informações básicas de qualquer elemento IFC

**Exemplo:**
```python
props = context.scene.og_props
ifc_prop = props.classes.add()
ifc_prop.name = "Flexible Pipe"
ifc_prop.code = "FP-001"
ifc_prop.uri = "http://bsdd.buildingsmart.org/..."
```

---

### 2. **Class_info**

Informações de uma classe no bSDD com suporte a hierarquia.

```python
class Class_info(PropertyGroup):
    code        : StringProperty(name='code')
    name        : StringProperty(name='name')
    description : StringProperty(name='description')
    uri         : StringProperty(name='uri')    
    propertyset : StringProperty(name='property set')
    has_children: BoolProperty(name="has children")    
    is_hidden   : BoolProperty(name="is Hidded", default=True)
    is_expanded : BoolProperty(name="Is Expanded", default=True)
    index       : IntProperty(name="index")
    parent      : StringProperty(name="parent")
    level_index : IntProperty(name="level index")
    type        : StringProperty(name="class type")
```

**Campos:**

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

**Hierarquia de Exemplo:**
```
Classes (level_index=1)
├── Pipes (level_index=2, parent="Classes")
│   ├── Flexible Pipes (level_index=3, parent="Pipes")
│   └── Rigid Pipes (level_index=3, parent="Pipes")
└── Fittings (level_index=2, parent="Classes")
```

---

### 3. **Class_type**

Similar a Class_info mas para tipos de produtos.

```python
class Class_type(PropertyGroup):
    id          : IntProperty(name='id')
    name        : StringProperty(name='name')
    description : StringProperty(name='description')
    element_type : StringProperty(name='element type')
    has_children: BoolProperty(name="has children")    
    is_hidden   : BoolProperty(name="is Hidded", default=True)
    is_expanded : BoolProperty(name="Is Expanded", default=True)
    index       : IntProperty(name="index")
    parent      : StringProperty(name="parent")
```

**Campos Únicos:**
- `id`: IntProperty - Identificador numérico
- `element_type`: StringProperty - Tipo de elemento IFC

**Diferenças de Class_info:**
- Usa `id` inteiro em vez de `code` string
- Sem `propertyset` e `uri`
- Sem `type` (substituído por `element_type`)

---

## 🔗 Relação Entre Property Groups

```python
# Em uma Scene do Blender:
scene.og_props
├── classes: CollectionProperty[Ifc_properties]
│   ├── [0] = {name, code, description, uri, is_selected}
│   ├── [1] = {...}
│   └── [n] = {...}
│
├── classes_shown: CollectionProperty[Ifc_properties]
│   └── (filtradas/visíveis)
│
├── types: CollectionProperty[Class_type]
│   ├── [0] = {id, name, element_type, ...}
│   └── [n] = {...}
│
└── types_show: CollectionProperty[Class_type]
    └── (filtradas/visíveis)
```

---

## 🔄 Fluxo de Atualização

```
Usuário interage com UI
        │
        ▼
Propriedade muda
        │
        ▼
Callback disparado (active_class_changed)
        │
        ▼
Flags resetadas (classes_loaded = False)
        │
        ▼
data.refresh() chamado
        │
        ▼
classes_shown repopulada de classes
        │
        ▼
Panel redesenhado com novos dados
```

---

## 📝 Registrando Property Groups

No `__init__.py`:

```python
from .properties import Class_info, Class_type, Ifc_properties

def register():
    bpy.utils.register_class(Ifc_properties)
    bpy.utils.register_class(Class_info)
    bpy.utils.register_class(Class_type)
    bpy.utils.register_class(SceneProperties)  # Agregador
    Scene.og_props = PointerProperty(type=SceneProperties)

def unregister():
    del Scene.og_props
    bpy.utils.unregister_class(SceneProperties)
    bpy.utils.unregister_class(Class_type)
    bpy.utils.unregister_class(Class_info)
    bpy.utils.unregister_class(Ifc_properties)
```

---

## 🎯 Padrões de Uso

### Adicionar Item a CollectionProperty
```python
props = context.scene.og_props
novo_item = props.classes.add()
novo_item.name = "Nova Classe"
novo_item.code = "NC-001"
```

### Remover Item
```python
props.classes.remove(index)
```

### Iterar Sobre Items
```python
for classe in props.classes:
    print(f"{classe.name}: {classe.description}")
```

### Buscar Item Específico
```python
for classe in props.classes:
    if classe.uri == target_uri:
        return classe
return None
```

### Limpar Collection
```python
props.classes.clear()
```

---

## 💾 Persistência de Dados

PropertyGroups são **automaticamente salvos** com o arquivo .blend:

```
arquivo.blend
├── Scene.og_props
│   ├── classes (salvo)
│   ├── types (salvo)
│   └── states (salvo)
```

Quando reabrir o arquivo, dados serão restaurados automaticamente.

---

## 🔍 Debugging

### Ver Todas as Propriedades
```python
props = bpy.context.scene.og_props
print(dir(props))  # Todas as propriedades
```

### Imprimir Valores
```python
for classe in props.classes:
    print(f"Nome: {classe.name}")
    print(f"  - Code: {classe.code}")
    print(f"  - Level: {classe.level_index}")
    print(f"  - Hidden: {classe.is_hidden}")
```

### Verificar Tipo
```python
print(type(props.classes[0]))  # <class 'bpy.types.Class_info'>
```

---

## ⚠️ Armadilhas Comuns

### 1. Modificar Items Durante Iteração
❌ Evite:
```python
for classe in props.classes:
    props.classes.remove(0)  # Altera índices!
```

✅ Melhor:
```python
indices = [i for i, c in enumerate(props.classes) if c.is_hidden]
for i in reversed(indices):
    props.classes.remove(i)
```

### 2. Não Inicializar PropertyGroup
❌ Evite:
```python
props.nome = "Valor"  # Sem definir propriedade antes
```

✅ Melhor:
```python
class MinhaGroup(PropertyGroup):
    nome: StringProperty(default="")

Scene.meu_grupo = PointerProperty(type=MinhaGroup)
```

### 3. Callbacks Causando Loops Infinitos
❌ Evite:
```python
def callback(self, context):
    self.outra_prop = value  # Dispara outro callback!
```

✅ Melhor:
```python
def callback(self, context):
    if not self.processando:
        self.processando = True
        # ... processar ...
        self.processando = False
```

---

## 🔗 Integração com Outros Módulos

- **operators.py**: Popula as CollectionProperties
- **panels.py**: Lê e exibe dados das PropertyGroups
- **data.py**: Gerencia callbacks e sincronização
- **__init__.py**: Registra as classes

