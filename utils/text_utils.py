def chunk_text(text, chunk_size=500, overlap=50):
    """
    Divide el texto en fragmentos con solapamiento para mantener el contexto.
    
    :param text: Texto completo a dividir
    :param chunk_size: Cantidad de caracteres por chunk
    :param overlap: Cantidad de caracteres que se repiten entre chunks
    :return: Lista de fragmentos de texto
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
