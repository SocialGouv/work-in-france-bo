"""
The data structure returned by the demarches-simplifiees.fr API endpoint
that list of all the dossiers of a procedure.

GET /api/v1/procedures/:procedure_id/dossiers
https://www.demarches-simplifiees.fr/docs/1.0/dossiers/index.fr.html
"""

RAW_DOSSIERS = {
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
