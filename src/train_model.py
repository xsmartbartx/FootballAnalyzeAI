import logging
from pathlib import Path
from data.dataset_config import DatasetConfig
from models.model_config import ModelConfig
from models.yolo_trainer import YOLOTrainer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_model():
    """Main function to train the model."""
    logger.info("Starting model training...")
    
    # Load dataset configuration
    base_path = Path("data")
    dataset_config = DatasetConfig(
        data_root=base_path,
        train_path=base_path / "train",
        val_path=base_path / "val"
    )
    
    # Initialize model configuration
    model_config = ModelConfig()
    
    # Initialize trainer
    trainer = YOLOTrainer(model_config)
    
    # Prepare dataset YAML
    dataset_yaml = trainer.prepare_dataset_yaml(
        train_path=dataset_config.train_path,
        val_path=dataset_config.val_path,
        classes=dataset_config.classes
    )
    
    # Train model
    logger.info("Training model...")
    trainer.train(dataset_yaml)
    
    # Evaluate model
    logger.info("Evaluating model...")
    metrics = trainer.evaluate(dataset_yaml)
    
    logger.info(f"Training completed. Validation metrics: {metrics}")

if __name__ == "__main__":
    train_model() 