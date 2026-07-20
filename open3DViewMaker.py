import open3d as o3d
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Generate 3D mesh perspectives")
parser.add_argument("--input", help="Input mesh file")
parser.add_argument("--views", type=int, default=5, help="Number of random perspectives to generate")
args = parser.parse_args()

mesh = o3d.io.read_triangle_mesh(args.input)
mesh.compute_vertex_normals()

def generate_random_rotation(mesh):
    # Generate a random rotation matrix
    R = mesh.get_rotation_matrix_from_xyz(np.random.rand(3) * 2 * np.pi)
    # Apply the transformation to the mesh
    mesh.rotate(R, center=mesh.get_center())
    return mesh

vis = o3d.visualization.Visualizer()
vis.create_window("3D Mesh Perspectives", width=600, height=600, left=0, top=0)
vis.get_render_option().background_color = [0, 0, 0]
view_control = vis.get_view_control()
for _ in range(args.views):
    vis.add_geometry(generate_random_rotation(mesh))
    random_translation = ((np.random.rand(3) * 1000 - 500) + mesh.get_center())  # Random translation
    view_control.set_lookat(random_translation)
    vis.capture_screen_image(f"perspective_{_}.png",True)
    vis.clear_geometries()