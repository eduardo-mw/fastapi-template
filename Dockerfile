FROM python:3.12.5-slim

WORKDIR /app

RUN pip install --upgrade pip 

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN rm requirements.txt dev-requirements.txt .dockerignore

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl", "--fail", "http://localhost:5000/health", "||", "exit", "1" ]

RUN groupadd -r fasty && useradd --no-log-init -r -g fasty fasty

RUN chown -R fasty:fasty /app

USER fasty

CMD ["fastapi", "run", "api/main.py"]