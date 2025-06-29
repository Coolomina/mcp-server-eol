FROM python:3.11-slim
WORKDIR /app

RUN pip install --no-cache-dir pdm

COPY pyproject.toml pdm.lock* README.md ./

ENV PDM_VENV_IN_PROJECT=false
ENV PDM_USE_VENV=false

RUN pdm install --prod --no-editable --no-self

WORKDIR /app

COPY src/ ./src/

ENV PYTHONPATH="/app/src:/app/__pypackages__/3.11/lib:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
CMD python -c "import mcp_server_eol.client; print('OK')" || exit 1

COPY config.json ./
CMD ["python", "-m", "mcp_server_eol.server"]
