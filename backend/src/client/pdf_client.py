"""
PDF text extraction client wrapper.

Responsibilities:
- validate(file_bytes) -> bool  : Checks if the bytes represent a parseable PDF with >= 1 page
- extract(file_bytes) -> str    : Extracts and concatenates all text from all pages of the PDF
                                  Uses pdfplumber for layout-aware extraction (handles tables/columns)
                                  Falls back to pypdf for simple text-layer PDFs
- Returns empty string if no text is extractable (caller is responsible for raising EMPTY_DOCUMENT)
- Does not persist the file — operates entirely on in-memory bytes
"""
