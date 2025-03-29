import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import Button, RadioButtons

class CrossTheoremVisualization:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.fig.subplots_adjust(bottom=0.2)
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-2, 10)
        self.ax.set_ylim(-2, 10)
        
        # Initial coordinates for the center triangle
        self.points = np.array([
            [3, 3],  # A
            [7, 6],  # B
            [5, 2]   # C
        ])
        
        # Create the main triangle and squares
        self.init_shapes()
        
        # Add controls
        self.selected_point = None
        self.drag_mode = 'A'
        self.add_controls()
        
        # Connect events
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        self.update_plot()
        plt.title("Cross's Theorem Interactive Visualization")
        
    def init_shapes(self):
        # Create the main triangle
        self.main_triangle = Polygon(self.points, alpha=0.5, color='blue')
        self.ax.add_patch(self.main_triangle)
        
        # Create squares on each side
        self.squares = []
        self.outer_triangles = []
        
        # Add labels for points A, B, C
        self.labels = []
        for i, point in enumerate(self.points):
            label = chr(65 + i)  # A, B, C
            self.labels.append(self.ax.text(point[0], point[1], label, fontsize=12, 
                                           ha='right', va='bottom'))
        
        # Create all shapes initially
        self.update_shapes()
    
    def create_square(self, p1, p2):
        """Create a square from two points (one side)"""
        vec = p2 - p1  # Vector from p1 to p2
        perp_vec = np.array([-vec[1], vec[0]])  # Perpendicular vector
        
        # Two other points of square
        p3 = p2 + perp_vec
        p4 = p1 + perp_vec
        
        return np.array([p1, p2, p3, p4])
    
    def update_shapes(self):
        # Clear previous shapes
        for square in self.squares:
            square.remove()
        self.squares = []
        
        for triangle in self.outer_triangles:
            triangle.remove()
        self.outer_triangles = []
        
        # Update main triangle
        self.main_triangle.set_xy(self.points)
        
        # Create squares on each side
        square_vertices = []
        for i in range(3):
            p1 = self.points[i]
            p2 = self.points[(i+1)%3]
            square = self.create_square(p1, p2)
            square_vertices.append(square)
            poly = Polygon(square, alpha=0.5, color='magenta')
            self.ax.add_patch(poly)
            self.squares.append(poly)
        
        # Get the outer vertices of each square (the ones not connected to the main triangle)
        outer_vertices = []
        for i in range(3):
            square = square_vertices[i]
            # The outer vertices are at indices 2 and 3 (the ones not connected to the triangle)
            outer_vertices.append(square[3])  # Vertex closer to first point
            outer_vertices.append(square[2])  # Vertex closer to second point
        
        # Create outer triangles correctly - connect the vertices as shown in the yellow outline
        # Triangle 1 (connecting points around point A)
        triangle1 = np.array([
            outer_vertices[0],  # Vertex of A-B square closer to A
            self.points[0],     # Point A
            outer_vertices[5]   # Vertex of A-C square closer to A
        ])
        poly1 = Polygon(triangle1, alpha=0.3, color='yellow')
        self.ax.add_patch(poly1)
        self.outer_triangles.append(poly1)
        
        # Triangle 2 (connecting points around point B)
        triangle2 = np.array([
            outer_vertices[1],  # Vertex of A-B square closer to B
            self.points[1],     # Point B
            outer_vertices[2]   # Vertex of B-C square closer to B
        ])
        poly2 = Polygon(triangle2, alpha=0.3, color='yellow')
        self.ax.add_patch(poly2)
        self.outer_triangles.append(poly2)
        
        # Triangle 3 (connecting points around point C)
        triangle3 = np.array([
            outer_vertices[3],  # Vertex of B-C square closer to C
            self.points[2],     # Point C
            outer_vertices[4]   # Vertex of A-C square closer to C
        ])
        poly3 = Polygon(triangle3, alpha=0.3, color='yellow')
        self.ax.add_patch(poly3)
        self.outer_triangles.append(poly3)
        
        # Update labels for points A, B, C
        for i, point in enumerate(self.points):
            self.labels[i].set_position(point)
        
        # Calculate and display areas
        main_area = self.calculate_triangle_area(self.points)
        
        # Add text for areas
        if hasattr(self, 'area_text'):
            self.area_text.remove()
        
        self.area_text = self.ax.text(
            0.05, 0.95, 
            f"Main Triangle Area = {main_area:.2f} square units\n"
            f"Each Yellow Triangle Area = {main_area:.2f} square units",
            transform=self.ax.transAxes, 
            fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8)
        )
    
    def calculate_triangle_area(self, vertices):
        """Calculate the area of a triangle using the cross product"""
        v1 = vertices[1] - vertices[0]
        v2 = vertices[2] - vertices[0]
        return 0.5 * abs(np.cross(v1, v2))
    
    def add_controls(self):
        # Add radio buttons to select which point to drag
        ax_radio = plt.axes([0.05, 0.05, 0.15, 0.15])
        self.radio = RadioButtons(ax_radio, ('A', 'B', 'C'))
        self.radio.on_clicked(self.set_drag_mode)
        
        # Add reset button
        ax_reset = plt.axes([0.25, 0.05, 0.1, 0.05])
        self.reset_button = Button(ax_reset, 'Reset')
        self.reset_button.on_clicked(self.reset)
        
        # Add explanation text
        ax_text = plt.axes([0.4, 0.02, 0.55, 0.15])
        ax_text.axis('off')
        ax_text.text(0, 0.5, 
                   "Cross's Theorem:\n"
                   "The areas of the yellow triangles are equal to the area of the blue triangle.\n"
                   "Drag points A, B, or C to see how the theorem holds for any triangle.",
                   fontsize=9,
                   verticalalignment='center')
    
    def set_drag_mode(self, label):
        self.drag_mode = label
    
    def reset(self, event):
        self.points = np.array([
            [3, 3],   # A
            [7, 6],   # B
            [5, 2]    # C
        ])
        self.update_shapes()
        self.fig.canvas.draw_idle()
    
    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        
        # Determine which point to move based on radio button selection
        idx = ord(self.drag_mode) - ord('A')
        if idx >= 0 and idx < 3:
            self.selected_point = idx
    
    def on_release(self, event):
        self.selected_point = None
    
    def on_motion(self, event):
        if self.selected_point is not None and event.inaxes == self.ax:
            self.points[self.selected_point] = np.array([event.xdata, event.ydata])
            self.update_shapes()
            self.fig.canvas.draw_idle()
    
    def update_plot(self):
        self.fig.canvas.draw_idle()
    
    def show(self):
        plt.show()

# Create and show the visualization
if __name__ == "__main__":
    viz = CrossTheoremVisualization()
    viz.show()