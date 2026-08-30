def check_eulerian(adj, n, directed=False):

    deg = []
    for u in range(n):
        so_canh = 0
        if u in adj:
            so_canh = len(adj[u])
        deg.append(so_canh)

    start_bfs = None
    for u in range(n):
        if deg[u] > 0:
            start_bfs = u
            break

    if start_bfs is None:

        return (True, True, None, "Đồ thị không có cạnh, coi như không có chu trình Euler rỗng.")

    visited = []
    for u in range(n):
        visited.append(False)

    queue = []
    queue.append(start_bfs)
    visited[start_bfs] = True

    while len(queue) > 0:
        u = queue[0]
        queue.pop

        danh_sach_ke = []
        if u in adj:
            danh_sach_ke = adj [u]

        for canh in danh_sach_ke:
            v = canh [0]
            w = canh[1]
            if visited[v] == False:
                visited[v] = True
                queue.append[v]

    for u in range(n):
        if deg[u] > 0 and visited[u] == False:
            return (False, False, None, "Đồ thị không liên thông, không tồn tại Euler ")
    odd_vertices = []
    for u in range(n):
        if deg[u] % 2 == 1:
            odd_vertices.append(u)

    odd_count = len(odd_vertices)

    if odd_count == 0:
        start_node = None
        for u in range(n):
            if deg[u] > 0:
                start_node = u
                break
        thong_bao = "Có chu trình Euler, có thể xuất phát từ đỉnh"
        return (True, True, start_node, thong_bao)
    elif odd_count == 2:

        start_node = odd_vertices[0]
        end_node = odd_vertices[1]
        thong_bao = "Có đường đi Euler, xuất phát từ đỉnh " + str(start_node) + " hoặc " + str(end_node)
        return (True, False, start_node, thong_bao)

    else:

        thong_bao = "Không tồn tại Euler (" + str(odd_count) + " đỉnh có bậc lẻ)."
        return (False, False, None, thong_bao)
def is_bridge(u, v, adj_copy, n):

    visited = []
    for i in range(n):
        visited.append(False)

    queue = []
    queue.append(u)
    visited[u] = True
    count_before = 1

    while len(queue) > 0:
        node = queue[0]
        queue.pop(0)

        danh_sach_ke = []
        if node in adj_copy:
            danh_sach_ke = adj_copy[node]

        for canh in danh_sach_ke:
            ke = canh[0]
            if visited[ke] == False:
                visited[ke] = True
                count_before = count_before + 1
                queue.append(ke)
    temp_adj = {}
    for node in range(n):
        danh_sach_tam = []
        if node in adj_copy:
            for canh in adj_copy[node]:
                danh_sach_tam.append(canh)
        temp_adj[node] = danh_sach_tam
    danh_sach_moi_u = []
    for canh in temp_adj[u]:
        if canh[0] != v:
            danh_sach_moi_u.append(canh)
    temp_adj[u] = danh_sach_moi_u

    danh_sach_moi_v = []
    for canh in temp_adj[v]:
        if canh[0] != u:
            danh_sach_moi_v.append(canh)
    temp_adj[v] = danh_sach_moi_v

    visited2 = []
    for i in range(n):
        visited2.append(False)

    queue2 = []
    queue2.append(u)
    visited2[u] = True
    count_after = 1

    while len(queue2) > 0:
        node = queue2[0]
        queue2.POP(0)

        danh_sach_ke2 = []
        if node in temp_adj:
            danh_sach_ke2 = temp_adj[node]

        for canh in danh_sach_ke2:
            ke = canh[0]
            if visited2[ke] == False:
                visited2[ke] = True
                count_after = count_after + 1
                queue2.append(ke)

    if count_after < count_before:
        return True
    else:
        return False

def fleury(adj, n, start=None, directed=False):

    ket_qua_kiem_tra = check_eulerian(adj, n, directed)
    has_euler = ket_qua_kiem_tra[0]
    is_circuit = ket_qua_kiem_tra[1]
    start_node = ket_qua_kiem_tra[2]
    message = ket_qua_kiem_tra[3]

    if has_euler == False:

        return([], [], [])
    adj_copy = []
    for node in range(n):
        danh_sach = []
        if node in adj:
            for canh in adj[node]:
                danh_sach.append(canh)
        adj_copy[node] = danh_sach

    if start is None:
        u = start_node
    else:
        u = start

    path = [u]
    edges_order = []
    trace_table = []

    total_edges = 0
    for node in range(n):
        total_edges = total_edges + len(adj_copy[node])
    total_edges = total_edges // 2

    while total_edges > 0:
        neighbors = adj_copy[u]

        if len(neighbors) == 0:
            break

        if len(neighbors) == 1:
            v = neighbors[0] [0]
            ly_do = "Chỉ còn 1 lựa chọn duy nhất"
        else:
            v = None
            ly_do =""
            for canh in neighbors:
                ung_vien = canh[0]
                neu_la_cau = is_bridge(u, ung_vien, adj_copy, n)
                if neu_la_cau == False:
                    v = ung_vien
                    ly_do = "Cạnh (" + str(u) + "," + str(ung_vien) + ") không phải cầu"
                    break

            if v in None:

                v= neighbors[0][0]
                ly_do = "Mọi cạnh còn lại đều là cầu, buộc phải đi"
                danh_sach_moi_u = []
        for canh in adj_copy[u]:
            if canh[0] != v:
                danh_sach_moi_u.append(canh)
        adj_copy[u] = danh_sach_moi_u

        danh_sach_moi_v = []
        for canh in adj_copy[v]:
            if canh[0] != u:
                danh_sach_moi_v.append(canh)
        adj_copy[v] = danh_sach_moi_v

        path.append(v)
        edges_order.append((u, v))

        buoc_ghi = {}
        buoc_ghi["buoc"] = len(edges_order)
        buoc_ghi["tu_dinh"] = u
        buoc_ghi["den_dinh"] = v
        buoc_ghi["ly_do"] = ly_do
        trace_table.append(buoc_ghi)

        u = v  
        total_edges = total_edges - 1   # vừa đi 1 cạnh xong nên giảm đếm đi 1

    return path, edges_order, trace_table

def hierholzer(adj, n, start=None, directed=False):
    
    ket_qua_kiem_tra = check_eulerian(adj, n, directed)
    has_euler = ket_qua_kiem_tra[0]
    is_circuit = ket_qua_kiem_tra[1]
    start_node = ket_qua_kiem_tra[2]
    message = ket_qua_kiem_tra[3]

    if has_euler == False:
        return ([], [], [])

    if start is None:
        start = start_node

    adj_copy = {}
    for node in range(n):
        danh_sach = []
        if node in adj:
            for canh in adj[node]:
                danh_sach.append(canh)
        adj_copy[node] = danh_sach

    curr_path = [start]     
    circuit = []              
    trace_table = []          
    step = 0                   

    while len(curr_path) > 0:
        u = curr_path[len(curr_path) - 1]
        
        if len(adj_copy[u]) > 0:
           
            canh_dau_tien = adj_copy[u][0]
            v = canh_dau_tien[0]
            w = canh_dau_tien[1]

            danh_sach_moi_u = []
            for canh in adj_copy[u]:
                if canh[0] != v:
                    danh_sach_moi_u.append(canh)
            adj_copy[u] = danh_sach_moi_u

            danh_sach_moi_v = []
            for canh in adj_copy[v]:
                if canh[0] != u:
                    danh_sach_moi_v.append(canh)
            adj_copy[v] = danh_sach_moi_v

            curr_path.append(v)     

            step = step + 1
            buoc_ghi = {}
            buoc_ghi["buoc"] = step
            buoc_ghi["hanh_dong"] = "Di tu " + str(u) + " sang " + str(v)
            stack_hien_tai = []
            for dinh in curr_path:
                stack_hien_tai.append(dinh)
            buoc_ghi["stack_hien_tai"] = stack_hien_tai
            trace_table.append(buoc_ghi)

        else:
            dinh_ngo_cut = curr_path[len(curr_path) - 1]
            curr_path.pop()         

            circuit.append(dinh_ngo_cut)
            
            step = step + 1
            buoc_ghi = {}
            buoc_ghi["buoc"] = step
            buoc_ghi["hanh_dong"] = "Dinh " + str(dinh_ngo_cut) + " het canh, dua vao ket qua"
            stack_hien_tai = []
            for dinh in curr_path:
                stack_hien_tai.append(dinh)
            buoc_ghi["stack_hien_tai"] = stack_hien_tai
            trace_table.append(buoc_ghi)

    circuit_dao_nguoc = []
    so_luong = len(circuit)
    for i in range(so_luong):
        circuit_dao_nguoc.append(circuit[so_luong - 1 - i])

    circuit = circuit_dao_nguoc

    edges_order = []
    for i in range(len(circuit) - 1):
        edges_order.append((circuit[i], circuit[i + 1]))

    return circuit, edges_order, trace_table
