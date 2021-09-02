from mailchimp_marketing import Client
import configuration as cfg
import requests
import json

chave_api = cfg.credenciais['chave_api']
servidor = cfg.credenciais['servidor']
lista = cfg.credenciais['lista']
root = 'https://'+servidor+'.api.mailchimp.com/3.0/'

parametros_membros = {
        'Authorization': 'apiKey '+chave_api,
}

def tags_para_lista(membro):
        tags = []
        if(membro['tags']):
                aux=[]
                for tag in membro['tags']:
                        aux.append(tag['name'])
                tags.append(aux)
        else:
                tags.append([])
        return tags

class Converter_lista:

        resposta = requests.get(root+'lists/'+lista+'/members?count=500&offset=0',headers=parametros_membros).json()
        membros = resposta['members']

        membros_basico = [
                [
                membro['email_address'].lower() if membro['email_address'] != '' else '',
                membro['merge_fields']['FNAME'].lower().capitalize() if membro['merge_fields']['FNAME'] != '' else '',
                membro['merge_fields']['LNAME'].lower().capitalize() if membro['merge_fields']['LNAME'] != '' else '',
                membro['status'],
                tags_para_lista(membro)[0]
                ] for membro in membros]

        for membro in membros_basico:
                dados = {
                        'email_address':membro[0],
                        'status': membro[3],
                        'merge-fieds':{
                                'FNAME':membro[1],
                                'LNAME':membro[2]
                        }
                }
                tags = membro[4]
                print(dados)

class Obter_tags:
        def __init__(self):
                resposta = requests.get(root+'lists/'+lista+'/tag-search?count=100',headers=parametros_membros).json()
                [print(respos['name']) for respos in resposta['tags']]

class Adicionar_audiencia:
        def __init__(self):
                self.mailchimp = Client()
                self.mailchimp.set_config({
                "api_key": cfg.credenciais['chave_api'],
                "server": cfg.credenciais['servidor']
                })

        def adicionar(self, audiencia, tags):
                self.mailchimp.lists.add_list_member(
                        lista,{
                                'email_address':audiencia[0],
                                'status':'subscribed',
                                'merge-fieds':{
                                        'FNAME': audiencia[1],
                                        'LNAME': audiencia[2]
                                },
                                'tags':{tags}
                        }
                )

#Converter_lista()
#Obter_tags()

# aluno
# interesse
# empresa
# ----------
# autocad
# revit
# sketchup
# excel
# design gráfico
# edição de video
# office
# produto
# promob
# solidworks
# design jogos