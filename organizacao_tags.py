from mailchimp_marketing import Client
import openpyxl
import configuration as cfg
import requests
from openpyxl import Workbook, workbook
from datetime import date
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
                        tags.append(tag['name'])
        else:
                tags.append('')
        retorno = ''
        for elemento in tags:
                retorno += ' '+elemento.lower()
        return traduzir_tags(retorno)

def substituir_padrao(busca,tags,retorno):
        if(tags.find(busca.lower())>0):
                retorno += busca.upper() + ", "
        return retorno

def traduzir_tags(tags):
        padrao = ['aluno', 'interesse','empresa','autocad','revit','sketchup','excel','design gráfico',
                'edição de vídeo','office','produto','promob','solidworks','design jogos']
        retorno = ''
        for palavra in padrao:
                retorno = substituir_padrao(palavra,tags,retorno)
        if(len(retorno)>2):
                retorno = retorno[:-2]
        return retorno

class Converter_lista:
        def __init__(self):
                resposta = requests.get(root+'lists/'+lista+'/members?count=1000&offset=0',headers=parametros_membros).json()
                membros = resposta['members']

                membros_basico = [
                        [
                        membro['email_address'].lower() if membro['email_address'] != '' else '',
                        membro['merge_fields']['FNAME'].lower().capitalize() if membro['merge_fields']['FNAME'] != '' else '',
                        membro['merge_fields']['LNAME'].lower().capitalize() if membro['merge_fields']['LNAME'] != '' else '',
                        membro['status'],
                        tags_para_lista(membro)
                        ] for membro in membros]
                self.salvar_contatos(membros_basico)
        
        def salvar_contatos(self,audiencia):
                wb = Workbook()
                ws = wb.create_sheet('contatos',0)
                for contato in audiencia:
                        ws.append(contato)
                wb.save('./ContatosMailChimp.xlsx')

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

        def adicionar(self, audiencia):
                self.mailchimp.lists.add_list_member(
                        lista,{
                                'email_address':audiencia[0],
                                'status':'subscribed',
                                'merge-fieds':{
                                        'FNAME': audiencia[1],
                                        'LNAME': audiencia[2]
                                },
                                'tags':{audiencia[4]}
                        }
                )

class Obter_dados_planilha:
        def __init__(self):
                ws = openpyxl.load_workbook('./ContatosMailChimp.xlsx',data_only=True)['contatos']
                contatos = []
                for row in range(1,ws.max_row+1):
                        contato=[]
                        contato.append(str(ws.cell(row,1).value))
                        contato.append(str(ws.cell(row,2).value))
                        contato.append(str(ws.cell(row,3).value))
                        contato.append(str(ws.cell(row,4).value))
                        tags = str(ws.cell(row,5).value).split(', ')
                        if(tags == ['None']):
                                contato.append([])
                        else:
                                contato.append(tags)
                        contatos.append(contato)
                        #Adicionar_audiencia.adicionar(Adicionar_audiencia,contato)

class Editar_tags:
        def __init__(self):
                self.mailchimp = Client()
                self.mailchimp.set_config({
                "api_key": cfg.credenciais['chave_api'],
                "server": cfg.credenciais['servidor']
                })
        
        def obter_hash(self):
                resposta = requests.get(root+'lists/'+lista+'/members?count=1000&offset=0',headers=parametros_membros).json()
                membros = resposta['members']
                return

Obter_dados_planilha()
#Converter_lista()