import bpy
import ifcopenshell
import ifcopenshell.util.element
import bonsai.tool as tool

from .ifc_utils import refresh_props

last_active = None


def refresh_layers(context):
    obj = context.view_layer.objects.active
    if obj is None:
        return
    model = tool.Ifc.get()
    if model is None:
        return
    entity = tool.Ifc.get_entity(obj)
    if entity is None:
        return
    ifc_type = ifcopenshell.util.element.get_type(entity)
    if ifc_type is None:
        return
    nested_elements = ifcopenshell.util.element.get_components(ifc_type) or []
    props = context.scene.og_props
    props.layers.clear()
    for element in nested_elements:
        new_layer = props.layers.add()
        new_layer.id = element.id()
        new_layer.name = element.Name or f"Element {element.id()}"
        new_layer.description = element.get_info() or ''


# Call back para carregar as propriedades ao mudar o objeto ativo
def call_back():
    try:
        bpy.ops.props.load_properties()
    except Exception as e:
        print(f"[call_back] error: {e}")
    try:
        refresh_tree_containers(bpy.context)
    except Exception as e:
        print(f"[call_back] refresh_tree error: {e}")
    try:
        refresh_layers(bpy.context)
    except Exception as e:
        print(f"[call_back] refresh_layers error: {e}")

# Handler para carregar as propriedades ao mudar o objeto ativo
def on_active_object_change(scene):
    global last_active
    obj = bpy.context.view_layer.objects.active
    if obj != last_active:
        last_active = obj        
        bpy.ops.props.load_properties()


def load_contained_elements_by_decomposition(container: ifcopenshell.entity_instance, name_props: str, context : bpy.types.Context ) -> None:
            props = context.scene.og_props        
            def get_decomposition(element: ifcopenshell.entity_instance, is_recursive : bool) -> set[ifcopenshell.entity_instance]:

                queue = [element]            
                results = []

                while queue:
                    element = queue.pop()
                    for rel in getattr(element, "IsGroupedBy", []):
                        related = rel.RelatedObjects
                        queue.extend(related)
                        results.extend(related) 
                    for rel in getattr(element, "ContainsElements", []):
                        related = rel.RelatedElements
                        queue.extend(related)
                        results.extend(related)      
                    for rel in getattr(element, "IsDecomposedBy", []):
                        related = rel.RelatedObjects
                        queue.extend(related)
                        results.extend(related)
                    for rel in getattr(element, "IsNestedBy", []):
                        related = rel.RelatedObjects
                        if related[0].is_a("IfcDistributionPort"):
                            continue
                        queue.extend(related)
                        results.extend(related)
                    if not is_recursive:
                        break
                return results

            def add_elements(elements, name_props, level=1):                
                for element in elements:                                            
                    new = getattr(props, name_props).add()
                    
                    new.name = element.Name or 'Unnamed'
                    new.type = element.is_a()
                    new.level = level 
                    new.id = element.id()                
                     
                    if hasattr(element, "ObjectType") and element.ObjectType:
                        new.object_type = element.ObjectType
                    elif hasattr(element, "ElementType") and element.ElementType:
                        new.object_type = element.ElementType
                    else:
                        new.object_type = 'Unnamed'      

                    children = [
                        e
                        for e in get_decomposition(element, is_recursive=False)
                        if not e.is_a("IfcFeatureElement")
                    ]
                    if children:
                        new.has_children = True                    
                        new.is_expanded = False
                        add_elements(children, name_props, level=level + 1)
            
            getattr(props, name_props).clear()
            elements = get_decomposition(container, is_recursive=False)
            add_elements(elements, name_props)


def draw_tree(layout, item, operators, attributes, property, only_children = False):

    ''' Desenha uma árvore de classes, produtos ou tipos no layout do blender.
            layout: layout do blender
            item: item da coleção a ser desenhado
            operators: operadores a serem adicionados para cada item
            attributes: atributos a serem mostrados para cada item
            property: nome da propriedade onde a coleção está armazenada
            only_children: se True, mostra apenas os operadores para os itens que tem filhos, caso contrário, mostra para todos os itens
        retorna o layout com a árvore desenhada
    '''
    if not item.is_hidden:
        
        row = layout.row(align=True)
        # adiciona os ícones de hierarquia
        for _ in range(0, item.level - 1):
            row.label(text="", icon="BLANK1")

        # adiciona o ícone de expandir/contrair    
        if item.has_children:
            if item.is_expanded:
                op = row.operator("element.contract_tree", text="", emboss=False, icon="DISCLOSURE_TRI_DOWN")
                op.index = item.index
                op.property = property
            else:
                op=row.operator("element.expand_tree", text="", emboss=False, icon="DISCLOSURE_TRI_RIGHT")
                op.index = item.index
                op.property = property
        else:
            row.label(text="", icon="BLANK1")
  
        # adiciona os atributos do item
        for att in attributes:            
            row.label(text=att[0], icon=att[1])  
        
        # se não for para mostrar apenas os filhos ou se o item não tiver filhos, mostra os operadores
        if not only_children or not item.has_children:
            for opt in operators:
                op = row.operator(opt['name'], text=opt['text'] if 'text' in opt else "", icon=opt['icon'])
                for att, value in opt['att']:
                    setattr(op, att, value)


