#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import requests
import xml.etree.ElementTree as ET

from requests.packages.urllib3.exceptions import InsecureRequestWarning

header_soap="""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<SOAP-ENV:Envelope 
    xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" 
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:fic="ficheid.webserv.experian.com"
    xmlns:obj="http://objet.ficheid.webserv.experian.com"
    xmlns:rec="http://rechdeno.methodes.ficheid.webserv.experian.com"
    xmlns:mns="java:com.experian.webserv.infogreffe"
    xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/">"""
    

header_body="""<SOAP-ENV:Body>
    <mns:getProduitsWebServicesXML>
      <arg0 xsi:type="xsd:string" >
      <demande>
	<emetteur>
	  <code_abonne>85000170</code_abonne>
	  <mot_passe>98541</mot_passe>"""
   
footer_body="""</arg0>
    </mns:getProduitsWebServicesXML>
  </SOAP-ENV:Body>"""
    
footer_soap="</SOAP-ENV:Envelope>"

ns = {'ev': 'http://schemas.xmlsoap.org/soap/envelope/'}
ns0= {'nsl': 'urn:local'}
nsfic= {'fic': 'ficheid.webserv.experian.com'}

def get_info_bilan(greffe,siren,num_gestion,millesime,num_depot,date_cloture,version):
    
    version="8"
    
    if siren!="":
        id_ent="""<num_siren>"""+siren+"""</num_siren>"""
    elif num_gestion !="":
        
        millesime1=num_gestion[2:4]
        statut=num_gestion[4:5]
        chrono=num_gestion[5:]
        id_ent="""
            <num_gest>
            <greffe>"""+greffe+"""</greffe>
            <dossier_millesime>"""+millesime1+"""</dossier_millesime>
            <dossier_statut>"""+statut+"""</dossier_statut>
            <dossier_chrono>"""+chrono+"""</dossier_chrono>
            </num_gest>"""
    else:
        print("manque identification d'entreprise")
        return("None")
        
    # Pour l'instant on travaille avec la date de clôture ou le millesime
    if millesime !="":
        id_depot="""<millesime>"""+millesime+"""</millesime>"""
    elif num_depot != "" and date_cloture != "":
        id_depot="""<num_depot>"""+num_depot+"""</num_depot>
            <date_cloture>"""+date_cloture+"""</date_cloture>"""
    elif date_cloture != "":
        id_depot="""<date_cloture>"""+date_cloture+"""</date_cloture>"""
    else:
        print("manque identification depot")
        return("None")
        
        
    
    
    cmd="""<commande>"""+id_ent+id_depot+"""
        <version_schema>"""+version+"""</version_schema>
        </commande>"""
    
        
    body="""<code_requete>
        <type_profil>A</type_profil>
        <origine_emetteur>IC</origine_emetteur>
        <nature_requete>C</nature_requete>
        <type_document>BI</type_document>
        <type_requete>S</type_requete>
        <mode_diffusion>
            <mode type="T"/>
        </mode_diffusion>
        <media>WS</media>
        </code_requete>
        </emetteur>"""+cmd+"""</demande>"""
        
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request=header_soap+header_body+body+footer_body+footer_soap
    encoded_request = request.encode('utf-8')
    


    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "urn:getProduitsWebServicesXML"}

    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",
                     headers = headers,
                     data = encoded_request,
                     verify=False)

    

    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)
    return_node=response_node.find('return')
    
    return(return_node)
    
