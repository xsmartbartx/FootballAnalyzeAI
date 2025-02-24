from pathlib import Path
import yaml
from ultralytics import YOLO
from .model_config import ModelConfig

class YOLOTrainer:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = None
        
    def prepare_dataset_yaml(self, train_path: Path, val_path: Path, classes: List[str]) -> Path:
        """
        Create YAML configuration file for YOLOv8 training
        """
        dataset_config = {
            'path': str(train_path.parent),  # Dataset root
            'train': str(train_path.relative_to(train_path.parent)),  # Train path relative to root
            'val': str(val_path.relative_to(val_path.parent)),  # Val path relative to root
            
            'names': {i: name for i, name in enumerate(classes)}
        }
        
        yaml_path = train_path.parent / 'dataset.yaml'
        with open(yaml_path, 'w') as f:
            yaml.dump(dataset_config, f, sort_keys=False)
            
        return yaml_path
    
    def load_model(self):
        """Load or create YOLOv8 model"""
        self.model = YOLO(self.config.model_name)
    
    def train(self, dataset_yaml: Path):
        """Train the model"""
        if self.model is None:
            self.load_model()
            
        self.model.train(
            data=str(dataset_yaml),
            epochs=self.config.epochs,
            batch=self.config.batch_size,
            imgsz=self.config.img_size,
            device=self.config.device,
            
            # Hyperparameters
            lr0=self.config.learning_rate,
            weight_decay=self.config.weight_decay,
            momentum=self.config.momentum,
            
            # Augmentation
            mosaic=self.config.mosaic,
            mixup=self.config.mixup,
            degrees=self.config.degrees,
            translate=self.config.translate,
            scale=self.config.scale,
            shear=self.config.shear,
            perspective=self.config.perspective,
            flipud=self.config.flipud,
            fliplr=self.config.fliplr,
            
            # Validation and saving
            val=self.config.val_interval,
            save_period=self.config.save_interval
        )
    
    def evaluate(self, dataset_yaml: Path):
        """Evaluate the model on validation set"""
        if self.model is None:
            self.load_model()
            
        metrics = self.model.val(data=str(dataset_yaml))
        return metrics 