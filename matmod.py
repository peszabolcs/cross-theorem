import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from ipywidgets import interact, widgets

def create_square(p1, p2):
    """Create a square from two points (one side)"""
    vec = p2 - p1  # Vector from p1 to p2
    perp_vec = np.array([-vec[1], vec[0]])  # Perpendicular vector
    
    # Two other points of square
    p3 = p2 + perp_vec
    p4 = p1 + perp_vec
    
    return np.array([p1, p2, p3, p4])

def calculate_triangle_area(vertices):
    """Calculate the area of a triangle using the cross product"""
    v1 = vertices[1] - vertices[0]
    v2 = vertices[2] - vertices[0]
    return 0.5 * abs(np.cross(v1, v2))

def plot_triangles(x_1, y_1, x_2, y_2, x_3, y_3):
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_xlim(-2, 10)
    ax.set_ylim(-2, 10)
    
    # Create points array
    points = np.array([
        [x_1, y_1],  # A
        [x_2, y_2],  # B
        [x_3, y_3]   # C
    ])
    
    # Create the main triangle
    main_triangle = Polygon(points, alpha=0.5, color='blue')
    ax.add_patch(main_triangle)
    
    # Add labels for points A, B, C
    for i, point in enumerate(points):
        label = chr(65 + i)  # A, B, C
        ax.text(point[0], point[1], label, fontsize=12, ha='right', va='bottom')
    
    # Create squares on each side
    square_vertices = []
    for i in range(3):
        p1 = points[i]
        p2 = points[(i+1)%3]
        square = create_square(p1, p2)
        square_vertices.append(square)
        poly = Polygon(square, alpha=0.5, color='magenta')
        ax.add_patch(poly)
    
    # Get the outer vertices of each square
    outer_vertices = []
    for i in range(3):
        square = square_vertices[i]
        outer_vertices.append(square[3])  # Vertex closer to first point
        outer_vertices.append(square[2])  # Vertex closer to second point
    
    # Create outer triangles
    # Triangle 1 (connecting points around point A)
    triangle1 = np.array([
        outer_vertices[0],  # Vertex of A-B square closer to A
        points[0],          # Point A
        outer_vertices[5]   # Vertex of A-C square closer to A
    ])
    poly1 = Polygon(triangle1, alpha=0.3, color='yellow')
    ax.add_patch(poly1)
    
    # Triangle 2 (connecting points around point B)
    triangle2 = np.array([
        outer_vertices[1],  # Vertex of A-B square closer to B
        points[1],          # Point B
        outer_vertices[2]   # Vertex of B-C square closer to B
    ])
    poly2 = Polygon(triangle2, alpha=0.3, color='yellow')
    ax.add_patch(poly2)
    
    # Triangle 3 (connecting points around point C)
    triangle3 = np.array([
        outer_vertices[3],  # Vertex of B-C square closer to C
        points[2],          # Point C
        outer_vertices[4]   # Vertex of A-C square closer to C
    ])
    poly3 = Polygon(triangle3, alpha=0.3, color='yellow')
    ax.add_patch(poly3)
    
    # Calculate and display areas
    main_area = calculate_triangle_area(points)
    
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

# Create interactive plot
interact(plot_triangles,
         x_1=widgets.FloatSlider(min=-2, max=10, step=0.1, value=3, description='A x:'),
         y_1=widgets.FloatSlider(min=-2, max=10, step=0.1, value=3, description='A y:'),
         x_2=widgets.FloatSlider(min=-2, max=10, step=0.1, value=7, description='B x:'),
         y_2=widgets.FloatSlider(min=-2, max=10, step=0.1, value=6, description='B y:'),
         x_3=widgets.FloatSlider(min=-2, max=10, step=0.1, value=5, description='C x:'),
         y_3=widgets.FloatSlider(min=-2, max=10, step=0.1, value=2, description='C y:'))