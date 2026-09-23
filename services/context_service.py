def build_context(results):
    context_parts = []

    for index, result in enumerate(results, start=1):

        source = result["source"]
        chunk_index = result["chunk_index"]
        text = result["text"]

        context_part = (
            f"[Source {index}]\n"
            f"File: {source}\n"
            f"Chunk: {chunk_index}\n\n"
            f"{text}"
        )

        context_parts.append(context_part)

    context = "\n\n---\n\n".join(context_parts)

    return context