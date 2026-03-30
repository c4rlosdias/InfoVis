# 📖 Glossário e Referência Rápida

---

## 📚 Glossário de Termos

### Termos Gerais

**Add-on**
- Extensão/plugin para Blender
- Código Python que estende funcionalidades
- Oil & Gas Tools é um add-on

**Blender**
- Software 3D open-source
- Host da aplicação
- Fornece API Python para extensões

**Contexto (context)**
- Objeto `bpy.context` do Blender
- Contém referências à cena, objetos, propriedades
- Passado como parâmetro em praticamente todas as funções

### Termos IFC

**IFC (Industry Foundation Classes)**
- Padrão aberto para dados de construção
- Define estrutura de dados para edifícios
- Formato: .ifc

**IFC Entity (Entidade)**
- Objeto dentro de um arquivo IFC
- Exemplos: IfcWall (parede), IfcDoor (porta)
- Cada entidade tem propriedades e relacionamentos

**bSDD (buildingSMART Data Dictionary)**
- Dicionário internacional de dados de construção
- Contém definições de tipos de elementos
- API acessível via HTTP

**GUID (GlobalId)**
- Identificador único global para cada entidade IFC
- Garante unicidade mesmo entre arquivos diferentes
- Formato: "3Q3YFPY9L0Hu0xsQc_HyHF"

**Pset (Property Set)**
- Conjunto de propriedades aplicável a um elemento
- Exemplo: Pset_WallCommon para paredes
- Contém propriedades como Name, Description, etc

**Qset (Quantity Set)**
- Conjunto de quantidades medidas
- Exemplo: Qto_WallBaseQuantities para paredes
- Contém: Height, Length, Area, Volume, etc

### Termos da Aplicação

**PropertyGroup**
- Classe que define estrutura de dados
- Anexada a objetos Blender (Scene, Object, etc)
- Dados persistem quando arquivo é salvo

**Operador**
- Ação que usuário pode executar
- Herdado de `bpy.types.Operator`
- Acessível via menu ou botão

**Panel**
- Painel de UI na viewport
- Herdado de `bpy.types.Panel`
- Contém botões, listas, campos de entrada

**Callback**
- Função disparada quando algo muda
- Exemplo: quando propriedade é alterada
- Permite reações automáticas

**Collection**
- Lista de items do mesmo tipo
- Armazenada em PropertyGroup
- Acessível como array: `collection[0]`, `collection.add()`

**Handler**
- Função registrada para evento do Blender
- Exemplo: `depsgraph_update_post` (cena mudou)
- Permite automação baseada em eventos

---

## 🎯 Referência Rápida de Código

### Acessar Propriedades
```python
props = context.scene.og_props              # PropertyGroup da cena
classes = props.classes                     # CollectionProperty
active_index = props.active_class_index     # IntProperty
```

### Iterar sobre Items
```python
for classe in props.classes:
    print(classe.name)

# Com índice
for i, classe in enumerate(props.classes):
    if i == props.active_class_index:
        print(f"Item ativo: {classe.name}")
```

### Adicionar Item a Collection
```python
new_item = props.classes.add()
new_item.name = "Novo Item"
new_item.code = "NI-001"
```

### Remover Item
```python
props.classes.remove(index)  # Remove por índice
```

### Limpar Collection
```python
props.classes.clear()  # Remove todos
```

### Buscar Item
```python
def find_by_name(context, target_name):
    for item in context.scene.og_props.classes:
        if item.name == target_name:
            return item
    return None
```

### Chamar Operador
```python
bpy.ops.namespace.operator_name()              # Sem parâmetros
bpy.ops.namespace.operator_name(prop="valor")  # Com parâmetros
```

### Registrar Classe
```python
from bpy.utils import register_class, unregister_class

register_class(MinhaClasse)      # Registra
unregister_class(MinhaClasse)    # Desregistra
```

### Registrar Handler
```python
def meu_handler(scene):
    print("Cena mudou!")

# Registrar
bpy.app.handlers.depsgraph_update_post.append(meu_handler)

# Desregistrar
bpy.app.handlers.depsgraph_update_post.remove(meu_handler)
```

### Acessar Arquivo IFC
```python
import ifcopenshell

ifc = ifcopenshell.open("caminho/arquivo.ifc")
walls = ifc.by_type("IfcWall")
door = ifc.by_id(123)

for entity in ifc:
    print(entity.is_a())  # Tipo de entidade
```

### Extrair Propriedades IFC
```python
import ifcopenshell.util.element as element

psets = element.get_psets(wall)              # Property Sets
qsets = element.get_qsets(wall)              # Quantity Sets
value = element.get_pset_value(wall, "...")  # Um valor específico
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
            # Lógica segura
            self.report({'INFO'}, "Sucesso")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
```

### Pattern: PropertyGroup com Callback
```python
class MeuPropertyGroup(PropertyGroup):
    valor: IntProperty(
        name="Valor",
        default=0,
        update=on_valor_changed
    )

def on_valor_changed(self, context):
    # Reagir a mudança
    print(f"Novo valor: {self.valor}")
```

### Pattern: Panel com Template List
```python
class MeuPanel(bpy.types.Panel):
    def draw(self, context):
        layout = self.layout
        props = context.scene.og_props
        
        layout.template_list(
            "UI_UL_list",
            "",
            props,
            "items",
            props,
            "active_index",
            rows=10
        )
```

### Pattern: Refresh de Dados
```python
def refresh_list(context):
    props = context.scene.og_props
    props.itens_visíveis.clear()
    
    for item in props.items_todos:
        if not item.is_hidden:
            novo = props.itens_visíveis.add()
            novo.name = item.name
            novo.valor = item.valor
```

