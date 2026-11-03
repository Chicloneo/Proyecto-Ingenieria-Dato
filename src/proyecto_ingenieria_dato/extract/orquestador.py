import extraer_medicamentos, preparar_dataset_medicamentos, web_scrapping, enriquecer_catalogo

# uv run orquestador.py
def main():
    extraer_medicamentos.main()
    preparar_dataset_medicamentos.main()
    web_scrapping.main()
    enriquecer_catalogo.main()


if __name__ == "__main__":
    main()