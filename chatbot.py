import os

from backend.ingest import ingest_document
from backend.rag_engine import ask_document


DATA_FOLDER = "data"
VECTOR_FOLDER = "vector_store"


def list_pdfs():

    pdfs = []

    if not os.path.exists(DATA_FOLDER):

        os.makedirs(DATA_FOLDER)

    for file in os.listdir(DATA_FOLDER):

        if file.lower().endswith(".pdf"):

            pdfs.append(file)

    return pdfs


def select_pdf():

    pdfs = list_pdfs()

    if len(pdfs) == 0:

        print("\nNo PDFs found in data folder.")
        print("Add PDFs to the data folder and try again.")

        return None

    print("\nAvailable PDFs:\n")

    for i, pdf in enumerate(pdfs, start=1):

        print(f"{i}. {pdf}")

    while True:

        try:

            choice = int(
                input("\nSelect PDF Number: ")
            )

            if 1 <= choice <= len(pdfs):

                return pdfs[choice - 1]

            print("Invalid choice.")

        except ValueError:

            print("Enter a valid number.")


def create_or_load_vector_store(pdf_name):

    document_id = pdf_name.replace(
        ".pdf",
        ""
    )

    index_path = (
        f"{VECTOR_FOLDER}/{document_id}/index.faiss"
    )

    if os.path.exists(index_path):

        print(
            "\nVector Store Found."
        )

        return document_id

    print(
        "\nVector Store Not Found."
    )

    print(
        "Creating Vector Store..."
    )

    pdf_path = (
        f"{DATA_FOLDER}/{pdf_name}"
    )

    ingest_document(
        pdf_path,
        document_id
    )

    print(
        "\nVector Store Created."
    )

    return document_id


def chat(document_id):

    print("\n" + "=" * 60)
    print("CHAT STARTED")
    print("Type 'exit' to quit")
    print("=" * 60)

    while True:

        question = input(
            "\nYou: "
        )

        if question.lower() == "exit":

            print(
                "\nGoodbye."
            )

            break

        try:

            result = ask_document(
                document_id,
                question
            )

            print("\nBot:")
            print("-" * 60)

            print(
                result["answer"]
            )

            print("\nSources:")

            for source in result["sources"]:

                print(
                    f"Chunk {source['chunk_id']} | "
                    f"{source['source']}"
                )

        except Exception as e:

            print(
                f"\nError: {e}"
            )


def main():

    print("\nRAG FOX CLI")

    pdf_name = select_pdf()

    if pdf_name is None:

        return

    document_id = (
        create_or_load_vector_store(
            pdf_name
        )
    )

    chat(document_id)


if __name__ == "__main__":

    main()