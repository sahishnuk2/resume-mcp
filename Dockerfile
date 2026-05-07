FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y texlive-latex-recommended texlive-latex-extra && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev
COPY . .
CMD ["uv", "run", "python", "main.py"]