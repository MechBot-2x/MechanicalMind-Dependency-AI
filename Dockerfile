FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements/base.txt
CMD ["python", "mechmind_cli.py"]