def refresh_classes(context):
    props = context.scene.og_props
    props.classes_shown.clear()
    for classe in props.classes:
        if not classe.is_hidden:
            new_item = props.classes_shown.add()
            new_item.code = classe.code
            new_item.name = classe.name
            new_item.description = classe.description
            new_item.level = classe.level
            new_item.uri = classe.uri
            new_item.index = classe.index
            new_item.has_children = classe.has_children
            new_item.is_expanded = classe.is_expanded
            new_item.is_hidden = classe.is_hidden
            new_item.type = classe.type


def refresh_products(context):
    props = context.scene.og_props
    props.products_show.clear()
    for classe in props.products:
        if not classe.is_hidden:
            new_item = props.products_show.add()
            new_item.code = classe.code
            new_item.name = classe.name
            new_item.description = classe.description
            new_item.level = classe.level
            new_item.uri = classe.uri
            new_item.index = classe.index
            new_item.has_children = classe.has_children
            new_item.is_expanded = classe.is_expanded
            new_item.is_hidden = classe.is_hidden
            new_item.type = classe.type


def refresh_types(context):
    props = context.scene.og_props
    props.types_show.clear()
    for classe in props.types:
        if not classe.is_hidden:
            new_item = props.types_show.add()
            new_item.id = classe.id
            new_item.tag = classe.tag
            new_item.name = classe.name
            new_item.description = classe.description
            new_item.level = classe.level
            new_item.element_type = classe.element_type
            new_item.qtde = classe.qtde
            new_item.unit = classe.unit
            new_item.index = classe.index
            new_item.has_children = classe.has_children
            new_item.is_expanded = classe.is_expanded
            new_item.is_hidden = classe.is_hidden


def refresh_container(context):
    props = context.scene.og_props
    props.containers_show.clear()
    for classe in props.elements_containers:
        if not classe.is_hidden:
            new_item = props.containers_show.add()            
            new_item.name = classe.name            
            new_item.level = classe.level 
            new_item.id = classe.id           
            new_item.index = classe.index
            new_item.has_children = classe.has_children
            new_item.is_expanded = classe.is_expanded
            new_item.is_hidden = classe.is_hidden 
            new_item.type = classe.type  
            new_item.object_type = classe.object_type  
            new_item.is_selected = classe.is_selected  


def refresh_tree(context, property):
    if property == 'classes':
        refresh_classes(context)
    elif property == 'products':
        refresh_products(context)
    elif property == 'types':
        refresh_types(context)
    elif property == 'elements_containers':
        refresh_container(context)


def move_to_assembly(parent, children, type):
    model = tool.Ifc.get()
    if type == 'Nests':
        if getattr(children, 'Nests', None):
            ifcopenshell.api.nest.change_nest(
                model,
                item=children,
                new_parent=parent
            )
        else:
            if getattr(children, 'ContainedInStructure', None):
                ifcopenshell.api.spatial.unassign_container(model, products=[children])
            ifcopenshell.api.nest.assign_object(
                model,
                related_objects=[children],
                relating_object=parent
            )

    else:
        if getattr(children, 'Decomposes', None):
            ifcopenshell.api.aggregate.unassign_object(
                model,
                products=[children]
            )
        
        ifcopenshell.api.spatial.unassign_container(model, products=[children])
        ifcopenshell.api.aggregate.assign_object(
            model,
            products=[children],
            relating_object=parent
        )

_syncing_tree = False

def refresh_tree_containers(context):
    global _syncing_tree
    obj = context.active_object
    if obj is None:
        return
    ifc_id = obj.BIMObjectProperties.ifc_definition_id
    props = context.scene.og_props
    _syncing_tree = True
    try:
        for i, item in enumerate(props.containers_show):
            if item.id == ifc_id:
                props.active_element_index = i
                break
    finally:
        _syncing_tree = False
