import os
from dotenv import load_dotenv
from transformers import AutoTokenizer
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling.chunking import HybridChunker
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector

load_dotenv()

COLLECTION_NAME = "syllabus_docs"

def ingest_pdf(url: str, source_name: str = "履修要綱.pdf") -> int:
    """PDFを解析してDBに保存し、チャンク数を返す"""
    print(f"[{source_name}] 解析を開始します...")

    pipeline_options = PdfPipelineOptions()
    pipeline_options.images_scale = 1.0
    pipeline_options.generate_page_images = False
    pipeline_options.generate_picture_images = False

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    # urlにはローカルパスかHTTP URLを渡す
    docling_doc = converter.convert(url).document

    tokenizer = AutoTokenizer.from_pretrained("BEE-spoke-data/cl100k_base")
    chunker = HybridChunker(tokenizer=tokenizer, max_tokens=300)

    langchain_docs = []
    for chunk in chunker.chunk(docling_doc):
        chunk_text = chunker.contextualize(chunk)
        page_no = None
        if chunk.meta.doc_items and chunk.meta.doc_items[0].prov:
            page_no = chunk.meta.doc_items[0].prov[0].page_no

        langchain_docs.append(Document(
            page_content=chunk_text,
            metadata={"source": source_name, "page": page_no},
        ))

    # ★ 関数の中でDBに保存する
    connection_string = os.environ.get("DATABASE_URL")
    PGVector.from_documents(
        embedding=OpenAIEmbeddings(),
        documents=langchain_docs,
        collection_name=COLLECTION_NAME,
        connection=connection_string,
    )

    print(f"解析完了: {len(langchain_docs)} チャンクをDBに保存しました。")
    return len(langchain_docs)