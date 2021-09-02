import configuration as cfg
import requests
import json

chave_api = cfg.credentials['chave_api']
servidor = cfg.credentials['servidor']
lista = cfg.credentials['lista']
root = 'https://'+servidor+'.api.mailchimp.com/3.0/'

parametros_membros = {
        'Authorization': 'apiKey '+chave_api,
}

resposta = requests.get(root+'lists/'+lista+'/members?count=1&offset=10&status=subscribed',headers=parametros_membros).json()
membros = resposta['members']
lista_membros = [[membro['email_address'],membro['merge_fields']['FNAME'],membro['merge_fields']['LNAME'], [tag if (len(tag) > 0) else None for tag in membro['tags']]] for membro in membros]
#print([tag if (len(tag) > 0) else None for tag in [membro['tags'] for membro in membros]])
#print([membro['merge_fields']['FNAME'] for membro in membros])
print(lista_membros)

#response = mailchimp.lists.add_list_member(cfg.credentials['lista'], {"email_address": "", "status": "subscribed"})