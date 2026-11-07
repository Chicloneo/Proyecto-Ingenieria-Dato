-- Ranking de precios por grupo
CREATE OR REPLACE VIEW Ranking_precios_por_grupo AS
SELECT 
    nombre, forma_farmaceutica, precio_venta_publico_iva,
    DENSE_RANK() OVER ( -- Precios empatados comparten posición
        PARTITION BY forma_farmaceutica 
        ORDER BY precio_venta_publico_iva DESC
    ) AS `Posición en su categoría`
FROM medicamentos;