# Mortalidad y Esperanza de Vida en la Comunitat Valenciana (2010-2023)

## Proyecto de Visualización de Datos

**Autor:** Cristóbal Eduardo Aguilar Gallardo  
**Fecha:** Enero 2026  
**Asignatura:** Visualización de Datos - Práctica 2

---

## Descripción

Este proyecto analiza los indicadores de **mortalidad** y **esperanza de vida a los 65 años** en la Comunitat Valenciana durante el período 2010-2023. El análisis se centra en responder 6 preguntas de investigación clave mediante visualizaciones interactivas.

### Dataset

- **Fuente:** [Portal Estadístico de la Generalitat Valenciana](https://pegv.gva.es/) - Conselleria de Sanitat
- **Registros:** 5.880
- **Variables:** 12
- **Período Mortalidad:** 2010-2023 (14 años)
- **Período Esperanza de Vida:** 2010-2022 (13 años)
- **Cobertura:** 24 departamentos de salud, 3 provincias
- **Indicador:** Tasa Ajustada por Edad (TAE) por 100.000 habitantes
- **Licencia:** CC-BY / Dominio público

---

## Preguntas de Investigación

1. ¿Cómo ha evolucionado la mortalidad general y cuál fue el impacto del COVID-19?
2. ¿Cuál es la jerarquía de las principales causas de mortalidad?
3. ¿Existen diferencias significativas en mortalidad y esperanza de vida entre hombres y mujeres?
4. ¿Qué disparidades territoriales existen entre los departamentos de salud?
5. ¿Cuál es la tendencia específica de la mortalidad por suicidio?
6. ¿Existe correlación entre las tasas de mortalidad y la esperanza de vida?

---

##  Hallazgos Principales

| Indicador | Valor | Interpretación |
|-----------|-------|----------------|
| Mortalidad 2023 | 819.88 por 100.000 | Mínimo histórico (**-10.0%** vs 2010) |
| Esperanza de vida (2022) | 20.6 años (a los 65) | Promedio ambos sexos |
| Brecha de género | 3.8 años | Mujeres viven más (22.5 vs 18.7) |
| Impacto COVID-19 | +3.2% | Exceso mortalidad 2021 vs pre-COVID |
| Tendencia suicidio | **+11.2%** | Única causa en aumento |
| Disparidad territorial | 24.5% | Entre Doctor Peset (783.1) y Ribera (975.2) |

### Cambios por Causa de Mortalidad (2010-2023)

| Causa | Tasa Promedio | Cambio |
|-------|---------------|--------|
| Cáncer | 228.8 | -8.1% |
| Cardiopatía Isquémica | 74.8 | **-36.0%** |
| Enf. Cerebrovascular | 57.1 | **-44.2%** |
| Suicidio | 7.6 | **+11.2%** ⚠️ |

### Ratios de Género (Hombres/Mujeres)

| Causa | Ratio |
|-------|-------|
| Suicidio | **3.11x** |
| Cardiopatía Isquémica | 2.29x |
| Cáncer | 2.08x |
| Mortalidad General | 1.58x |
| Enf. Cerebrovascular | 1.22x |

---

##  Estructura del Repositorio

```
├── README.md                           # Este archivo
├── data/
│   ├── raw/                            # Datos originales de Conselleria
│   │   ├── esperanza-de-vida-a-los-65-en-la-comunitat-valenciana.csv
│   │   ├── tae-mortalidad-general-en-la-comunitat-valenciana.csv
│   │   ├── tae-mortalidad-cancer-en-la-comunitat-valenciana.csv
│   │   ├── tae-mortalidad-cardiopatia-isquemica-en-la-comunitat-valenciana.csv
│   │   ├── tae-mortalidad-enfermedad-cerebrovascular-en-la-comunitat-valenciana.csv
│   │   └── tae-mortalidad-suicidio-en-la-comunitat-valenciana.csv
│   └── processed/
│       └── mortalidad_esperanza_vida_cv.csv  # Dataset consolidado
├── codigo/
│   └── generar_figuras.py              # Script Python para figuras estáticas
├── figuras/
│   ├── fig1_evolucion_mortalidad_general.png
│   ├── fig2_jerarquia_causas_mortalidad.png
│   ├── fig3_evolucion_causas_especificas.png
│   ├── fig4_disparidad_genero_ratio.png
│   ├── fig5_comparativa_sexo_causa.png
│   ├── fig6_esperanza_vida_genero.png
│   ├── fig7_ranking_departamentos.png
│   ├── fig8_heatmap_departamentos.png
│   ├── fig9_tendencia_suicidio.png
│   ├── fig10_scatter_correlacion.png
│   ├── fig11_comparativa_provincias.png
│   ├── fig12_impacto_covid.png
│   └── fig13_dashboard_resumen.png
├── docs/
│   ├── GUION_VIDEO.md                  # Guion del vídeo de presentación
│   └── JUSTIFICACION_VISUAL.md         # Justificación de codificaciones
└── dashboard/
    └── index.html                      # Dashboard interactivo
```

---

##  Requisitos

```bash
pip install pandas matplotlib seaborn numpy scipy
```

---

##  Uso

### Generar todas las figuras:

```bash
cd codigo
python generar_figuras.py
```

### Ver el dashboard interactivo:

Abrir `dashboard/index.html` en un navegador o acceder al enlace publicado.

---

##  Visualizaciones

### Figura 1: Evolución Temporal
![Evolución Mortalidad](figuras/fig1_evolucion_mortalidad_general.png)

### Figura 13: Dashboard Resumen
![Dashboard](figuras/fig13_dashboard_resumen.png)

---

##  Codificaciones Visuales

| Elemento | Codificación | Justificación |
|----------|--------------|---------------|
| Series temporales | Gráfico de líneas | Expresividad para datos continuos |
| Comparación por sexo | Colores azul/morado | Convención y efectividad |
| Disparidades territoriales | Heatmap + barras | Patrones bidimensionales |
| Correlaciones | Scatter plot (624 puntos) | Estándar para relaciones bivariadas |
| Período COVID | Sombreado destacado | Destaque visual del período crítico |

---


##  Dashboard Interactivo

https://practica-de-visualizacion-2026.vercel.app/

---

##  Fuentes de Datos

Todos los datos provienen del **Portal Estadístico de la Generalitat Valenciana** (Conselleria de Sanitat Universal i Salut Pública):

- [Portal Estadístico GVA](https://pegv.gva.es/)
- [Conselleria de Sanitat](https://www.san.gva.es/)

### Nota Metodológica

- Los datos de **esperanza de vida** están disponibles hasta 2022 (no hay datos de 2023 en la fuente oficial).
- El scatter de correlación incluye **624 observaciones** (24 departamentos × 13 años × 2 sexos).
- La correlación Mortalidad vs Esperanza de Vida es **r = -0.986** (p < 0.001).

---

##  Licencia

Este proyecto está bajo licencia MIT. Los datos originales son de dominio público (CC-BY).

---

##  Contacto

**Cristóbal Eduardo Aguilar Gallardo**  
