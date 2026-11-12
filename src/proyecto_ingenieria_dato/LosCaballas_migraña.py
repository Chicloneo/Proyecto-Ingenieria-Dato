from proyecto_ingenieria_dato.extract import orquestador as extract
from proyecto_ingenieria_dato.transform import orquestador as transform
from proyecto_ingenieria_dato.load import orquestador as load
import logging, subprocess, sys
from pathlib import Path


# Logging config
LOG_DIR = Path(__file__).parents[2].resolve() / "logs"
LOG_FILE = LOG_DIR / "run.log"

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def execute_process(process: function, name: str):
    logging.info(f"Executing: {name}")
    try:
        process()
        logging.info(f"SUCCESS executing: {name}")
    except Exception as e:
        logging.error(f"ERROR in {name}: {e}")
        raise Exception(f"Critical error in {name}")

def main():
    execute_process(extract.main, "Extract")
    execute_process(transform.main, "Transform")
    execute_process(load.main, "Load")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"Pipeline interrupted: {e}")
        sys.exit(1)




