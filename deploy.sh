cd pudata
git pull origin main

rm -rf ~/airflow/dags

cp -r ~/pudata/etl/airflow/dags ~/airflow/dags
cp -r ~/pudata/module ~/airflow/dags