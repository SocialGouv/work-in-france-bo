"""
The data structure returned by the demarches-simplifiees.fr API endpoint:
https://www.demarches-simplifiees.fr/api/v1/procedures/3272/dossiers
"""

RAW_DOSSIERS_JSON = {
  'dossiers': [{
    'id': 44950,
    'updated_at': '2018-03-27T09:15:10.780Z',
    'initiated_at': '2018-03-27T08:54:07.829Z',
  }],
  'pagination': {
    'page': 1,
    'resultats_par_page': 1000,
    'nombre_de_page': 1,
  }
}
