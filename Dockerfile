# Usa uma imagem base Python oficial leve
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que a aplicação Flask vai rodar
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
