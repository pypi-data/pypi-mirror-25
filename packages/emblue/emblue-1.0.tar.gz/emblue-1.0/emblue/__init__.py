#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
import copy


headers = {'content-type': 'application/json'}
base_url='http://api.embluemail.com/Services/EmBlue3Service.svc/Json/'

def log_in(Token):
	url = str(base_url)+'Authenticate'
	request = {'User': 'erickhv@gmail.com', 'Pass': 'Ehv_8606761'}
	request['Token']=Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def rev_conexion(Temp_Token):
	url = str(base_url)+'CheckConnection'
	request = {}
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def nuevo_grupo(Temp_Token,Name):
	url = str(base_url)+'NewGroup'
	request = {}
	request['Token']=Temp_Token
	request['Name']=Name
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	if res_json['GroupId']==0:return False
	else:return res_json['GroupId']

def renombrar_grupo(Temp_Token,GroupId,Name):
	url = str(base_url)+'RenameGroup'
	request = {}
	request['GroupId']=GroupId
	request['Token']=Temp_Token
	request['Name']=Name
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json['Result']

def eliminar_grupo(Temp_Token,GroupId):
	url = str(base_url)+'DeleteGroup'
	request = {}
	request['GroupId']=GroupId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json['Result']

def obtener_grupo(Temp_Token,GroupId):
	url = str(base_url)+'GetNameGroupById'
	request = {}
	request['GroupId']=GroupId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def buscar_grupo(Temp_Token,Name='',FirstResult=0):
	url = str(base_url)+'SearchGroup'
	request = {'Order':'asc'}
	request['Token']=Temp_Token
	request['Search']=Name
	request['FirstResult']=FirstResult
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def listar_campos(Temp_Token):
	url = str(base_url)+'ListCustomFields'
	request = {}
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def obtener_info_campo(Temp_Token,CustomFieldId):
	url = str(base_url)+'GetInfoCustomField'
	request = {}
	request['Token']=Temp_Token
	request['CustomFieldId']=CustomFieldId
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	map_tipo_dato={1:'Fecha',2:'Numerico',3:'Alfanumerico',4:'Email',5:'Sexo',6:'Pais'}
	map_tipo_opcion={1:'Ninguno',2:'Radio',3:'Combo'}
	return res_json,map_tipo_opcion,map_tipo_dato

