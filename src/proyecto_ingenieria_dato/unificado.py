from .extract import web_scrapping
from .extract import preparar_dataset_medicamentos
from .extract import extraer_medicamentos
from .extract import enriquecer_catalogo
from .transform import contracts
from .transform import kmeans
from .transform import transform
from .load import kpis
from .load import load
from .load.KPIs import KPI_1
from .load.KPIs import KPI_2
from .load.KPIs import KPI_3
from .load.KPIs import KPI_4
from .load.KPIs import KPI_5
from .load.KPIs import KPI_extra 

def main():
    extraer_medicamentos.main()
    preparar_dataset_medicamentos.main()
    web_scrapping.main()
    enriquecer_catalogo.main()
    transform.main()
    kmeans.main()
    kpis.main()
    load.main()
    KPI_1
    KPI_2
    KPI_3
    KPI_4
    KPI_5
    KPI_extra


if __name__ == "__main__":
    main()