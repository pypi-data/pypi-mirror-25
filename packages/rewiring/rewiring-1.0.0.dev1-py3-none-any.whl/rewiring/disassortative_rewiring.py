 __all__ = ['second_order_assortative_mixing_disassortative_rewiring']



def equal_degree_nodes(G,node):
    degree_dist=sorted(G.degree_iter(),key=itemgetter(1),reverse=True)
    ad=[]
    for x,y in degree_dist:
        if y == G.degree(node):
            ad.append(x)
    return ad


 def node_neighbor_max_degree_xy(G, x='out', y='in', weight=None, nodes=None):
    if nodes is None:
        nodes = set(G)
    else:
        nodes = set(nodes)
    xdeg = G.degree
    ydeg = G.degree
    for start_node_ID in xdeg(nodes):
        neighbors = (nbr for _,nbr in G.edges(start_node_ID) if nbr in nodes)
        
        for end_node_ID in neighbors:
            nbrdeg_start = G.degree(G[start_node_ID])
            nbrdeg_end = G.degree(G[end_node_ID])
            
            nbrdeg_start.pop(end_node_ID)
            nbrdeg_end.pop(start_node_ID)
            
            a = []
            b = []
            for n in nbrdeg_start:                
                a.append(nbrdeg_start[n])
            if a:
                degu = max(a)-1 
            else:
                degu = 1
            for m in nbrdeg_end:
                b.append(nbrdeg_end[m])
            if b:
                degv = max(b)-1
            else:
                degv = 1
            
            yield( start_node_ID,end_node_ID,degu,degv)


def new_maxi_degree(G,start_node_ID,end_node_ID):
    nodes = set(G)

    nbrdeg_start = G.degree(G[start_node_ID])
    nbrdeg_end = G.degree(G[end_node_ID])
            
    nbrdeg_start.pop(end_node_ID)
    nbrdeg_end.pop(start_node_ID)
           
    a = []
    b = []
    for n in nbrdeg_start:                
        a.append(nbrdeg_start[n])
    if a:
        degu = max(a)-1 
    else:
        degu = 1
    for m in nbrdeg_end:
        b.append(nbrdeg_end[m])
    if b:
        degv = max(b)-1
    else:
        degv = 1
            
    return( start_node_ID,end_node_ID,degu,degv)        



def second_order_assortative_mixing_disassortative_rewiring(G,times,difference=0.001,interval=100):

    node_neg_maxi_degree=node_neighbor_max_degree_xy(G)
    a1,b1,x1,y1=zip(*node_neg_maxi_degree)
    second_order_coef = stats.pearsonr(x1,y1)[0]
    
    a1=list(a1)
    b1=list(b1)
    x1=list(x1)
    y1=list(y1)
    
    sec_order_coefficient = []
    count_number = [0]


    for n in range(times*2):
        
        
        a,x = random.choice(G.edges())  #randomly choose an edge from network

        A = random.choice([a,x]) #randomly choose a node from this edge for next step KA = KB

        X = x if A == a else a  #for constant A and X
    
        B ,Y = random.choice(G.edges(equal_degree_nodes(G,A))) # another edge where KA = KB
    
    
        if A == B:
            pass
    
        elif X == Y:
            pass
    
        elif A == Y:
            pass
    
        elif B == X:
            pass
    
        else:
        
            if (G.has_edge(A,Y) == False and G.has_edge(B,X) == False):
            
                count_number[0]=count_number[0]+1
            
                a1=list(a1)
                b1=list(b1)
                x1=list(x1)
                y1=list(y1)
                a2=tuple(a1)
                b2=tuple(b1)
                x2=tuple(x1)
                y2=tuple(y1)
            
            
                second_order_coef_b = stats.pearsonr(x1,y1)[0]
           
            
            
                G.remove_edge(A,X)
                G.remove_edge(B,Y)
                G.add_edge(A,Y)
                G.add_edge(B,X)
                        
        
                for i in range(len(x1)):
                    if a1[i] == A and b1[i]==X:
                        b1[i]=Y
                        a1[i],b1[i],x1[i],y1[i] = new_maxi_degree(G,a1[i],b1[i])
        
                    if a1[i] == B and b1[i]==Y:
                        b1[i]=X
                        a1[i],b1[i],x1[i],y1[i] = new_maxi_degree(G,a1[i],b1[i])
    
                    if a1[i] == X and b1[i]==A:
                        b1[i]=B
                        a1[i],b1[i],x1[i],y1[i] = new_maxi_degree(G,a1[i],b1[i])
        
                    if a1[i] == Y and b1[i]==B:
                        b1[i]=A
                        a1[i],b1[i],x1[i],y1[i] = new_maxi_degree(G,a1[i],b1[i])
                
                    if a1[i] == A or a1[i] == X or a1[i] == B or a1[i] == Y:
                        a1[i],b1[i],x1[i],y1[i] = new_maxi_degree(G,a1[i],b1[i])
                    if b1[i] == A or b1[i] == X or b1[i] == B or b1[i] == Y:
                        a1[i],b1[i],x1[i],y1[i] = new_maxi_degree(G,a1[i],b1[i])

        
                second_order_coef_af = stats.pearsonr(x1,y1)[0]
            
                #("hh")
                if second_order_coef_b <= second_order_coef_af:
                    G.remove_edge(A,Y)
                    G.remove_edge(B,X)
                    G.add_edge(A,X)
                    G.add_edge(B,Y)
                
                    a1,b1,x1,y1=a2,b2,x2,y2
                else:
                    pass

        if count_number[0]!= 0 and count_number[0] in range(0,times,interval):
        
            if second_order_coef_b <= second_order_coef_af:
                sec_order_coefficient.append(second_order_coef_b)
            else:
                sec_order_coefficient.append(second_order_coef_af)
            
    
        if count_number[0] == times:
            return G
        
        if len(sec_order_coefficient) >1 and sec_order_coefficient[-1]- sec_order_coefficient[-1] < difference:
            return G

        




