# 💎 Hermes: Modular Data Mining Tool

> **Refactored V5.0**: Now powered by **FastAPI**, **Hexagonal Architecture**, and **Vanilla JS**.

Hermes is a powerful, modular data mining application designed to perform descriptive statistics, data cleaning, outlier detection, clustering, and interactive visualization on CSV and Excel datasets.

![Hermes UI](file:///home/medalcode/.gemini/antigravity/brain/7cba53f4-27f8-4935-98f6-51a16f5e0069/hermes_new_ui_1768885882639.png)

## 🚀 Key Features

- **Modular Architecture**: Built on Hexagonal Architecture (Ports & Adapters) for maximum maintainability and testability.
- **Modern Web UI**: Custom Dark Theme interface built with HTML5, CSS3, and JavaScript (No more Gradio).
- **FastAPI Backend**: High-performance REST API handling all domain logic.
- **Interactive Visualization**: Charts powered by **Plotly.js** (Zoom, Pan, Hover).
- **Unsupervised Learning**: K-Means Clustering integration.
- **Data Ops**:
  - Missing Value Imputation (Mean, Median, Zero, Drop).
  - Scaling (MinMax, Z-Score).
  - Outlier Detection & Treatment (IQR Method).

## 🛠️ Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/Medalcode/Hermes.git
    cd Hermes
    ```

2.  **Create a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Usage

Run the application using the entry point:

```bash
# Make sure venv is active
python src/main.py
```

Open your browser at **`http://localhost:8000`**.

## 🏗️ Project Structure

```
src/
├── core/                 # Domain Layer (Business Logic)
│   ├── domain_services.py  # Stats, Cleaning, Clustering Logic
│   └── models.py           # Data Classes (Session)
├── adapters/             # Interface Layer
│   ├── api/                # FastAPI Router (Backend)
│   ├── fs/                 # File System Adapter
│   └── visualization/      # Plotting Adapter (Plotly)
└── main.py               # Application Entry Point

static/                   # Frontend Assets (CSS, JS)
templates/                # HTML Templates
tests/                    # Unit Tests
```

## 🧪 Running Tests

Ensure the core logic is working correctly:

```bash
PYTHONPATH=. pytest tests/
```

## 🔄 History

- **V5.0 (Current)**: Full migration to FastAPI + Custom UI. Hexagonal Architecture. Plotly.
- **V4.0**: Refactor to Modular Structure (Gradio).
- **Legacy**: Monolithic script `final_eval3mineria.py`.

---

_Created by Medalcode & Team_
