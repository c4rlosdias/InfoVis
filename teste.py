import bpy

# Seleciona o objeto ativo
obj = bpy.context.active_object

# Garante que estamos acessando os dados da malha
mesh = obj.data

# Lista de coordenadas dos vértices
vertices = [v.co for v in mesh.vertices]

# Lista de faces (índices dos vértices que formam cada face)
faces = [[v for v in p.vertices] for p in mesh.polygons]

# Exibe os resultados
print("Coordenadas dos vértices:")
l_v = []

for v in vertices:
    print([v.x, v.y, v.z])
print(l_v)
print("\nFaces:")
for f in faces:
    print(f)