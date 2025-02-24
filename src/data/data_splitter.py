import shutil
from pathlib import Path
import random
from typing import List, Tuple

class DataSplitter:
    """Splits dataset into training and validation sets"""
    
    @staticmethod
    def split_dataset(
        source_dir: Path,
        train_dir: Path,
        val_dir: Path,
        split_ratio: float = 0.8
    ) -> Tuple[int, int]:
        """
        Split the dataset into training and validation sets
        
        Args:
            source_dir: Directory containing all images
            train_dir: Directory for training images
            val_dir: Directory for validation images
            split_ratio: Ratio of training to total data
            
        Returns:
            Tuple of (train_count, val_count)
        """
        # Get all image files
        image_files = list(source_dir.glob("*.jpg"))
        random.shuffle(image_files)
        
        # Calculate split
        split_idx = int(len(image_files) * split_ratio)
        train_files = image_files[:split_idx]
        val_files = image_files[split_idx:]
        
        # Copy files to respective directories
        for f in train_files:
            shutil.copy2(f, train_dir / f.name)
            
        for f in val_files:
            shutil.copy2(f, val_dir / f.name)
            
        return len(train_files), len(val_files) 