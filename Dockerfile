FROM python:3.11.15-slim

WORKDIR /workspace/tech_support_fraud_detection

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -yq chromium chromium-driver fontconfig fonts-noto-cjk fonts-ipafont fonts-ipaexfont
RUN fc-cache -fv

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY main.py .

ENTRYPOINT ["python", "main.py"]