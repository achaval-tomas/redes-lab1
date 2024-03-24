import requests

url = 'http://localhost:5000'

def print_pelicula(pelicula):
     print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")


# Obtener todas las películas
response = requests.get(f'{url}/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print_pelicula(pelicula)
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post(f'{url}/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print_pelicula(pelicula)
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'{url}/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print_pelicula(pelicula)
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'{url}/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print_pelicula(pelicula_actualizada)
else:
    print("Error al actualizar la película.")
print()

# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'{url}/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.")
else:
    print("Error al eliminar la película.")
print()


# Obtener películas de un género específico
genero = "AcCióN"
response = requests.get(f'{url}/peliculas?genero={genero}')
if response.status_code == 200:
    peliculas = response.json()
    print(f"Películas del género '{genero}':")
    for pelicula in peliculas:
        print_pelicula(pelicula)
else:
    print(f"Error al obtener películas del género '{genero}'.")
print()

# Buscar película por título
titulo = "tHe"
response = requests.get(f'{url}/peliculas?titulo={titulo}')
if response.status_code == 200:
    peliculas = response.json()
    print(f"Películas que contienen al string '{titulo}':")
    for pelicula in peliculas:
        print_pelicula(pelicula)
else:
    print(f"Error al obtener películas que contienen '{titulo}'.")
print()

# Obtener película aleatoria
response = requests.get(f'{url}/peliculas/random')
if response.status_code == 200:
    pelicula = response.json()
    print(f"Película random:")
    print_pelicula(pelicula)
else:
    print(f"Error al obtener película random.")
print()


# Obtener película aleatoria de un género en específico
genero = "drama"
response = requests.get(f'{url}/peliculas/random?genero={genero}')
if response.status_code == 200:
    pelicula = response.json()
    print(f"Película random del género '{genero}':")
    print_pelicula(pelicula)
else:
    print(f"Error al obtener película random del género '{genero}'.")
print()


# Obtener película aleatoria por género y con información del próximo feriado
genero = "acción"
response = requests.get(f'{url}/peliculas/feriado?genero={genero}')
if response.status_code == 200:
    pelicula = response.json()['pelicula']
    print(f"Película random del género '{genero}':")
    print_pelicula(pelicula)

    feriado = response.json()['holiday']
    print("Próximo feriado:")
    print(f"Fecha: {feriado['dia']}/{feriado['mes']}, Motivo: {feriado['motivo']}")
else:
    print(f"Error al obtener película random del género '{genero}' con feriado.")
print()

# Obtener error al buscar película con ID que no existe
bad_id = 8000
response = requests.get(f'{url}/peliculas/{bad_id}')
if response.status_code == 404:
    print(f"No se encontró película con id {bad_id}. Test exitoso.")
else:
    print("El código de respuesta fue incorrecto. Test fallido.")
print()

# Obtener error al buscar película random con género que no existe
bad_genero = "tragicomedia"
response = requests.get(f'{url}/peliculas/random?genero={bad_genero}')
if response.status_code == 404:
    print(f"No existen películas de {bad_genero}. Test exitoso.")
else:
    print("El código de respuesta fue incorrecto. Test fallido.")
print()

# Obtener error al consultar /peliculas/feriado sin especificar un género
response = requests.get(f'{url}/peliculas/feriado')
if response.status_code == 400:
    print("Request malformado. Test exitoso.")
else:
    print("El código de respuesta fue incorrecto. Test fallido.")
print()

# Eliminar una película inexistente devuelve 404
bad_id = 1
response = requests.delete(f'{url}/peliculas/{bad_id}')
if response.status_code == 404:
    print(f"Pelicula con id={bad_id} not found. Test exitoso.")
else:
    print("El código de respuesta fue incorrecto. Test fallido.")
print()

# Actualizar una pelicula inexistente devuelve 404
bad_id = 1
datos_actualizados = {
    'titulo': 'holahola',
    'genero': 'Comedia'
}
response = requests.put(f'{url}/peliculas/{bad_id}', json=datos_actualizados)
if response.status_code == 404:
    print(f"Pelicula con id={bad_id} not found. Test exitoso.")
else:
    print("El código de respuesta fue incorrecto. Test fallido.")
print()
