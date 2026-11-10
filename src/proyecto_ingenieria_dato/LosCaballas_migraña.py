from proyecto_ingenieria_dato.extract import orquestador as extract
from proyecto_ingenieria_dato.transform import orquestador as transform
from proyecto_ingenieria_dato.load import orquestador as load

def main():
    extract.main()
    transform.main()
    load.main()

if __name__ == "__main__":
    main()