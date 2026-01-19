# Guia de Desenvolvimento - Oil & Gas Tools

## 🎯 Objetivo

Este guia fornece instruções práticas para desenvolvedores que desejam adicionar funcionalidades, corrigir bugs ou manter o Oil & Gas Tools.

---

## 🔧 Ambiente de Desenvolvimento

### Requisitos
- Blender 5.0+ instalado
- Python 3.10+
- Git (para controle de versão)
- VS Code ou editor de código preferido

### Setup Inicial

1. **Clone o repositório:**
```bash
git clone <repo-url> oil-gas-addon
cd oil-gas-addon
```

2. **Instale dependências locais:**
```bash
pip install -r requirements.txt
```

3. **Configure o Blender:**
```bash
# Copie para pasta de add-ons
cp -r . "/path/to/Blender/5.0/scripts/addons/oil-gas-addon"
```

4. **Ative em Blender:**
   - Edit > Preferences > Add-ons
   - Busque "Oil & Gas"
   - Clique para ativar

### Setup de Debug

**No Blender, abra o console:**
- Shift + F4

**Teste de inicialização:**
```python
import bpy
from oil_gas_addon import operators, panels, properties

print("Módulos carregados com sucesso!")
print(f"Operadores: {len([x for x in dir(operators) if 'Operator' in x])}")
```

---

## 📝 Adicionar uma Nova Funcionalidade

### Exemplo: Adicionar novo operador

**1. Defina em `operators.py`:**
```python
class Operator_my_new_operator(bpy.types.Operator):
    """Tooltip de ajuda"""
    bl_idname = "og.my_operator"
    bl_label = "Meu Novo Operador"
    bl_description = "Descrição completa"
    
    # Propriedades do operador
    my_prop: bpy.props.StringProperty(
        name="Propriedade",
        description="Descrição",
        default=""
    )
    
    @classmethod
    def poll(cls, context):
        """Quando o operador está disponível?"""
        return context.scene.og_props.classes_loaded
    
    def execute(self, context):
        """Lógica principal"""
        props = context.scene.og_props
        
        # Seu código aqui
        self.report({'INFO'}, "Operador executado!")
        
        return {'FINISHED'}
```

**2. Registre em `__init__.py`:**
```python
from .operators import *

classes = [
    # ... outras classes ...
    Operator_my_new_operator,  # <- Adicione aqui
]
```

**3. Adicione botão no painel em `panels.py`:**
```python
def draw(self, context):
    layout = self.layout
    
    # Novo botão
    row = layout.row()
    op = row.operator("og.my_operator", text="Executar Meu Operador")
    op.my_prop = "valor_padrao"
```

**4. Teste:**
- Recarregue o add-on (Edit > Preferences > Add-ons > Desabilitar/Habilitar)
- Veja botão aparecer no painel
- Clique e teste

---

## 🎨 Adicionar Novo Painel

**1. Defina em `panels.py`:**
```python
class Panel_my_panel(bpy.types.Panel):
    """Painel de informações do meu módulo"""
    bl_label = "Meu Painel"
    bl_idname = "VIEW3D_PT_my_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = "O&G Tools"
    bl_order = 1  # Ordem entre os painéis
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        self.layout.label(text="", icon='TOOL_SETTINGS')
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.og_props
        
        # Seu conteúdo aqui
        layout.label(text="Bem-vindo ao meu painel!")
```

**2. Nenhuma mudança necessária em outros arquivos** (descoberta automática)

---

## 🔧 Adicionar Nova PropertyGroup

**1. Defina em `properties.py`:**
```python
class My_custom_property(PropertyGroup):
    """Minhas propriedades customizadas"""
    
    my_string: StringProperty(
        name="Minha String",
        description="Descrição",
        default="valor padrão"
    )
    
    my_number: IntProperty(
        name="Meu Número",
        description="Um número",
        default=0,
        min=0,
        max=100
    )
    
    my_list: CollectionProperty(
        type=My_item_property
    )
    
    active_index: IntProperty(default=0)
```

**2. Agregue em `OG_scene_properties`:**
```python
class OG_scene_properties(PropertyGroup):
    # ... propriedades existentes ...
    
    minha_propriedade: PointerProperty(
        type=My_custom_property
    )
```

