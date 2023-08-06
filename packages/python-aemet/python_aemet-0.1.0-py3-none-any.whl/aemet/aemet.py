from aemet.constants import (
    API_KEY, BASE_URL, DAILY_PREDICTION_API_URL,
    PERIOD_WEEKLY, PERIOD_DAILY, WEEKLY_PREDICTION_API_URL,
    TOWN_API_URL
)
import requests
import csv
import json

class Prediccion:
    def __init__(self, provincia, version, id, origen,
            elaborado, prediccion, nombre):
        self.provincia = provincia
        self.version = version
        self.id = id
        self.origen = origen
        self.elaborado = elaborado
        self.prediccion = prediccion
        self.nombre = nombre

    @staticmethod
    def load(data, period):
        if period == PERIOD_DAILY:
            prediccion = PrediccionDiaria.load(data['prediccion'])
        elif period == PERIOD_WEEKLY:
            prediccion = PrediccionSemanal.load(data['prediccion'])

        return Prediccion(
            provincia=data['provincia'],
            version=data['version'],
            id=data['id'],
            origen=data['origen'],
            elaborado=data['elaborado'],
            prediccion=prediccion,
            nombre=data['nombre']
        )

class PrediccionSemanal:
    def __init__(self, uvMax=0, rachaMax=[], fecha='', sensTermica=[], humedadRelativa=[],
            temperatura=[], estadoCielo=[], cotaNieveProv=[], viento=[], probPrecipitacion=[]):
        self.uvMax = uvMax
        self.rachaMax = rachaMax
        self.fecha = fecha
        self.sensTermica = sensTermica
        self.humedadRelativa = humedadRelativa
        self.temperatura = temperatura
        self.estadoCielo = estadoCielo
        self.cotaNieveProv = cotaNieveProv
        self.viento = viento
        self.probPrecipitacion = probPrecipitacion

    @staticmethod
    def load(data):
        predicciones = []
        for dia in data['dia']:
            try:
                uvMax = dia['uvMax']
            except KeyError:
                uvMax = []
            predicciones.append(
                PrediccionSemanal(
                    uvMax=uvMax,
                    rachaMax=dia['rachaMax'],
                    fecha=dia['fecha'],
                    sensTermica=dia['sensTermica'],
                    humedadRelativa=dia['humedadRelativa'],
                    temperatura=dia['temperatura'],
                    cotaNieveProv=dia['cotaNieveProv'],
                    viento=dia['viento'],
                    probPrecipitacion=dia['probPrecipitacion'],
                )
            )
        return predicciones

class PrediccionDiaria:
    def __init__(self, estadoCielo=[], precipitacion=[], vientoAndRachaMax=[], ocaso='',
            probTormenta=[], probPrecipitacion=[], orto='', humedadRelativa=[], nieve=[],
            probNieve=[], fecha='', temperatura=[], sensTermica=[]):
        self.estadoCielo = estadoCielo
        self.precipitacion = precipitacion
        self.vientoAndRachaMax = vientoAndRachaMax
        self.ocaso = ocaso
        self.probTormenta = probTormenta
        self.probPrecipitacion = probPrecipitacion
        self.orto = orto
        self.humedadRelativa = humedadRelativa
        self.nieve = nieve
        self.probNieve = probNieve
        self.fecha = fecha
        self.temperatura = temperatura
        self.sensTermica = sensTermica

    @staticmethod
    def load(data):
        periodos = []
        for p in data['dia']:
            try:
                periodos.append(
                    PrediccionDiaria(
                        estadoCielo=p['estadoCielo'],
                        precipitacion=p['precipitacion'],
                        vientoAndRachaMax=p['vientoAndRachaMax'],
                        ocaso=p['ocaso'],
                        probTormenta=p['probTormenta'],
                        probPrecipitacion=p['probPrecipitacion'],
                        orto=p['orto'],
                        humedadRelativa=p['humedadRelativa'],
                        nieve=p['nieve'],
                        probNieve=p['probNieve'],
                        fecha=p['fecha'],
                        temperatura=p['temperatura'],
                        sensTermica=p['sensTermica']
                    )
                )
            except KeyError:
                pass
        return periodos

class Municipio:
    with open('data/municipios.json') as f:
        MUNICIPIOS = json.loads(f.read())

    def __init__(self, cod_auto, cpro, cmun, dc, nombre):
        self.cod_auto = cod_auto
        self.cpro = cpro
        self.cmun = cmun
        self.dc = dc
        self.nombre = nombre

    @staticmethod
    def load(data):
        return Municipio(
            cod_auto=data['CODAUTO'],
            cpro=data['CPRO'],
            cmun=data['CMUN'],
            dc=data['DC'],
            nombre=data['NOMBRE']
        )

    @staticmethod
    def get_municipio(id):
        print(id)
        return Municipio()

    @staticmethod
    def buscar(name):
        municipio = list(filter(lambda t: name in t['NOMBRE'], Municipio.MUNICIPIOS))[0]
        municipio = Municipio.load(municipio)
        return municipio

    def get_codigo(self):
        return '{}{}'.format(self.cpro, self.cmun)

class AemetClient:
    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.querystring = {
            'api_key': self.api_key
        }
        self.headers = {
            'cache-control': 'no-cache'
        }

    def _get_request_data(self, url):
        r = requests.get(
            url,
            headers=self.headers,
            params=self.querystring,
            verify=False    # Avoid SSL Verification .__.
        )
        if r.status_code == 200:
            r = requests.get(r.json()['datos'], verify=False)
            data = r.json()[0]
            return data
        return {
            'error': r.status_code
        }

    def get_prediccion(self, codigo_municipio, period=PERIOD_WEEKLY):
        if period == PERIOD_WEEKLY:
            url = '{}{}{}'.format(
                BASE_URL,
                WEEKLY_PREDICTION_API_URL,
                codigo_municipio
            )
        else:
            url = '{}{}{}'.format(
                BASE_URL,
                DAILY_PREDICTION_API_URL,
                codigo_municipio
            )
        data = self._get_request_data(url)
        return Prediccion.load(data, period)

    def get_municipio(self, name):
        url = '{}{}'.format(BASE_URL, TOWN_API_URL)
        r = requests.get(
            url,
            params = {
                "nombre": name,
                'api_key': self.api_key
            },
            headers=self.headers,
            verify=False
        )
        data = r.json()
        return data

if __name__ == '__main__':
    municipio = Municipio.buscar('Fuenmayor')
    client = AemetClient()
    prediccion = client.get_prediccion(municipio.get_codigo(), period=PERIOD_DAILY)
    print(prediccion.prediccion[2].ocaso)
