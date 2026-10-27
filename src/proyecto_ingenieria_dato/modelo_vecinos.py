#A terminar despues


import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

RANDOM_STATE = 42


def separar_variables(
    datos: pd.DataFrame,
    columna_objetivo: str,
    columnas_a_excluir: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.Series]:
    """Separa X e y; decidir objetivo y exclusiones al revisar el Excel."""
    if columna_objetivo not in datos.columns:
        raise ValueError(f"No existe la columna objetivo {columna_objetivo!r}.")

    columnas_a_excluir = columnas_a_excluir or []
    X = datos.drop(columns=[columna_objetivo, *columnas_a_excluir], errors="ignore")
    y = datos[columna_objetivo]
    return X, y


def crear_pipeline(
    variables_numericas: list[str],
    variables_nominales: list[str],
    variables_ordinales: list[str],
    categorias_ordinales: list[list[str]],
) -> Pipeline:

    # TODO: clasificar las columnas del Excel y definir el orden ordinal, si aplica.
    transformadores = []

    if variables_numericas:
        transformadores.append(
            (
                "numeric",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                variables_numericas,
            )
        )

    if variables_nominales:
        transformadores.append(
            (
                "nominal",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                variables_nominales,
            )
        )

    if variables_ordinales:
        transformadores.append(
            (
                "ordinal",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "encoder",
                            OrdinalEncoder(
                                categories=categorias_ordinales,
                                handle_unknown="use_encoded_value",
                                unknown_value=-1,
                            ),
                        ),
                        ("scaler", StandardScaler()),
                    ]
                ),
                variables_ordinales,
            )
        )

    if not transformadores:
        raise ValueError("Hay que indicar al menos una variable predictora.")

    preprocesador = ColumnTransformer(transformers=transformadores)
    return Pipeline(
        [
            ("preprocessing", preprocesador),
            ("model", KNeighborsRegressor()),
        ]
    )


def entrenar_y_evaluar(
    X: pd.DataFrame,
    y: pd.Series,
    pipeline: Pipeline,
) -> tuple[GridSearchCV, dict[str, float]]:
    """Busca hiperparámetros y evalúa el mejor modelo en el conjunto de test."""
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )

    # TODO: ajustar vecinos y número de particiones al tamaño del Excel.
    busqueda = GridSearchCV(
        estimator=pipeline,
        param_grid={
            "model__n_neighbors": [3, 5, 7, 11],
            "model__weights": ["uniform", "distance"],
            "model__p": [1, 2],
        },
        scoring="neg_root_mean_squared_error",
        cv=5,
        n_jobs=-1,
        return_train_score=True,
    )
    busqueda.fit(X_train, y_train)

    predicciones = busqueda.predict(X_test)
    metricas = {
        "rmse": mean_squared_error(y_test, predicciones) ** 0.5,
        "mae": mean_absolute_error(y_test, predicciones),
        "r2": r2_score(y_test, predicciones),
    }
    return busqueda, metricas