**3. Registre em `__init__.py`:**
```python
from .properties import My_custom_property

classes = [
    # ...
    My_custom_property,
]
```

**4. Use em operadores/painéis:**
```python
props = context.scene.og_props
valor = props.minha_propriedade.my_string
```

---

## 🔄 Fluxos Comuns

### Operação: Processar Arquivo IFC

```python
import ifcopenshell

def process_ifc_file(filepath):
    try:
        # Abrir arquivo
        ifc_file = ifcopenshell.open(filepath)
        
        # Validar
        if not ifc_file.is_valid():
            raise ValueError("IFC inválido")
        
        # Iterar elementos
        walls = ifc_file.by_type("IfcWall")
        for wall in walls:
            print(f"Parede: {wall.Name}")
            
            # Extrair propriedades
            psets = element.get_psets(wall)
            qsets = element.get_qsets(wall)
            
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False
```

### Operação: Atualizar UI

```python
def update_ui_list(context):
    """Padrão para atualizar listas na UI"""
    props = context.scene.og_props
    
    # 1. Limpar lista visível
    props.my_list_shown.clear()
    
    # 2. Repopular com itens filtrados
    for item in props.my_list:
        if should_show(item):  # Seu critério de filtro
            new_item = props.my_list_shown.add()
            copy_properties(item, new_item)
    
    # 3. Forçar redesenho (opcional)
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()
```

### Operação: Chamar Callback

```python
def my_callback(self, context):
    """Chamado quando propriedade muda"""
    print(f"Propriedade mudou para: {self.my_prop}")
    
    # Atualizar dados dependentes
    update_related_data(context)

# Na definição da PropertyGroup:
my_prop: StringProperty(
    name="Propriedade",
    update=my_callback
)
```

---

## 🧪 Testes

### Teste Manual
```python
# No console Blender
import bpy
from oil_gas_addon import operators, data

# Simular mudança de objeto
bpy.context.scene.og_props.active_class_index = 0

# Chamar refresh
data.refresh(bpy.context)

# Verificar resultado
props = bpy.context.scene.og_props
print(f"Classes visíveis: {len(props.classes_shown)}")
```

### Verificar Sem Erros
```python
# Importar todos os módulos
try:
    from oil_gas_addon import __init__, operators, panels, properties, data
    print("✓ Todos os módulos importados com sucesso")
except ImportError as e:
    print(f"✗ Erro de importação: {e}")
```

### Validar Estrutura IFC
```python
import ifcopenshell

filepath = "files/test.ifc"
ifc = ifcopenshell.open(filepath)

# Verificar estrutura
print(f"Projeto: {ifc.by_type('IfcProject')[0].Name}")
print(f"Edifício: {ifc.by_type('IfcBuilding')[0].Name if ifc.by_type('IfcBuilding') else 'Nenhum'}")
print(f"Total de elementos: {len(ifc)}")
```

---

## 🐛 Debugging

### Ativar Logging Detalhado
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def minha_funcao():
    logger.debug("Iniciando operação")
    logger.info("Passo 1 concluído")
    logger.warning("Atenção: algo inesperado")
    logger.error("Erro fatal")
```

### Inspecionar Propriedades
```python
# No console Blender
props = bpy.context.scene.og_props

# Ver todas as propriedades
print(dir(props))

# Verificar tipos
for classe in props.classes:
    print(f"{classe.name}: {type(classe.name)} = '{classe.name}'")

# Verificar indices
print([i for i, c in enumerate(props.classes) if c.name == "target"])
```

### Rastrear Callbacks
```python
def traced_callback(self, context):
    print(f"[CALLBACK] Disparado: {self}")
    print(f"[CALLBACK] Valor: {self.minha_prop}")
    # Seu código
