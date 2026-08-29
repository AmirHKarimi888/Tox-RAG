from pathlib import Path


# ============================================================
# PROJECT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ============================================================
# DIRECTORIES
# ============================================================

DATA_DIR = PROJECT_ROOT / "data"
PDF_DIR = DATA_DIR / "pdf"
OUTPUT_DIR = DATA_DIR / "output"

MODELS_DIR = PROJECT_ROOT / "models" / "docling"


# ============================================================
# DOCLING
# ============================================================

DOCLING_ARTIFACTS_PATH = MODELS_DIR


# ============================================================
# OFFLINE MODE
# ============================================================

HF_HUB_OFFLINE = "1"


# ============================================================
# VALIDATION
# ============================================================

def validate_paths() -> None:
    """Validate required project directories."""

    if not PDF_DIR.exists():
        raise FileNotFoundError(
            f"PDF directory not found: {PDF_DIR}"
        )

    if not MODELS_DIR.exists():
        raise FileNotFoundError(
            f"Docling model directory not found: {MODELS_DIR}"
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )