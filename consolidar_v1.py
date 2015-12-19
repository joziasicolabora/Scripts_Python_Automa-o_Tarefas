# -*- coding: cp1252 -*-
'''
Consolidar - Programa responsável por gerar o grafico generido dos Procons

Para ser executado necessita de um arquivo contendo todos os vertices que
comporão o novo grafo, que foi nomeado lista_procons, contendoo mesmo conteúdo
que o graphSON. EX.: 
	{"graph":{
		"mode":"NORMAL",
		"vertices":[],
		"edges":[]
		}
	}
Ainda é necessário um novo arquivo contendo a exportação do turbilet com os valores
necessarios para criarmos o relacionamentos, aqui nomeado procons.csv. EX.:
Id UF	UF	Id cidade	Cidade	Id Endereço	Endereço	                    Id nome	Nome	                Id Telefone	Telefone	Id CEP	CEP
11	MG	12995131329     Alfenas	12995131331	Pça Dr. Emílio da Silveira	12995131330	PROCON Alfenas	12995131332		12995131333	1       00.000-000

Cuidado quando carregar os vertices eles podem conter o caracter ";", que pode quebrar o codigo.


Desenvolvido por iColabora
'''

#uuid biblioteca que gera o uuid
import uuid




grafo = open("lista_procons.txt","r")# Carrega a graphSON
relacionamentos = open("procons.csv","r") #Carrega a tabela
vertices = []
arestas = []

#Extrai todos os vertices
for i in grafo.readlines():
    if '"_type":"vertex"' in i:
        vertices.append(i)
grafo.close()


#Modifica o Id do vertice para um UUID
vert = open("vertices.txt","w")
for i in range(len(vertices)):
    idV = vertices[i].split('", "')
    vertices[i] = vertices[i].replace(idV[1]+'"','_id":"'+str(uuid.uuid5(uuid.NAMESPACE_DNS, idV[1].split(':')[-1][1:]))+'"')
    vert.write(vertices[i].strip()+"\n")
vert.close()


#Criar novas arestas
edges = open("edges.txt","w")
for i in relacionamentos:
    valores =  i.split(";")
    id_uf = valores[0]
    uf = valores[1]
    id_cidade = valores[2]
    cidade = valores[3]
    id_endereco = valores[4]
    endereco = valores[5]
    id_nome = valores[6]
    nome = valores[7]
    id_telefone = valores[8]
    telefone = valores[9]
    id_cep = valores[10]
    cep = valores[11][:-1]

    edges.write('{"weight": {"type":"string", "value":"%s"}, "_id":"%s", "_outV":"%s", "_inV":"%s", "_label":"relacionado", "_type":"edge"},\n'%(uf+"->"+cidade,str(uuid.uuid4()),str(uuid.uuid5(uuid.NAMESPACE_DNS, id_uf)),str(uuid.uuid5(uuid.NAMESPACE_DNS, id_cidade))))
    edges.write('{"weight": {"type":"string", "value":"%s"}, "_id":"%s", "_outV":"%s", "_inV":"%s", "_label":"relacionado", "_type":"edge"},\n'%(cidade+"->"+nome,str(uuid.uuid4()),str(uuid.uuid5(uuid.NAMESPACE_DNS, id_cidade)),str(uuid.uuid5(uuid.NAMESPACE_DNS, id_nome))))
    edges.write('{"weight": {"type":"string", "value":"%s"}, "_id":"%s", "_outV":"%s", "_inV":"%s", "_label":"relacionado", "_type":"edge"},\n'%(nome+"->"+telefone,str(uuid.uuid4()),str(uuid.uuid5(uuid.NAMESPACE_DNS, id_nome)),str(uuid.uuid5(uuid.NAMESPACE_DNS, id_telefone))))
    edges.write('{"weight": {"type":"string", "value":"%s"}, "_id":"%s", "_outV":"%s", "_inV":"%s", "_label":"relacionado", "_type":"edge"},\n'%(nome+"->"+endereco,str(uuid.uuid4()),str(uuid.uuid5(uuid.NAMESPACE_DNS, id_nome)),str(uuid.uuid5(uuid.NAMESPACE_DNS, id_endereco))))
    edges.write('{"weight": {"type":"string", "value":"%s"}, "_id":"%s", "_outV":"%s", "_inV":"%s", "_label":"relacionado", "_type":"edge"},\n\n'%(endereco+"->"+cep,str(uuid.uuid4()),str(uuid.uuid5(uuid.NAMESPACE_DNS, id_endereco)),str(uuid.uuid5(uuid.NAMESPACE_DNS, id_cep))))
    
edges.close()


