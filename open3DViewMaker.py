import open3d as o3d
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Generate 3D mesh perspectives")
parser.add_argument("--input", help="Input mesh file")
parser.add_argument("--views", type=int, default=5, help="Number of random perspectives to generate")
args = parser.parse_args()

mesh = o3d.io.read_triangle_mesh(args.input)
mesh.compute_vertex_normals()

vis = o3d.visualization.Visualizer()
vis.create_window("3D Mesh Perspectives", width=600, height=600, left=0, top=0)
vis.get_render_option().background_color = [0, 0, 0]
view_control = vis.get_view_control()
vis.add_geometry(mesh)
for _ in range(args.views):

    # Generate a random translation vector
    # random_translation = ((np.random.rand(3) * 1000 - 500) + mesh.get_center())
    random_translation = mesh.get_center()

    # Generate a random rotation vector
    theta = np.random.rand() * 2 * np.pi
    phi = np.arccos(2 * np.random.rand() - 1)
    random_rotation = np.array([
        np.sin(phi) * np.cos(theta),
        np.sin(phi) * np.sin(theta),
        np.cos(phi)
    ])

    # Generate a random rotation vector
    theta = np.random.rand() * 2 * np.pi
    phi = np.arccos(2 * np.random.rand() - 1)
    random_front = np.array([
        np.sin(phi) * np.cos(theta),
        np.sin(phi) * np.sin(theta),
        np.cos(phi)
    ])
    
    view_control.set_zoom(1)
    view_control.set_front(random_front)
    view_control.set_up(random_rotation)
    view_control.set_lookat(random_translation)
    
    vis.capture_screen_image(f"perspective_{_}.png",True)