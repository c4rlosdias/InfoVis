# 📖 Glossário e Referência Rápida

---

## 📚 Glossário de Termos

### Termos Gerais

**Add-on**
- Extensão/plugin para Blender
- Oil & Gas Tools é um add-on (versão 0.1.2)

**Blender**
- Software 3D open-source (versão 5.0+)
- Host da aplicação
- Fornece API Python para extensões

**Contexto (context)**
- Objeto `bpy.context` do Blender
- Contém referências à cena, objetos, propriedades

**Bonsai**
- Add-on BIM para Blender (anteriormente BlenderBIM)
- Dependência principal — fornece IfcStore e ferramentas IFC

### Termos IFC

**IFC (Industry Foundation Classes)**
- Padrão aberto para dados de construção
- Formato: .ifc

**IFC Entity (Entidade)**
- Objeto dentro de um arquivo IFC
- Exemplos: IfcWall, IfcPipeSegment, IfcFlexiblePipe

**bSDD (buildingSMART Data Dictionary)**
- Dicionário internacional de dados de construção
- API REST acessível via HTTP
- Módulo: `data/bsdd.py`

**GUID (GlobalId)**
- Identificador único global para cada entidade IFC

**Pset (Property Set)**
- Conjunto de propriedades aplicável a um elemento
- Exemplo: Pset_WallCommon, EPset_OG

**Qset (Quantity Set)**
- Conjunto de quantidades medidas

**IDS (Information Delivery Specification)**
- Especificação de requisitos de informação em XML
- Exportado via operador `ids.export` em `operators/dictionary.py`

### Termos da Aplicação

**PropertyGroup**
- Classe que define estrutura de dados Blender
- Definidas em `properties/types.py` e `properties/main.py`

**Operador**
- Ação executável pelo usuário via botão/menu
- Organizados em `operators/` (6 submódulos)

**Panel**
- Painel de UI na viewport
- Todos definidos em `panels/main.py`

**Callback**
- Função disparada quando propriedade muda
- Definidos em `properties/main.py`

**Collection**
- Lista de items do mesmo tipo (CollectionProperty)

**Handler**
- Função registrada para evento do Blender
- `depsgraph_update_post` + msgbus

**Autenticação (auth)**
- Sistema de login por senha (SHA-256 + salt)
- Módulo: `auth.py`
- Senha: pré-estabelecida, verificada via `auth.is_authenticated()`

**AddonPreferences (Preferências)**
- Configurações persistentes do add-on
- Classe: `OilGasAddonPreferences` em `__init__.py`
- Campos: CDE URL, token, debug mode, auth password

**CDE (Common Data Environment)**
- Ambiente de dados comum para projetos
- Módulo: `data/cde.py` (stub/mock)

---

## 🏗️ Estrutura Modular

```
oil-gas-addon/
+-- __init__.py          # Registro, preferences, auth operators
+-- auth.py              # Autentica\u00e7\u00e3o SHA-256
+-- data/                # Camada de dados
|   +-- bsdd.py          # Cliente REST bSDD
|   +-- catalog.py       # Import IFC, Catalog, PropTempl
|   +-- cde.py           # API CDE (mock)
|   +-- tree.py          # \u00c1rvore, refresh, callbacks
|   +-- ifc_utils.py     # Utilidades IFC
+-- properties/          # Modelos de dados
|   +-- types.py         # PropertyGroups individuais
|   +-- main.py          # OG_Properties + callbacks
+-- operators/           # L\u00f3gica de neg\u00f3cio
|   +-- common.py        # Utilit\u00e1rios compartilhados
|   +-- dictionary.py    # Operadores bSDD
|   +-- decomposition.py # Decomposi\u00e7\u00e3o IFC
|   +-- catalog.py       # Cat\u00e1logo de tipos
|   +-- connections.py   # Conex\u00f5es IFC
|   +-- properties.py    # Propriedades e gr\u00e1ficos
+-- panels/              # Interface do usu\u00e1rio
    +-- main.py          # Pain\u00e9is e UILists
```