---

## 📊 Estrutura de Dados Padrão

### Classe Hierárquica
```
Class_info
├── code: "001"              (identificação)
├── name: "Pipe"
├── description: "Descrição"
├── uri: "http://bsdd/..."   (único)
├── level_index: 1           (profundidade)
├── parent: "Classes"        (elemento pai)
├── index: 0                 (posição sequencial)
├── has_children: True       (tem subclasses?)
├── is_hidden: False         (oculto na UI?)
├── is_expanded: True        (expandido?)
└── type: "IfcPipeSegment"   (tipo IFC)
```

### Tipo de Produto
```
Class_type
├── id: 123                   (id numérico)
├── name: "Produto"
├── description: "Descrição"
├── element_type: "IfcPipe"   (tipo de elemento)
├── level_index: 2
├── parent: "Categoria"
├── index: 5
├── has_children: False
└── is_hidden: False
```

---

## 🎨 Convenções de Nomenclatura

### Operadores
```python
Operator_get_properties           # CamelCase com Operator_ prefixo
Operator_load_decomposition
Operator_expand_classes

# bl_idname (snake_case com ponto)
bl_idname = "og.get_properties"
bl_idname = "og.load_decomposition"
```

### Painéis
```python
Panel_Connect                      # CamelCase com Panel_ prefixo
Panel_Properties
Panel_Analysis

# bl_idname (VIEW3D_PT_<nome>)
bl_idname = "VIEW3D_PT_og_connect"
```

### PropertyGroups
```python
Ifc_properties                     # CamelCase com underscore
Class_info
Class_type
OG_scene_properties
```

### Funções
```python
build_classes()                    # snake_case
refresh_products()
set_hide_class()
on_active_object_change()
```

### Variáveis
```python
props = context.scene.og_props     # snake_case
active_index = 0
dynamic_items = []
```

---

## 🔍 Debugging Rápido

### Console Blender (Shift + F4)
```python
# Imprimir propriedades
props = bpy.context.scene.og_props
print(len(props.classes))
print([c.name for c in props.classes[:5]])

# Chamar função
from oil_gas_addon.data import refresh
refresh(bpy.context)

# Verificar handlers
print(bpy.app.handlers.depsgraph_update_post)
```

### Imprimir Objeto Selecionado
```python
obj = bpy.context.active_object
print(f"Nome: {obj.name}")
print(f"Tipo: {obj.type}")
print(f"Dados: {obj.data}")
```

### Validar IFC
```python
import ifcopenshell
ifc = ifcopenshell.open("arquivo.ifc")
print(f"Válido: {ifc.is_valid()}")
print(f"Esquema: {ifc.schema}")
print(f"Total entidades: {len(ifc)}")
```

---

## 📋 Checklist de Deployment

- [ ] Código testado em Blender
- [ ] Sem erros no console
- [ ] Docstrings completas
- [ ] Sem trailing whitespace
- [ ] Imports organizados
- [ ] Variáveis bem nomeadas
- [ ] Funções pequenas e focadas
- [ ] Tratamento de exceções
- [ ] Mensagens de erro claras
- [ ] Comentários onde necessário
- [ ] Git commit com mensagem descritiva
- [ ] Documentação atualizada

---

## 🚀 Comandos Úteis

### Terminal
```bash
# Verificar sintaxe Python
python -m py_compile arquivo.py

# Executar testes
python -m pytest tests/

# Formatar código
black arquivo.py

# Verificar estilo
pylint arquivo.py

# Gerar documentação
sphinx-build -b html docs/ docs/_build/
```

### Git
```bash
# Ver status
git status

# Commit com mensagem
git commit -m "feat: descrição"

# Ver histórico
git log --oneline -10

# Criar branch
git checkout -b feature/nome

# Merge
git merge feature/nome
```

### Blender (Python Script)
```python
# Recarregar addon
import importlib
from oil_gas_addon import operators
importlib.reload(operators)

# Registrar classes
bpy.utils.register_class(Operator_novo)
```

---

## 🆘 Problemas Comuns

**"AttributeError: module 'bpy' has no attribute 'types'"**
- Falta import: `import bpy`

**"RuntimeError: context is incorrect"**
- Função chamada fora de contexto Blender
- Use `bpy.context` apropriadamente

**"Operador não aparece no menu"**
- Não registrado em `__init__.py`
- `bl_idname` inválido
- Erro de sintaxe

**"PropertyGroup não persiste"**
- Não registrado com `register_class()`
- Não anexado corretamente: `Scene.prop = PointerProperty(...)`

**"Handler chamado múltiplas vezes"**
- Registrado múltiplas vezes sem remover
- Verificar com: `print(bpy.app.handlers.event)`

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

---

## 🎓 Exercícios Sugeridos

1. **Iniciante**
   - Adicione um novo atributo StringProperty a uma PropertyGroup
   - Crie um botão que imprime "Olá Mundo" no console

2. **Intermediário**
   - Crie um novo operador que ordena as classes por nome
   - Adicione um painel que mostra estatísticas dos dados

3. **Avançado**
   - Implemente cache de dados com invalidação automática
   - Crie exportador de dados para CSV/JSON
   - Adicione sistema de plugins para extensões

---

## 📝 Notas Finais

- **Sempre** revise a documentação relevante antes de implementar
- **Sempre** teste em Blender depois de mudanças
- **Sempre** commit regularmente no Git
- **Sempre** mantenha a documentação atualizada

---

**Boa sorte com o desenvolvimento! 🚀**
