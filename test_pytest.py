import requests
import pytest

url = 'http://127.0.0.1:5000'

initial_peliculas = [
    {'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'titulo': 'Star Wars', 'genero': 'Acción'},
    {'titulo': 'Goodwill Hunting', 'genero': 'Drama'},
]


@pytest.fixture(scope="function", autouse=True)
def before_each():
    res = requests.get(f'{url}/reset')
    assert res.status_code == 204
    for p in initial_peliculas:
        res = requests.post(f'{url}/peliculas', json=p)
        assert res.status_code == 201
        assert res.json()['titulo'] == p['titulo']
        assert res.json()['genero'] == p['genero']


def test_obtener_peliculas():
    res = requests.get(f'{url}/peliculas')
    assert res.status_code == 200
    assert len(res.json()) == len(initial_peliculas)
    for ip, p in zip(initial_peliculas, res.json()):
        assert ip.items() <= p.items()


def test_agregar_pelicula():
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    res = requests.post(f'{url}/peliculas', json=nueva_pelicula)
    assert res.status_code == 201
    for (k, v) in nueva_pelicula.items():
        assert v == res.json()[k]


def test_obtener_detalle_pelicula():
    res = requests.get(f'{url}/peliculas/1')
    assert res.status_code == 200
    assert res.json()['titulo'] == 'Indiana Jones'


def test_actualizar_detalle_pelicula():
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    res = requests.put(f'{url}/peliculas/1', json=datos_actualizados)
    assert res.status_code == 200
    assert res.json()['titulo'] == 'Nuevo título'


def test_eliminar_pelicula():
    res = requests.delete(f'{url}/peliculas/1')
    assert res.status_code == 200


def test_obtener_peliculas_por_genero():
    genero = "AcCióN"
    res = requests.get(f'{url}/peliculas?genero={genero}')
    assert res.status_code == 200
    assert len(res.json()) == len([p for p in initial_peliculas
                                   if p['genero'] == 'Acción'])
    for ip, p in zip(initial_peliculas, res.json()):
        assert ip.items() <= p.items()


def test_buscar_pelicula_por_titulo():
    titulo = "tHe"
    res = requests.get(f'{url}/peliculas?titulo={titulo}')
    assert res.status_code == 200


def test_obtener_pelicula_aleatoria():
    res = requests.get(f'{url}/peliculas/random')
    assert res.status_code == 200


def test_obtener_pelicula_aleatoria_con_genero():
    genero = "DrAmA"
    res = requests.get(f'{url}/peliculas/random?genero={genero}')
    assert res.status_code == 200
    pelicula = res.json()
    assert pelicula['genero'].lower() == genero.lower()


def test_obtener_pelicula_feriado_por_genero():
    genero = initial_peliculas[1]['genero']
    res = requests.get(f'{url}/peliculas/feriado?genero={genero}')
    assert res.status_code == 200
    body = res.json()
    assert 'holiday' in body
    assert 'dia' in body['holiday']
    assert 'mes' in body['holiday']
    assert 'motivo' in body['holiday']
    assert body['pelicula']['genero'] == genero


def test_obtener_pelicula_inexistente():
    bad_id = 80000
    response = requests.get(f'{url}/peliculas/{bad_id}')
    assert response.status_code == 404


def test_obtener_pelicula_random_con_genero_que_no_existe():
    bad_genero = "tragicomedia"
    response = requests.get(f'{url}/peliculas/random?genero={bad_genero}')
    assert response.status_code == 404


def test_consultar_feriado_sin_genero():
    res = requests.get(f'{url}/peliculas/feriado')
    assert res.status_code == 400


def test_eliminar_pelicula_inexistente():
    bad_id = 69420
    res = requests.delete(f'{url}/peliculas/{bad_id}')
    assert res.status_code == 404


def actualizar_pelicula_inexistente():
    bad_id = 9999
    actualizacion = {
        'titulo': 'holahola',
        'genero': 'Comedia'
    }
    res = requests.put(f'{url}/peliculas/{bad_id}', json=actualizacion)
    assert res.status_code == 404
    res = requests.get(f'{url}/peliculas')
    assert res.status_code == 200
    assert initial_peliculas.items() <= res.json().items()
