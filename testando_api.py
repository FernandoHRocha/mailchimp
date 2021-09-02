from mailchimp_marketing import Client
import configuration as cfg

mailchimp = Client()
mailchimp.set_config({
   "api_key": cfg.credentials['chave_api'],
   "server": cfg.credentials['servidor']
})

#response = mailchimp.lists.add_list_member(cfg.credentials['lista'], {"email_address": "fhrlobacz@hotmail.com", "status": "subscribed"})

# response = mailchimp.lists.tag_search(cfg.credentials['lista'])
# print('tags')
# for res in response['tags']:
#   print(res['name'])

# response = mailchimp.lists.get_list_members_info(cfg.credentials['lista'])
# print('membros')
# for res in response['members']:
#   print(res['email_address'])
