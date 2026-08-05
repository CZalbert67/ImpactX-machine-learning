"""Convenient local launcher for the ImpactX API and web frontend."""

from __future__ import annotations

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "impactx_ml.api:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
