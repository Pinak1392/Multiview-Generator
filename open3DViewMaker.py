import open3d as o3d
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(description="Generate 3D mesh perspectives")
parser.add_argument("--input", help="Input mesh file or directory containing mesh files", required=True)
parser.add_argument("--views", type=int, default=5, help="Number of random perspectives to generate")
parser.add_argument("--zoomMax", type=float, default=1.0, help="Maximum zoom level for the views")
parser.add_argument("--zoomMin", type=float, default=0.5, help="Minimum zoom level for the views")
parser.add_argument("--translation_variance", type=float, default=1.0, help="Multiplier for translation variance based on mesh size")
parser.add_argument("-r", "--recursive", action="store_true", help="Recursively process directories for mesh files", default=False)
args = parser.parse_args()


pathsToProcess = []
if args.recursive:
    for root, dirs, files in os.walk(args.input):
        for file in files:
            if file.endswith(('.ply', '.obj', '.stl')):
                pathsToProcess.append(os.path.join(root, file))
else:
    pathsToProcess.append(args.input)

vis = o3d.visualization.Visualizer()
vis.create_window("3D Mesh Perspectives", width=600, height=600, left=0, top=0)
view_control = vis.get_view_control()

# Set up rendering options
render_option = vis.get_render_option()
render_option.background_color = [0, 0, 0]
render_option.light_on = True
render_option.mesh_shade_option = o3d.visualization.MeshShadeOption.Color

for path in pathsToProcess:
    if not os.path.exists(f"output/{os.path.splitext(os.path.basename(path))[0]}"):
        os.makedirs(f"output/{os.path.splitext(os.path.basename(path))[0]}")
    mesh = o3d.io.read_triangle_mesh(path)
    mesh.compute_vertex_normals()
    translation_range = mesh.get_max_bound() - mesh.get_min_bound()
    translation_range *= args.translation_variance
    vis.add_geometry(mesh)

    for _ in range(args.views):

        # Generate a random translation vector
        random_translation = ((np.random.rand(3) * translation_range - translation_range / 2) + mesh.get_center())

        # Zoom variance
        random_zoom = np.random.uniform(args.zoomMin, args.zoomMax)

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
        
        view_control.set_zoom(random_zoom)
        view_control.set_front(random_front)
        view_control.set_up(random_rotation)
        view_control.set_lookat(random_translation)

        vis.update_renderer()
        vis.capture_screen_image(f"output/{os.path.splitext(os.path.basename(path))[0]}/perspective_{_}.png", True)