def get_nearest_node(G, lat, lon):
    min_dist = float('inf')
    nearest_node = None
    
    for n, data in G.nodes(data=True):
        node_lat, node_lon = data['pos']
        dist = (lat - node_lat)**2 + (lon - node_lon)**2
        if dist < min_dist:
            min_dist = dist
            nearest_node = n
    
    return nearest_node
