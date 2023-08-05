# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 18:11:54 2017

@author: thiag
"""
####The code that runs goes here

from pylab import rcParams
rcParams['figure.figsize'] = 8, 6
rcParams['figure.dpi'] = 200
rcParams['font.size'] = 22


def word_list_to_cloud(topwords):
    
    from wordcloud import WordCloud
    from datetime import datetime
    import matplotlib.pyplot as plt
    
    x = ' '.join(topwords)
    wordcloud = WordCloud().generate(x)
    plt.axis('off')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.savefig(folder + 'wordcloud'+ datetime.now().strftime('%Y%m%d%H%M%S') + 
                '.png')
    plt.show()

def summary_list_top_words(summarylist, nwords = 50):

    from sklearn.feature_extraction.text import TfidfVectorizer
#initialize the tf idf matrix

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1,1),
                         min_df = 0, stop_words = ['quot'])

#fit and transform the list of lattes cv summaries to tf idf matrix

    tfidf_matrix =  tf.fit_transform(summarylist)
    feature_names = tf.get_feature_names() 

    dense = tfidf_matrix.todense()

    lattessummary = dense[0].tolist()[0]

#if the score of the word is >0, add the word and its score to the wordscores
#list

    wordscores = [pair for pair in zip(range(0, len(lattessummary)), 
                                       lattessummary) if pair[1] > 0]

#sort the score list by the score (second term)

    sorted_wordscores = sorted(wordscores, key=lambda t: t[1] * -1)

    topwords = []

    for word, score in [(feature_names[word_id], score) for (word_id, score) 
                        in sorted_wordscores][:50]:
        print('{0: <40} {1}'.format(word, score))
        topwords.append(word)
        
    return(topwords)


def getnodeconnections(edgelist, edgenetwork, depth=1):
    import networkx as nx
    if (depth>2)|(depth<1):
        print("invalid depth supplied")
    connections = []
    dummie = edgenetwork.edges()
    
    if depth == 1:
        for i in range(0,len(edgelist)):
            x = 0
            for y in dummie:
                if edgelist[i] in y: x = x + 1
            connections.append(x)
    
    elif depth == 2:
        for i in range (0,len(edgelist)):
            x = 0
#list all the edges connecting to node intlist[i]
            dummie2 = network.edges(edgelist[i])
            for y in dummie2:
#verify connections of those connected to intlist[i]
                for z in dummie:
                    if y[1] in z: x = x + 1
            connections.append(x)
    
    return connections

def nodesclass(graph, nodeslist):
    import networkx as nx
    nx.set_node_attributes(graph,"type","external")
    for x in graph.nodes():
        if x in nodeslist:
            graph.node[x]["type"] = "internal"
    return graph



def lattesowner(filename):
    import zipfile
    import xml.etree.ElementTree as ET
    #abre o arquivo zip baixado do site do lattes
    archive = zipfile.ZipFile((filename), 'r')
#cvdata = archive.read('curriculo.xml')
    cvfile = archive.open('curriculo.xml', 'r')

#inicializa o xpath
    tree = ET.parse(cvfile)
    root = tree.getroot()
#get the cv owner name
    cvowner = root[0].attrib['NOME-COMPLETO']
    return cvowner


def lattesage(rawdata):
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    from datetime import datetime
    x = [datetime.today()-datetime.strptime(str(i),'%d%m%Y') \
         for i in rawdata['atualizado']]
    y = np.array([round(i.days/30) for i in x])

#histograma da idade dos curriculos lattes
    plt.figure(figsize=(8,6), dpi=200)
    dummie = plt.hist(y, bins=range(0,round(max(y)+10, 2)),
                      align='left', histtype='bar', rwidth=0.95)

    plt.axvline(y.mean(), color='black', linestyle='dashed',
                linewidth=2)
    plt.text(round(max(y)+10, 2)*0.3, 0.8*max(dummie[0]),
             'Mean = ' + str(round(y.mean(),2)))            
    plt.suptitle('Age of Lattes CV in months', fontsize=20)
    plt.show()
    del dummie


def lattespibics(rawdata):

    import matplotlib.pyplot as plt
#histograma de quantas vezes o aluno fez bolsa PIBIC
    plt.figure(figsize=(8,6), dpi=200)

    plt.hist(rawdata['quantasVezesPIBIC'], 
             bins=range(max(rawdata['quantasVezesPIBIC'])+2), align='left',
             histtype='bar', rwidth=0.95)

    plt.xticks(range(min(rawdata['quantasVezesPIBIC']),
                     max(rawdata['quantasVezesPIBIC'])+1), fontsize=22)



    plt.suptitle('Scientific Initiation Grants per Student', fontsize=20)
    plt.show()

def mastersrateyear(rawdata):
#Histograma dos mestrandos

    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,6), dpi=200)

    #If the first year is zero, get the second smaller year
    if min(rawdata['anoPrimeiroM']):
        anomaster0 = min(rawdata['anoPrimeiroM'])
    else:
        anomaster0 = sorted(set(rawdata['anoPrimeiroM']))[1]
#last year of occurence of a masters degree
    anomaster1 = max(rawdata['anoPrimeiroM'])

#plot the histogram and store in x
    dummie = plt.hist(rawdata['anoPrimeiroM'], bins=range(anomaster0,
                      anomaster1), align='left', histtype='bar', rwidth=0.95)
 
    plt.suptitle('Masters Degrees Obtained per Year', fontsize=20)

#Plot the total of people who finished masters degree in the given position
    plt.text(anomaster0, 0.8*max(dummie[0]), 'Total = ' +
             str(len(rawdata['anoPrimeiroM'].loc[lambda s:s>0])), size='20')
    plt.show()

    del dummie


def lattesgradlevel(rawdata):

    pibics = len(rawdata.loc[rawdata.quantasVezesPIBIC >= 1])
    masters = len(rawdata.loc[rawdata.quantosM >= 1])
    phds = len(rawdata.loc[rawdata.quantosD >= 1])
    pphds = len(rawdata.loc[rawdata.quantosPD >= 1])

    graddata = pd.DataFrame([pibics, masters, phds, pphds],
                            index=['Scientific Initiation','Masters','PhD',
                                   'Postdoctorate'],
                            columns=['Quantity'])


    plt.figure(figsize=(8,6), dpi=200)
    fig = graddata.plot(y='Quantity', kind='bar', legend=False)
    fig.set_xticklabels(graddata.index, rotation=45)
    plt.title('Academic Level of the Students')
    plt.show()

def getpubyeardata(rawdata):
    
    import pandas as pd
    
#normalizar o ano da primeira publicacao
#o primeiro ano de publicacao e 2004
#ArtComp2004 = coluna 11
#TrabCong2004 = coluna 24

#Concatena a quantidade de artigos e de trabalhos em congressos apresentados
#como indice de produtividade
    pubyeardata = pd.DataFrame(index=rawdata.index)
    for i in range(0, 13):
#        pubyeardata['pub' + str(2004 + i)] = rawdata['ArtComp' +  
#                    str(2004 + i)] + rawdata['TrabCong' + str(2004 + i)]
        
        
        pubyeardata['pub' + str(2004 + i)] = rawdata['papers' +  
                    str(2004 + i)] + rawdata['works' + str(2004 + i)]
                                         
        pubdata = pubyeardata.copy()
        strindex = ['year']*pubdata.shape[1]
        for i in range(1,pubdata.shape[1]):
            strindex[i] = strindex[i] + str(i+1)
        pubdata.columns = strindex
    return pubdata

def firstnonzero(frame, nrow):
#shifta o primeiro indice para o primeiro ano em que houve producao
    
    import pandas as pd
    
    n = frame.shape[1]
    count = 0
    while ((frame.iloc[nrow, 0] == 0) & (count < n)):
        for j in range(0, n-1):
            frame.set_value(nrow, frame.columns[j], frame.iloc[nrow,j+1])
        frame.set_value(nrow, frame.columns[n-1], 0)
        count = count + 1
        
def firstnonzero2(frame, frameindex, nrow):
    #shifta o primeiro indice para o primeiro ano do PIBIC
    import pandas as pd
    
    n = frame.shape[1]
    
    count = 0
    nshift = frameindex[nrow] - 2004
    if nshift > 0:
        for j in range(0, n-1-nshift):
            frame.set_value(nrow, frame.columns[j], frame.iloc[nrow,j+nshift])
            frame.set_value(nrow, frame.columns[n-1-j], 0)
        count = count + 1

def setfuzzycmeansclstr(imin, imax, cleandata):

    import matplotlib.pyplot as plt
    import skfuzzy as fuzz
    import numpy as np
    from sklearn import metrics
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import scale

    
    fpcs = []
    centers = []
    clusters = []
    for i in range(imin, imax):
        center, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(\
            cleandata.transpose(), i, 2, error=0.005, \
            maxiter=1000, init=None)
        cluster_membership = np.argmax(u, axis=0)
#plota o histograma de cada centroide
        plt.figure()
    
        clusterweight = plt.hist(cluster_membership, bins=range(i+1),
                                 align='left', histtype='bar', rwidth=0.95)
        plt.xticks(range(0,i))
        plt.title('Number of Points in Each Centroid of the ' + 
                  str(i)+' Centroid Model')   
        plt.show()

#agrupa funcao de desempenho
        fpcs.append(fpc)
#agrupa os centroides
        centers.append(center)
#agrupa o peso dos centroides
        clusters.append(cluster_membership)
    
        fig, ax = plt.subplots()
        plt.title('Model with ' + str(i) + ' Mean Publication Profiles')
        for j in range(0,i):
            ax.plot(center[j], label=str(clusterweight[0][j]))
        
        legend = ax.legend(loc='upper right', shadow=True)
        plt.show()
    
#    plt.figure()
#    plt.plot(center, label=cluster_membership)
#    plt.title(str(i)+ ' Centroides')

    plt.figure()
    plt.plot(range(imin,imax),fpcs,'-x')
    plt.title('Fuzzy C Means Performance related to the Centroid Quantity')
    plt.show()
    return centers, clusters, fpcs


def getgradyears(x, gradkind):

    nfirst = nquant = 0
    if (x.attrib["ANO-DE-CONCLUSAO"]!="") | (x.attrib["ANO-DE-INICIO"]!=""):
        nquant = nquant + 1
        if nquant==1:
            if x.attrib["ANO-DE-CONCLUSAO"]=="":
                x.attrib["ANO-DE-CONCLUSAO"] = \
                    str(int(x.attrib["ANO-DE-INICIO"]) + xpectdyears(gradkind))
            nfirst = int(x.attrib["ANO-DE-CONCLUSAO"])
#Se terminou o curso
        if x.attrib["ANO-DE-CONCLUSAO"]=="":
            x.attrib["ANO-DE-CONCLUSAO"] = \
                str(int(x.attrib["ANO-DE-INICIO"]) + xpectdyears(gradkind))
                
        if nfirst > int(x.attrib["ANO-DE-CONCLUSAO"]):
            nfirst = int(x.attrib["ANO-DE-CONCLUSAO"]) 

    return [nfirst, nquant]

def xpectdyears(gradtype):
    if gradtype == "GRADUACAO":
        return 4
    elif gradtype == "MESTRADO":
        return 2 
    elif gradtype == "DOUTORADO":
        return 4                   
    elif gradtype == "POS-DOUTORADO":
        return 2
    else:
        print("Invalid input for graduation type in function xpectdyears")
        return 0


def getgraph(filename):

#From input file filename gets all partnerships occurred between the owner of 
#the Lattes CV of the filename file and phd presentations listed on that CV.

    import zipfile
    import xml.etree.ElementTree as ET
    import networkx as nx

#opens zip file downloaded from lattes website
#abre o arquivo zip baixado do site do lattes
    
    archive = zipfile.ZipFile((filename), 'r')
    cvfile = archive.open('curriculo.xml', 'r')

#inicializa o arquivo xpath
#initializes xpath file
    
    tree = ET.parse(cvfile)
    root = tree.getroot()

## get all the authors names cited on lattes cv
#    x = root.findall('.//*[@NOME-COMPLETO-DO-AUTOR]')
#    nameattb = 'NOME-COMPLETO-DO-AUTOR'
## get all the phd commitees found in the lattes cv
    x = root.findall('.//PARTICIPACAO-EM-BANCA-DE-DOUTORADO/*[@NOME-DO-CANDIDATO]')
    nameattb = 'NOME-DO-CANDIDATO'
## get all commitees found in the lattes cv
#   x = root.findall('.//PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO//*[@NOME-DO-CANDIDATO]')
#    nameattb = 'NOME-DO-CANDIDATO'
    y = list(enumerate(x))

#initialize the graph
    cvgraph = nx.Graph()

#get the cv owner name
    cvowner = root[0].attrib['NOME-COMPLETO']
    
#add the node representing the cv owner
    cvgraph.add_node(cvowner)

#for each name found in the cv
    for elem in x:
        dummie = elem.attrib[nameattb]
        if dummie != cvowner:
            if not(dummie in cvgraph.nodes()):
                cvgraph.add_node(dummie)
                cvgraph.add_edge(cvowner, dummie, weight=1)
            else:
                cvgraph[cvowner][dummie]['weight'] += 1
        
    return cvgraph

def topncontributions(xgraph, n):
    
#from a given graph xgraph, gets the n biggest weights and returns
    
    import networkx as nx
    import numpy as np
    topcontribs = []
    
#takes the weights from the graph edges
    
    netweights = list([x[2]['weight'] for x in xgraph.edges(data=True)])
    
#creates a list with the sorted weights
    
    weightlist = list(np.sort(netweights)[::-1])

    for i in range(0,n):
        dummie = [k for k in xgraph.edges(data=True) if
                  k[2]['weight'] == weightlist[i]]
        for z in dummie: topcontribs.append(z)

    for z in topcontribs:
        print(xgraph.node[z[0]]['name'] + ' and ' + xgraph.node[z[1]]['name'] +
              ' have worked together ' + str(z[2]['weight']) + ' times.')
    networklarge = [x for x in xgraph.edges(data=True) if 
                    x[2]['weight'] > weightlist[n]]
    nx.draw(nx.Graph(networklarge), with_labels=True)
    return topcontribs


def getfileslist(folder):
    import os
    import zipfile
    import xml.etree.ElementTree as ET

    fileslist = os.listdir(folder)
    goodlist = badlist = []
    goodlist = [x for x in fileslist if x.endswith('.zip')]
    badlist = [x for x in fileslist if not x.endswith('.zip')]

#test each xml for parsing capabilities
    for filename in goodlist:
        try:
            archive = zipfile.ZipFile((folder + filename), 'r')
            if (archive.namelist()[0][-3:]=='xml')| \
                (archive.namelist()[0][-3:]=='XML'):
                cvfile = archive.open(archive.namelist()[0], 'r')
                ET.parse(cvfile)
            else:
                print('Error: file ' + archive.namelist()[0] + \
                      'is not a xml file.')
        except:
            print('XML parsing error in file ' + filename)
            goodlist.remove(filename)
            badlist.append(filename)
    return [goodlist, badlist]

def getcolab(filename, columns):
    
    import zipfile
    import xml.etree.ElementTree as ET
    import pandas as pd
    
#abre o arquivo zip baixado do site do lattes
    archive = zipfile.ZipFile((filename), 'r')
#cvdata = archive.read('curriculo.xml')
    cvfile = archive.open('curriculo.xml', 'r')

#inicializa o xpath
    tree = ET.parse(cvfile)
    root = tree.getroot()
    
    #cv owner id
    cvid = root.attrib['NUMERO-IDENTIFICADOR']
    
    colabframe = pd.DataFrame(columns=columns)
    
    #list of all works in events
    
    colabtype = 'T'
    
    xworks = root.findall('.//TRABALHO-EM-EVENTOS')
    
    for x in xworks:
        authors = x.findall('AUTORES')
        for y in authors:
            try:
                dummieid = y.attrib['NRO-ID-CNPQ']
            except:
                dummieid = ''
            if (dummieid != '') & (dummieid != cvid):
                cvid2 = y.attrib['NRO-ID-CNPQ']
                year = x[0].attrib['ANO-DO-TRABALHO']
                title = x[0].attrib['TITULO-DO-TRABALHO']
                dummie = pd.DataFrame(data=[[colabtype, cvid, cvid2, year, title]],
                                      columns = columns)
                colabframe = colabframe.append(dummie)
    
    #list of all papers            
    colabtype = 'A'
    
    xpapers = root.findall('.//ARTIGO-PUBLICADO')
    
    for x in xpapers:
        authors = x.findall('AUTORES')
        for y in authors:
            try:
                dummieid = y.attrib['NRO-ID-CNPQ']
            except:
                dummieid = ''
            if (dummieid != '') & (dummieid != cvid):
                cvid2 = y.attrib['NRO-ID-CNPQ']
                year = x[0].attrib['ANO-DO-ARTIGO']
                title = x[0].attrib['TITULO-DO-ARTIGO']
                dummie = pd.DataFrame(data=[[colabtype, cvid, cvid2, year, title]],
                                      columns = columns)
                colabframe = colabframe.append(dummie)
    
    return colabframe

def joingraphs(vecgraph):
    import networkx as nx
    if len(vecgraph) < 2:
        return vecgraph
    elif len(vecgraph) == 2:
        return nx.compose(vecgraph[0],vecgraph[1])
    else:
        dummie = nx.compose(vecgraph[0], vecgraph[1])
        for i in range(2, len(vecgraph)):
            dummie = nx.compose(dummie, vecgraph[i])
        return dummie
