import os
import joblib
import config
import numpy as np
import pandas as pd

import tensorflow as tf

from utils import (
    get_train_test_set,
    SpatialProjection
)

from model.projectionnet.tf import ProjectionNet
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"

# ... Configuration
data_dir = "data/dataset/raw"
model_dir = "models/"
subjects = os.listdir(data_dir)


# ... Dataset Generation
print("-" * 70 + "\nGenerating Dataset\n" + "-" * 70)
sp_augment = [
    SpatialProjection(
        img_len=config.IMG_LEN,
        polyfit_degree=degree
    )
    for degree in config.AUGMENTATION_LEVELS]

(X_train, X_test, y_train, y_test) = get_train_test_set(
    data_dir=data_dir,
    subjects=subjects,
    gestures=config.GESTURES,
    feature_landmarks=config.PROJECTION_LANDMARKS,
    augmentation_levels=sp_augment
)

# ... Model Initialization
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(config.IMG_LEN, config.IMG_LEN, config.N_CHANNELS),
    include_top=False,
    weights="imagenet"
)

model = ProjectionNet(
    img_size=config.IMG_LEN,
    segment_len=config.SEGMENT_LEN,
    n_classes=len(config.GESTURES),
    base_model=base_model
).get_model(
    n_projections=config.N_CHANNELS,
    n_channels=len(config.DIST_FEATURES)
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=config.LEARNING_RATE),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['accuracy']
)

# ... Model Training
print("-" * 70 + "\nTraining Model ... \n" + "-" * 70)
callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=config.PATIENCE,
        restore_best_weights=True
    )
]

history = model.fit(
    x=X_train,
    y=y_train,
    validation_data=(X_test, y_test),
    batch_size=config.BATCH_SIZE,
    epochs=config.MAX_EPOCHS,
    verbose=1,
    callbacks=callbacks
)

# ... Evaluation
print("-" * 70 + "\nMetrics \n" + "-" * 70)
results = pd.DataFrame()
loss, accuarcy = model.evaluate(X_test, y_test)
y_pred = np.argmax(model.predict(X_test), axis=1)
precision = precision_score(y_test, y_pred, average=None, zero_division=0)
recall = recall_score(y_test, y_pred, average=None, zero_division=0)
f_score = f1_score(y_test, y_pred, average=None, zero_division=0)
results["precision"] = precision
results["recall"] = recall
results["f1-score"] = f_score
print(classification_report(y_test, y_pred, zero_division=0))

# ... Save Results
print("-" * 70 + "\nSaving Results ... \n" + "-" * 70)
best_accuracy = 0
try:
    best_accuracy = joblib.load(os.path.join(model_dir, "best_acc.joblib"))
except:
    print("No Previous Accuracy Found!")

if accuarcy > best_accuracy:
    model.save(os.path.join(model_dir, "stack_cnn.h5"), save_format="h5")
    joblib.dump(history, os.path.join(model_dir, "stack_cnn_history.joblib"))
    joblib.dump(y_test, os.path.join(model_dir, "stack_cnn_y_true.joblib"))
    joblib.dump(y_pred, os.path.join(model_dir, "stack_cnn_y_pred.joblib"))
    joblib.dump(accuarcy, os.path.join(model_dir, "best_acc.joblib"))
    results.to_excel(os.path.join(model_dir, "stack_cnn.xlsx"),
                     sheet_name="metrics", index=False)
