import requests
from collections import defaultdict


def create_civic_gene_dataframe():
    payload = {'count': 999}  # Only 295 genes at time of writing
    request = requests.get('https://civic.genome.wustl.edu/api/genes/', params=payload)
    assert request.status_code == 200, 'Request failed: {}'.format(request.status_code)

    records = request.json()['records']
    genes = defaultdict(dict)
    for record in records:
        gene = record['name']
        genes[gene]['gene'] = gene
        genes[gene]['aliases'] = ', '.join(record['aliases'])
        genes[gene]['description'] = record['description']

