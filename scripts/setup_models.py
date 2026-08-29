from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "models" / "docling"


def run(*args: str) -> None:
    subprocess.run(
        [sys.executable, "-m", *args],
        check=True,
    )


def exists(*paths: str) -> bool:
    return all((MODEL_DIR / path).exists() for path in paths)


def download_models() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    os.environ.pop("HF_HUB_OFFLINE", None)

    # Layout
    if not (
        (MODEL_DIR / "docling-project--docling-layout-heron").exists()
        or (MODEL_DIR / "docling-project--docling-layout-heron-onnx").exists()
    ):
        print("Downloading Layout...")
        run(
            "docling.cli.models",
            "download",
            "layout",
            "-o",
            str(MODEL_DIR),
        )

    # TableFormer
    if not (
        MODEL_DIR
        / "docling-project--docling-models"
        / "model_artifacts"
        / "tableformer"
    ).exists():
        print("Downloading TableFormer...")
        run(
            "docling.cli.models",
            "download",
            "tableformer",
            "-o",
            str(MODEL_DIR),
        )

    # RapidOCR English / Torch
    if not exists(
        "RapidOcr/ch_ptocr_mobile_v2.0_cls_mobile.pth",
        "RapidOcr/PP-OCRv6_det_small.pth",
        "RapidOcr/PP-OCRv6_rec_small.pth",
        "RapidOcr/ppocrv6_dict.txt",
    ):
        print("Downloading RapidOCR English...")
        run(
            "docling.cli.models",
            "download",
            "rapidocr",
            "--rapidocr-backend-lang",
            "torch:english",
            "-o",
            str(MODEL_DIR),
        )


def validate() -> None:
    layout = (
        (MODEL_DIR / "docling-project--docling-layout-heron").exists()
        or (MODEL_DIR / "docling-project--docling-layout-heron-onnx").exists()
    )

    tableformer = (
        MODEL_DIR
        / "docling-project--docling-models"
        / "model_artifacts"
        / "tableformer"
    ).exists()

    rapidocr = exists(
        "RapidOcr/ch_ptocr_mobile_v2.0_cls_mobile.pth",
        "RapidOcr/PP-OCRv6_det_small.pth",
        "RapidOcr/PP-OCRv6_rec_small.pth",
        "RapidOcr/ppocrv6_dict.txt",
    )

    if not all((layout, tableformer, rapidocr)):
        raise RuntimeError(
            f"Model setup incomplete.\n"
            f"Model directory: {MODEL_DIR}"
        )


def main() -> None:
    print(f"Project : {PROJECT_ROOT}")
    print(f"Models  : {MODEL_DIR}")

    download_models()
    validate()

    print("\nModel setup complete.")
    print(f"Artifacts: {MODEL_DIR}")


if __name__ == "__main__":
    main()