---

## 🎯 Referência Rápida de Código

### Acessar Propriedades
```python
props = context.scene.og_props
classes = props.classes
active_index = props.active_class_index
```

### Verificar Autenticação
```python
from oil_gas_addon.auth import is_authenticated
if is_authenticated():
    # Conte\u00fado protegido
```

### Acessar Preferências
```python
prefs = bpy.context.preferences.addons['oil_gas_addon'].preferences
print(prefs.cde_url)
```

### Adicionar Item a Collection
```python
new_item = props.classes.add()
new_item.name = "Novo Item"
```

### Chamar Operador
```python
bpy.ops.bsdd.get_class()
bpy.ops.props.load_properties()
```

### Registrar/Desregistrar Classe
```python
bpy.utils.register_class(MinhaClasse)
bpy.utils.unregister_class(MinhaClasse)
```

### Acessar Arquivo IFC
```python
import ifcopenshell
from bonsai.bim.ifc import IfcStore
ifc = IfcStore.get_file()
walls = ifc.by_type("IfcWall")
```

---

## 🔧 Padrões Comuns

### Pattern: Operador com Validação
```python
class Operator_example(bpy.types.Operator):
    bl_idname = "og.example"
    bl_label = "Exemplo"

    @classmethod
    def poll(cls, context):
        return len(context.scene.og_props.classes) > 0

    def execute(self, context):
        try:
            props = context.scene.og_props
            self.report({'INFO'}, "Sucesso")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
```

### Pattern: Refresh de Dados
```python
def refresh_list(context):
    props = context.scene.og_props
    props.items_shown.clear()
    for item in props.items_all:
        if not item.is_hidden:
            novo = props.items_shown.add()
            novo.name = item.name
```

---

## 🎨 Convenções de Nomenclatura

### Operadores
```python
Operator_get_properties            # CamelCase com Operator_ prefixo
bl_idname = "bsdd.get_prop"       # namespace.snake_case
```

### Painéis
```python
Panel_Connect                      # CamelCase com Panel_ prefixo
bl_idname = "VIEW3D_PT_og_connect"
bl_category = "O&G-Dictionary"    # Categorias: O&G-Dictionary, O&G-Occurrence, O&G-Catalog, O&G-Info
```

### PropertyGroups
```python
Ifc_properties                     # CamelCase com underscore
Class_info
OG_Properties                      # Agregador principal
```

### Funções
```python
build_classes()                    # snake_case
refresh_products()
set_hide_class()
```

---

## 🔍 Debugging Rápido

### Console Blender (Shift + F4)
```python
# Imports
import bpy
from oil_gas_addon import operators, data, properties, auth

# Propriedades
props = bpy.context.scene.og_props
print(len(props.classes))

# Autentica\u00e7\u00e3o
print(f"Autenticado: {auth.is_authenticated()}")

# Recarregar m\u00f3dulo
import importlib
from oil_gas_addon.data import bsdd
importlib.reload(bsdd)
```

---

## 🆘 Problemas Comuns

**"Login necessário" em todos os painéis**
- Execute `bpy.ops.og.login(password="certi2024")` ou use o painel de login

**"AttributeError: module 'bpy' has no attribute 'types'"**
- Falta import: `import bpy`

**"RuntimeError: context is incorrect"**
- Função chamada fora de contexto Blender

**"Operador não aparece no menu"**
- Não exportado no `operators/__init__.py`
- Não registrado na lista `classes` do `__init__.py` raiz

**"PropertyGroup não persiste"**
- Não registrada com `register_class()`
- Não exportada no `properties/__init__.py`

---

## 📞 Recursos

| Recurso | Link |
|---------|------|
| Blender API | https://docs.blender.org/api/current/ |
| ifcopenshell | http://docs.ifcopenshell.org/ |
| buildingSMART | https://www.buildingsmart.org/ |
| Matplotlib | https://matplotlib.org/ |
| Pandas | https://pandas.pydata.org/ |
| SciPy | https://scipy.org/ |
