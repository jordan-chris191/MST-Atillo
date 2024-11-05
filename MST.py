import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
import time

class GraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Visualization with MST Algorithms")
        self.graph = nx.Graph()
        self.mst_edges = []  # Store MST edges for visualization
        self.mst_nodes = set()  # Store MST nodes for visualization
        
        # Create a Matplotlib figure for graph visualization
        self.fig, self.ax = plt.subplots(figsize=(8, 6))

        # Node Input
        self.node_label = tk.Label(master, text="Node ID:")
        self.node_label.pack()
        self.node_entry = tk.Entry(master)
        self.node_entry.pack()
        self.add_node_button = tk.Button(master, text="Add Node", command=self.add_node)
        self.add_node_button.pack()

        # Edge Input
        self.source_label = tk.Label(master, text="Source Node:")
        self.source_label.pack()
        self.source_entry = tk.Entry(master)
        self.source_entry.pack()

        self.target_label = tk.Label(master, text="Target Node:")
        self.target_label.pack()
        self.target_entry = tk.Entry(master)
        self.target_entry.pack()

        self.weight_label = tk.Label(master, text="Edge Weight:")
        self.weight_label.pack()
        self.weight_entry = tk.Entry(master)
        self.weight_entry.pack()

        self.add_edge_button = tk.Button(master, text="Add Edge", command=self.add_edge)
        self.add_edge_button.pack()

        # Minimum Spanning Tree Algorithms
        self.run_kruskal_button = tk.Button(master, text="Run Kruskal's Algorithm", command=self.run_kruskal)
        self.run_kruskal_button.pack()

        self.run_prim_button = tk.Button(master, text="Run Prim's Algorithm", command=self.run_prim)
        self.run_prim_button.pack()

        self.run_boruvka_button = tk.Button(master, text="Run Borůvka's Algorithm", command=self.run_boruvka)
        self.run_boruvka_button.pack()

        # Clear Graph
        self.clear_button = tk.Button(master, text="Clear Graph", command=self.clear_graph)
        self.clear_button.pack()

        # Initial graph visualization
        self.visualize_graph()

    def add_node(self):
        node_id = self.node_entry.get()
        if node_id:
            if node_id not in self.graph.nodes:
                self.graph.add_node(node_id)
                self.visualize_graph()  # Update visualization
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
                    messagebox.showinfo("Success", f"Edge '{source} - {target}' with weight {weight} added.")
                    self.visualize_graph()  # Update visualization
                else:
                    messagebox.showwarning("Warning", "Both nodes must exist.")
            except ValueError:
                messagebox.showerror("Error", "Weight must be a number.")
            self.source_entry.delete(0, tk.END)
            self.target_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)

    def run_kruskal(self):
        if not self.graph.edges:
            messagebox.showwarning("Warning", "No edges in the graph.")
            return
        
        mst_edges = list(nx.minimum_spanning_edges(self.graph, algorithm='kruskal', data=True))
        self.animate_mst(mst_edges, "Kruskal's Algorithm")

    def run_prim(self):
        if not self.graph.edges:
            messagebox.showwarning("Warning", "No edges in the graph.")
            return
        
        mst_edges = list(nx.minimum_spanning_edges(self.graph, algorithm='prim', data=True))
        self.animate_mst(mst_edges, "Prim's Algorithm")

    def run_boruvka(self):
        if not self.graph.edges:
            messagebox.showwarning("Warning", "No edges in the graph.")
            return
        
        mst_edges = list(nx.minimum_spanning_edges(self.graph, algorithm='boruvka', data=True))
        self.animate_mst(mst_edges, "Borůvka's Algorithm")

    def animate_mst(self, mst_edges, algorithm_name):
        self.ax.clear()  # Clear the previous graph
        self.visualize_graph()  # Show the original graph
        plt.title(f"Animating {algorithm_name} - Step by Step")
        plt.draw()  # Draw the updated graph

        self.mst_edges = []  # Reset MST edges for animation
        self.mst_nodes = set()  # Reset MST nodes for animation
        for u, v, d in mst_edges:
            self.mst_edges.append((u, v))  # Store MST edges
            self.mst_nodes.update([u, v])  # Store MST nodes
            self.graph.add_edge(u, v, weight=d['weight'])  # Add edge to the MST
            self.visualize_graph()  # Update the visualization
            time.sleep(1)  # Pause for animation effect

        # Display the final MST
        self.visualize_graph()  # Final visualization

    def visualize_graph(self):
        self.ax.clear()  # Clear the previous graph
        pos = nx.spring_layout(self.graph, seed=42)  # Define the layout for the graph with fixed seed for consistency

        # Draw edges with specific colors
        edges = self.graph.edges()
        
        edge_colors = ['#90EE90' if (u, v) in self.mst_edges or (v, u) in self.mst_edges else 'black' for u, v in edges]
        nx.draw_networkx_edges(self.graph, pos, edge_color=edge_colors, ax=self.ax, width=2)

        # Draw the entire graph with default edge color
        nx.draw(self.graph, pos, with_labels=True, node_size=700, node_color='lightblue', ax=self.ax, width=2)

        # Draw nodes with specific colors
        node_colors = ['#90EE90' if node in self.mst_nodes else 'lightblue' for node in self.graph.nodes()]
        nx.draw_networkx_nodes(self.graph, pos, node_color=node_colors, ax=self.ax, node_size=700)

        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        # Draw edge labels with a slight offset for better visibility
        nx.draw_networkx_edge_labels(
            self.graph,
            pos,
            edge_labels=edge_labels,
            ax=self.ax,
            label_pos=0.5,  # Center the label on the edge
            font_color='black',
            font_size=10,
            verticalalignment='center'  # Vertical alignment for better placement
        )

        self.ax.set_title("Graph Visualization")
        plt.draw()  # Draw the updated graph
        plt.pause(0.1)  # Pause for a moment to update the plot

    def clear_graph(self):
        self.graph.clear()
        self.mst_edges.clear()  # Clear MST edges
        self.mst_nodes.clear()  # Clear MST nodes
        messagebox.showinfo("Success", "Graph cleared.")
        self.visualize_graph()  # Update visualization

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    plt.ion()  # Turn on interactive mode
    plt.show()  # Show the matplotlib figure
    root.mainloop()