from rich import print as pprint
import re

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import (CharacterTextSplitter, RecursiveCharacterTextSplitter)

q1_pdf = "OpenSourceLicenses.pdf"
q2_pdf = "勞動基準法.pdf"


def hw02_1(q1_pdf):
    # 讀取PDF文件
    loader = PyPDFLoader(q1_pdf)
    documents = loader.load()  # 加載文檔

    # 使用CharacterTextSplitter進行文本分割
    splitter = CharacterTextSplitter(
        separator="\n",  # 默認分隔符，也可根據需求調整
        chunk_size=1000,  # 每個chunk的字符數大小
        chunk_overlap=0   # 無重疊部分
    )
    chunks = splitter.split_documents(documents)  # 分割為多個chunks

    # 獲取最後一個chunk物件
    last_chunk = chunks[-1]

    # 輸出最後一個chunk物件的內容
    print("檔名:", last_chunk.metadata.get("source", "未知"))
    print("頁數:", last_chunk.metadata.get("page", "未知"))
    print("內文:")
    print(last_chunk.page_content)
    return last_chunk

def hw02_2(q2_pdf):
    # 使用 PyPDFLoader 加載 PDF 文件
    loader = PyPDFLoader(q2_pdf)
    documents = loader.load()  # 加載文檔

    # 將所有頁面內容合併為完整文本，避免跨頁問題
    full_text = "\n".join(doc.page_content for doc in documents)

    # 使用 RecursiveCharacterTextSplitter 配置針對章節分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=60,  # 每個 chunk 的最大字數
        chunk_overlap=0,  # 無重疊
        separators=[
            r"\n.*第.*章.*?\n",  # 僅分割章節
            r"第.*(?:\d+-\d+|\d+).*條.*\n"  # 匹配格式：第 x 條或第 x-x 條, # 分割條文 (例如：第 1 條)
        ],
        is_separator_regex=True  # 啟用正則表達式
    )

    # 分割文本
    chunks = text_splitter.split_text(full_text)
    # 測試顯示部分分割結果
    for i, chunk in enumerate(chunks[:-1]):  # 顯示全部chunks
        pprint(f"\nChunk {i + 1}:\n{chunk}")
    
    print(f"總共分割為 {len(chunks)} 個 chunks")
    return len(chunks)

if __name__ == '__main__':
    # 讀取PDF文件
    #q1_pdf = "./OpenSourceLicenses.pdf"  # 替換成你的PDF文件路徑
    #response = hw02_1(q1_pdf)
    response = hw02_2(q2_pdf)
    pprint(response)