def get_bilan_gestion(greffe,num_gestion,num_depot,date_cloture,version):
    
    millesime1=num_gestion[0:2]
    statut=num_gestion[2:3]
    chrono=num_gestion[3:]
    id_ent="""
        <num_gest>
        <greffe>"""+greffe+"""</greffe>
        <dossier_millesime>"""+millesime1+"""</dossier_millesime>
        <dossier_statut>"""+statut+"""</dossier_statut>
        <dossier_chrono>"""+chrono+"""</dossier_chrono>
        </num_gest>"""

    id_depot="""<num_depot>"""+num_depot+"""</num_depot>
            <date_cloture>"""+date_cloture+"""</date_cloture>"""
                
    cmd="""<commande>"""+id_ent+id_depot+"""
        <version_schema>"""+str(version)+"""</version_schema>
        </commande>"""
    

        
    body="""<code_requete>
        <type_profil>A</type_profil>
        <origine_emetteur>IC</origine_emetteur>
        <nature_requete>C</nature_requete>
        <type_document>BS</type_document>
        <type_requete>S</type_requete>
        <mode_diffusion>
            <mode type="XL"/>
        </mode_diffusion>
        <media>WS</media>
        </code_requete>
        </emetteur>"""+cmd+"""</demande>"""
        
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request=header_soap+header_body+body+footer_body+footer_soap
    
    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "urn:getProduitsWebServicesXML"}

    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",
                     headers = headers,
                     data = encoded_request,
                     verify=False)

    

    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)
    return_node=response_node.find('return')   
    return(return_node)


def get_info_last_bilan(greffe,siren,num_gestion,version):
    
    version="8"
    depot=[]
    
    if siren!="":
        id_ent="""<num_siren>"""+siren+"""</num_siren>"""
    elif num_gestion !="":
        
        millesime1=num_gestion[2:4]
        statut=num_gestion[4:5]
        chrono=num_gestion[5:]
        id_ent="""
            <num_gest>
            <greffe>"""+greffe+"""</greffe>
            <dossier_millesime>"""+millesime1+"""</dossier_millesime>
            <dossier_statut>"""+statut+"""</dossier_statut>
            <dossier_chrono>"""+chrono+"""</dossier_chrono>
            </num_gest>"""
    else:
        print("manque identification d'entreprise")
        depot.append('None')
        return(depot)

                
    cmd="""<commande>"""+id_ent+"""
        <version_schema>"""+str(version)+"""</version_schema>
        </commande>"""

    body="""<code_requete>
        <type_profil>A</type_profil>
        <origine_emetteur>IC</origine_emetteur>
        <nature_requete>C</nature_requete>
        <type_document>BI</type_document>
        <type_requete>S</type_requete>
        <mode_diffusion>
            <mode type="T"/>
        </mode_diffusion>
        <media>WS</media>
        </code_requete>
        </emetteur>"""+cmd+"""</demande>"""
        
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request=header_soap+header_body+body+footer_body+footer_soap
    
    encoded_request = request.encode('utf-8')
    


    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "urn:getProduitsWebServicesXML"}

    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",
                     headers = headers,
                     data = encoded_request,
                     verify=False)

    

    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)
    return_node=response_node.find('return')   
    if return_node.text is None:
        last_mill=1800
        list_bilan=return_node.find('liste_bilan_complet')
        for bilan in list_bilan.findall('bilan_complet'):
            type_compte=bilan.find('type_comptes')
            millesime=bilan.find('millesime')
            if type_compte.text=='sociaux':
                if int(millesime.text)>last_mill:
                    last_mill=int(millesime.text)
                    node_bilan=bilan
        depot.append('OK')
        depot.append(node_bilan)
    else:
        depot.append(return_node.text)
    return(depot)

def get_bilan(greffe,siren,num_gestion,millesime,num_depot,date_cloture,version):
    
    millesime1=num_gestion[2:4]
    statut=num_gestion[4:5]
    chrono=num_gestion[5:]
    id_ent="""
        <num_gest>
        <greffe>"""+greffe+"""</greffe>
        <dossier_millesime>"""+millesime1+"""</dossier_millesime>
        <dossier_statut>"""+statut+"""</dossier_statut>
        <dossier_chrono>"""+chrono+"""</dossier_chrono>
        </num_gest>"""

    id_depot="""<num_depot>"""+num_depot+"""</num_depot>
            <date_cloture>"""+date_cloture+"""</date_cloture>"""
                
    cmd="""<commande>"""+id_ent+id_depot+"""
        <version_schema>"""+str(version)+"""</version_schema>
        </commande>"""
    

        
    body="""<code_requete>
        <type_profil>A</type_profil>
        <origine_emetteur>IC</origine_emetteur>
        <nature_requete>C</nature_requete>
        <type_document>BS</type_document>
        <type_requete>S</type_requete>
        <mode_diffusion>
            <mode type="XL"/>
        </mode_diffusion>
        <media>WS</media>
        </code_requete>
        </emetteur>"""+cmd+"""</demande>"""
        
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request=header_soap+header_body+body+footer_body+footer_soap
    
    encoded_request = request.encode('utf-8')
    


    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "urn:getProduitsWebServicesXML"}

    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",
                     headers = headers,
                     data = encoded_request,
                     verify=False)

    

    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)
    return_node=response_node.find('return')   
    return(return_node)
    
    
    

