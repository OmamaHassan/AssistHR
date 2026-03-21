import os
import pymupdf
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

try:
    from mistralai import Mistral
    client = Mistral(api_key=MISTRAL_API_KEY)
except Exception:
    try:
        from mistralai.client import MistralClient
        client = MistralClient(api_key=MISTRAL_API_KEY)
    except Exception:
        client = None
        print("⚠️ Mistral client not initialized")


def is_scanned_pdf(file_path: str) -> bool:
    doc         = pymupdf.open(file_path)
    text_length = sum(len(page.get_text().strip()) for page in doc)
    doc.close()
    return text_length < 10



def extract_pdf_text(file_path: str) -> list:
    doc  = pymupdf.open(file_path)
    docs = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        blocks.sort(key=lambda b: (
            round(b["bbox"][1] / 10) * 10,
            b["bbox"][0]
        ))

        lines_out = []
        font_size = 11
        is_bold   = False

        for block in blocks:
            if block["type"] != 0:
                continue

            block_lines = []

            for line in block["lines"]:
                line_text = ""
                for span in line["spans"]:
                    text      = span["text"].strip()
                    font_size = span["size"]
                    is_bold   = "bold" in span["font"].lower()
                    if not text:
                        continue
                    if line_text:
                        line_text += " "
                    line_text += text

                if line_text.strip():
                    if (font_size > 11 or is_bold) and lines_out:
                        block_lines.append("")
                    block_lines.append(line_text.strip())

            if block_lines:
                lines_out.extend(block_lines)
                lines_out.append("")

        text = "\n".join(lines_out).strip()

        if text.strip():
            docs.append(Document(
                page_content=text,
                metadata={
                    "source": file_path,
                    "page"  : page_num + 1
                }
            ))

    doc.close()
    return docs


def ocr_image_with_mistral(image_path: str) -> str:
    with open(image_path, "rb") as f:
        response = client.ocr(
            model="mistral-ocr-latest",
            file=f
        )
    return response.text


def pdf_to_images(pdf_path: str) -> list:
    doc         = pymupdf.open(pdf_path)
    image_paths = []
    for page_index in range(len(doc)):
        page     = doc.load_page(page_index)
        pix      = page.get_pixmap()
        img_path = f"temp_page_{page_index}.png"
        pix.save(img_path)
        image_paths.append(img_path)
    doc.close()
    return image_paths


def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    images    = pdf_to_images(pdf_path)
    full_text = ""
    for img in images:
        text       = ocr_image_with_mistral(img)
        full_text += text + "\n"
        os.remove(img)
    return full_text


def load_document(file_path: str) -> list:
    ext = file_path.lower().split(".")[-1]

    if ext == "pdf":
        if is_scanned_pdf(file_path):
            print(f"  [Scanned PDF] Using OCR: {file_path}")
            text = extract_text_from_scanned_pdf(file_path)
            return [Document(
                page_content=text,
                metadata={"source": file_path, "page": 1}
            )]
        else:
            print(f"  [Digital PDF] Using PyMuPDF: {file_path}")
            return extract_pdf_text(file_path)

    elif ext == "docx":
        loader = Docx2txtLoader(file_path)
        return loader.load()

    elif ext == "txt":
        with open(file_path, "r",
                  encoding="utf-8",
                  errors="ignore") as f:
            text = f.read()
        return [Document(
            page_content=text,
            metadata={"source": file_path, "page": 1}
        )]

    elif ext in ["jpg", "jpeg", "png"]:
        text = ocr_image_with_mistral(file_path)
        return [Document(
            page_content=text,
            metadata={"source": file_path, "page": 1}
        )]

    else:
        raise ValueError(f"Unsupported file type: .{ext}")