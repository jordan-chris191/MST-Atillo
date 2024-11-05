import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Visualization with MST Algorithms")
        self.graph = nx.Graph()
        self.mst_edges = []
        self.mst_nodes = set()

        # Main Frame for left-side controls and right-side graph
        main_frame = tk.Frame(master)
        main_frame.pack(fill="both", expand=True)

        # Left Frame for controls
        self.controls_frame = tk.Frame(main_frame)
        self.controls_frame.pack(side="left", padx=10, pady=10, fill="y")

        # Right Frame for the graph visualization
        self.graph_frame = tk.Frame(main_frame)
        self.graph_frame.pack(side="right", expand=True, fill="both")

        # Create a Matplotlib figure for graph visualization
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.algorithm_status_text = self.fig.text(0.5, 0.95, "No algorithm run yet.", ha='center', fontsize=12, color='black')

        # Embed Matplotlib figure into Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

        # Node Input
        self.node_frame = ttk.LabelFrame(self.controls_frame, text="Node Input", padding=(10, 10))
        self.node_frame.pack(fill="x", pady=(0, 10))

        self.node_label = ttk.Label(self.node_frame, text="Node ID:")
        self.node_label.pack(side="left", padx=(0, 5))

        self.node_entry = ttk.Entry(self.node_frame)
        self.node_entry.pack(side="left", fill="x", expand=True)

        self.add_node_button = ttk.Button(self.node_frame, text="Add Node", command=self.add_node)
        self.add_node_button.pack(side="left", padx=(5, 0))

        # Edge Input
        self.edge_frame = ttk.LabelFrame(self.controls_frame, text="Edge Input", padding=(10, 10))
        self.edge_frame.pack(fill="x", pady=(0, 10))

        self.source_label = ttk.Label(self.edge_frame, text="Source Node:")
        self.source_label.pack(fill="x")

        self.source_entry = ttk.Entry(self.edge_frame)
        self.source_entry.pack(fill="x", padx=(0, 5))

        self.target_label = ttk.Label(self.edge_frame, text="Target Node:")
        self.target_label.pack(fill="x")

        self.target_entry = ttk.Entry(self.edge_frame)
        self.target_entry.pack(fill="x", padx=(0, 5))

        self.weight_label = ttk.Label(self.edge_frame, text="Edge Cost:")
        self.weight_label.pack(fill="x")

        self.weight_entry = ttk.Entry(self.edge_frame)
        self.weight_entry.pack(fill="x", padx=(0, 5))

        self.add_edge_button = ttk.Button(self.edge_frame, text="Add Edge", command=self.add_edge)
        self.add_edge_button.pack(pady=(5, 0))

        # Minimum Spanning Tree Algorithms
        self.algorithm_frame = ttk.LabelFrame(self.controls_frame, text="MST Greedy Algorithms", padding=(10, 10))
        self.algorithm_frame.pack(fill="x", pady=(0, 10))

        self.run_kruskal_button = ttk.Button(self.algorithm_frame, text="Run Kruskal's Algorithm", command=self.run_kruskal)
        self.run_kruskal_button.pack(pady=(5, 0))

        self.run_prim_button = ttk.Button(self.algorithm_frame, text="Run Prim's Algorithm", command=self.run_prim)
        self.run_prim_button.pack(pady=(5, 0))

        self.run_boruvka_button = ttk.Button(self.algorithm_frame, text="Run Borůvka's Algorithm", command=self.run_boruvka)
        self.run_boruvka_button.pack(pady=(5, 0))

        # Clear Graph
        self.clear_button = ttk.Button(self.controls_frame, text="Clear Graph", command=self.clear_graph)
        self.clear_button.pack(pady=(10, 0))

        # Initial graph visualization
        self.visualize_graph()

    def add_node(self):
        node_id = self.node_entry.get()
        if node_id:
            if node_id not in self.graph.nodes:
                self.graph.add_node(node_id)
                self.visualize_graph()
            else:
                messagebox.showwarning("Warning", f"Node '{node_id}' already exists.")
            self.node_entry.delete(0, tk.END)

    def add_edge(self):
        source = self.source_entry.get()
        target = self.target_entry.get()
        weight = self.weight_entry.get()

        if source and target and weight:
            try:
                weight = float(weight)
                if source in self.graph.nodes and target in self.graph.nodes:
                    self.graph.add_edge(source, target, weight=weight)
                    self.visualize_graph()
                else:
                    messagebox.showwarning("Warning", "Both nodes must exist.")
            except ValueError:
                messagebox.showerror("Error", "Weight must be a number.")
            self.source_entry.delete(0, tk.END)
            self.target_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)

    def run_kruskal(self):
        self.reset_graph_colors()
        if not self.graph.edges:
            messagebox.showwarning("Warning", "No edges in the graph.")
            return
        mst_edges = list(nx.minimum_spanning_edges(self.graph, algorithm='kruskal', data=True))
        self.animate_mst(mst_edges, "Kruskal's Algorithm")

    def run_prim(self):
        self.reset_graph_colors()
        if not self.graph.edges:
            messagebox.showwarning("Warning", "No edges in the graph.")
            return
        mst_edges = list(nx.minimum_spanning_edges(self.graph, algorithm='prim', data=True))
        self.animate_mst(mst_edges, "Prim's Algorithm")

    def run_boruvka(self):
        self.reset_graph_colors()
        if not self.graph.edges:
            messagebox.showwarning("Warning", "No edges in the graph.")
            return
        # Borůvka's algorithm implementation
        mst_edges = list(nx.minimum_spanning_edges(self.graph, algorithm='boruvka', data=True))
        self.animate_mst(mst_edges, "Borůvka's Algorithm")

    def reset_graph_colors(self):
        """Reset the MST edges and nodes to their original colors."""
        self.mst_edges.clear()
        self.mst_nodes.clear()

    def animate_mst(self, mst_edges, algorithm_name):
        self.algorithm_status_text.set_text(f"{algorithm_name}")
        total_cost = 0

        def animate_step(index):
            if index < len(mst_edges):
                u, v, d = mst_edges[index]
                self.mst_edges.append((u, v))
                self.mst_nodes.update([u, v])
                total_cost = sum(d['weight'] for _, _, d in mst_edges[:index + 1])
                self.visualize_graph(total_cost)
                self.master.after(1000, lambda: animate_step(index + 1))
            else:
                self.algorithm_status_text.set_text(f"{algorithm_name} Completed")

        animate_step(0)

    def visualize_graph(self, total_cost=None):
        self.ax.clear()
        pos = nx.spring_layout(self.graph, seed=42)

        # Draw nodes
        node_colors = ['lightgreen' if node in self.mst_nodes else 'lightblue' for node in self.graph.nodes]
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, ax=self.ax, node_size=700)

        # Draw edges
        edges = self.graph.edges()
        edge_colors = ['lightgreen' if (u, v) in self.mst_edges or (v, u) in self.mst_edges else 'black' for u, v in edges]
        nx.draw_networkx_edges(self.graph, pos, edge_color=edge_colors, ax=self.ax, width=2)

        # Draw edge labels
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=self.ax, font_color='black')

        # Total cost display
        if total_cost is not None:
            self.ax.text(0.5, 1.05, f"Total Cost of MST: {total_cost}", fontsize=12, ha='center', transform=self.ax.transAxes)

        # Draw node labels
        nx.draw_networkx_labels(self.graph, pos, ax=self.ax, font_size=10, font_color='black')
        self.ax.set_title("Graph Visualization")
        self.canvas.draw()

    def clear_graph(self):
        self.graph.clear()
        self.reset_graph_colors()
        messagebox.showinfo("Graph Cleared", "The graph has been cleared.")
        self.visualize_graph()

def main():
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()