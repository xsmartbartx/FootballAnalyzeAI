from pathlib import Path
from data.dataset_config import DatasetConfig
from data.dataset_preparation import DatasetPreparation
from data.data_splitter import DataSplitter

def main():
    # Configure paths
    base_path = Path("data")
    config = DatasetConfig(
        data_root=base_path,
        train_path=base_path / "train",
        val_path=base_path / "val"
    )
    
    # Initialize dataset preparation
    dataset_prep = DatasetPreparation(config)
    
    # Process videos (you'll need to add your video paths)
    videos_path = Path("raw_videos")
    for video_file in videos_path.glob("*.mp4"):
        dataset_prep.process_video(
            video_path=video_file,
            output_path=base_path / "frames"
        )
    
    # Split dataset
    splitter = DataSplitter()
    train_count, val_count = splitter.split_dataset(
        source_dir=base_path / "frames",
        train_dir=config.train_path,
        val_dir=config.val_path
    )
    
    print(f"Dataset prepared successfully:")
    print(f"Training samples: {train_count}")
    print(f"Validation samples: {val_count}")

if __name__ == "__main__":
    main() 