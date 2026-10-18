import sys
import heapq

def parse_map():
    """Считывает карту из стандартного ввода до команды END"""
    day_cost = 0
    entrance = ""
    profit = {}
    adj = {}
    edge_prob = {}
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if line == "END":
            break
        parts = line.split()
        if parts[0] == "day_cost":
            day_cost = int(parts[1])
        elif parts[0] == "entrance":
            entrance = parts[1]
        elif parts[0] == "vertex":
            v = parts[1]
            profit[v] = int(parts[2])
            if v not in adj:
                adj[v] = []
        elif parts[0] == "edge":
            e_id, u, v, prob = parts[1], parts[2], parts[3], float(parts[4])
            edge_prob[e_id] = prob
            if u not in adj: adj[u] = []
            if v not in adj: adj[v] = []
            adj[u].append((e_id, v))
            adj[v].append((e_id, u))
            
    return day_cost, entrance, profit, adj, edge_prob

def get_other_end(adj, u, e_id):
    """Возвращает смежную вершину для заданного ребра из текущей вершины"""
    for cand_e, cand_v in adj[u]:
        if cand_e == e_id:
            return cand_v
    return None

def solve():
    day_cost, entrance, profit, adj, edge_prob = parse_map()
    
    all_rooms = list(profit.keys())
    visited = set()
    edge_status = {}
    current_room = entrance
    
    while True:
        if current_room not in visited:
            visited.add(current_room)
            
            if len(visited) == len(all_rooms):
                print("END")
                break
                
            print("LOOK")
            for _ in range(len(adj[current_room])):
                line = sys.stdin.readline().strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 4:
                        edge_status[parts[1]] = parts[3]
                
        queue = [(current_room, [])]
        visited_bfs = {current_room}
        path_to_go = None
        
        while queue:
            u, path = queue.pop(0)
            if u not in visited:
                path_to_go = path
                break
            for e_id, v in adj[u]:
                if edge_status.get(e_id) == 'OK' and v not in visited_bfs:
                    visited_bfs.add(v)
                    queue.append((v, path + [e_id]))
                    
        if path_to_go is not None:
            for e_id in path_to_go:
                print(f"MOVE {e_id}")
                sys.stdin.readline()
                current_room = get_other_end(adj, current_room, e_id)
            continue
            
        dist = {u: float('inf') for u in all_rooms}
        first_broken = {u: None for u in all_rooms}
        pq = []
        
        for u in visited:
            dist[u] = 0
            heapq.heappush(pq, (0, u))
            
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
                
            for e_id, v in adj[u]:
                status = edge_status.get(e_id, 'UNKNOWN')
                if status == 'OK':
                    w = 0
                elif status == 'BROKEN':
                    w = day_cost
                else:
                    w = (1.0 - edge_prob[e_id]) * day_cost
                    
                new_d = d + w
                if new_d < dist[v]:
                    dist[v] = new_d
                    fb = first_broken[u]
                    if fb is None and status != 'OK':
                        fb = e_id
                    first_broken[v] = fb
                    heapq.heappush(pq, (new_d, v))
                    
        best_val = 0
        best_edge = None
        
        for u in all_rooms:
            if u not in visited:
                val = profit[u] - dist[u]
                if val > best_val:
                    best_val = val
                    best_edge = first_broken[u]
                    
        if best_edge is not None:
            print(f"CLEAR {best_edge}")
            sys.stdin.readline()
            edge_status[best_edge] = 'OK'
            current_room = entrance
            continue
            
        print("END")
        sys.stdin.readline()
        break

if __name__ == '__main__':
    solve()