def get_endettement(greffe,num_gestion,siren,type_ins):
    


    if siren !="":
        cmd="""<commande>
        <num_siren>"""+siren+"""</num_siren>
        <type_inscription>"""+type_ins+"""</type_inscription>
        <version_schema>5</version_schema>
        </commande>"""        
    else:        
        millesime=num_gestion[2:4]
        statut=num_gestion[4:5]
        chrono=num_gestion[5:]
    
        cmd="""<commande>
        <num_gest>
        <greffe>"""+greffe+"""</greffe>
        <dossier_millesime>"""+millesime+"""</dossier_millesime>
        <dossier_statut>"""+statut+"""</dossier_statut>
        <dossier_chrono>"""+chrono+"""</dossier_chrono>
        </num_gest>
        <type_inscription>"""+type_ins+"""</type_inscription>
        <version_schema>5</version_schema>
        </commande>"""

    body="""<code_requete>
        <type_profil>A</type_profil>
        <origine_emetteur>IC</origine_emetteur>
        <nature_requete>C</nature_requete>
        <type_document>PN</type_document>
        <type_requete>S</type_requete>
        <mode_diffusion>
        <mode type="XL"/>
        </mode_diffusion>
        <media>WS</media>
        </code_requete>
        </emetteur>"""+cmd+"""</demande>"""
        
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request=header_soap+header_body+body+footer_body+footer_soap
    #print(request)
    encoded_request = request.encode('utf-8')
    


    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "urn:getProduitsWebServicesXML"}

    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",
                     headers = headers,
                     data = encoded_request,
                     verify=False)

    

    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)
    return_node=response_node.find('return')   
    return(return_node)
        
        
def get_kbis(greffe,num_gestion,siren):
    
    if siren !="":
        cmd="""<commande>
        <num_siren>"""+siren+"""</num_siren>
        <version_schema>6</version_schema>
        </commande>"""        
    else:        
        millesime=num_gestion[2:4]
        statut=num_gestion[4:5]
        chrono=num_gestion[5:]
    
        cmd="""<commande>
        <num_gest>
        <greffe>"""+greffe+"""</greffe>
        <dossier_millesime>"""+millesime+"""</dossier_millesime>
        <dossier_statut>"""+statut+"""</dossier_statut>
        <dossier_chrono>"""+chrono+"""</dossier_chrono>
        </num_gest>
        <version_schema>6</version_schema>
        </commande>"""


    body="""<code_requete>
        <type_profil>A</type_profil>
        <origine_emetteur>IC</origine_emetteur>
        <nature_requete>C</nature_requete>
        <type_document>KB
        </type_document>
        <type_requete>S</type_requete>
        <mode_diffusion>
        <mode type="XL"/>
        </mode_diffusion>
        <media>WS</media>
        </code_requete>
        </emetteur>"""+cmd+"""</demande>"""

      
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request=header_soap+header_body+body+footer_body+footer_soap
    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "urn:getProduitsWebServicesXML"}

    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",
                     headers = headers,
                     data = encoded_request,
                     verify=False)


    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)
    return_node=response_node.find('return')   
    return(return_node)

    
