import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from ipywidgets import interact, widgets

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def to_array(self) -> np.ndarray:
        return np.array([self.x, self.y])

class Triangle:
    def __init__(self, point_a: Point, point_b: Point, point_c: Point):
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c
        self.points = np.array([point_a.to_array(), point_b.to_array(), point_c.to_array()])
    
    def calculate_area(self) -> float:
        v1 = self.points[1] - self.points[0]
        v2 = self.points[2] - self.points[0]
        return 0.5 * abs(np.cross(v1, v2))
    
    def create_square(self, p1: Point, p2: Point) -> np.ndarray:
        vec = p2.to_array() - p1.to_array()
        perp_vec = np.array([-vec[1], vec[0]])
        p3 = p2.to_array() + perp_vec
        p4 = p1.to_array() + perp_vec
        return np.array([p1.to_array(), p2.to_array(), p3, p4])
    
    def plot(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_aspect('equal')
        ax.set_xlim(-2, 10)
        ax.set_ylim(-2, 10)
        
        # Create the main triangle
        main_triangle = Polygon(self.points, alpha=0.5, color='blue')
        ax.add_patch(main_triangle)
        
        # Add labels for points
        for i, point in enumerate([self.point_a, self.point_b, self.point_c]):
            label = chr(65 + i)  # A, B, C
            ax.text(point.x, point.y, label, fontsize=12, ha='right', va='bottom')
        
        # Create squares on each side
        square_vertices = []
        for i in range(3):
            p1 = Point(self.points[i][0], self.points[i][1])
            p2 = Point(self.points[(i+1)%3][0], self.points[(i+1)%3][1])
            square = self.create_square(p1, p2)
            square_vertices.append(square)
            poly = Polygon(square, alpha=0.5, color='magenta')
            ax.add_patch(poly)
        
        # Get the outer vertices of each square and add labels
        outer_vertices = []
        outer_labels = ['P', 'Q', 'R', 'S', 'T', 'U', 'V']
        for i, square in enumerate(square_vertices):
            # Add label for the outer vertex closer to the first point
            outer_vertices.append(square[3])
            ax.text(square[3][0], square[3][1], outer_labels[i*2], fontsize=12, ha='right', va='bottom')
            
            # Add label for the outer vertex closer to the second point
            outer_vertices.append(square[2])
            ax.text(square[2][0], square[2][1], outer_labels[i*2+1], fontsize=12, ha='right', va='bottom')
        
        # Create outer triangles
        # Triangle 1 (connecting points around point A)
        triangle1 = np.array([
            outer_vertices[0],  # Vertex P
            self.points[0],     # Point A
            outer_vertices[5]   # Vertex U
        ])
        poly1 = Polygon(triangle1, alpha=0.3, color='yellow')
        ax.add_patch(poly1)
        
        # Triangle 2 (connecting points around point B)
        triangle2 = np.array([
            outer_vertices[1],  # Vertex Q
            self.points[1],     # Point B
            outer_vertices[2]   # Vertex R
        ])
        poly2 = Polygon(triangle2, alpha=0.3, color='yellow')
        ax.add_patch(poly2)
        
        # Triangle 3 (connecting points around point C)
        triangle3 = np.array([
            outer_vertices[3],  # Vertex S
            self.points[2],     # Point C
            outer_vertices[4]   # Vertex T
        ])
        poly3 = Polygon(triangle3, alpha=0.3, color='yellow')
        ax.add_patch(poly3)
        
        # Calculate and display areas
        main_area = self.calculate_area()
        
        # Add text for areas
        ax.text(
            0.05, 0.95, 
            f"Main Triangle Area = {main_area:.2f} square units\n"
            f"Each Yellow Triangle Area = {main_area:.2f} square units",
            transform=ax.transAxes, 
            fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8)
        )
        
        plt.title("Cross's Theorem Interactive Visualization")
        plt.show()

def plot_triangles(x_1: float, y_1: float, x_2: float, y_2: float, x_3: float, y_3: float):
    point_a = Point(x=x_1, y=y_1)
    point_b = Point(x=x_2, y=y_2)
    point_c = Point(x=x_3, y=y_3)
    
    triangle = Triangle(point_a=point_a, point_b=point_b, point_c=point_c)
    triangle.plot()

# Create interactive plot
interact(plot_triangles,
         x_1=widgets.FloatSlider(min=-2, max=10, step=0.1, value=3, description='A x:'),
         y_1=widgets.FloatSlider(min=-2, max=10, step=0.1, value=3, description='A y:'),
         x_2=widgets.FloatSlider(min=-2, max=10, step=0.1, value=7, description='B x:'),
         y_2=widgets.FloatSlider(min=-2, max=10, step=0.1, value=6, description='B y:'),
         x_3=widgets.FloatSlider(min=-2, max=10, step=0.1, value=5, description='C x:'),
         y_3=widgets.FloatSlider(min=-2, max=10, step=0.1, value=2, description='C y:'))