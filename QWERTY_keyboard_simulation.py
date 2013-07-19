#QWERTY_keyboard_simulation.py
#fingerkeying - an implementation of QWERTY Keyboard
#Author Ekta Grover ekta1007@gmail.com (19th July, 2013)

from itertools import chain #for flattening the list of lists, used for debugging
from random import random
import matplotlib.pyplot as plt
import networkx as nx

G=nx.Graph()
# Keying in the structure of the QWERTY keyboard
row1=['q','w','e','r','t','y','u','i','o','p']
row2=['a','s','d','f','g','h','j','k','l']
row3=['z','x','c','v','b','n','m']

# add each rows independetly with the corresponding weights - we will use only weight of 1 , so we connect only adjacent nodes
for i in range(0,len(row1)-1):
    G.add_edge(row1[i],row1[i+1],weight=1,color='red')
  
for i in range(0,len(row2)-1):
    G.add_edge(row2[i],row2[i+1],weight=1,color='blue')
    
for i in range(0,len(row3)-1):
    G.add_edge(row3[i],row3[i+1],weight=1,color='green')

# add the next row in there - row1 with row2
for i in range(0, len(row1)):
    if i==0:
        G.add_edge(row1[i],row2[i],weight=1,color='cyan')
        G.add_edge(row1[i],row2[i+1],weight=1,color='cyan')
    elif i<= 7 :
        G.add_edge(row1[i],row2[i-1],weight=1,color='cyan')
        G.add_edge(row1[i],row2[i],weight=1,color='cyan')
        G.add_edge(row1[i],row2[i+1],weight=1,color='cyan')
    elif i==8:
        G.add_edge(row1[i],row2[i-1],weight=1,color='cyan')
        G.add_edge(row1[i],row2[i],weight=1,color='cyan')
    elif i==9:
        G.add_edge(row1[i],row2[i-1],weight=1,color='cyan')

# add the next row in there -- row2 with row3
for i in range(0, len(row2)):
    if i==0:
        G.add_edge(row2[i],row3[i],weight=1,color='black')
        G.add_edge(row2[i],row3[i+1],weight=1,color='black')
    elif i<= 5 :
        G.add_edge(row2[i],row3[i-1],weight=1,color='black')
        G.add_edge(row2[i],row3[i],weight=1,color='black')
        G.add_edge(row2[i],row3[i+1],weight=1,color='black')
    elif i==6:
        G.add_edge(row2[i],row3[i-1],weight=1,color='black')
        G.add_edge(row2[i],row3[i],weight=1,color='black')
    elif i==7:
        G.add_edge(row2[i],row3[i-2],weight=1,color='black')
        G.add_edge(row2[i],row3[i-1],weight=1,color='black')
    elif i==8:
        G.add_edge(row2[i],row3[i-2],weight=1,color='black')

# added all unidirected graphs with weights   

"""
#Good to see & possibly debug the structure of the graph as follows -
G.number_of_nodes()
G.number_of_edges()
list_of_all_nodes=[row1,row2,row3]
#flatten all_nodes as a single list - of which we can find the length, and see all edges together
list_of_all_nodes=list(chain.from_iterable(all_nodes))
"""

edgelist1=[(u,v) for (u,v,y) in G.edges(data=True) if y['color']=='red']
edgelist2=[(u,v) for (u,v,y) in G.edges(data=True) if y['color']=='blue']
edgelist3=[(u,v) for (u,v,y) in G.edges(data=True) if y['color']=='green']
edgelist4=[(u,v) for (u,v,y) in G.edges(data=True) if y['color']=='black']
edgelist5=[(u,v) for (u,v,y) in G.edges(data=True) if y['color']=='cyan']

pos=nx.spring_layout(G)
#color coding the rows of the keyboard differently, and picking up the labels of the nodes
nx.draw_networkx_nodes(G,pos,nodelist=row1,node_color='red',node_size=400)
nx.draw_networkx_nodes(G,pos,nodelist=row2,node_color='blue',node_size=400)
nx.draw_networkx_nodes(G,pos,nodelist=row3,node_color='green',node_size=400)

nx.draw_networkx_edges(G,pos,edgelist1,width=4,edge_color='red')
nx.draw_networkx_edges(G,pos,edgelist2,width=4,edge_color='blue')
nx.draw_networkx_edges(G,pos,edgelist3,width=4,edge_color='green')
nx.draw_networkx_edges(G,pos,edgelist4,width=3,edge_color='black')
nx.draw_networkx_edges(G,pos,edgelist5,width=3,edge_color='cyan')

# labels
nx.draw_networkx_labels(G,pos,font_size=15,font_family='calibri',node_color='yellow')

plt.axis('off')
plt.savefig("finger_keying.png")
plt.show() # display


"""
Base assumptions for the algorithm 
<convert the words to lower case, as is the standard practice - can also convert it to upper case>
1. Two words have more probabilty to be similar if the difference of their lengths does not exceed a threshold - we take this threshold as 1/3rd of the minimum of the two words keyed in
2. Will use the LevenshteinDistance if the differnce in lenghts exceeds a threshold - meaning it must not be a typo, and we must find the regular distance metric
"""

def LevenshteinDistance(s, t):
    len_s=len(s)
    len_t=len(t)
    if len_s == 0:
        return len_t
    if len_t == 0:
        return len_s
    if s[len_s-1] == t[len_t-1] :
        cost = 0
    else : 
        cost =1 
    return min(LevenshteinDistance(s[0:len_s-1], t) + 1,LevenshteinDistance(s, t[0:len_t-1]) + 1,LevenshteinDistance(s[0:len_s-1], t[0:len_t-1]) + cost)

connected_node_list=G.edges()
def Qwerty_dist(word1,word2):
    #changing to lower case so that the comparision is regularized
    word1=word1.lower()
    word2=word2.lower()
    dist=0
    threshold=(min(len(word1),len(word2)))/3
    if abs(len(word1)-len(word2)<threshold):
        for i in range(0,min(len(word1),len(word2))):
            if word1[i]==word2[i]:
                pass
            elif ((word1[i],word2[i]) or (word2[i],word1[i])) in connected_node_list :
                #meaning the intention of the user must have been same and it's indeed a typo
                pass
                #word2[i]==word1[i]
            elif ((word1[i],word2[i]) or (word2[i],word1[i])) not in connected_node_list :
            #looks like the characters in the words just got reversed !
                if i<=min(len(word1),len(word2))-2 :
                    if word1[i]==word2[i+1] and word1[i+1]==word2[i]:
                        pass
                else: 
                    dist=dist+1
    #if the differnce in lengths exceeds then call the regular levenshein distance
    else :
        dist=LevenshteinDistance(word1,word2)
    if dist ==0:
        print "The words are identical"
    else :
        print "The distance between %s and %s is %d" %(word1,word2,dist)

# seeing sample runs 
Qwerty_dist('ekta','keta')
Qwerty_dist('ekta','seta')
Qwerty_dist('ekta','setam')
Qwerty_dist('ekta grover','sdfg')
