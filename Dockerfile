FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml .
COPY src/ ./src/
RUN python -m pip wheel --no-cache-dir --no-deps --wheel-dir /wheels .

FROM python:3.12-slim
RUN groupadd -r impactx && useradd -r -g impactx impactx
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels
USER impactx
WORKDIR /home/impactx
CMD ["python", "-c", "import impactx_ml; print(impactx_ml.__version__)"]
