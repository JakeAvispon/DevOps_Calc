FROM python:3.9-slim
WORKDIR /app
RUN pip install flask
COPY . .
EXPOSE 5000
# Se actualizó el nombre del archivo a ejecutar
CMD ["python", "calc.py"]