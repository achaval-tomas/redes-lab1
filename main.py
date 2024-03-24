from flask import Flask, jsonify, request
from random import choice

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]


def buscar_pelicula(id):
    for i in range(len(peliculas)):
        if peliculas[i]['id'] == id:
            return peliculas[i], i

    return None, None


def filtrar_por_genero(peliculas, genero):
    genero = genero.lower()
    return [p for p in peliculas if p['genero'].lower() == genero]


def filtrar_por_titulo(peliculas, titulo):
    titulo = titulo.lower()
    return [p for p in peliculas if titulo in p['titulo'].lower()]


def obtener_peliculas():
    filtradas = peliculas

    genero = request.args.get('genero', None)
    if genero is not None:
        filtradas = filtrar_por_genero(filtradas, genero)

    titulo = request.args.get('titulo', None)
    if titulo is not None:
        filtradas = filtrar_por_titulo(filtradas, titulo)

    return jsonify(filtradas)


def obtener_pelicula(id):
    pelicula_encontrada, _ = buscar_pelicula(id)

    if pelicula_encontrada is None:
        return '', 404

    return jsonify(pelicula_encontrada)


def obtener_pelicula_random():
    filtradas = peliculas

    genero = request.args.get('genero', None)
    if genero is not None:
        filtradas = filtrar_por_genero(filtradas, genero)

    if filtradas == []:
        return '', 404

    return jsonify(choice(filtradas))


def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    pelicula, _ = buscar_pelicula(id)

    if pelicula is None:
        return '', 404

    json = request.json

    if 'titulo' not in json or 'genero' not in json:
        return '', 400

    pelicula['titulo'] = json['titulo']
    pelicula['genero'] = json['genero']

    return jsonify(pelicula)


def eliminar_pelicula(id):
    _, index = buscar_pelicula(id)

    if index is None:
        return '', 404

    peliculas.pop(index)

    return jsonify({'mensaje': 'Película eliminada correctamente'})


def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


app.add_url_rule('/peliculas', None,
                 obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', None,
                 obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', None,
                 agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', None,
                 actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', None,
                 eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/random', None,
                 obtener_pelicula_random, methods=['GET'])

if __name__ == '__main__':
    app.run()
