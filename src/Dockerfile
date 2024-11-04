FROM python:latest

COPY requirements.txt . 

RUN pip3 install -r requirements.txt

COPY extract_data.py . 

COPY transform_data.py .

COPY load_data.py .

COPY etl_pipeline.py .

CMD ["python3", "etl_pipeline.py"]