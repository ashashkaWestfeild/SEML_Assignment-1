# Loan Underwriting & Credit Risk Service (Group 84)

This repository contains the complete, production-grade implementation of the **Loan Approval Risk Assessment Service**, designed for automated consumer lending credit risk evaluation. 

The project applies **Software Engineering for ML (SE4ML)** best practices, integrating **GR4ML requirements modeling** and **Sculley's "Hidden Technical Debt" architectural framework** using a **Pipe-and-Filter design pattern**.

---

## 📂 Project Structure

```
├── README.md
├── requirements.txt
├── .gitignore
├── configs/
│   └── config.yaml               # Externalized system and model thresholds
├── data/
│   ├── generate_data.py          # Synthetic loan data generator
│   └── loan_data.csv             # 5,000 records of demographic & credit data
├── app/
│   ├── __init__.py
│   ├── config.py                 # PyYAML-based configuration management
│   ├── schemas.py                # Pydantic input/output schemas (robustness boundary)
│   ├── pipeline.py              # Pipe-and-Filter execution engine
│   ├── logger.py                 # Structured JSON logger & runtime timers
│   ├── main.py                   # FastAPI serving microservice
│   └── model.pkl                 # Serialization of trained RandomForest model
├── training/
│   ├── __init__.py
│   ├── step1_notebook.py         # Baseline RandomForest training pipeline
│   └── step2_mlflow_train.py     # MLOps instrumentation script with MLflow tracking
├── tests/
│   ├── __init__.py
│   └── test_quality_attrs.py     # Quality attribute verification test suite
├── diagrams/
│   ├── gr4ml_business_view.png   # GR4ML Business modeling view
│   ├── gr4ml_analytics_design_view.png  # GR4ML Analytics design view
│   ├── gr4ml_data_prep_view.png  # GR4ML Data preparation workflow view
│   └── system_architecture.png   # Comprehensive system component connections
├── Group_84.ipynb                # Executed Jupyter Notebook report
└── Group_84.pdf                  # Formatted PDF publication-ready report
```

---

## 🏗️ Architecture Design & Patterns

### **1. Pipe-and-Filter Pattern**
To ensure clean isolation, testability, and swappability of logic, the runtime prediction sequence is structured as a series of decoupled Filters connected by Pipes:
* **Filter 1 (validate_input):** Validates business constraints on demographic parameters (e.g., checks that requested loan amount is <= 500% of annual income).
* **Filter 2 (extract_features):** Generates derived financial metrics (Net Worth, Debt-to-Income) and prepares feature vectors.
* **Filter 3 (run_model):** Invokes model estimation and applies classification thresholds.
* **Filter 4 (format_response):** Maps the default probability to structured risk tiers (LOW/MEDIUM/HIGH) and packages it into the output schema.

### **2. Microservices Serving & Event-Driven Monitoring**
* The pipeline is wrapped in a containerized-ready **FastAPI** service.
* Application metrics (e.g. latency, credit score, approval status) are pushed asynchronously in a **structured JSON log format** to stdout, mimicking integrations with logging aggregation agents (Elastic/Splunk).
* Exposes a `/health` endpoint for orchestrators (Kubernetes) to run active liveness/readiness checks.

---

## ⚙️ Quick Start

### **1. Environment Setup**
Install all dependencies listed in the `requirements.txt`:
```bash
pip install -r requirements.txt
```

### **2. Data Generation**
Generate a synthetic dataset of 5,000 credit profiles matching standard banking distributions:
```bash
python data/generate_data.py
```

### **3. Model Training**
Train the Random Forest classifier and output the serialized binary file (`app/model.pkl`):
```bash
python training/step1_notebook.py
```

To run training with MLOps metrics and parameter logging to MLflow:
```bash
python training/step2_mlflow_train.py
```

### **4. Run Quality Tests**
Execute the unit test suite verifying the 4 key quality attributes (**Robustness, Reliability, Performance, Maintainability**):
```bash
python tests/test_quality_attrs.py
```

### **5. Run FastAPI Serving App**
Run the production web server locally:
```bash
uvicorn app.main:app --reload --port 8000
```
Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser to interact with the OpenAPI/Swagger documentation.