def buscar_contacto(Temp_Token,Name='',FirstResult=0):
	url = str(base_url)+'SearchContact'
	request = {'Order':'asc','GroupId':'0'}
	request['Token']=Temp_Token
	request['Search']=Name
	request['FirstResult']=FirstResult
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def revisar_contacto(Temp_Token,EmailId):
	url = str(base_url)+'CheckContact'
	request = {}
	request['EmailId']=EmailId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def editar_campo(Temp_Token,EmailId,EditedFields):
	url = str(base_url)+'EditCustomFieldsOneContact'
	request = {}
	request['EmailId']=EmailId
	request['EditedFields']=EditedFields
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def vincular_contacto_grupo(Temp_Token,EmailId,SelectGroups,DeselectGroups):
	url = str(base_url)+'RelatedContactGroups'
	request = {}
	request['EmailId']=EmailId
	request['SelectGroups']=SelectGroups
	request['DeselectGroups']=DeselectGroups
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def nuevo_contacto(Temp_Token,Email,SelectGroups,EditCustomFields):
	url = str(base_url)+'NewContact'
	request = {}
	request['Email']=Email
	request['SelectGroups']=SelectGroups
	request['EditCustomFields']=EditCustomFields
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def nuevo_contacto_express(Temp_Token,Email,SelectGroups,EditCustomFields):
	url = str(base_url)+'NewContactExpress'
	request = {}
	request['Email']=Email
	request['SelectGroups']=SelectGroups
	request['EditCustomFields']=EditCustomFields
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def agregar_contactos(Temp_Token,Emails,SelectGroups):
	url = str(base_url)+'NewContactAll'
	request = {}
	request['Emails']=Emails
	request['SelectGroups']=SelectGroups
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def obtener_grupos_de_contacto(Temp_Token,EmailId):
	url = str(base_url)+'GetGroupsForEmailId'
	request = {}
	request['EmailId']=EmailId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def obtener_contactos_de_grupo(Temp_Token,GroupId,FirstResult=0):
	url = str(base_url)+'GetEmailsByGroup'
	request = {}
	request['GroupId']=GroupId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def obtener_campos_de_contacto(Temp_Token,EmailId):
	url = str(base_url)+'GetCustomFieldsByEmail'
	request = {}
	request['EmailId']=EmailId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def obtener_remitentes(Temp_Token,OnlyDefault=False):
	url = str(base_url)+'GetSenders'
	request = {}
	request['OnlyDefault']=OnlyDefault
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def obtener_nombre_remitentes(Temp_Token,Name='',FirstResult=0):
	url = str(base_url)+'GetSenderName'
	request = {'Order':'asc'}
	request['Search']=Name
	request['FirstResult']=FirstResult
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def obtener_mail_remitentes(Temp_Token,Name=''):
	url = str(base_url)+'GetSenderEmail'
	request = {'Order':'asc'}
	request['Search']=Name
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def revisar_mail_remitente(Temp_Token,IdSenderEmail):
	url = str(base_url)+'CheckSenderEmail'
	request = {}
	request['IdSenderEmail']=IdSenderEmail
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def revisar_nombre_remitente(Temp_Token,IdSenderName):
	url = str(base_url)+'CheckSenderName'
	request = {}
	request['IdSenderName']=IdSenderName
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def crear_campana(Temp_Token,Name):
	url = str(base_url)+'NewCampaign'
	request = {}
	request['Name']=Name
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def renombrar_campana(Temp_Token,CampaignId,Name):
	url = str(base_url)+'RenameCampaign'
	request = {}
	request['CampaignId']=CampaignId
	request['Name']=Name
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def eliminar_campana(Temp_Token,CampaignId):
	url = str(base_url)+'DeleteCampaign'
	request = {}
	request['CampaignId']=CampaignId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def buscar_campana(Temp_Token,From='',Until='',Name=''):
	url = str(base_url)+'SearchCampaign'
	request = {'Order':'asc'}
	request['Search']=Name
	request['DateFrom']=From
	request['DateTo']=Until
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def crear_accion(Temp_Token,CampaignId,Name):
	url = str(base_url)+'NewAction'
	request = {}
	request['CampaignId']=CampaignId
	request['Name']=Name
	request['TypeAction']=1
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def duplicar_accion(Temp_Token,CampaignId,ActionId,Name):
	url = str(base_url)+'DuplicateAction'
	request = {}
	request['CampaignId']=CampaignId
	request['ActionId']=ActionId
	request['Name']=Name
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def renombrar_accion(Temp_Token,ActionId,Name):
	url = str(base_url)+'RenameAction'
	request = {}
	request['ActionId']=ActionId
	request['Name']=Name
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def eliminar_accion(Temp_Token,ActionId):
	url = str(base_url)+'DeleteAction'
	request = {}
	request['ActionId']=ActionId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def buscar_accion(Temp_Token,CampaignId,From='',Until='',Name='',FirstResult=0):
	url = str(base_url)+'SearchAction'
	request = {'Order':'asc'}
	request['Search']=Name
	request['FirstResult']=FirstResult
	request['CampaignId']=CampaignId
	request['DateFrom']=From
	request['DateTo']=Until
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def asociar_grupo_con_accion(Temp_Token,ActionId,GroupsId):
	url = str(base_url)+'SetRecipients'
	request = {}
	request['ActionId']=ActionId
	request['GroupsId']=GroupsId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def asignar_sender_y_subject(Temp_Token,ActionId,SenderId,Subject):
	url = str(base_url)+'SetSender'
	request = {}
	request['ActionId']=ActionId
	request['SenderId']=SenderId
	request['Subject']=Subject
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def asignar_html(Temp_Token,ActionId,Code,Url):
	url = str(base_url)+'SetMessage'
	request = {}
	request['ActionId']=ActionId
	request['Code']=Code
	request['Url']=Url
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def asignar_fecha_envio(Temp_Token,ActionId,Date):
	url = str(base_url)+'SetMessage'
	request = {}
	request['ActionId']=ActionId
	request['Date']=Date
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def asignar_opciones(Temp_Token,ActionId,PrimeraLinea='',SocialHeader=False,SocialFooter=False,OnlineHeader=False,LegalesFooter=True,SuscribirHeader=False,SuscribirFooter=False,DatosFooter=False):
	url = str(base_url)+'SetOptions'
	request = {}
	request['ActionId']=ActionId
	request['Token']=Temp_Token
	request['SocialHeader']=SocialHeader
	request['SocialFooter']=SocialFooter
	request['OnlineHeader']=OnlineHeader
	request['OnlineFooter']=OnlineFooter
	request['LegalesFooter']=LegalesFooter
	request['SuscribirHeader']=SuscribirHeader
	request['SuscribirFooter']=SuscribirFooter
	request['PrimeraLinea']=PrimeraLinea
	request['DatosFooter']=DatosFooter
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def asignar_split_test(Temp_Token,ActionId,SampleB,SampleC,Size=10):
	url = str(base_url)+'SetSplitTest'
	request = {}
	request['ActionId']=ActionId
	request['SampleB']=Date
	request['SampleC']=Date
	request['Size']=Size
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def pausar_accion(Temp_Token,ActionId):
	url = str(base_url)+'PauseAction'
	request = {}
	request['ActionId']=ActionId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def confirmar_accion(Temp_Token,ActionId):
	url = str(base_url)+'ConfirmAction'
	request = {}
	request['ActionId']=ActionId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def cerrar_accion(Temp_Token,ActionId):
	url = str(base_url)+'CloseAction'
	request = {}
	request['ActionId']=ActionId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def ejecutar_trigger(Temp_Token,ActionId,EmailsIds):
	url = str(base_url)+'ExecuteTrigger'
	request = {}
	request['ActionId']=ActionId
	request['EmailsIds']=EmailsIds
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def ejecutar_trigger_express(Temp_Token,ActionId,Email):
	url = str(base_url)+'ExecuteTriggerExpress'
	request = {}
	request['ActionId']=ActionId
	request['Email']=Email
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def ejecutar_trigger_a_grupo(Temp_Token,ActionId,GroupId):
	url = str(base_url)+'ExecuteTriggerAll'
	request = {}
	request['ActionId']=ActionId
	request['GroupId']=GroupId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def activar_trigger(Temp_Token,ActionId):
	url = str(base_url)+'ActivateTrigger'
	request = {}
	request['ActionId']=ActionId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def desactivar_trigger(Temp_Token,ActionId):
	url = str(base_url)+'DesactivateTrigger'
	request = {}
	request['ActionId']=ActionId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def enviar_sendmail(Temp_Token,ActionId,Emails,Message,Subject):
	url = str(base_url)+'SendMail'
	request = {}
	request['Token']=Temp_Token
	request['Emails']=Emails
	request['ActionId']=Temp_Token
	request['Message']=Temp_Token
	request['Subject']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def enviar_sendmail_express(Temp_Token,ActionId,Email,Message,Subject):
	url = str(base_url)+'SendMailExpress'
	request = {}
	request['Token']=Temp_Token
	request['Email']=Email
	request['ActionId']=Temp_Token
	request['Message']=Temp_Token
	request['Subject']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def buscar_sendmail_fecha(Temp_Token,Timestamp):
	url = str(base_url)+'SearchSendMailByTimestamp'
	request = {}
	request['Token']=Temp_Token
	request['Timestamp']=Timestamp
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def buscar_sendmail(Temp_Token,ActionId,From='',Until='',Name='',FirstResult=0):
	url = str(base_url)+'SearchSendMail'
	request = {'Order':'asc'}
	request['Search']=Name
	request['FirstResult']=FirstResult
	request['ActionId']=ActionId
	request['DateFrom']=From
	request['DateTo']=Until
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def revisar_sendmail(Temp_Token,ActionId,Message,Subject):
	url = str(base_url)+'CheckSendMail'
	request = {}
	request['Token']=Temp_Token
	request['ActionId']=ActionId
	request['Message']=Message
	request['Subject']=Subject
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def enviar_sms(Temp_Token,ActionId,Emails,Message):
	url = str(base_url)+'SendSMS'
	request = {}
	request['Token']=Temp_Token
	request['ActionId']=ActionId
	request['Emails']=Emails
	request['Message']=Message
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def buscar_sms_fecha(Temp_Token,Timestamp):
	url = str(base_url)+'SearchSMSByTimestamp'
	request = {}
	request['Token']=Temp_Token
	request['Timestamp']=Timestamp
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def buscar_sms(Temp_Token,ActionId,From='',Until='',Name='',FirstResult=0,Sent=True,Failed=False):
	url = str(base_url)+'SearchSMS'
	request = {'Order':'asc'}
	request['Search']=Name
	request['FirstResult']=FirstResult
	request['ActionId']=ActionId
	request['DateFrom']=From
	request['DateTo']=Until
	request['Sent']=Sent
	request['Failed']=Failed
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def revisar_sms(Temp_Token,ActionId,Message):
	url = str(base_url)+'CheckSMS'
	request = {}
	request['Token']=Temp_Token
	request['ActionId']=ActionId
	request['Message']=Message
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def resumen_reporte(Temp_Token,ActionId):
	url = str(base_url)+'GetSummary'
	request = {}
	request['Token']=Temp_Token
	request['ActionId']=ActionId
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def actividad_por_accion(Temp_Token,ActionId,ActivityId=1):
	#Summary = 1,Open = 2,Clicks = 3,Viral = 4, Suscribe = 5,Unsuscribe  = 6,Bounces = 7,Social = 8
	url = str(base_url)+'SearchActivityByAction'
	request = {}
	request['Token']=Temp_Token
	request['ActionId']=ActionId
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def buscar_contactos_por_actividad(Temp_Token,ActionId,ActivityId=1,Name='',FirstResult=0):
	#OriginalsSent = 1,EffectivesSent = 2,TotalOpen = 3,UniqueOpen = 4,RecurrentOpen = 5,TotalClicks = 6,UniqueClicks = 7,
	#RecurrentClicks = 8,Viral = 9,Suscribe = 10,Unsuscribe = 11,Bounces = 12,TotalSocial = 13,SocialFacebook = 14,SocialTwitter = 15 ,
	url = str(base_url)+'SearchContactsByActivity'
	request = {'Order':'asc'}
	request['Search']=Name
	request['FirstResult']=FirstResult
	request['ActionId']=ActionId
	request['ActivityId']=ActivityId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def actividad_por_contacto(Temp_Token,EmailId):
	url = str(base_url)+'GetActivityByEmail'
	request = {}
	request['EmailId']=EmailId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def compartir_reporte(Temp_Token,ActionId):
	url = str(base_url)+'ShareReports'
	request = {}
	request['ActionId']=ActionId
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def obtener_reportes_automaticos(Temp_Token):
	url = str(base_url)+'GetAutomaticReportsFiles'
	request = {}
	request['Token']=Temp_Token
	response = requests.post(url, data=json.dumps(request), headers=headers)
	res_json=json.loads(response.text)
	return res_json

