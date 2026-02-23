## README

This project implements a simple ETL pipeline that extracts automotive listings
from the Lalafo REST API, processes the data, and exports structured Excel datasets.

The pipeline consists of two main parts:

1. Data extraction from API
2. Data processing and normalization

### Technologies

- Python
- Requests
- Pandas
- Matplotlib
- ExcelWriter (openpyxl)

### Run
pip install -r requirements.txt

## System Architecture

```mermaid
flowchart TD

subgraph External Source
    API[Lalafo REST API]
end

subgraph Extraction Layer
    EX[lalafo_parser.py]
    RAW[Brand-Level Raw Excel Files]
end

subgraph Processing Layer
    PR[dataset_processing.py]
    AGG[Dataset Aggregation]
    CLEAN[Cleaning & Normalization]
    IMP[Statistical Imputation]
end

subgraph Outputs
    FINAL[Processed Excel Dataset]
    SHOW[Preview CSV & Charts]
end

API --> EX
EX --> RAW
RAW --> PR
PR --> AGG
AGG --> CLEAN
CLEAN --> IMP
IMP --> FINAL
FINAL --> SHOW
