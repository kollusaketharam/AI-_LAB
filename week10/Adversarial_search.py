import matplotlib.pyplot as plt
import networkx as nx

# --- Alpha-Beta Pruning ---
def alpha_beta(node_id, depth, alpha, beta, maximizing_player, tree, G, node_data, pruned_edges):
    node_info = node_data[node_id]

    # Leaf node
    if depth == len(tree) - 1:
        value = tree[depth][node_info['index']]
        G.nodes[node_id]['value'] = value
        return value

    if maximizing_player:
        value = float('-inf')
        for child_id in node_info['children']:
            val = alpha_beta(child_id, depth + 1, alpha, beta, False, tree, G, node_data, pruned_edges)
            value = max(value, val)
            alpha = max(alpha, value)
            G.nodes[node_id]['value'] = value
            if beta <= alpha:
                # prune remaining children
                idx = node_info['children'].index(child_id)
                for pruned in node_info['children'][idx + 1:]:
                    pruned_edges.append((node_id, pruned))
                break
        return value
    else:
        value = float('inf')
        for child_id in node_info['children']:
            val = alpha_beta(child_id, depth + 1, alpha, beta, True, tree, G, node_data, pruned_edges)
            value = min(value, val)
            beta = min(beta, value)
            G.nodes[node_id]['value'] = value
            if beta <= alpha:
                # prune remaining children
                idx = node_info['children'].index(child_id)
                for pruned in node_info['children'][idx + 1:]:
                    pruned_edges.append((node_id, pruned))
                break
        return value


# --- Build user-defined tree ---
def build_tree():
    levels = int(input("Enter number of levels (including leaf level): "))
    tree = []

    for lvl in range(levels):
        if lvl == levels - 1:
            leaf_values = list(map(int, input(f"Enter leaf node values for level {lvl + 1} (space-separated): ").split()))
            tree.append(leaf_values)
        else:
            nodes = int(input(f"Enter number of nodes at level {lvl + 1}: "))
            tree.append([None] * nodes)
    return tree


def create_graph(tree):
    G = nx.DiGraph()
    node_data = {}
    node_id = 0
    prev_level_ids = []

    for lvl, nodes in enumerate(tree):
        current_ids = []
        for i in range(len(nodes)):
            role = "MAX" if lvl % 2 == 0 else "MIN"
            G.add_node(node_id, label=f"{role}\nL{lvl}N{i}", value=None, subset=lvl)
            node_data[node_id] = {"level": lvl, "index": i, "children": []}
            current_ids.append(node_id)
            node_id += 1

        # connect parents to children
        if lvl > 0:
            parent_ids = prev_level_ids
            ratio = len(current_ids) // len(parent_ids)
            for p_idx, pid in enumerate(parent_ids):
                for c in range(ratio):
                    child_id = current_ids[p_idx * ratio + c]
                    G.add_edge(pid, child_id)
                    node_data[pid]['children'].append(child_id)

        prev_level_ids = current_ids

    root_id = 0
    return G, root_id, node_data


# --- Visualization ---
def visualize_tree(G, pruned_edges):
    # Now we can use 'subset' attribute properly
    pos = nx.multipartite_layout(G, subset_key="subset")
    plt.figure(figsize=(10, 6))

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=False)
    nx.draw_networkx_edges(G, pos, edgelist=pruned_edges, edge_color="red", style="dashed", width=2)

    labels = {}
    colors = []
    for node, data in G.nodes(data=True):
        value = data["value"]
        labels[node] = f"{data['label']}\n{value if value is not None else ''}"
        colors.append("lightblue" if value is None else "#90EE90")

    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=1200, edgecolors="black")
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)
    plt.title("Alpha-Beta Pruning Tree\n(Red dashed edges = Pruned branches)")
    plt.axis("off")
    plt.show()


# --- Main ---
def main():
    print("\n--- Alpha-Beta Pruning Tree Builder ---\n")
    tree = build_tree()
    G, root_id, node_data = create_graph(tree)

    pruned_edges = []
    print("\nStarting Alpha-Beta Pruning...\n")

    root_value = alpha_beta(root_id, 0, float('-inf'), float('inf'), True, tree, G, node_data, pruned_edges)
    print(f"\nFinal Value at Root Node (MAX): {root_value}\n")

    visualize_tree(G, pruned_edges)


if __name__ == "__main__":
    main()
