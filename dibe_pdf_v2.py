# -*- coding: Utf-8 -*-



# USAGE: python dibe_pdf.py -i <identification> -f <fichier.csv> -d <directory>





import io

import os

import requests

import xml.etree.ElementTree as ET

import sys

import getopt

import psycopg2





import xlrd

import xlwt

from xlwt import Workbook



from requests.packages.urllib3.exceptions import InsecureRequestWarning



ns = {'ev': 'http://schemas.xmlsoap.org/soap/envelope/'}

ns0= {'nsl': 'urn:local'}



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

    

footer_body="""</arg0>

    </mns:getProduitsWebServicesXML>

  </SOAP-ENV:Body>"""

    

footer_soap="</SOAP-ENV:Envelope>"



def get_data(siren,codegreffe,dtdepot):

    dtsaisie=""

    CMD="select dtsaisie from ta_suividem_ass where codetypeacte='BENh' and siren='"+str(siren)+"' and codegreffe='"+str(codegreffe)+"' and dtdepot='"+dtdepot+"' and dtsaisie is not null and coderetour='0' "

    cursor_pg.execute(CMD)

    #nb=cursor_pg.rowcount

    return (dtsaisie)

    





def create_header_body(ident):

    

    header=""

    ligne=ident.split('-')

    if len(ligne)>=2:

        codeabonne=ligne[0]

        mdp=ligne[1]

    else:

        return(header)



    header="""<SOAP-ENV:Body> 

                <mns:getProduitsWebServicesXML> 

                <arg0 xsi:type="xsd:string" > 

                <demande> 

                <emetteur> 

                <code_abonne>"""+str(codeabonne)+"""</code_abonne> 

                <mot_passe>"""+str(mdp)+"""</mot_passe>""" 

    

    return(header)



def get_liste_depot_gestion(greffe,millesime,statut,chrono,num_depot,ident):

    



    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    

    header_body=create_header_body(ident)

    

    if header_body=="":

        return("Pb d'identification")

        

    if len(ident.split('-'))==3:

        ref=ident.split('-')[2]

    else:

        ref="sans reference"

        

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

       <num_gest>

       <greffe>"""+greffe+"""</greffe>

                     <dossier_millesime>"""+millesime+"""</dossier_millesime>

                     <dossier_statut>"""+statut+"""</dossier_statut>

                     <dossier_chrono>"""+chrono+"""</dossier_chrono>

                  </num_gest>

        <num_depot>"""+num_depot+"""</num_depot>

        <reference_client>"""+str(ref)+"""</reference_client>

        <version_schema>6</version_schema>

        </commande>

        </demande>"""

    

    request=header_soap+header_body+body+footer_body+footer_soap

    

    

    

    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",

            "Content-Length": str(len(encoded_request)),

            "SOAPAction": "urn:getProduitsWebServicesXML"}

    

    



    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",

                     headers = headers,

                     data = encoded_request,

                     verify=False)



    if int(response.status_code) !=200:

        print(response.status_code)

    

    tree = ET.fromstring(response.text)

    body_node=tree.find('ev:Body', ns)

    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)

    return_node=response_node.find('return')    

    return(return_node)

    

    

def get_liste_depot(siren,num_depot,ident):

    



    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    

    header_body=create_header_body(ident)

    

    if header_body=="":

        return("Pb d'identification")

        

    if len(ident.split('-'))==3:

        ref=ident.split('-')[2]

    else:

        ref="sans reference"

        

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

        <reference_client>"""+str(ref)+"""</reference_client>

        <version_schema>6</version_schema>

        </commande>

        </demande>"""

    

    request=header_soap+header_body+body+footer_body+footer_soap

    

    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",

            "Content-Length": str(len(encoded_request)),

            "SOAPAction": "urn:getProduitsWebServicesXML"}



    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",

                     headers = headers,

                     data = encoded_request,

                     verify=False)



    if int(response.status_code) !=200:

        print(response.status_code)

    

    tree = ET.fromstring(response.text)

    body_node=tree.find('ev:Body', ns)

    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)

    return_node=response_node.find('return')    

    return(return_node)

    

