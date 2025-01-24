from rich import print as pprint

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
    pass

if __name__ == '__main__':
    # 讀取PDF文件
    q1_pdf = "./OpenSourceLicenses.pdf"  # 替換成你的PDF文件路徑
    #q1_pdf = "./綠色能源的現況與未來發展趨勢之探索.pdf"  # 替換成你的PDF文件路徑
    response = hw02_1(q1_pdf)
    pprint(response)
