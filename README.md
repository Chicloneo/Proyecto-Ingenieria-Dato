# Proyecto de Ingeniería del Dato

Pipeline de extracción, transformación y carga (ETL) de medicamentos. El flujo
completo ejecuta estas etapas en orden:

1. **Extracción:** obtiene y prepara el catálogo de medicamentos.
2. **Transformación:** valida los datos y genera los clústeres.
3. **Carga:** carga los resultados en MySQL y ejecuta las consultas KPI.

## Requisitos

- Docker Desktop (o Docker Engine) con Docker Compose.
- Para ejecutar el proyecto fuera de Docker: Python 3.14 y
  [uv](https://docs.astral.sh/uv/).

## Configuración

Desde la raíz del repositorio, crea un archivo `.env` (no lo subas al
repositorio: está excluido por `.gitignore`) con las credenciales de MySQL:

```dotenv
SQL_USER=root
SQL_PASSWORD=elige-una-contraseña
```

Compose usa `SQL_PASSWORD` para inicializar la contraseña de root en el
contenedor MySQL. La aplicación se conecta al servicio `db`, a la base de datos
`MUIAAp_2026`; por eso `SQL_USER` debe ser `root` con la configuración actual.

## Levantar todo con Docker

En la raíz del proyecto:

```bash
docker compose up --build -d
```

Compose construye la imagen de la aplicación, levanta MySQL y espera a que la
base de datos esté disponible antes de iniciar la aplicación. Esta última
arranca cron, que ejecuta el pipeline completo **una vez por minuto**.

Comandos útiles:

```bash
# Ver el estado de los servicios
docker compose ps

# Seguir los logs de los contenedores
docker compose logs -f

# Seguir el log del pipeline (se guarda también en el host)
tail -f logs/run.log

# Detener los contenedores; conserva los datos de MySQL
docker compose down
```

Los datos de MySQL persisten en el volumen `mysql_data`. Los directorios
`data/`, `images/`, `models/` y `logs/` están compartidos entre el contenedor y
el host, de modo que los ficheros generados se pueden consultar desde el
proyecto.

## Ejecutar el pipeline manualmente

Con los servicios levantados, ejecuta el flujo completo dentro del contenedor:

```bash
docker compose exec app uv run --no-sync python src/proyecto_ingenieria_dato/LosCaballas_migraña.py
```

La aplicación ya lo ejecuta automáticamente cada minuto. Una ejecución manual
puede coincidir con la programada; comprueba `logs/run.log` antes de lanzarla.

También se puede ejecutar una etapa concreta:

```bash
# Extracción
docker compose exec app uv run --no-sync python -m proyecto_ingenieria_dato.extract.orquestador

# Transformación
docker compose exec app uv run --no-sync python -m proyecto_ingenieria_dato.transform.orquestador

# Carga en MySQL y cálculo de KPI
docker compose exec app uv run --no-sync python -m proyecto_ingenieria_dato.load.orquestador
```

Las etapas dependen de los ficheros generados por las anteriores. Para ejecutar
solo transformación o carga, asegúrate de que sus datos de entrada ya existan
en `data/` y de que MySQL esté iniciado para la carga.

## Desarrollo local y notebooks

Para instalar las dependencias con uv:

```bash
uv sync
```

Los notebooks están en `Notebooks/` y se pueden abrir desde VS Code con el
entorno virtual creado por uv. Para el pipeline completo, se recomienda usar
Docker: la configuración de base de datos de la aplicación apunta al nombre de
servicio `db`, disponible en la red de Compose.
