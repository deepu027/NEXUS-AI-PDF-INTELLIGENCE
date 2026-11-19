import fitz


def extract_pdf_text(pdf_file):
    """Extract selectable text from an uploaded PDF file."""
    try:
        pdf_bytes = pdf_file.getvalue()
        if not pdf_bytes:
            raise ValueError("The uploaded PDF is empty.")

        document = fitz.open(stream=pdf_bytes, filetype="pdf")
        try:
            page_count = len(document)
            pages = [page.get_text("text") for page in document]
            full_text = "\n\n".join(pages).strip()
        finally:
            document.close()

        if not full_text:
            raise ValueError(
                "No selectable text was found. This may be a scanned PDF; "
                "OCR support is not included in this starter project."
            )

        return full_text, page_count

    except Exception as exc:
        if isinstance(exc, ValueError):
            raise
        raise ValueError(f"Could not read this PDF: {exc}") from exc
