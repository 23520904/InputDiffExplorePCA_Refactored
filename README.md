# Input Difference Exploration with PCA for Neural Distinguishers

A cryptography research repository implementing Principal Component Analysis (PCA) to explore and evaluate input differences for training neural distinguishers on block ciphers.

---

## Overview

This repository implements a scientific approach to discover optimal input differences for neural distinguishers in symmetric-key cryptography, specifically targeting the Simon and Speck block ciphers. 

The core problem in training neural distinguishers is finding input differences that yield the highest accuracy, which traditionally requires expensive trial-and-error network training. This repository solves this by introducing a much faster heuristic workflow: it generates data for various input differences, applies PCA for dimensionality reduction, and uses K-means clustering (evaluated via silhouette scores) to assess the quality of the differences *before* committing to full neural network training. 

By filtering out weak input differences early, researchers can focus their computational resources on the most promising candidates.

---

## Repository Structure

```text
InputDiffExplorePCA_Refactored/
├── data/                  # Directory for storing generated datasets
├── notebooks/             # Jupyter notebooks for interactive analysis and visualization
├── outputs/               # Generated models, logs, and experiment results
│   ├── clustering_results/
│   ├── explore_results/
│   ├── freshly_trained_nets/
│   ├── logs/
│   └── npy/
├── scripts/               # Executable scripts for exploration and training experiments
├── src/                   # Core Python source code
│   ├── crypto/            # Implementations of cryptographic algorithms (Simon, Speck)
│   ├── clustering_helper.py
│   ├── dataset.py
│   ├── explore_input_diff.py
│   ├── pca_helper.py
│   └── train_nets.py
└── README.md
```

### Major Directories
*   **`src/`**: Contains the reusable core logic of the pipeline, including data generation, machine learning models, PCA, and clustering utilities.
*   **`src/crypto/`**: Contains the raw implementations of the target block ciphers.
*   **`scripts/`**: Houses the standalone Python scripts used to launch lengthy exploration tasks and model training runs.
*   **`notebooks/`**: Used for post-experiment analysis, checking neural network accuracies, and visualizing PCA clusters.
*   **`outputs/`**: The designated output location for all generated artifacts, ensuring the source directories remain clean.

---

## Installation

**Python Version:** Python 3.8+ (tested on 3.8.10)

**Required Packages:**
*   `tensorflow`
*   `keras`
*   `numpy`
*   `scikit-learn`
*   `matplotlib`
*   `scipy`
*   `silence_tensorflow`

**Installation Commands:**

```bash
# Clone the repository
git clone <repository_url>
cd InputDiffExplorePCA_Refactored

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the required dependencies
pip install tensorflow keras numpy scikit-learn matplotlib scipy silence_tensorflow
```

---

## Usage

### Run Exploration Experiments
To explore input differences for a specific cipher (e.g., 8-round Simon) across various Hamming weights:
```bash
python scripts/explore_simon_nr8_diff.py
```

### Train Neural Distinguishers
To train a neural network using a selected input difference:
```bash
python scripts/train_speck_nr5_left.py
```

### Use Notebooks
Launch Jupyter Notebook to interact with the analysis files:
```bash
jupyter notebook notebooks/check_accuracy.ipynb
```

### Locate Generated Outputs
After running an experiment, results will automatically be saved into the `outputs/` directory. For example, explored difference scores are saved in `outputs/explore_results/`.

---

## Workflow

The repository follows a systematic pipeline to discover and utilize optimal input differences:

1.  **Generate Dataset:** Generate ciphertext pairs with a specific input difference using the target cipher.
    ↓
2.  **Explore Input Differences:** Iteratively test candidate differences based on their Hamming weight.
    ↓
3.  **PCA:** Apply Principal Component Analysis to the dataset for dimensionality reduction and eigenvalue decomposition.
    ↓
4.  **Clustering:** Perform K-means clustering on the PCA components and calculate the silhouette score.
    ↓
5.  **Select Good Differences:** Analyze the silhouette scores to identify input differences that show strong non-random characteristics.
    ↓
6.  **Train Neural Distinguisher:** Train a deep residual neural network on the most promising input differences.
    ↓
7.  **Evaluation:** Validate the network's accuracy and loss to confirm the effectiveness of the chosen difference.

---

## Key Components

*   **`src/dataset.py`**: Handles the generation of real and random training/evaluation datasets for the Simon and Speck ciphers.
*   **`src/explore_input_diff.py`**: The main orchestrator for testing various input differences. It coordinates dataset generation, PCA, and clustering to compute silhouette scores.
*   **`src/pca_helper.py`**: Provides utilities for Principal Component Analysis, including eigenvalue decomposition, dimensionality reduction, and 2D/3D visualizations.
*   **`src/clustering_helper.py`**: Implements K-means clustering and silhouette score calculations to quantitatively evaluate PCA results.
*   **`src/train_nets.py`**: Defines and trains the ResNet (residual neural network) architecture used as the actual neural distinguisher.
*   **`src/crypto/simon.py` & `src/crypto/speck.py`**: The core cryptographic implementations of the Simon and Speck block ciphers used to generate the datasets.

---

## Outputs

All artifacts generated during experiments are routed to the `outputs/` directory:

*   **`outputs/explore_results/`**: Text files containing silhouette scores and computation times for explored input differences.
*   **`outputs/freshly_trained_nets/`**: Saved neural network models (`.h5`), training histories (`.p`), and validation arrays (`.npy`).
*   **`outputs/clustering_results/`**: Visualizations and figures representing clustered datasets.
*   **`outputs/logs/`**: General runtime logs from executed scripts.

---

## Reproducing Experiments

To reproduce the findings of the paper, execute the scripts in the following order:

1.  **Exploration Phase:** Run the exploration scripts in the `scripts/` directory, such as `explore_simon_nr8_diff.py` or `explore_speck_nr5_diff.py`. These scripts will systematically test input differences for different numbers of rounds and output their silhouette scores to `outputs/explore_results/`.
2.  **Selection Phase:** Review the text files in `outputs/explore_results/` to identify the input differences that achieved the highest silhouette scores.
3.  **Training Phase:** Run the corresponding training scripts for the promising differences, such as `train_speck_nr5_explored_diff_hw2.py` or `train_simon_nr8_left.py`. These will train the neural distinguishers and save the models in `outputs/freshly_trained_nets/`.
4.  **Evaluation Phase:** Open `notebooks/check_accuracy.ipynb` and modify the paths to point to your freshly generated `.p` history files. Execute the notebook to verify the final accuracy of the trained neural distinguishers.

---

## Notes

*   This repository preserves the original research implementation and experimental logic.
*   The recent refactoring only reorganized the project structure to improve readability and maintainability.
*   **No algorithmic behavior has been intentionally changed.** The underlying mathematics, neural network architecture, and cipher implementations remain exactly as originally published.

---

## Future Improvements

While the current implementation correctly reflects the research, the following engineering improvements could be considered for future iterations:

*   **Configuration Management:** Abstracting hardcoded parameters (like rounds, block sizes, and epochs) into dedicated YAML or JSON configuration files.
*   **Experiment Tracking:** Integrating tools like MLflow or Weights & Biases (W&B) to automatically log metrics, hyperparameters, and model artifacts.
*   **Automated Testing:** Implementing unit tests (e.g., using `pytest`) for the `crypto` modules to ensure cipher implementations remain correct across environments.
*   **Packaging:** Adding a `pyproject.toml` or `setup.py` to allow the project to be installed as a standard Python module, simplifying imports across scripts and notebooks.
