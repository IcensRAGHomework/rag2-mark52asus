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

    # 初步按行分割文本
    lines = full_text.split("\n")

    final_chunks = []
    buffer = []
    in_article = False  # 用來追蹤是否處於條文的內容中

    for line in lines:
        line = line.strip()  # 去除多餘空白
        if not line:
            continue  # 跳過空行

        # 合併「法規名稱」和「修正日期」
        if "法規名稱：" in line or "修正日期：" in line:
            buffer.append(line)
            continue

        # 如果遇到章節標題
        if line.startswith("第") and "章" in line:
            if buffer:
                final_chunks.append("\n".join(buffer).strip())  # 儲存前面的內容
                buffer = []
            final_chunks.append(line)  # 單獨儲存章節標題
            in_article = False  # 重置條文追蹤狀態
            continue

        # 如果遇到條文標題
        if line.startswith("第") and "條" in line:
            # 檢查是否為數字條文或帶有附加標記的條文
            if re.match(r"^第\s*\d+(-\d+)?\s*條", line):  # 匹配數字條文或「-1」形式的條文
                if buffer:
                    final_chunks.append("\n".join(buffer).strip())  # 儲存前面的條文內容
                    buffer = []
                buffer.append(line)  # 開始新的條文
                in_article = True  # 標記進入條文內容
                continue

        # 條文的內容，繼續追加到當前 buffer
        buffer.append(line)

    # 儲存最後剩餘的內容
    if buffer:
        final_chunks.append("\n".join(buffer).strip())

    # 輸出每個 chunk 的詳細內容以供檢查 (僅輸出前 5 個)
    for i, chunk in enumerate(final_chunks[:114]):
        print(f"Chunk {i+1}:\n{chunk}\n{'-'*80}")

    # 回傳 chunks 數量
    return len(final_chunks)
if __name__ == '__main__':
    # 讀取PDF文件
    #q1_pdf = "./OpenSourceLicenses.pdf"  # 替換成你的PDF文件路徑
    #response = hw02_1(q1_pdf)
    response = hw02_2(q2_pdf)
    pprint(response)
