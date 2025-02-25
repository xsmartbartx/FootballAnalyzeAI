from pathlib import Path
from data.dataset_config import DatasetConfig
from data.annotation_handler import AnnotationHandler
from tools.labeling_tool import LabelingTool

def main():
    # Configure paths
    base_path = Path("data")
    config = DatasetConfig(
        data_root=base_path,
        train_path=base_path / "train",
        val_path=base_path / "val"
    )
    
    # Initialize annotation handler
    annotation_handler = AnnotationHandler(base_path / "annotations")
    
    # Initialize labeling tool
    labeling_tool = LabelingTool(config, annotation_handler)
    
    # Label training images
    print("Labeling training images...")
    for image_path in config.train_path.glob("*.jpg"):
        print(f"Labeling {image_path.name}")
        labeling_tool.label_image(image_path)
        
    print("\nLabeling completed!")
    print("Instructions:")
    print("- Left click and drag to draw bounding box")
    print("- Press 'c' to change class")
    print("- Press 's' to save annotations")
    print("- Press 'z' to undo last box")
    print("- Press 'q' to quit current image")

if __name__ == "__main__":
    main() 