def get_liste_actes(siren,ident):

    

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    

    header_body=create_header_body(ident)



    if header_body=="":

        return("Pb d'identification")

        

    if len(ident.split('-'))==3:

        ref=ident.split('-')[2]

    else:

        ref="sans reference"

        

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

            <reference_client>"""+str(ref)+"""</reference_client>

            <version_schema>6</version_schema>

            </commande>

            </demande>"""

    request=header_soap+header_body+body+footer_body+footer_soap

    

    encoded_request = request.encode('utf-8')

    headers = { "Content-Type": "text/xml;charset=UTF-8",

            "Content-Length": str(len(encoded_request)),

            "SOAPAction": "urn:getProduitsWebServicesXML"}



    response = requests.post(url="https://webservices.infogreffe.fr/WSContextInfogreffe/INFOGREFFE",

                     headers = headers,

                     data = encoded_request,

                     verify=False)

    

    if int(response.status_code) !=200:

        print(response.status_code)

        

    tree = ET.fromstring(response.text)

    body_node=tree.find('ev:Body', ns)

    response_node=body_node.find('nsl:getProduitsWebServicesXMLResponse',ns0)

    return_node=response_node.find('return')

    return(return_node)

    

    

def download_acte(url,siren,directory,date,ref):

    filename=directory+"/BE_"+siren+"_"+str(ref)+"_dibe_"+str(date)+".pdf"

    #filename=directory+"/"+siren+"_dibe_"+str(date)+".pdf"

    if simul!='oui':



        r = requests.get(url)

        file=io.open(filename,"wb")

        file.write(r.content)

        file.close()

#    else:

#        print(siren)

    

    return(os.path.basename(filename))



        

# Programme principal





outdir="."

ident="08500-00170"

password="98541"

filename=""

simul="non"

entete='false'

indice=0

flagref='false'

flagsiren='false'



optlist, args = getopt.getopt(sys.argv[1:], 'f:d:i:s:erp:')



for opt, arg in optlist:

    if opt in ("-d"):

        outdir=arg

    elif opt in ("-i"):

        ident=arg

    elif opt in ("-f"):

        filename=arg

    elif opt in ("-p"):

        password=arg

    elif opt in ("-s"):

        flagsiren='true'

        siren=arg

    elif opt in ("-e"):

        entete='true'

    elif opt in ("-r"):

        flagref='true'



liste_result=[]

champ_id=ident.split('-')



ident=champ_id[0][1:]+champ_id[1][1:]+'-'+password



    

root,ext=os.path.splitext(filename)

    

liste_sirens=[]

liste_refs=[]

ref=""



if flagsiren=='false':



    if ext==".csv":

        file_siren=open(filename,'r')

        #lecture de l'entete

        if entete=='true':

            file_siren.readline()
            

        for ligne in file_siren:

            siren=ligne.split(';')[0].replace('\n','').replace(' ','')

            if flagref=='true':

                ref=ligne.split(';')[1].replace('\n','').replace(' ','')

            #siren=ligne.replace('\n','').split(";")[0]

            liste_sirens.append(siren)

            liste_refs.append(ref)

        

    elif ext==".xls":

        wb = xlrd.open_workbook(filename)

        sh=wb.sheet_by_index(0)

        if entete=='true':

            indice=1

        for rownum in range(indice,sh.nrows):

            if sh.row_values(rownum)[0] !="":

                siren=str(int(sh.row_values(rownum)[0])).zfill(9)

                if sh.ncols > 1 and flagref=='true':

                    celltype=sh.cell_type(rownum,1)

                    if celltype==2:

                        ref=str(int(sh.row_values(rownum)[1]))

                    else:

                        ref=str(sh.row_values(rownum)[1])

            liste_sirens.append(siren)

            liste_refs.append(ref)

    elif ext==".xlsx":

        wb = xlrd.open_workbook(filename)

        sh=wb.sheet_by_index(0)

        if entete=='true':

            indice=1

        for rownum in range(indice,sh.nrows):

            if sh.row_values(rownum)[0] !="":

                if sh.cell_type(rownum,0) == 2:

                    siren=str(int(sh.row_values(rownum)[0])).zfill(9)

                elif sh.cell_type(rownum,0) ==1:

                    siren=str(sh.row_values(rownum)[0]).replace(' ','').zfill(9)

                if sh.ncols > 1 and flagref=='true':

                    celltype=sh.cell_type(rownum,1)

                    if celltype==2:

                        ref=str(int(sh.row_values(rownum)[1]))

                    else:

                        ref=str(sh.row_values(rownum)[1])

            liste_sirens.append(siren)

            liste_refs.append(ref)

        

    else:

        print("Format de fichier non reconnu")

        exit()

        

    outname, fileExtension = os.path.splitext(os.path.basename(filename))

    outputname=outdir+"/"+outname+"_dibe_result.csv"

                

        

else:

    liste_sirens.append(siren)

    liste_refs.append(ref)

    outputname=outdir+"/"+str(siren)+"_dibe_result.csv"

    



fileout=io.open(outputname,'w',encoding='iso-8859-15')

fileout.write("siren;Ref.client;Date de depot;Commentaire \n")







for i in range(len(liste_sirens)):

    

    list_depot=[]

    etat_depot=0



    siren=liste_sirens[i]

    refclient=liste_refs[i]

    #
    #   enlever l'espace suivante de siren
    #
    siren = siren.strip()

    if siren.isdigit():
        

        liste_actes=get_liste_actes(siren,ident)

        if liste_actes=="Pb d'identification" :

            print("Pb d'identification")

            exit(3)

    

        return_text=liste_actes.text

        

        if return_text is None:

            # on recherche le depot BENh

            liste_depot_acte=liste_actes.find('liste_depot_acte')

    

            for depot_acte in liste_depot_acte.findall('depot_acte'):

                date_depot=depot_acte.find('date_depot').text

                for acte in depot_acte.findall('acte'):

                    type_acte=acte.find('type_acte').text

                    if type_acte=="BENh" or type_acte=="BE":

                        list_depot.append(siren)

                        list_depot.append(date_depot)

                        num_depot=depot_acte.find('num_depot').text

                        list_depot.append(num_depot)

                        greffe=depot_acte.find('num_gest').find('greffe').text

                        list_depot.append(greffe)

                        millesime=depot_acte.find('num_gest').find('dossier_millesime').text

                        list_depot.append(millesime)

                        statut=depot_acte.find('num_gest').find('dossier_statut').text

                        list_depot.append(statut)

                        chrono=depot_acte.find('num_gest').find('dossier_chrono').text

                        list_depot.append(chrono)

                        



            nb_depot=int(len(list_depot)/7)

            

            if nb_depot > 1:

                date_old="1900-01-01"

                # on recherche le plus recent

                for k in range(nb_depot):

                    date=list_depot[3*k+1]

                    if date > date_old:

                        indice=k

                        date_old=date

                num_depot=list_depot[7*indice+2]

                datedepot=list_depot[7*indice+1]

                greffe=list_depot[7*indice+3]

                millesime=list_depot[7*indice+4]

                statut=list_depot[7*indice+5]

                chrono=list_depot[7*indice+6]

            elif nb_depot == 1:

                num_depot=list_depot[2]

                datedepot=list_depot[1]

                greffe=list_depot[3]

                millesime=list_depot[4]

                statut=list_depot[5]

                chrono=list_depot[6]

            else:

                liste_result.append(siren+";"+str(refclient)+";;pas de depot DIBE pour ce siren; \n")

                etat_depot=1



            if etat_depot!=1:

                # appel du depot

                

                depot=get_liste_depot_gestion(greffe,millesime,statut,chrono,num_depot,ident)

                

                

                if depot=="Pb d'identification":

                    print("Pb d'identification")

                    exit(3)



                depot_acte=depot.find('depot_acte')

                if depot_acte is not None:

                    acte=depot_acte.find('acte')

                    url_acces=acte.find('url_acces')



                    pdfname=download_acte(url_acces.text,siren,outdir,datedepot,refclient)



                    liste_result.append(siren+";"+str(refclient)+";"+str(datedepot)+";"+str(pdfname)+"\n")

                else:

                    liste_result.append(siren+";"+str(refclient)+";;"+str(depot.text)+"\n")

                    print(depot.text)

            

        elif return_text[0:3]=="003":

            print("Pb d'identification")

            exit(3)

        else:

            liste_result.append(siren+";"+str(refclient)+";;"+return_text+"\n")

        

    else:

        print("pb sur siren")



        

for i in range(len(liste_result)):

    fileout.write(liste_result[i])

    

fileout.close()



    

 

  

        



