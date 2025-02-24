from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

@dataclass
class DatasetConfig:
    """Configuration for dataset preparation"""
    data_root: Path
    train_path: Path
    val_path: Path
    classes: List[str] = field(default_factory=lambda: [
        'player',
        'goalkeeper',
        'referee',
        'ball'
    ])
    input_size: int = 1280  # Optimized resolution
    batch_size: int = 16    # Can be adjusted based on GPU 