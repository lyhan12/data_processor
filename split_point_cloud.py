import argparse
import open3d as o3d

import numpy as np
import os

def main():
    Parser = argparse.ArgumentParser()
    Parser.add_argument("--input_file", required=True, help="Input point cloud file")
    Parser.add_argument("--model_path", required=True, help="Output path to save process point clouds")
    Parser.add_argument("--transform_path", help="Path to the transform file to be applied to inputs", default=None)
    args = Parser.parse_args()

    input_file = args.input_file
    model_path = args.model_path
    transform_path = args.transform_path

    if transform_path is None:
        transform_path = os.path.join(model_path, "transform.txt")

    pcd = o3d.io.read_point_cloud(input_file)

    # read transform
    trasnform = np.loadtxt(transform_path, delimiter=" ")
    pcd.transform(trasnform)

    o3d.io.write_point_cloud(os.path.join(model_path, "points3D.ply"), pcd)

    # count folders in model_path
    folders = [f for f in os.listdir(model_path) if os.path.isdir(os.path.join(model_path, f))]
    split_model_paths = [f for f in folders if f.isnumeric()]

    bbox_name = "bbox_scene.txt"
    splot_bboxes = []
    for split_model_path in split_model_paths:
        bbox_path = os.path.join(model_path, split_model_path, bbox_name)
        with open(bbox_path) as f:
            bbox = np.loadtxt(f, delimiter=",")
        splot_bboxes.append(bbox)

    print("Split Model Num : ", len(split_model_paths))
    print("Transform : ", trasnform)
    print("BBoxes : ", splot_bboxes)

    for idx, split_bbox in enumerate(splot_bboxes):
        bbox = o3d.geometry.AxisAlignedBoundingBox(min_bound=split_bbox[0], max_bound=split_bbox[1])
        # crop point cloud
        pcd_cropped = pcd.crop(bbox)
        o3d.io.write_point_cloud(os.path.join(model_path, split_model_paths[idx], "points3D.ply"), pcd_cropped)

if __name__ == "__main__":
    main()

