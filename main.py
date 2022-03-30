def dfs (node, adj, visited, cluster_lst):
    if (not visited[node]):
        visited[node] = 1
        cluster_lst.append(node)
        for child in adj[node]:
            dfs(child, adj, visited, cluster_lst)

def cost_cluster (nodes, bombs, r):
    # TODO: NP-Hard
    deg_positions = []
    deg_explode_area = 0
    deg_num_jammers = 0

    match_positions = []
    match_explode_area = 0
    match_num_jammers = 0
    
    n = len(nodes)
    adj = {}
    deg_visited = {}
    match_visited = {}
    for i in nodes:
        adj[i] = []
        deg_visited[i] = 0
        match_visited[i] = 0
    for i in range(n):
        for j in range(i+1, n):
            dist = pow(pow(bombs[nodes[i]][0] - bombs[nodes[j]][0], 2) + pow(bombs[nodes[i]][1] - bombs[nodes[j]][1], 2), 0.5)
            if (dist <= r):
                adj[nodes[i]].append(nodes[j])
                adj[nodes[j]].append(nodes[i])
    
    # nodes.sort(key = lambda x: len(adj[x]))
    vertices = {}
    for i in nodes:
        vertices[i] = len(adj[i])
    
    while (True):
        cur_ver = max(vertices, key = vertices.get)
        if (vertices[cur_ver] == -1):
            break
        if (not deg_visited[cur_ver]):
            deg_num_jammers += 1
            deg_positions.append([bombs[cur_ver][0], bombs[cur_ver][1]])
            deg_visited[cur_ver] = 1
            vertices[cur_ver] = -1
            for node in adj[cur_ver]:
                vertices[node] = -1
                deg_visited[node] = 1
                for node_k in adj[node]:
                    if (vertices[node_k] > 0):
                        vertices[node_k] -= 1
        else:
            vertices[cur_ver] = -1

    for i in nodes:
        if (not match_visited[i]):
            not_visited = None
            should_include = True
            for j in adj[i]:
                if (match_visited[j]):
                    should_include = False
                    break
                if (not match_visited[j]):
                    not_visited = j
            if (should_include):
                if (not_visited == None):
                    match_num_jammers += 1
                    match_positions.append([bombs[i][0], bombs[i][1]])
                else:
                    match_visited[i] = 1
                    match_visited[not_visited] = 1
                    match_num_jammers += 2
                    match_positions.append([bombs[i][0], bombs[i][1]])
                    match_positions.append([bombs[not_visited][0], bombs[not_visited][1]])
    for i in nodes:
        deg_explode_area += 0.7*3.14*pow(bombs[i][2], 2)
        match_explode_area += 0.7*3.14*pow(bombs[i][2], 2)

    if (deg_num_jammers < match_num_jammers):
        return deg_explode_area, deg_num_jammers, deg_positions
    else:
        return match_explode_area, match_num_jammers, match_positions

def calc_cost (explode_area, num_jammers):
    return (100*pow(num_jammers, 2)) + explode_area

n, k = list(map(int, input().split()))
bombs = []
cur_explode_area = 0

for _ in range(n):
    xi, yi, ri = list(map(int, input().split()))
    bombs.append([xi, yi, ri])
    cur_explode_area += 0.7*3.14*pow(ri, 2)

bombs.sort(key = lambda x: x[2], reverse = True)

# adj_forward = {}
adj_backward = {}
for i in range(n):
    # adj_forward[i] = []
    adj_backward[i] = []

for i in range(n):
    for j in range(i+1, n):
        dist = pow(pow(bombs[i][0] - bombs[j][0], 2) + pow(bombs[i][1] - bombs[j][1], 2), 0.5)
        if (bombs[i][2] >= dist):
            # adj_forward[i].append(j)
            adj_backward[j].append(i)
        if (bombs[j][2] >= dist):
            # adj_forward[j].append(i)
            adj_backward[i].append(j)

cur_num_jammers = 0
cur_cost = calc_cost(cur_explode_area, cur_num_jammers)
visited = [0 for i in range(n)]
jammer_positions = []

save_bomb = 0
while (save_bomb < n):
    if (visited[save_bomb]):
        save_bomb += 1
    else:
        save_cluster = [] 
        dfs(save_bomb, adj_backward, visited, save_cluster)
        explode_area, num_jammers, positions = cost_cluster(save_cluster, bombs, k)
        temp_cost = calc_cost(cur_explode_area - explode_area, cur_num_jammers + num_jammers)
        if (temp_cost <= cur_cost):
            cur_explode_area -= explode_area
            cur_num_jammers += num_jammers
            cur_cost = temp_cost
            jammer_positions += positions
        else:
            for node in save_cluster:
                visited[node] = 0
        save_bomb += 1

print(cur_num_jammers)
for position in jammer_positions:
    print(position[0], position[1])
