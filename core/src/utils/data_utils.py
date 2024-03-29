import os
import random
import joblib
import numpy as np
import pandas as pd

from typing import List, Tuple
from rich.progress import Progress

from .os_utils import create_if_not_exists, get_file_count
from .projection import SpatialProjection
from .features import extract_flxion_features
from .img_utils import create_img_stack

random.seed(42)


def pre_process_recording(data: pd.DataFrame) -> pd.DataFrame:
    data.drop(columns=["time"], inplace=True)
    data.drop(0, inplace=True)  # Remove first All-0 row
    return data - data.iloc[:10].median()  # Initial position correction


def get_train_test_set(
    data_dir: str,
    subjects: List[str],
    gestures: List[str],
    feature_landmarks: List[str],
    augmentation_levels: List[SpatialProjection],
    test_subject: str = None,
    test_size: float = 0.2
) -> Tuple[np.ndarray]:

    # ... Look for existing data
    try:
        save_dir = os.path.join(data_dir, "processed", test_subject)
        dataset = joblib.load(os.path.join(save_dir, "dataset.joblib"))
        X_train = dataset["X_train"]
        X_test = dataset["X_test"]
        y_train = dataset["y_train"]
        y_test = dataset["y_test"]
        return (X_train, X_test, y_train, y_test)
    except:
        pass

    train_features = []
    train_images = []
    train_labels = []
    test_features = []
    test_images = []
    test_labels = []

    total_files = get_file_count(os.path.join(data_dir, "raw"))

    with Progress() as progress:
        count = 0
        loader_pid = progress.add_task("", total=total_files)

        for subject in subjects:
            for gesture in gestures:
                gesture_dir = os.path.join(data_dir, "raw", subject, gesture)
                recordings = os.listdir(gesture_dir)
                for recording in recordings:
                    progress.update(
                        task_id=loader_pid,
                        advance=1,
                        description=f"[{(count + 1):>5}/{total_files:>5}]" +
                        " processing files: "
                    )
                    count += 1

                    file_path = os.path.join(gesture_dir, recording)
                    data = pd.read_csv(file_path)
                    data = pre_process_recording(data)

                    if data.shape[0] == 0:
                        continue

                    # ... Flag for determining Trainning and Testing Samples
                    for_training = random.random() >= test_size
                    if test_subject != None:
                        for_training = subject != test_subject

                    for sp in augmentation_levels:
                        _images = []
                        for landmark in feature_landmarks:
                            _images.extend(
                                sp.get_projection_images(
                                    data=data.filter(regex=landmark),
                                    subject=subject,
                                    gesture=gesture
                                )
                            )

                        _features = extract_flxion_features(data)

                        img = create_img_stack(_images)

                        if for_training:
                            train_features.append(_features)
                            train_images.append(img)
                            train_labels.append(gestures.index(gesture))
                        else:
                            test_features.append(_features)
                            test_images.append(img)
                            test_labels.append(gestures.index(gesture))
                            break
            # break

    train_features = np.array(train_features)
    train_images = np.array(train_images, dtype="uint8")
    test_features = np.array(test_features)
    test_images = np.array(test_images, dtype="uint8")

    X_train = np.split(train_features, train_features.shape[-1], axis=-1) + \
        [np.squeeze(img) for img in np.split(train_images, 3, axis=-1)]

    X_test = np.split(test_features, test_features.shape[-1], axis=-1) + \
        [np.squeeze(img) for img in np.split(test_images, 3, axis=-1)]

    y_train = np.array(train_labels, dtype="uint8")
    y_test = np.array(test_labels, dtype="uint8")

    # ... Saving Dataset
    save_dir = os.path.join(data_dir, "processed", test_subject)
    create_if_not_exists(save_dir)
    joblib.dump(
        {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test
        },
        os.path.join(save_dir, "dataset.joblib")
    )

    print("-" * 70)
    print("Train Features Shape: ", X_train[0].shape)
    print("Train Images Shape: ", X_train[-1].shape)
    print("Test Features Shape: ", X_test[0].shape)
    print("Test Images Shape: ", X_test[-1].shape)
    print("Train Labels Shape: ", y_train.shape)
    print("Test Labels Shape: ", y_test.shape)
    print("-" * 70)

    return (X_train, X_test, y_train, y_test)