def get_statut_ajour_siren(siren):

    body="""<code_requete>
            <type_profil>A</type_profil>
            <origine_emetteur>IC</origine_emetteur>
            <nature_requete>C</nature_requete>
            <type_document>ST
            </type_document>
            <type_requete>S</type_requete>
            <mode_diffusion>
            <mode type="T"/>
            </mode_diffusion>
            <media>WS</media>
            </code_requete>
            </emetteur>
            <commande>
            <num_siren>"""+siren+"""</num_siren>
            <version_schema>6</version_schema>
            </commande>
            </demande>"""
      
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request=header_soap+header_body+body+footer_body+footer_soap
    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "urn:getProduitsWebServicesXML"}

    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",
                     headers = headers,
                     data = encoded_request,
                     verify=False)



    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)
    return_node=response_node.find('return')   
    return(return_node)
    
    
def get_statut_ajour(greffe,num_gestion):
    
    millesime=num_gestion[2:4]
    statut=num_gestion[4:5]
    chrono=num_gestion[5:]
    
    body="""<code_requete>
            <type_profil>A</type_profil>
            <origine_emetteur>IC</origine_emetteur>
            <nature_requete>C</nature_requete>
            <type_document>ST
            </type_document>
            <type_requete>S</type_requete>
            <mode_diffusion>
            <mode type="T"/>
            </mode_diffusion>
            <media>WS</media>
            </code_requete>
            </emetteur>
            <commande>
            <num_gest>
            <greffe>"""+greffe+"""</greffe>
            <dossier_millesime>"""+millesime+"""</dossier_millesime>
            <dossier_statut>"""+statut+"""</dossier_statut>
            <dossier_chrono>"""+chrono+"""</dossier_chrono>
            </num_gest>
            <version_schema>6</version_schema>
            </commande>
            </demande>"""
      
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request=header_soap+header_body+body+footer_body+footer_soap
    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "urn:getProduitsWebServicesXML"}

    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",
                     headers = headers,
                     data = encoded_request,
                     verify=False)



    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)
    return_node=response_node.find('return')   
    return(return_node)



def get_liste_actes(siren):
    
    body="""<code_requete>
            <type_profil>A</type_profil>
            <origine_emetteur>IC</origine_emetteur>
            <nature_requete>C</nature_requete>
            <type_document>AC
            </type_document>
            <type_requete>S</type_requete>
            <mode_diffusion>
            <mode type="T"/>
            </mode_diffusion>
            <media>WS</media>
            </code_requete>
            </emetteur>
            <commande>
            <num_siren>"""+siren+"""</num_siren>
            <version_schema>6</version_schema>
            </commande>
            </demande>"""
      
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    request=header_soap+header_body+body+footer_body+footer_soap

    encoded_request = request.encode('utf-8')



    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "urn:getProduitsWebServicesXML"}

    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",
                     headers = headers,
                     data = encoded_request,
                     verify=False)



    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)
    return_node=response_node.find('return')
    return(return_node)
    
def get_liste_depot(siren,num_depot):
    
    body="""<code_requete>
            <type_profil>A</type_profil>
            <origine_emetteur>IC</origine_emetteur>
            <nature_requete>C</nature_requete>
            <type_document>AC
            </type_document>
            <type_requete>S</type_requete>
            <mode_diffusion>
            <mode type="T"/>
            </mode_diffusion>
            <media>WS</media>
            </code_requete>
            </emetteur>
            <commande>
            <num_siren>"""+siren+"""</num_siren>
            <num_depot>"""+num_depot+"""</num_depot>
            <version_schema>6</version_schema>
            </commande>
            </demande>"""
      
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request=header_soap+header_body+body+footer_body+footer_soap
    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "urn:getProduitsWebServicesXML"}

    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",
                     headers = headers,
                     data = encoded_request,
                     verify=False)

    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)
    return_node=response_node.find('return')    
    return(return_node)
    