def obtener_grupos(Token,Temp_Token):
	groups={}
	groups_template={'Name':'','NumberAdressees':0,'NumberContacts':0}
	FirstResult=0
	Start_Size=0
	Finish_Size=1
	while Start_Size!=Finish_Size:
		status=rev_conexion(Temp_Token)
		if status['Result']==False:Temp_Token=log_in(token_jockey)["Token"]
		Start_Size=len(groups)
		search_result=buscar_grupo(Temp_Token,'',FirstResult)
		for group in search_result:
			if group['GroupId'] not in groups:
				groups[group['GroupId']]=groups_template.copy()
			groups[group['GroupId']]['Name']=group['Name']
			groups[group['GroupId']]['NumberAdressees']=group['NumberAdressees']
			groups[group['GroupId']]['NumberContacts']=group['NumberContacts']
		FirstResult=len(groups)
		Finish_Size= len(groups)
	return groups

def obtener_usuarios(Token,Temp_Token):
	users={}
	users_template={'Email':''}
	FirstResult=0
	Start_Size=0
	Finish_Size=1
	while Start_Size!=Finish_Size:
		status=rev_conexion(Temp_Token)
		if status['Result']==False:Temp_Token=log_in(token_jockey)["Token"]
		Start_Size=len(users)
		search_result=buscar_contacto(Temp_Token,'',FirstResult)
		for user in search_result:
			if user['EmailId'] not in users:
				users[user['EmailId']]=users_template.copy()
			users[user['EmailId']]['Email']=user['Email']
		FirstResult=len(users)
		Finish_Size= len(users)
	return users

def obtener_usuarios_full(Token,Temp_Token):
	campos={}
	campos_template={'name':'','value':''}
	for item in listar_campos(Temp_Token):
		if not item['id'] in campos:
			campos[item['id']]=campos_template.copy()
		campos[item['id']]['name']=item['nombre']
	users={}
	users_template={'Email':''}
	FirstResult=0
	Start_Size=0
	Finish_Size=1
	while Start_Size!=Finish_Size:
		status=rev_conexion(Temp_Token)
		if status['Result']==False:Temp_Token=log_in(token_jockey)["Token"]
		Start_Size=len(users)
		search_result=buscar_contacto(Temp_Token,'',FirstResult)
		for user in search_result:
			if user['EmailId'] not in users:
				users[user['EmailId']]=copy.deepcopy(campos)
			for campo in obtener_campos_de_contacto(Temp_Token,user['EmailId']):
				users[user['EmailId']][campo['id']]['value']=campo['valor']
		FirstResult=len(users)
		Finish_Size= len(users)
	return users


	