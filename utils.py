import copy
import networkx as nx




def argmax(d):
    # d is dict
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


def get_dt(G, source=0):
    i = 0
    dt = {}
    for start, end in list(nx.algorithms.edge_dfs(G, source=source)):
        if start not in dt:
            dt[start] = i
            i += 1
        if end not in dt:
            dt[end] = i
            i += 1
    return dt



def get_minus_di(i, G):
    G_without_i = copy.deepcopy(G)
    G_without_i.remove_node(i)
    left_nodes_after_removing_i = nx.dfs_tree(G_without_i, source=0).nodes
    minus_di = left_nodes_after_removing_i
    return minus_di



def get_minus_di_and_Ti(i, G):
    G_without_i = copy.deepcopy(G)
    G_without_i.remove_node(i)
    left_nodes_after_removing_i = nx.dfs_tree(G_without_i, source=0).nodes
    minus_di = left_nodes_after_removing_i
    new_G = copy.deepcopy(G)
    new_G.remove_nodes_from(left_nodes_after_removing_i)
    Ti = nx.dfs_tree(new_G, source=i)
    return minus_di, Ti


def get_di(G, minus_di):
    return [n for n in G.nodes if n not in minus_di]


def show_di_and_Ti(i, G):
    minus_di, Ti = get_minus_di_and_Ti(i, G)
    di = [i for i in G.nodes if i not in minus_di]
    print("di: ", di)
    print("minus_di: ", minus_di)
    nx.draw(Ti, with_labels=True, font_weight='bold')
    plt.show()


def get_Ti(i, dfs_tree):
    return nx.dfs_tree(dfs_tree, source=i)


def get_full_dfs_tree(G, source=0):
    full_dfs_tree = nx.DiGraph()
    full_dfs_tree.add_nodes_from(G.nodes)
    dfs_edges = list(nx.algorithms.edge_dfs(G, source=source))
    print(dfs_edges)
    full_dfs_tree.add_edges_from(dfs_edges)
    full_dfs_tree.source = source
    print(full_dfs_tree.source)
    return full_dfs_tree







def get_parent(i, dfs_tree):
    return [edge[0] for edge in dfs_tree.in_edges(i)]

def get_child(i, dfs_tree):
    return [edge[1] for edge in dfs_tree.out_edges(i)]

def get_ancestors(i, dfs_tree):
    return nx.ancestors(dfs_tree, i)

def get_descendants(i, dfs_tree):
    return nx.descendants(dfs_tree, i)

def get_dti(dt, Ti):
    new_dt = dict((node, dt[node]) for node in Ti.nodes)
    return min(new_dt.values())

def get_dtTi(dt, Ti):
    new_dt = dict((node, dt[node]) for node in Ti.nodes)
    return max(new_dt.values())


def get_w(valuations):
    valuations_for_w = {i: valuations[i]['valuation'] for i in valuations}
    return argmax(valuations_for_w)
   

def get_C(G, w):
    C = [0, w]
    for i in G.nodes:
        if i not in [0, w]:
            minus_di = get_minus_di(i, G)
            if w in get_di(G, minus_di):
                C.append(i) 
    return C


def analysis(G, C, w):
    count = 0
    index = 0
    new_C = copy.deepcopy(C)
    while new_C:
        cur = new_C[index]
        n = G.neighbors(cur)
        succ = (n and w)
        if not succ:
            index += 1
            continue
        new = new_C.pop(index)
        if new == w:
            break
        index = 0
        count += 1
    
    return count

def get_max_val_from_nodes(G, nodes):
    valuations = dict(G.nodes(data='valuation'))
    vals = {i: valuations[i] for i in nodes}
    return max(vals.values())


def get_payments(G, C, w):
    # G: graph
    # C: critical nodes (list of ints)
    # w: winner (int)
    p = {}
    dt = get_dt(G)
    order = sorted([i for i in dt if i in C], key=lambda x: dt[x])

    for i in range(len(order) - 1):

        to = order[i]
        frm = order[i+1]
        nodes_left = get_minus_di(frm, G)
        p[(frm, to)] = get_max_val_from_nodes(G, nodes_left)

    return p


def get_allocation(G, C, p):
    a = {}
    dt = get_dt(G)
    valuations = dict(G.nodes(data='valuation'))
    order = sorted([i for i in dt if i in C], key=lambda x: dt[x])
    
    for i in range(len(order)):

        to = order[i]
        try:
            frm = order[i+1]
        except:
            a[to] = 1
            return a
        
        if p[(frm, to)] == valuations[to]:
            a[to] = 1
            return a
        else:
            a[to] = 0   
    return a



def get_final_payments(G, C, a, p):
    final_p = {}
    dt = get_dt(G)
    order = sorted([i for i in dt if i in C], key=lambda x: dt[x])
    for i in range(len(order)-1):
        to = order[i]
        frm = order[i+1]
        if a[to] == 1:
            break
        final_p[(frm, to)] = p[(frm, to)]
        
    return final_p

# def get_C(G, valuations):
#     C = [0]
#     w = get_w(valuations)
#     dt = get_dt(G, source=0)
#     for i in G.nodes:
#         if i not in C:
#             _, Ti = get_minus_di_and_Ti(i, G)
#             if w in Ti.successors(i):
#                 C.append(i)
#             dti = get_dti(dt, Ti)
#             dtTi = get_dtTi(dt, Ti)
#             if dt[w] >= dti and dt[w] <= dtTi:
#                 print('dti: ', dti)
#                 print('dt[w]: ', dt[w])
#                 print('dtTi: ', dtTi)
#                 C.append(i)
#                 print(i)
#     return C
# 
# 
# def get_Di(dfs_tree):
#     pass
# def get_eti(i, dt, dfs_tree, full_dfs_tree):
#     descendants = get_descendants(i, dfs_tree)
#     all_reachable = get_descendants(i, full_dfs_tree)
#     back_nodes = list(filter(lambda x: x not in descendants, all_reachable))
#     return min([dt[i] for i in back_nodes])
# 

