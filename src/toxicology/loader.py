"""
loader.py

Load and convert toxicology PDF documents using Docling.

This module is intentionally responsible only for document loading.
Model downloads are handled separately by:

    scripts/setup_models.py

The loader always uses the project's local Docling artifacts so that
PDF processing can be performed offline.
"""

from __future__ import annotations

import os
from pathlib import Path

from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
)
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend


# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------

# loader.py is located in:
#     p4/src/toxicology/
#
# Therefore:
#     parents[2] -> p4/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

PDF_DIR = PROJECT_ROOT / "data" / "pdf"
MODELS_DIR = PROJECT_ROOT / "models" / "docling"


# ---------------------------------------------------------------------
# Offline configuration
# ---------------------------------------------------------------------

# Prevent Docling/Hugging Face from trying to download missing models.
os.environ["HF_HUB_OFFLINE"] = "1"


# ---------------------------------------------------------------------
# Converter creation
# ---------------------------------------------------------------------

def create_converter() -> DocumentConverter:
    """
    Create a Docling converter configured to use local model artifacts.

    The model directory is passed explicitly through artifacts_path,
    which keeps model discovery independent of the current working
    directory.
    """

    if not MODELS_DIR.is_dir():
        raise FileNotFoundError(
            f"Docling model directory was not found:\n{MODELS_DIR}"
        )

    pipeline_options = PdfPipelineOptions(
        artifacts_path=MODELS_DIR,
    )

    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=PyPdfiumDocumentBackend,
            )
        }
    )


# ---------------------------------------------------------------------
# PDF loading
# ---------------------------------------------------------------------

def load_pdf(pdf_path: str | Path):
    """
    Convert one PDF into a DoclingDocument.

    Parameters
    ----------
    pdf_path:
        Path to the PDF file.

    Returns
    -------
    DoclingDocument
        The converted Docling document.

    Raises
    ------
    FileNotFoundError
        If the PDF does not exist.
    ValueError
        If the supplied file is not a PDF.
    """

    pdf_path = Path(pdf_path).resolve()

    if not pdf_path.is_file():
        raise FileNotFoundError(
            f"PDF file was not found:\n{pdf_path}"
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            f"Expected a PDF file, got:\n{pdf_path}"
        )

    converter = create_converter()

    result = converter.convert(pdf_path)

    return result.document


# ---------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------

def load_pdf_from_data(filename: str):
    """
    Load a PDF located inside data/pdf/.

    Example
    -------
    document = load_pdf_from_data("Stacey.pdf")
    """

    return load_pdf(PDF_DIR / filename)


# ---------------------------------------------------------------------
# Simple command-line test
# ---------------------------------------------------------------------

if __name__ == "__main__":
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in:\n{PDF_DIR}"
        )

    print(f"Project : {PROJECT_ROOT}")
    print(f"Models  : {MODELS_DIR}")
    print(f"PDF     : {pdf_files[0]}")
    print()

    document = load_pdf(pdf_files[0])

    print("PDF loaded successfully.")
    print(f"Pages   : {len(document.pages)}")