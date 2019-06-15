from io import BytesIO
import base64
import matplotlib.pyplot as plt
import networkx as nx
import random
import uuid


def random_2_number_not_repeat(fr, to):  # 隨機兩數字不重複
    if fr == to:
        return fr, to
    i1 = random.randint(fr, to)
    i2 = random.randint(fr, to)
    while i1 == i2:
        i2 = random.randint(fr, to)
    return i1, i2


def calculate_account_relations(accounts, transaction_records):  # 計算每個帳戶與其他帳戶的關係
    account_relations = []

    # 先塞滿
    for a in accounts:
        relation = {}
        for a2 in accounts:
            if a.customer.name != a2.customer.name:  # 跳過自己
                relation[a2.customer.name] = 0

        obj = {}
        obj['name'] = a.customer.name
        obj['relation'] = relation
        account_relations.append(obj)

    # 將transactions分配到account_relations, 雙方的關係金額一樣(所以才有2個迴圈, 要改再改)
    for tr in transaction_records:
        if tr.operation != 3:
            continue

        # 累積from_account與to_account交易關係
        for ar in account_relations:
            if ar['name'] == tr.from_account.customer.name:
                ar['relation'][tr.to_account.customer.name] += int(tr.amount)

        # 累積to_account與from_account交易關係
        for ar in account_relations:
            if ar['name'] == tr.to_account.customer.name:
                ar['relation'][tr.from_account.customer.name] += int(tr.amount)

    return account_relations


def calculate_account_relation(account, transaction_records):
    relation = {}

    for tr in transaction_records:
        if tr.from_account.customer.name == account.customer.name:
            if tr.to_account.customer.name in relation:
                relation[tr.to_account.customer.name] += int(tr.amount)
            else:
                relation[tr.to_account.customer.name] = int(tr.amount)
        elif tr.to_account.customer.name == account.customer.name:
            if tr.from_account.customer.name in relation:
                relation[tr.from_account.customer.name] += int(tr.amount)
            else:
                relation[tr.from_account.customer.name] = int(tr.amount)

    obj = {}
    obj['name'] = account.customer.name
    obj['relation'] = relation
    return obj


def get_transaction_circle_relation_image(accounts, transactions):
    account_relations = calculate_account_relations(accounts, transactions)

    G = nx.Graph()
    # 畫node
    total_amounts = []
    for ar in account_relations:
        G.add_node(ar['name'])
        total_amounts.append(sum([v for k, v in ar['relation'].items()]))

    pos = nx.spring_layout(G)

    max_total_amounts = max(total_amounts)
    min_total_amounts = min(total_amounts)
    delta_total_amounts = max_total_amounts - min_total_amounts

    sizes = []
    for amount in total_amounts:
        my_delta = amount - min_total_amounts
        weight = my_delta * 1.0 / delta_total_amounts  # 0~1
        # 依比例設node_size大小, 最小100, 最大2000
        size = weight * 1900 + 100
        sizes.append(size)

    nx.draw_networkx_nodes(G,
                           pos,
                           node_color='green',
                           node_size=sizes)

    # node上的字
    labels = {}
    for ar in account_relations:
        labels[ar['name']] = ar['name']
    nx.draw_networkx_labels(G,
                            pos,
                            labels,
                            font_size=16)

    # node之間的線
    for i in range(len(account_relations)-1):
        for j in range(i+1, len(account_relations)):
            weight = account_relations[i]['relation'][account_relations[j]['name']]
            if weight != 0:
                G.add_edge(account_relations[i]['name'],
                           account_relations[j]['name'],
                           weight=weight)

    all_weights = []
    for (node1, node2, data) in G.edges(data=True):
        all_weights.append(data['weight'])

    unique_weights = list(set(all_weights))
    max_weight = max(unique_weights)
    min_weight = min(unique_weights)
    delta_weight = max_weight - min_weight

    for weight in unique_weights:
        weighted_edges = [(node1, node2) for (node1, node2, edge_attr) in G.edges(
            data=True) if edge_attr['weight'] == weight]
        my_delta = weight - min_weight
        weight = my_delta * 1.0 / delta_weight  # 0~1
        # 依比例設edge_width寬度, 最小1, 最大10
        width = weight * 9 + 1
        nx.draw_networkx_edges(G, pos, edgelist=weighted_edges, width=width)

    plt.axis('off')
    save_file = BytesIO()
    plt.savefig(save_file, format='png')
    save_file_base64 = base64.b64encode(save_file.getvalue()).decode('utf8')
    plt.clf()
    return save_file_base64


def get_transaction_star_relation_image(account, transaction_records):
    # transaction_records為轉帳以及與account相關的(不用再次塞選)
    account_relation = calculate_account_relation(account, transaction_records)

    G = nx.Graph()

    # 自己的node
    G.add_node(account_relation['name'])

    # 其他人的node
    for k, v in account_relation['relation'].items():
        G.add_node(k)

    pos = nx.spring_layout(G)

    amount_list = [v for k, v in account_relation['relation'].items()]
    max_amount = max(amount_list)
    min_amount = min(amount_list)
    delta_amount = max_amount - min_amount

    node_size_list = [0]
    for k, v in account_relation['relation'].items():
        my_delta = v - min_amount

        # 0~1
        weight = 1.0 * my_delta / delta_amount

        # 依比例設node_size大小, 最小100, 最大2000
        node_size = weight * 1900 + 100
        node_size_list.append(node_size)

    # 畫node & node_size & node_color
    nx.draw_networkx_nodes(G,
                           pos,
                           node_color='green',
                           node_size=node_size_list)
    # 畫node上的標籤
    labels = {account_relation['name']: account_relation['name']}
    for k, v in account_relation['relation'].items():
        labels[k] = k
    nx.draw_networkx_labels(G,
                            pos,
                            labels,
                            font_size=16)

    # 畫node之間的線
    for k, v in account_relation['relation'].items():
        G.add_edge(account_relation['name'],
                   k,
                   weight=v)
    nx.draw_networkx_edges(G, pos, width=1)

    plt.axis('off')
    save_file = BytesIO()
    plt.savefig(save_file, format='png')
    save_file_base64 = base64.b64encode(save_file.getvalue()).decode('utf8')
    plt.clf()
    return save_file_base64
