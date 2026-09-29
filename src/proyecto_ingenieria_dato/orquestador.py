import proyecto_ingenieria_dato.extraer_medicamentos as extraer_medicamentos
import proyecto_ingenieria_dato.preparar_dataset_medicamentos as preparar_dataset_medicamentos
import proyecto_ingenieria_dato.web_scrapping as web_scrapping
import proyecto_ingenieria_dato.enriquecer_catalogo as enriquecer_catalogo

def main():
    extraer_medicamentos.main()
    preparar_dataset_medicamentos.main()
    web_scrapping.main()
    enriquecer_catalogo.main()


if __name__ == "__main__":
    main()