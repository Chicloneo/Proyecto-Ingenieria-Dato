El objetivo del historial de usuario 1 es obtener todos los datos de todos los medicamentos que se usan para la migraña.

En primer lugar, hacemos una petición __POST__ (con Postman) al centro de información de medicamentos CIMA

```bash
[{
"seccion": "4.1",
"texto": "migraña",
"contiene": 1
}]
```

El resultado es (primeras líneas)

```bash
"totalFilas": 70
"pagina": 1,
"tamanioPagina": 200,
```

Es decir, tenemos 70 medicamentos para combatir la migraña. Si `total_filas` fuera mayor que `200`, habría que modificar el script para que consultara la siguiente página. En este caso todos los medicamentos están en la página 1.

Uno de ellos es, por ejemplo

```bash
"nombre": "ALMOTRIPTAN CINFA 12,5 MG COMPRIMIDOS RECUBIERTOS CON PELICULA EFG"
```

que tiene asociado un número de registro

```bash
"nregistro": "78686"
```

Ahora podemos hacer una petición __GET__ otra url del CIMA para obtener sus datos. Para ello añadimos el parámetro `nregistro = 78686`. La respuesta que nos da es

```bash
{
    "nregistro": "78686",
    "nombre": "ALMOTRIPTAN CINFA 12,5 MG COMPRIMIDOS RECUBIERTOS CON PELICULA EFG",
    "pactivos": "ALMOTRIPTAN",
    "labtitular": "Laboratorios Cinfa S.A.",
    ...
}
```

Pero ahora necesitamos hacer eso para todos los medicamentos. Ello queda reflejado en el archivo `medicamentos_a_xlsx.py`