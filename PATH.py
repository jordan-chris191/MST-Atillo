import tkinter as tk
from tkinter import simpledialog, messagebox
from collections import deque, defaultdict

# Vertex and Edge classes remain unchanged
class Vertex:
    def __init__(self, label, x, y):
        self.label = label
        self.edges = []
        self.neighbors = []
        self.is_source = False
        self.cost = float('inf')
        self.previous = None
        self.x = x
        self.y = y

class Edge:
    def __init__(self, from_vertex, to_vertex, cost=1):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.cost = cost

class Graph:
    def __init__(self):
        self.vertices = []

    def add_vertex(self, label, x, y):
        vertex = Vertex(label, x, y)
        self.vertices.append(vertex)
        return vertex

    def add_edge(self, from_vertex, to_vertex, cost=1):
        edge = Edge(from_vertex, to_vertex, cost)
        from_vertex.edges.append(edge)
        from_vertex.neighbors.append(to_vertex)
        return edge

    def dijkstra(self, source):
        source.cost = 0
        unvisited = self.vertices.copy()

        while unvisited:
            current_vertex = min(unvisited, key=lambda vertex: vertex.cost)
            unvisited.remove(current_vertex)

            for edge in current_vertex.edges:
                neighbor = edge.to_vertex
                new_cost = current_vertex.cost + edge.cost
                if new_cost < neighbor.cost:
                    neighbor.cost = new_cost
                    neighbor.previous = current_vertex

        result = []
        for vertex in self.vertices:
            result.append(f"{vertex.label}: Cost = {vertex.cost}, Previous = {vertex.previous.label if vertex.previous else None}")
        return result

    def dials_algorithm(self, source, max_edge_cost):
        source.cost = 0
        bucket = defaultdict(deque)
        bucket[0].append(source)
        max_cost = max_edge_cost * len(self.vertices)

        for i in range(max_cost + 1):
            while bucket[i]:
                current_vertex = bucket[i].popleft()
                if current_vertex.cost < i:
                    continue  # Skip already processed nodes with smaller cost

                for edge in current_vertex.edges:
                    neighbor = edge.to_vertex
                    new_cost = current_vertex.cost + edge.cost
                    if new_cost < neighbor.cost:
                        if neighbor.cost != float('inf'):
                            bucket[neighbor.cost].remove(neighbor)
                        neighbor.cost = new_cost
                        neighbor.previous = current_vertex
                        bucket[new_cost].append(neighbor)

        result = []
        for vertex in self.vertices:
            result.append(f"{vertex.label}: Cost = {vertex.cost}, Previous = {vertex.previous.label if vertex.previous else None}")
        return result

class DijkstraApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Shortest Path Solver")
        self.master.configure(bg="#2e2e2e")  # Dark background color

        self.graph = Graph()
        self.current_mode = tk.StringVar(value="drawVertex")
        self.selected_vertex = None
        self.start_vertex = None

        # Frame for the graph canvas
        self.graph_frame = tk.Frame(master, bg="#ffffff")
        self.graph_frame.pack(side=tk.LEFT, padx=(10, 0), pady=10)

        # Canvas for drawing the graph
        self.canvas = tk.Canvas(self.graph_frame, width=640, height=480, bg='#ffffff')
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Frame for controls on the right
        self.control_frame = tk.Frame(master, bg="#2e2e2e")
        self.control_frame.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        # Control settings
        tk.Radiobutton(self.control_frame, text="Draw vertex", variable=self.current_mode, value="drawVertex", bg="#2e2e2e", fg="white", selectcolor="#4b4b4b").pack(anchor='w', padx=5)
        tk.Radiobutton(self.control_frame, text="Draw edge", variable=self.current_mode, value="drawEdge", bg="#2e2e2e", fg="white", selectcolor="#4b4b4b").pack(anchor='w', padx=5)
        tk.Radiobutton(self.control_frame, text="Set Start", variable=self.current_mode, value="setStart", bg="#2e2e2e", fg="white", selectcolor="#4b4b4b").pack(anchor='w', padx=5)
        tk.Radiobutton(self.control_frame, text="Set cost", variable=self.current_mode, value="setCost", bg="#2e2e2e", fg="white", selectcolor="#4b4b4b").pack(anchor='w', padx=5)

        # Buttons for running algorithms
        self.dijkstra_button = tk.Button(self.control_frame, text="Run Dijkstra", command=self.run_dijkstra, bg="#4caf50", fg="white", padx=10, pady=5)
        self.dijkstra_button.pack(pady=5)

        self.dials_button = tk.Button(self.control_frame, text="Run Dial's Algorithm", command=self.run_dials_algorithm, bg="#2196f3", fg="white", padx=10, pady=5)
        self.dials_button.pack(pady=5)

        # Text area for results
        self.result_area = tk.Text(self.control_frame, height=10, width=40, bg="#f0f0f0", fg="black", padx=10, pady=10)
        self.result_area.pack(pady=10)

    def on_canvas_click(self, event):
        mode = self.current_mode.get()
        
        if mode == "drawVertex":
            label = simpledialog.askstring("Input", "Enter vertex label (single character):")
            if label:
                vertex = self.graph.add_vertex(label, event.x, event.y)
                self.draw_vertex(vertex)

        elif mode == "drawEdge":
            clicked_vertex = self.find_vertex_at(event.x, event.y)
            if clicked_vertex:
                if self.start_vertex is None:
                    self.start_vertex = clicked_vertex
                else:
                    cost = simpledialog.askinteger("Input", "Enter edge cost:")
                    if cost is not None:
                        edge = self.graph.add_edge(self.start_vertex, clicked_vertex, cost)
                        self.draw_edge(edge)
                    self.start_vertex = None

        elif mode == "setStart":
            self.selected_vertex = self.find_vertex_at(event.x, event.y)
            if self.selected_vertex:
                self.selected_vertex.is_source = True
                messagebox.showinfo("Vertex Selected", f"Starting vertex set to {self.selected_vertex.label}")

        elif mode == "setCost":
            vertex = self.find_vertex_at(event.x, event.y)
            if vertex:
                cost = simpledialog.askinteger("Input", "Enter new cost for vertex:")
                if cost is not None:
                    vertex.cost = cost
                    messagebox.showinfo("Cost Set", f"Vertex {vertex.label} cost set to {cost}")

    def draw_vertex(self, vertex):
        x, y = vertex.x, vertex.y
        # Create a more detailed polygon for the vertex
        self.canvas.create_polygon(x - 20, y - 20, x + 20, y - 20, x + 20, y + 20, x - 20, y + 20,
                                    fill='#4caf50', outline='black', width=2, smooth=True)
        self.canvas.create_text(x, y, text=vertex.label, fill="white", font=("Arial", 12, "bold"))

    def draw_edge(self, edge):
        x1, y1 = edge.from_vertex.x, edge.from_vertex.y
        x2, y2 = edge.to_vertex.x, edge.to_vertex.y
        # Draw a smooth line for the edge
        self.canvas.create_line(x1, y1, x2, y2, fill='black', width=3, smooth=True)
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        self.canvas.create_text(mid_x, mid_y, text=str(edge.cost), fill="red", font=("Arial", 10))

    def find_vertex_at(self, x, y):
        for vertex in self.graph.vertices:
            if (vertex.x - 20 <= x <= vertex.x + 20) and (vertex.y - 20 <= y <= vertex.y + 20):
                return vertex
        return None

    def run_dijkstra(self):
        if self.selected_vertex:
            results = self.graph.dijkstra(self.selected_vertex)
            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END, "\n".join(results))
        else:
            messagebox.showwarning("Warning", "Please select a starting vertex.")

    def run_dials_algorithm(self):
        if self.selected_vertex:
            max_edge_cost = simpledialog.askinteger("Input", "Enter the maximum edge cost:")
            if max_edge_cost is not None:
                results = self.graph.dials_algorithm(self.selected_vertex, max_edge_cost)
                self.result_area.delete(1.0, tk.END)
                self.result_area.insert(tk.END, "\n".join(results))
        else:
            messagebox.showwarning("Warning", "Please select a starting vertex.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraApp(root)
    root.mainloop()
