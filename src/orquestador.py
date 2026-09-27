import extraer_medicamentos
import preparar_dataset_medicamentos
import web_scrapping
import enriquecer_catalogo

def main():
    extraer_medicamentos.main()
    preparar_dataset_medicamentos.main()
    web_scrapping.main()
    enriquecer_catalogo.main()


if __name__ == "__main__":
    main()