```

---

## 📋 Checklist para Novos Operadores

- [ ] Herdou de `bpy.types.Operator`
- [ ] Definiu `bl_idname` (format: "namespace.operator_name")
- [ ] Definiu `bl_label` (texto amigável)
- [ ] Implementou `execute()`
- [ ] Retorna `{'FINISHED'}` ou `{'CANCELLED'}`
- [ ] Adicionado à lista `classes` em `__init__.py`
- [ ] Testou em Blender
- [ ] Adicionou botão em painel (se aplicável)
- [ ] Documentado com docstring
- [ ] Tratou exceções

---

## 📋 Checklist para Novos Painéis

- [ ] Herdou de `bpy.types.Panel`
- [ ] Definiu `bl_idname` (format: "VIEW3D_PT_nome")
- [ ] Definiu `bl_label` e `bl_category`
- [ ] Definiu `bl_space_type = 'VIEW_3D'`
- [ ] Definiu `bl_region_type = 'UI'`
- [ ] Implementou `draw()`
- [ ] Testou layout em diferentes tamanhos de painel
- [ ] Usado `template_list()` para listas grandes
- [ ] Quebrou textos longos com `_label_multiline()`
- [ ] Adicionado à lista `classes` em `__init__.py`

---

## 🔍 Padrões a Evitar

### ❌ Modificar lista durante iteração
```python
# ERRADO
for item in props.classes:
    props.classes.remove(0)

# CORRETO
indices_to_remove = [i for i, item in enumerate(props.classes) if condition]
for i in reversed(indices_to_remove):
    props.classes.remove(i)
```

### ❌ Loops infinitos em callbacks
```python
# ERRADO
def callback(self, context):
    self.related_prop = self.my_prop  # Dispara outro callback!

# CORRETO
def callback(self, context):
    if not getattr(self, '_updating', False):
        self._updating = True
        self.related_prop = self.my_prop
        self._updating = False
```

### ❌ Operadores sem poll()
```python
# ERRADO
def execute(self, context):
    # Código que pode falhar se dados não carregados
    value = context.scene.og_props.classes[0]

# CORRETO
@classmethod
def poll(cls, context):
    return len(context.scene.og_props.classes) > 0

def execute(self, context):
    # Agora seguro
    value = context.scene.og_props.classes[0]
```

---

## 🚀 Performance

### Otimizações
1. **Use geradores** para grandes datasets
2. **Cache dados** em variáveis globais (se estável)
3. **Evite rebuild completo** quando possível
4. **Use indices** em vez de iterar
5. **Processe em background** com jobs

### Exemplo - Generator
```python
def find_all_pipes(context):
    """Generator eficiente"""
    for classe in context.scene.og_props.classes:
        if "pipe" in classe.name.lower():
            yield classe

# Uso
for pipe in find_all_pipes(context):
    print(pipe.name)
```

### Exemplo - Cache
```python
_cache = {}

def get_data(key):
    if key not in _cache:
        _cache[key] = expensive_operation(key)
    return _cache[key]

def clear_cache():
    global _cache
    _cache = {}
```

---

## 📚 Boas Práticas

1. **Documente funções complexas**
```python
def build_hierarchy(context, data, level=1):
    """Constrói hierarquia de dados.
    
    Args:
        context: Contexto Blender
        data: Lista de dicionários com dados
        level: Nível inicial (padrão 1)
        
    Returns:
        int: Número de itens processados
    """
```

2. **Use type hints** (Python 3.10+)
```python
def my_function(context: bpy.context, count: int) -> bool:
    pass
```

3. **Trate exceções apropriadamente**
```python
try:
    result = dangerous_operation()
except FileNotFoundError:
    self.report({'ERROR'}, "Arquivo não encontrado")
    return {'CANCELLED'}
except Exception as e:
    self.report({'ERROR'}, f"Erro inesperado: {str(e)}")
    return {'CANCELLED'}
```

4. **Forneça feedback ao usuário**
```python
self.report({'INFO'}, "Operação concluída")
self.report({'WARNING'}, "Aviso: algo inesperado")
self.report({'ERROR'}, "Erro: operação falhou")
```

---

## 🔗 Integração com Git

### Workflow de Desenvolvimento
```bash
# Criar branch para feature
git checkout -b feature/minha-funcionalidade

# Fazer alterações
# Testar em Blender

# Commit
git add .
git commit -m "feat: adiciona minha funcionalidade

- Detalhe 1
- Detalhe 2"

# Push
git push origin feature/minha-funcionalidade

# Criar Pull Request
# Revisão
# Merge
```

### Mensaje de Commit
Prefixos recomendados:
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `refactor:` Refatoração
- `perf:` Melhoria de performance
- `test:` Testes

---

## 📞 Suporte e Contato

- **Issues**: Abra no repositório
- **Discussões**: Seção de Discussions
- **Contato**: Carlos Dias

