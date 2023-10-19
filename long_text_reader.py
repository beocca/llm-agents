import os
from typing import List

from langchain.schema import SystemMessage, HumanMessage, AIMessage


PROMPT_SYSTEM = """

"""

PROMPT_MAIN = """

""" 



def read_file(path:str) -> str:
    
    if path.endswith(".pdf"):
        # TODO: read pdf
        pass

    else:
        ext = path.split(".")[-1]
        raise ValueError(f"Invalid filetype: .{ext}")


def chunk_text(text:str, chunk_size=512, overlap=128) -> List[str]:
    raise NotImplementedError()


def main(filepath:str, instructions:str="Read and summarize the document") -> None:
    
    # Get formatted messages
    format_messages = lambda **kwargs: [
        SystemMessage(content=PROMPT_SYSTEM),
        HumanMessage(content=PROMPT_MAIN.fromat(**kwargs))
    ]
    
    # Get text chunks
    text = read_file(filepath)
    chunks = chunk_text(text)

    # Set variables for reading
    current_summary = str()

    # Read the document
    for chunk in chunks:

        # TODO: Format messages
        messages = format_messages()

        # TODO: Create completion

        # TODO: Update variables






if __name__ == "__main__":
    
    filepath = os.path.join("resources", "RISHandbuchBundesnormen.pdf")
    
    main()
    print("...done")
