# Glossario e Referencia Rapida

## Termos principais

**InfoVis**
- add-on para Blender voltado a visualizacao e enriquecimento de dados IFC
- nome definido em `bl_info` em `__init__.py`

**Add-on**
- extensao carregada pelo Blender
- registrada por classes Python derivadas de tipos como `bpy.types.Operator`, `bpy.types.Panel` e `bpy.types.PropertyGroup`

**Blender**
- aplicacao hospedeira do add-on
- fornece API Python, UI, handlers e `msgbus`

**Contexto**
- objeto `bpy.context`
- concentra acesso a cena, objeto ativo, preferencias e estado da interface

**Bonsai**
- ecossistema BIM usado pelo projeto para acesso a dados IFC no Blender

## Termos IFC e integracao

**IFC**
- formato aberto para dados de construcao
- usado como base para leitura de elementos, propriedades, documentos e relacoes

**IFC Entity**
- entidade individual dentro de um arquivo IFC
- exemplos comuns: `IfcWall`, `IfcPipeSegment`, `IfcDistributionElement`

**bSDD**
- buildingSMART Data Dictionary
- dicionario externo consultado por `data/bsdd.py`

**GUID / GlobalId**
- identificador unico de uma entidade IFC

**Pset**
- conjunto de propriedades associado a um elemento

**IDS**
- Information Delivery Specification
- pode ser exportado a partir de operadores do dominio `dictionary`

**CDE**
- Common Data Environment
- integracao apoiada por `data/cde.py`

## Termos internos do projeto

**PropertyGroup**
- estrutura de dados registrada no Blender
- definida em `modules/*/properties.py` e agregada em `modules/og_properties.py`

**OG_Properties**
- agregador central de estado do add-on
- fica em `context.scene.og_props`

**Operator**
- acao executavel exposta ao usuario
- normalmente localizada em `modules/*/operators.py`

**Panel**
- componente visual na sidebar da View3D
- normalmente localizado em `modules/*/panels.py`

**UIList**
- lista visual usada para exibir colecoes Blender com selecao e interacao

**CollectionProperty**
- colecao tipada usada para armazenar listas dentro de `PropertyGroup`s

**Handler**
- funcao registrada em eventos do Blender, como carregamento de arquivo

**msgbus**
- mecanismo de observacao do Blender usado para reagir a mudancas no objeto ativo

**AddonPreferences**
- preferencias persistentes do add-on, definidas em `OilGasAddonPreferences`

## Estrutura do repositorio

```text
InfoVis/
|-- __init__.py
|-- auth.py
|-- data/
|   |-- bsdd.py
|   |-- catalog.py
|   |-- cde.py
|   |-- ifc_utils.py
|   `-- tree.py
|-- modules/
|   |-- __init__.py
|   |-- og_properties.py
|   |-- common/
|   |-- dictionary/
|   |-- decomposition/
|   |-- catalog/
|   |-- connections/
|   |-- props/
|   |-- settings/
|   `-- types/
|-- resources/
|-- libs311/
`-- libs313/
```

## Referencia rapida de codigo

### Acessar o estado principal

```python
props = bpy.context.scene.og_props
print(len(props.classes))
```

### Acessar preferencias do add-on

```python
prefs = bpy.context.preferences.addons["InfoVis"].preferences
print(prefs.cde_url)
```

Se o pacote tiver sido instalado com outro nome de pasta, a chave em `addons[...]` deve seguir o nome real do pacote carregado pelo Blender.

### Chamar operadores comuns

```python
bpy.ops.bsdd.get_prop()
bpy.ops.props.load_properties()
bpy.ops.og.login()
```

### Adicionar item em colecao Blender

```python
item = props.classes.add()
item.name = "Novo item"
```

### Consultar autenticacao

```python
import InfoVis.auth as auth
print(auth.is_authenticated())
```

## Convencoes usadas no codigo

### Classes Blender

```python
class Operator_get_properties(bpy.types.Operator):
    ...

class Panel_Properties(bpy.types.Panel):
    ...
```

### `bl_idname`

```python
bl_idname = "bsdd.get_prop"
bl_idname = "props.load_properties"
bl_idname = "og.login"
```

### Funcoes auxiliares

```python
refresh_classes()
refresh_props()
build_classes()
```

## Padroes recorrentes

**Estado centralizado**
- os paineis e operadores leem e escrevem principalmente em `context.scene.og_props`

**Refresh apos mutacao**
- alteracoes em colecoes ou selecao costumam ser seguidas por chamadas de `refresh_*()` em `data/tree.py` ou `data/ifc_utils.py`

**Registro centralizado**
- toda nova classe Blender deve entrar em `modules/__init__.py`

**Separacao por dominio**
- UI, operadores e dados ficam organizados por dominio funcional em `modules/`

## Debug rapido

### Console Python do Blender

```python
import bpy
import importlib
import InfoVis.auth as auth
from InfoVis.modules import get_classes

props = bpy.context.scene.og_props
print(len(get_classes()))
print(auth.is_authenticated())
print(hasattr(props, "classes"))
```

### Recarregar um modulo

```python
import importlib
import InfoVis.data.bsdd as bsdd

importlib.reload(bsdd)
```

## Problemas comuns

**Operador nao aparece na interface**
- a classe nao foi adicionada a `modules/__init__.py`
- o arquivo nao foi recarregado no Blender depois da mudanca

**PropertyGroup nao persiste**
- o tipo nao foi registrado antes de `OG_Properties`
- a propriedade nao foi anexada corretamente ao agregador central ou a `Scene`

**Erro de contexto no Blender**
- operador ou funcao foi chamado fora do contexto esperado pela UI ou pelo objeto ativo

**ImportError de dependencia cientifica**
- ambiente Blender nao encontrou as bibliotecas embarcadas ou faltou instalacao dinamica fora do Windows

**Dados nao atualizam ao trocar selecao**
- verificar handlers, assinatura de `msgbus` e funcoes de `refresh_*()`

## Recursos externos

| Recurso | Link |
|---------|------|
| Blender API | https://docs.blender.org/api/current/ |
| IfcOpenShell | https://docs.ifcopenshell.org/ |
| buildingSMART | https://www.buildingsmart.org/ |
| Matplotlib | https://matplotlib.org/ |
| SciPy | https://scipy.org/ |