def get_acte(siren,num_depot,num_acte):
    
    body="""<code_requete>
            <type_profil>A</type_profil>
            <origine_emetteur>IC</origine_emetteur>
            <nature_requete>C</nature_requete>
            <type_document>AC
            </type_document>
            <type_requete>S</type_requete>
            <mode_diffusion>
            <mode type="T"/>
            </mode_diffusion>
            <media>WS</media>
            </code_requete>
            </emetteur>
            <commande>
            <num_siren>"""+siren+"""</num_siren>
            <num_depot>"""+num_depot+"""</num_depot>
            <num_acte>"""+num_acte+"""</num_acte>
            <version_schema>6</version_schema>
            </commande>
            </demande>"""
      
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request=header_soap+header_body+body+footer_body+footer_soap
    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": "urn:getProduitsWebServicesXML"}

    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",
                     headers = headers,
                     data = encoded_request,
                     verify=False)

    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)
    return_node=response_node.find('return')    
    return(return_node)
    
def get_ficheEntreprise(siren):

    body="""<SOAP-ENV:Body>
            <fic:getFicheIdentite>
            <fic:in0>
            <obj:siren>"""+siren+"""</obj:siren>
            </fic:in0>
            </fic:getFicheIdentite>
            </SOAP-ENV:Body>"""
            

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request= header_soap+body+footer_soap
    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": ""}

    response = requests.post(url="http://services.infogreffe.fr/axis/services/ServiceFicheIdentite",
                     headers = headers,
                     data = encoded_request,
                     auth= ('INFOGREFFE', 'JsE2=BDC'),
                     verify=False)
    
    if int(response.status_code) == 200:
        tree = ET.fromstring(response.text)
        body_node=tree.find('ev:Body', ns)
        response_node=body_node.find('fic:getFicheIdentiteResponse',nsfic)
        #print(response_node)
        return_node=response_node.find('fic:getFicheIdentiteReturn',nsfic)
        return(return_node)
    else:
        print(response.status_code)
        return(response.status_code)
        
    
    
def get_ficheEntrepriseEnrichie(siren):

    body="""<SOAP-ENV:Body>
            <fic:getFicheIdentiteEnrichie>
            <fic:in0>
            <obj:siren>"""+siren+"""</obj:siren>
            </fic:in0>
            </fic:getFicheIdentiteEnrichie>
            </SOAP-ENV:Body>"""
            

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request= header_soap+body+footer_soap
    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": ""}

    response = requests.post(url="http://services.infogreffe.fr/axis/services/ServiceFicheIdentite",
                     headers = headers,
                     data = encoded_request,
                     auth= ('INFOGREFFE', 'JsE2=BDC'),
                     verify=False)

    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('fic:getFicheIdentiteEnrichieResponse',nsfic)
    return_node=response_node.find('fic:getFicheIdentiteEnrichieReturn',nsfic)
    return(return_node)
    


def find_ficheEntreprise(denomination,dept):
    nsfic= {'fic': 'ficheid.webserv.experian.com'}
    
    ligne_dep=""
    
    if dept != "":
        ligne_dep="""<rec:codeDepartement>"""+dept+"""</rec:codeDepartement>"""

    body="""<SOAP-ENV:Body>
            <fic:rechFicheIdentiteParDeno>
            <fic:in0>
            <rec:denomination>"""+denomination+"""</rec:denomination>
            """+ligne_dep+"""
            </fic:in0>
            </fic:rechFicheIdentiteParDeno>
            </SOAP-ENV:Body>"""
            

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    request= header_soap+body+footer_soap
    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",
            "Content-Length": str(len(encoded_request)),
            "SOAPAction": ""}

    response = requests.post(url="http://services.infogreffe.fr/axis/services/ServiceFicheIdentite",
                     headers = headers,
                     data = encoded_request,
                     auth= ('INFOGREFFE', 'JsE2=BDC'),
                     verify=False)

    tree = ET.fromstring(response.text)
    body_node=tree.find('ev:Body', ns)
    response_node=body_node.find('fic:rechFicheIdentiteParDenoResponse',nsfic)
    if response_node is not None:
        return_node=response_node.find('fic:rechFicheIdentiteParDenoReturn',nsfic)
    else:
        return_node = None
        
    return(return_node)
    
