import ifcopenshell
import re

# model = ifcopenshell.open('Exemplo_Crushing.ifc')

# properties = model.by_type('IfcProperty')
# for property in properties:
#     name = property.Name
#     description = ''
#     if name:
#         descriptions = re.findall(r'[A-Z][a-z]*', name)
#         description = ' '.join(descriptions)
#         print(description)
#         property.Description = description

# model.write('Exemplo_Crushing_2.ifc')


model = ifcopenshell.open('Exemplo_Crushing_2.ifc')

properties = model.by_type('IfcProperty')
for property in properties:
    description = property.Description
    if description:
        descriptions = description.split('Table')
        if len(descriptions) > 1:
            print(descriptions[1])
            property.Description = descriptions[1]

model.write('Exemplo_Crushing_3.ifc')