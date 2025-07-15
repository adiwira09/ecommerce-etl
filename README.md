# E-Commerce ETL Dashboard Project

## 📌 Overview
Project ini membangun pipeline ETL untuk dataset transaksi e-commerce menggunakan Apache Airflow & PostgreSQL, lalu divisualisasikan dalam dashboard Metabase.

## 🧱 Tech Stack
- Apache Airflow (ETL & Orchestration)
- PostgreSQL (Data Warehouse)
- Metabase (BI Dashboard)
- Docker Compose

## Folder Struktur
airflow_project/
├── dags/
│   ├── etl_load_csv.py
│   └── transform_clean_transactions.py
├── data/
│   └── Online Retail.csv
├── metabase/
│   └── dashboard.pdf
├── docker-compose.yml
└── README.md

## 🔄 Pipeline Flow

1. **Extract & Load**: CSV → PostgreSQL (`raw_transactions`)
2. **Transform & Clean**: PostgreSQL → PostgreSQL (`clean_transactions`)
3. **Visualize**: Dashboard via Metabase

## 📊 Dashboard Preview

![Dashboard Screenshot](metabase/dashboard_screenshot.png)

## 📈 Example Query Dashboard
- Total Revenue
- Revenue per Country
- Produk Terlaris
- Revenue Harian

## ▶️ How to Run
```bash
docker compose up airflow-init
docker compose up -d
```
Airflow Web Server Access : http://localhost:8080
Metabase Access : http://localhost:3000