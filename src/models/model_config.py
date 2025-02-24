from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

@dataclass
class ModelConfig:
    """Configuration for YOLOv8 model training"""
    model_name: str = 'yolov8x.pt'  # Base model to start from
    epochs: int = 100
    batch_size: int = 16
    img_size: int = 1280
    device: str = 'cuda'  # or 'cpu'
    
    # Training hyperparameters
    learning_rate: float = 0.01
    weight_decay: float = 0.0005
    momentum: float = 0.937
    
    # Data augmentation
    mosaic: bool = True
    mixup: bool = True
    degrees: float = 10.0  # rotation
    translate: float = 0.1
    scale: float = 0.5
    shear: float = 2.0
    perspective: float = 0.0
    flipud: float = 0.0
    fliplr: float = 0.5
    
    # Validation
    val_interval: int = 1
    save_interval: int = 10 