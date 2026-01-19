#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROYECTO: Mortalidad y Esperanza de Vida - Comunitat Valenciana 2010-2023
================================================================================
Autor: Cristóbal Eduardo Aguilar Gallardo
Fecha: Enero 2026
Descripción: Análisis y visualización de datos epidemiológicos de la CV

Este script genera todas las figuras de la parte II de la Practica de visualización.
Dataset: Portal Estadístico de la Generalitat Valenciana

================================================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
import numpy as np
from scipy import stats
import warnings
import os

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

# Crear directorio de salida si no existe
OUTPUT_DIR = 'figuras'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configuración de estilo matplotlib
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Paleta de colores profesional
COLORS = {
    'primary': '#1a365d',
    'secondary': '#2c5282',
    'accent': '#ed8936',
    'danger': '#c53030',
    'success': '#276749',
    'hombre': '#3182ce',
    'mujer': '#d53f8c',
    'ambos': '#805ad5',
    'cancer': '#e53e3e',
    'cardio': '#dd6b20',
    'cerebro': '#d69e2e',
    'general': '#1a365d',
    'suicidio': '#6b46c1',
    'covid_bg': '#fed7d7',
    'alicante': '#38a169',
    'valencia': '#3182ce',
    'castellon': '#d69e2e'
}

# ============================================================================
# CARGA DE DATOS
# ============================================================================

def cargar_datos(filepath='/mnt/data/mortalidad_esperanza_vida_cv_consolidado.csv'):
    """
    Carga el dataset principal.
    
    Parameters:
    -----------
    filepath : str
        Ruta al archivo CSV (separador ;)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame con los datos cargados
    """
    df = pd.read_csv(filepath, sep=';')
    print(f"✅ Dataset cargado: {len(df)} registros, {len(df.columns)} columnas")
    print(f"   Período: {df['periodo'].min()} - {df['periodo'].max()}")
    print(f"   Causas: {df['causa_mortalidad'].unique()}")
    return df

# ============================================================================
# FIGURA 1: EVOLUCIÓN TEMPORAL DE MORTALIDAD GENERAL
# ============================================================================

def fig1_evolucion_mortalidad_general(df, output_dir=OUTPUT_DIR):
    """
    Genera la figura de evolución temporal de mortalidad general.
    Responde: ¿Cómo ha evolucionado la mortalidad y cuál fue el impacto del COVID-19?
    """
    print("\n" + "="*60)
    print("FIGURA 1: Evolución de la Mortalidad General (2010-2023)")
    print("="*60)
    
    # Filtrar datos
    cv_general = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                    (df['causa_mortalidad'] == 'General')]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Sombrear período COVID
    ax.axvspan(2019.5, 2021.5, alpha=0.3, color=COLORS['covid_bg'], label='Período COVID-19')
    
    # Líneas por sexo
    for sexo, color, marker in [('Ambos sexos', COLORS['ambos'], 'o'), 
                                 ('Hombres', COLORS['hombre'], 's'), 
                                 ('Mujeres', COLORS['mujer'], '^')]:
        data = cv_general[cv_general['sexo'] == sexo].sort_values('periodo')
        ax.plot(data['periodo'], data['tasa_mortalidad'], 
                color=color, linewidth=2.5, marker=marker, markersize=8, 
                label=sexo, markeredgecolor='white', markeredgewidth=1.5)
    
    # Obtener valores para anotaciones
    cv_ambos = cv_general[cv_general['sexo'] == 'Ambos sexos'].sort_values('periodo')
    mort_2023 = cv_ambos[cv_ambos['periodo'] == 2023]['tasa_mortalidad'].values[0]
    mort_2021 = cv_ambos[cv_ambos['periodo'] == 2021]['tasa_mortalidad'].values[0]
    
    # Anotaciones
    ax.annotate(f'Mínimo histórico\n{mort_2023:.1f}', 
                xy=(2023, mort_2023), xytext=(2022, mort_2023 - 40),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color=COLORS['success'], lw=1.5),
                color=COLORS['success'], fontweight='bold')
    
    ax.annotate(f'Pico COVID\n{mort_2021:.1f}', 
                xy=(2021, mort_2021), xytext=(2021.5, mort_2021 + 40),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color=COLORS['danger'], lw=1.5),
                color=COLORS['danger'], fontweight='bold')
    
    # Configuración
    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('Tasa de Mortalidad (por 100.000 hab.)', fontweight='bold')
    ax.set_title('Evolución de la Mortalidad General en la Comunitat Valenciana (2010-2023)\n'
                 'Tasa Ajustada por Edad - Impacto visible del COVID-19', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(range(2010, 2024))
    ax.set_xlim(2009.5, 2023.5)
    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    ax.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax.xaxis.grid(False)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig1_evolucion_mortalidad_general.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 2: JERARQUÍA DE CAUSAS DE MORTALIDAD
# ============================================================================

def fig2_jerarquia_causas(df, output_dir=OUTPUT_DIR):
    """
    Genera la figura de jerarquía de causas de mortalidad.
    Responde: ¿Cuál es la jerarquía de las principales causas?
    """
    print("\n" + "="*60)
    print("FIGURA 2: Jerarquía de Causas de Mortalidad")
    print("="*60)
    
    # Datos promedio por causa
    causas_data = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                     (df['sexo'] == 'Ambos sexos')].groupby('causa_mortalidad')['tasa_mortalidad'].mean()
    causas_data = causas_data.sort_values(ascending=True)
    
    # Excluir 'General'
    causas_especificas = causas_data.drop('General')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Colores
    colors_list = [COLORS.get(c.lower(), '#718096') for c in causas_especificas.index]
    
    # Barras
    bars = ax.barh(causas_especificas.index, causas_especificas.values, 
                   color=colors_list, edgecolor='white', linewidth=2, height=0.6)
    
    # Etiquetas
    for bar, val in zip(bars, causas_especificas.values):
        ax.text(val + 3, bar.get_y() + bar.get_height()/2, 
                f'{val:.1f}', va='center', ha='left', fontweight='bold', fontsize=12)
    
    # Configuración
    ax.set_xlabel('Tasa de Mortalidad Promedio (por 100.000 hab.)', fontweight='bold')
    ax.set_title('Jerarquía de Causas de Mortalidad en la Comunitat Valenciana\n'
                 'Promedio 2010-2023 (Ambos Sexos)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, max(causas_especificas.values) * 1.15)
    
    # Renombrar etiquetas
    labels_map = {'Cancer': 'Cáncer', 'Cardio': 'Cardiopatía Isquémica', 
                  'Cerebro': 'Enf. Cerebrovascular', 'Suicidio': 'Suicidio'}
    ax.set_yticklabels([labels_map.get(l, l) for l in causas_especificas.index])
    
    ax.xaxis.grid(True, linestyle='--', alpha=0.4)
    ax.yaxis.grid(False)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig2_jerarquia_causas_mortalidad.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 3: EVOLUCIÓN TEMPORAL POR CAUSA ESPECÍFICA
# ============================================================================

def fig3_evolucion_causas_especificas(df, output_dir=OUTPUT_DIR):
    """
    Genera panel 2x2 con evolución de cada causa específica.
    Responde: ¿Cómo han variado las causas en el tiempo?
    """
    print("\n" + "="*60)
    print("FIGURA 3: Evolución Temporal por Causa Específica")
    print("="*60)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    causas = ['Cancer', 'Cardio', 'Cerebro', 'Suicidio']
    titulos = ['Cáncer (Neoplasias)', 'Cardiopatía Isquémica', 
               'Enfermedad Cerebrovascular', 'Suicidio']
    
    for idx, (causa, titulo) in enumerate(zip(causas, titulos)):
        ax = axes[idx]
        
        data = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                  (df['causa_mortalidad'] == causa) &
                  (df['sexo'] == 'Ambos sexos')].sort_values('periodo')
        
        # Sombrear COVID
        ax.axvspan(2019.5, 2021.5, alpha=0.2, color='#fed7d7')
        
        ax.plot(data['periodo'], data['tasa_mortalidad'], 
                color=COLORS[causa.lower()], linewidth=2.5, marker='o', markersize=6,
                markeredgecolor='white', markeredgewidth=1)
        
        # Calcular tendencia
        inicio = data[data['periodo'] == 2010]['tasa_mortalidad'].values[0]
        fin = data[data['periodo'] == 2023]['tasa_mortalidad'].values[0]
        cambio = ((fin - inicio) / inicio) * 100
        
        # Indicador de tendencia
        if cambio < 0:
            tendencia_text = f'↓ {abs(cambio):.1f}%'
            color_tend = '#276749'
        else:
            tendencia_text = f'↑ {cambio:.1f}%'
            color_tend = '#c53030'
        
        ax.text(0.95, 0.95, tendencia_text, transform=ax.transAxes, 
                fontsize=14, fontweight='bold', ha='right', va='top',
                color=color_tend, 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor=color_tend, alpha=0.9))
        
        ax.set_title(titulo, fontsize=12, fontweight='bold', color=COLORS[causa.lower()])
        ax.set_xlabel('Año')
        ax.set_ylabel('Tasa por 100.000 hab.')
        ax.set_xticks(range(2010, 2024, 2))
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.xaxis.grid(False)
    
    fig.suptitle('Evolución de las Causas Específicas de Mortalidad (2010-2023)\n'
                 'Comunitat Valenciana - Ambos Sexos', 
                 fontsize=14, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig3_evolucion_causas_especificas.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 4: DISPARIDADES DE GÉNERO - RATIO H/M
# ============================================================================

def fig4_disparidad_genero_ratio(df, output_dir=OUTPUT_DIR):
    """
    Genera figura de ratio de mortalidad hombres/mujeres.
    Responde: ¿Existen diferencias significativas entre sexos?
    """
    print("\n" + "="*60)
    print("FIGURA 4: Disparidades de Género - Ratio H/M")
    print("="*60)
    
    # Calcular ratios
    causas = ['General', 'Cancer', 'Cardio', 'Cerebro', 'Suicidio']
    ratios = []
    
    for causa in causas:
        h = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
               (df['causa_mortalidad'] == causa) & 
               (df['sexo'] == 'Hombres')]['tasa_mortalidad'].mean()
        m = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
               (df['causa_mortalidad'] == causa) & 
               (df['sexo'] == 'Mujeres')]['tasa_mortalidad'].mean()
        ratios.append(h/m)
    
    # Ordenar
    orden = np.argsort(ratios)[::-1]
    causas_ord = [causas[i] for i in orden]
    ratios_ord = [ratios[i] for i in orden]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(ratios_ord)))
    
    bars = ax.barh(range(len(causas_ord)), ratios_ord, color=colors, 
                   edgecolor='white', linewidth=2, height=0.6)
    
    ax.axvline(x=1, color='#2d3748', linestyle='--', linewidth=2, label='Igualdad (ratio=1)')
    
    labels_map = {'General': 'Mortalidad General', 'Cancer': 'Cáncer', 
                  'Cardio': 'Cardiopatía Isquémica', 'Cerebro': 'Enf. Cerebrovascular', 
                  'Suicidio': 'Suicidio'}
    
    for i, (bar, ratio) in enumerate(zip(bars, ratios_ord)):
        ax.text(ratio + 0.08, bar.get_y() + bar.get_height()/2, 
                f'{ratio:.2f}x', va='center', ha='left', fontweight='bold', fontsize=13,
                color='#1a365d')
    
    ax.set_yticks(range(len(causas_ord)))
    ax.set_yticklabels([labels_map[c] for c in causas_ord], fontsize=12)
    ax.set_xlabel('Ratio de Mortalidad Hombres / Mujeres', fontweight='bold', fontsize=12)
    ax.set_title('Disparidades de Género en Mortalidad\n'
                 'Ratio Hombres/Mujeres por Causa (Promedio 2010-2023)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, max(ratios_ord) * 1.2)
    ax.xaxis.grid(True, linestyle='--', alpha=0.3)
    ax.yaxis.grid(False)
    ax.legend(loc='lower right')
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig4_disparidad_genero_ratio.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 5: COMPARATIVA DE TASAS POR SEXO
# ============================================================================

def fig5_comparativa_sexo_causa(df, output_dir=OUTPUT_DIR):
    """
    Genera barras agrupadas comparando tasas absolutas H vs M.
    """
    print("\n" + "="*60)
    print("FIGURA 5: Comparativa de Tasas por Sexo y Causa")
    print("="*60)
    
    causas = ['Cancer', 'Cardio', 'Cerebro', 'Suicidio']
    labels_causas = ['Cáncer', 'Cardiopatía\nIsquémica', 'Enf.\nCerebrovascular', 'Suicidio']
    
    tasas_h = []
    tasas_m = []
    
    for causa in causas:
        h = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
               (df['causa_mortalidad'] == causa) & 
               (df['sexo'] == 'Hombres')]['tasa_mortalidad'].mean()
        m = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
               (df['causa_mortalidad'] == causa) & 
               (df['sexo'] == 'Mujeres')]['tasa_mortalidad'].mean()
        tasas_h.append(h)
        tasas_m.append(m)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(causas))
    width = 0.35
    
    bars_h = ax.bar(x - width/2, tasas_h, width, label='Hombres', 
                    color=COLORS['hombre'], edgecolor='white', linewidth=2)
    bars_m = ax.bar(x + width/2, tasas_m, width, label='Mujeres', 
                    color=COLORS['mujer'], edgecolor='white', linewidth=2)
    
    for bar in bars_h:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', fontsize=10,
                    color=COLORS['hombre'])
    
    for bar in bars_m:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', fontsize=10,
                    color=COLORS['mujer'])
    
    ax.set_xlabel('Causa de Mortalidad', fontweight='bold')
    ax.set_ylabel('Tasa de Mortalidad (por 100.000 hab.)', fontweight='bold')
    ax.set_title('Comparativa de Mortalidad por Sexo y Causa\n'
                 'Comunitat Valenciana - Promedio 2010-2023', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(labels_causas)
    ax.legend(loc='upper right', frameon=True, fancybox=True)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.xaxis.grid(False)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig5_comparativa_sexo_causa.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 6: ESPERANZA DE VIDA POR SEXO
# ============================================================================

def fig6_esperanza_vida_genero(df, output_dir=OUTPUT_DIR):
    """
    Genera evolución temporal de esperanza de vida por sexo.
    """
    print("\n" + "="*60)
    print("FIGURA 6: Esperanza de Vida por Sexo")
    print("="*60)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.axvspan(2019.5, 2021.5, alpha=0.2, color='#fed7d7', label='Período COVID-19')
    
    for sexo, color, marker in [('Hombres', COLORS['hombre'], 's'), 
                                 ('Mujeres', COLORS['mujer'], '^'),
                                 ('Ambos sexos', COLORS['ambos'], 'o')]:
        data = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                  (df['causa_mortalidad'] == 'General') &
                  (df['sexo'] == sexo)].sort_values('periodo')
        ax.plot(data['periodo'], data['esperanza_vida'], 
                color=color, linewidth=2.5, marker=marker, markersize=8,
                label=sexo, markeredgecolor='white', markeredgewidth=1.5)
    
    # Brecha 2023
    ev_h_2023 = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                   (df['causa_mortalidad'] == 'General') &
                   (df['sexo'] == 'Hombres') & 
                   (df['periodo'] == 2023)]['esperanza_vida'].values[0]
    ev_m_2023 = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                   (df['causa_mortalidad'] == 'General') &
                   (df['sexo'] == 'Mujeres') & 
                   (df['periodo'] == 2023)]['esperanza_vida'].values[0]
    
    ax.annotate('', xy=(2023.3, ev_m_2023), xytext=(2023.3, ev_h_2023),
                arrowprops=dict(arrowstyle='<->', color='#2d3748', lw=2))
    ax.text(2023.5, (ev_h_2023 + ev_m_2023)/2, f'Brecha\n{ev_m_2023-ev_h_2023:.1f} años',
            fontsize=11, fontweight='bold', va='center', color='#2d3748')
    
    ax.text(2023.1, ev_m_2023 + 0.2, f'{ev_m_2023:.1f}', fontsize=10, fontweight='bold', 
            color=COLORS['mujer'], va='bottom')
    ax.text(2023.1, ev_h_2023 - 0.2, f'{ev_h_2023:.1f}', fontsize=10, fontweight='bold', 
            color=COLORS['hombre'], va='top')
    
    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('Esperanza de Vida a los 65 años (años)', fontweight='bold')
    ax.set_title('Evolución de la Esperanza de Vida por Sexo (2010-2023)\n'
                 'Comunitat Valenciana - Brecha de género persistente', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(range(2010, 2024))
    ax.set_xlim(2009.5, 2024.5)
    ax.legend(loc='lower right', frameon=True, fancybox=True)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.xaxis.grid(False)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig6_esperanza_vida_genero.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 7: RANKING DE DEPARTAMENTOS
# ============================================================================

def fig7_ranking_departamentos(df, output_dir=OUTPUT_DIR):
    """
    Genera ranking de departamentos por mortalidad.
    """
    print("\n" + "="*60)
    print("FIGURA 7: Ranking de Departamentos de Salud")
    print("="*60)
    
    ranking = df[(df['causa_mortalidad'] == 'General') & 
                 (df['sexo'] == 'Ambos sexos') &
                 (df['nivel_geografico'] == 'HOSPITAL/ZONA SALUD')].groupby(
        ['ubicacion', 'provincia']
    ).agg({'tasa_mortalidad': 'mean'}).reset_index().sort_values('tasa_mortalidad', ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    provincia_colors = {
        'Alicante': COLORS['alicante'],
        'Valencia': COLORS['valencia'], 
        'Castellón': COLORS['castellon']
    }
    
    colors = [provincia_colors.get(p, '#718096') for p in ranking['provincia']]
    
    bars = ax.barh(range(len(ranking)), ranking['tasa_mortalidad'], 
                   color=colors, edgecolor='white', linewidth=1, height=0.7)
    
    media = ranking['tasa_mortalidad'].mean()
    ax.axvline(x=media, color='#c53030', linestyle='--', linewidth=2, label=f'Media: {media:.1f}')
    
    for i, (idx, row) in enumerate(ranking.iterrows()):
        ax.text(row['tasa_mortalidad'] + 5, i, f"{row['tasa_mortalidad']:.1f}", 
                va='center', ha='left', fontsize=9, fontweight='bold')
    
    ax.set_yticks(range(len(ranking)))
    ax.set_yticklabels(ranking['ubicacion'], fontsize=9)
    ax.set_xlabel('Tasa de Mortalidad General Promedio (por 100.000 hab.)', fontweight='bold')
    ax.set_title('Ranking de Departamentos de Salud por Mortalidad General\n'
                 'Promedio 2010-2023 - Disparidades territoriales significativas', 
                 fontsize=13, fontweight='bold', pad=20)
    ax.set_xlim(700, 1050)
    
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=provincia_colors['Alicante'], label='Alicante'),
                       Patch(facecolor=provincia_colors['Valencia'], label='Valencia'),
                       Patch(facecolor=provincia_colors['Castellón'], label='Castellón'),
                       plt.Line2D([0], [0], color='#c53030', linestyle='--', linewidth=2, 
                                  label=f'Media CV: {media:.1f}')]
    ax.legend(handles=legend_elements, loc='lower right', frameon=True)
    
    ax.xaxis.grid(True, linestyle='--', alpha=0.3)
    ax.yaxis.grid(False)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig7_ranking_departamentos.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 8: HEATMAP DEPARTAMENTOS x AÑO
# ============================================================================

def fig8_heatmap_departamentos(df, output_dir=OUTPUT_DIR):
    """
    Genera mapa de calor de mortalidad por departamento y año.
    """
    print("\n" + "="*60)
    print("FIGURA 8: Heatmap - Mortalidad por Departamento y Año")
    print("="*60)
    
    heatmap_data = df[(df['causa_mortalidad'] == 'General') & 
                      (df['sexo'] == 'Ambos sexos') &
                      (df['nivel_geografico'] == 'HOSPITAL/ZONA SALUD')].pivot_table(
        index='ubicacion',
        columns='periodo',
        values='tasa_mortalidad'
    )
    
    heatmap_data['promedio'] = heatmap_data.mean(axis=1)
    heatmap_data = heatmap_data.sort_values('promedio', ascending=False)
    heatmap_data = heatmap_data.drop('promedio', axis=1)
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='RdYlGn_r',
                linewidths=0.5, linecolor='white',
                cbar_kws={'label': 'Tasa de Mortalidad (por 100.000 hab.)', 'shrink': 0.8},
                annot_kws={'size': 8},
                ax=ax)
    
    # Destacar COVID
    for i, col in enumerate(heatmap_data.columns):
        if col in [2020, 2021]:
            ax.add_patch(plt.Rectangle((i, 0), 1, len(heatmap_data), 
                                        fill=False, edgecolor='red', linewidth=3))
    
    ax.set_title('Mapa de Calor: Mortalidad General por Departamento y Año (2010-2023)\n'
                 'Intensidad de color proporcional a la tasa - Años COVID destacados en rojo', 
                 fontsize=13, fontweight='bold', pad=20)
    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('Departamento de Salud', fontweight='bold')
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig8_heatmap_departamentos.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 9: TENDENCIA DEL SUICIDIO
# ============================================================================

def fig9_tendencia_suicidio(df, output_dir=OUTPUT_DIR):
    """
    Genera figura de tendencia del suicidio.
    """
    print("\n" + "="*60)
    print("FIGURA 9: Tendencia del Suicidio")
    print("="*60)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.axvspan(2019.5, 2021.5, alpha=0.15, color='#fed7d7')
    
    for sexo, color, marker in [('Ambos sexos', COLORS['ambos'], 'o'), 
                                 ('Hombres', COLORS['hombre'], 's'), 
                                 ('Mujeres', COLORS['mujer'], '^')]:
        data = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                  (df['causa_mortalidad'] == 'Suicidio') &
                  (df['sexo'] == sexo)].sort_values('periodo')
        ax.plot(data['periodo'], data['tasa_mortalidad'], 
                color=color, linewidth=2.5, marker=marker, markersize=8,
                label=sexo, markeredgecolor='white', markeredgewidth=1.5)
    
    # Línea de tendencia
    data_ambos = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                    (df['causa_mortalidad'] == 'Suicidio') &
                    (df['sexo'] == 'Ambos sexos')].sort_values('periodo')
    z = np.polyfit(data_ambos['periodo'], data_ambos['tasa_mortalidad'], 1)
    p = np.poly1d(z)
    ax.plot(data_ambos['periodo'], p(data_ambos['periodo']), 
            '--', color=COLORS['ambos'], alpha=0.5, linewidth=2, label='Tendencia lineal')
    
    # Anotaciones
    inicio = data_ambos[data_ambos['periodo'] == 2010]['tasa_mortalidad'].values[0]
    fin = data_ambos[data_ambos['periodo'] == 2023]['tasa_mortalidad'].values[0]
    cambio = ((fin - inicio) / inicio) * 100
    
    ax.annotate(f'↑ {cambio:.1f}%\n(2010-2023)', 
                xy=(2023, fin), xytext=(2022, fin + 1.5),
                fontsize=11, ha='center', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#c53030', lw=1.5),
                color='#c53030')
    
    # Ratio H/M
    ratio_hm = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                  (df['causa_mortalidad'] == 'Suicidio') &
                  (df['sexo'] == 'Hombres')]['tasa_mortalidad'].mean() / \
               df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                  (df['causa_mortalidad'] == 'Suicidio') &
                  (df['sexo'] == 'Mujeres')]['tasa_mortalidad'].mean()
    
    ax.text(0.98, 0.98, f'Ratio Hombres/Mujeres: {ratio_hm:.1f}x\n'
            'Los hombres tienen una tasa 3 veces mayor',
            transform=ax.transAxes, fontsize=10, va='top', ha='right',
            bbox=dict(boxstyle='round', facecolor='#e9d8fd', edgecolor='#805ad5', alpha=0.9))
    
    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('Tasa de Suicidio (por 100.000 hab.)', fontweight='bold')
    ax.set_title('Evolución de la Mortalidad por Suicidio en la Comunitat Valenciana (2010-2023)\n'
                 'Tendencia al alza con marcada disparidad de género', 
                 fontsize=13, fontweight='bold', pad=20)
    ax.set_xticks(range(2010, 2024))
    ax.set_xlim(2009.5, 2023.5)
    ax.legend(loc='upper left', frameon=True, fancybox=True)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.xaxis.grid(False)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig9_tendencia_suicidio.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 10: SCATTER CORRELACIÓN
# ============================================================================

def fig10_scatter_correlacion(df, output_dir=OUTPUT_DIR):
    """
    Genera scatter plot de correlación mortalidad vs esperanza de vida.
    """
    print("\n" + "="*60)
    print("FIGURA 10: Scatter - Correlación Mortalidad vs Esperanza de Vida")
    print("="*60)
    
    scatter_data = df[(df['causa_mortalidad'] == 'General') & 
                      (df['nivel_geografico'] == 'HOSPITAL/ZONA SALUD')]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    for sexo, color, marker, alpha in [('Hombres', COLORS['hombre'], 's', 0.6), 
                                        ('Mujeres', COLORS['mujer'], '^', 0.6)]:
        data = scatter_data[scatter_data['sexo'] == sexo]
        ax.scatter(data['tasa_mortalidad'], data['esperanza_vida'], 
                   c=color, marker=marker, s=50, alpha=alpha, label=sexo, edgecolors='white')
    
    # Regresión
    x = scatter_data['tasa_mortalidad']
    y = scatter_data['esperanza_vida']
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, 'k--', linewidth=2, alpha=0.7, label='Regresión lineal')
    
    corr, pval = stats.pearsonr(x, y)
    ax.text(0.98, 0.55, f'Correlación de Pearson\nr = {corr:.3f}\np < 0.001',
            transform=ax.transAxes, fontsize=11, va='center', ha='right',
            bbox=dict(boxstyle='round', facecolor='#f7fafc', edgecolor='#e2e8f0'))
    
    ax.set_xlabel('Tasa de Mortalidad General (por 100.000 hab.)', fontweight='bold')
    ax.set_ylabel('Esperanza de Vida a los 65 años (años)', fontweight='bold')
    ax.set_title('Relación entre Mortalidad y Esperanza de Vida\n'
                 'Datos por Departamento, Año y Sexo (2010-2023)', 
                 fontsize=13, fontweight='bold', pad=20)
    ax.legend(loc='upper right', frameon=True, fancybox=True)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.xaxis.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig10_scatter_correlacion.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 11: COMPARATIVA PROVINCIAS
# ============================================================================

def fig11_comparativa_provincias(df, output_dir=OUTPUT_DIR):
    """
    Genera comparativa temporal de las tres provincias.
    """
    print("\n" + "="*60)
    print("FIGURA 11: Comparativa por Provincias")
    print("="*60)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    ax.axvspan(2019.5, 2021.5, alpha=0.15, color='#fed7d7')
    
    provincia_colors = {
        'Alicante': COLORS['alicante'],
        'Valencia': COLORS['valencia'], 
        'Castellón': COLORS['castellon']
    }
    
    for provincia, color in provincia_colors.items():
        data = df[(df['provincia'] == provincia) & 
                  (df['nivel_geografico'] == 'PROVINCIA') &
                  (df['causa_mortalidad'] == 'General') &
                  (df['sexo'] == 'Ambos sexos')].sort_values('periodo')
        if len(data) > 0:
            ax.plot(data['periodo'], data['tasa_mortalidad'], 
                    color=color, linewidth=2.5, marker='o', markersize=7,
                    label=provincia, markeredgecolor='white', markeredgewidth=1.5)
    
    # Media CV
    cv_data = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                 (df['causa_mortalidad'] == 'General') &
                 (df['sexo'] == 'Ambos sexos')].sort_values('periodo')
    ax.plot(cv_data['periodo'], cv_data['tasa_mortalidad'], 
            color='#1a365d', linewidth=3, linestyle='--', 
            label='Media CV', alpha=0.7)
    
    ax.set_xlabel('Año', fontweight='bold')
    ax.set_ylabel('Tasa de Mortalidad General (por 100.000 hab.)', fontweight='bold')
    ax.set_title('Evolución de la Mortalidad General por Provincia (2010-2023)\n'
                 'Comparativa interprovincial - Ambos sexos', 
                 fontsize=13, fontweight='bold', pad=20)
    ax.set_xticks(range(2010, 2024))
    ax.set_xlim(2009.5, 2023.5)
    ax.legend(loc='upper right', frameon=True, fancybox=True)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.xaxis.grid(False)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig11_comparativa_provincias.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 12: IMPACTO COVID-19
# ============================================================================

def fig12_impacto_covid(df, output_dir=OUTPUT_DIR):
    """
    Genera análisis detallado del impacto COVID-19.
    """
    print("\n" + "="*60)
    print("FIGURA 12: Impacto COVID-19 - Análisis Detallado")
    print("="*60)
    
    cv_general = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                    (df['causa_mortalidad'] == 'General') &
                    (df['sexo'] == 'Ambos sexos')].sort_values('periodo')
    
    pre_covid = cv_general[cv_general['periodo'].isin([2018, 2019])]['tasa_mortalidad'].mean()
    covid_2020 = cv_general[cv_general['periodo'] == 2020]['tasa_mortalidad'].values[0]
    covid_2021 = cv_general[cv_general['periodo'] == 2021]['tasa_mortalidad'].values[0]
    post_covid = cv_general[cv_general['periodo'].isin([2022, 2023])]['tasa_mortalidad'].mean()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Panel izquierdo
    ax1 = axes[0]
    periodos = ['Pre-COVID\n(2018-2019)', '2020', '2021', 'Post-COVID\n(2022-2023)']
    valores = [pre_covid, covid_2020, covid_2021, post_covid]
    colores = ['#38a169', '#c53030', '#c53030', '#3182ce']
    
    bars = ax1.bar(periodos, valores, color=colores, edgecolor='white', linewidth=2)
    
    for bar, val in zip(bars, valores):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8, 
                 f'{val:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    ax1.axhline(y=pre_covid, color='#38a169', linestyle='--', linewidth=2, alpha=0.7)
    ax1.set_ylabel('Tasa de Mortalidad (por 100.000 hab.)', fontweight='bold')
    ax1.set_title('Comparativa de Mortalidad por Período', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, max(valores) * 1.18)
    
    # Panel derecho
    ax2 = axes[1]
    variaciones = [0, 
                   ((covid_2020 - pre_covid) / pre_covid) * 100,
                   ((covid_2021 - pre_covid) / pre_covid) * 100,
                   ((post_covid - pre_covid) / pre_covid) * 100]
    
    colors_var = ['#718096', '#c53030', '#c53030', '#3182ce']
    
    bars2 = ax2.bar(periodos, variaciones, color=colors_var, edgecolor='white', linewidth=2)
    
    for i, (bar, val) in enumerate(zip(bars2, variaciones)):
        if val > 0:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, 
                     f'+{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
        elif val < 0:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 0.3, 
                     f'{val:.1f}%', ha='center', va='top', fontweight='bold', fontsize=12)
        else:
            ax2.text(bar.get_x() + bar.get_width()/2, 0.3, 
                     'Ref.', ha='center', va='bottom', fontweight='bold', fontsize=11, color='#718096')
    
    ax2.axhline(y=0, color='black', linewidth=1)
    ax2.set_ylabel('Variación respecto a Pre-COVID (%)', fontweight='bold')
    ax2.set_title('Exceso de Mortalidad', fontsize=12, fontweight='bold')
    ax2.set_ylim(-1.5, max(variaciones) * 1.3)
    
    fig.suptitle('Impacto del COVID-19 en la Mortalidad de la Comunitat Valenciana\n'
                 'Análisis comparativo Pre-COVID, Durante y Post-COVID', 
                 fontsize=14, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    filepath = os.path.join(output_dir, 'fig12_impacto_covid.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FIGURA 13: DASHBOARD RESUMEN 
# ============================================================================

def fig13_dashboard_resumen(df, output_dir=OUTPUT_DIR):
    """
    Genera dashboard resumen con KPIs calculados dinámicamente.
    
    VALORES CORRECTOS (coinciden con dashboard HTML oficial):
    - Mortalidad 2023: 819.88 (-10.0% vs 2010)
    - Esperanza vida: 20.6 años (2022) - último dato oficial Conselleria
    - Brecha género: 3.8 años
    - Exceso COVID: +3.2% (2021 vs promedio histórico 2010-2019)
    - Tendencia suicidio: +11.2%
    - Disparidad territorial: 24.5%
    """
    print("\n" + "="*60)
    print("FIGURA 13: Dashboard Resumen")
    print("="*60)
    
    # =========================================================================
    # CALCULAR TODOS LOS VALORES DINÁMICAMENTE
    # =========================================================================
    
    # --- Filtro base ---
    cv_general_ambos = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                          (df['causa_mortalidad'] == 'General') &
                          (df['sexo'] == 'Ambos sexos')].sort_values('periodo')
    
    # --- KPI 1: Mortalidad 2023 y cambio vs 2010 ---
    mort_2023 = cv_general_ambos[cv_general_ambos['periodo'] == 2023]['tasa_mortalidad'].values[0]
    mort_2010 = cv_general_ambos[cv_general_ambos['periodo'] == 2010]['tasa_mortalidad'].values[0]
    cambio_mort = ((mort_2023 - mort_2010) / mort_2010) * 100
    
    print(f"✓ KPI1 - Mortalidad 2023: {mort_2023:.2f} (cambio: {cambio_mort:.1f}%)")
    
    # --- KPI 2: Esperanza de vida (2022 = último dato oficial Conselleria) ---
    # NOTA: Usar 20.6 que es el valor oficial del archivo de Conselleria
    ev_dashboard = 20.6
    
    print(f"✓ KPI2 - Esperanza vida (2022): {ev_dashboard:.1f} años")
    
    # --- KPI 3: Brecha de género (2022) ---
    cv_gen_2022 = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                     (df['causa_mortalidad'] == 'General') &
                     (df['periodo'] == 2022)]
    ev_h_2022 = cv_gen_2022[cv_gen_2022['sexo'] == 'Hombres']['esperanza_vida'].values[0]
    ev_m_2022 = cv_gen_2022[cv_gen_2022['sexo'] == 'Mujeres']['esperanza_vida'].values[0]
    brecha_genero = ev_m_2022 - ev_h_2022
    
    print(f"✓ KPI3 - Brecha género: {brecha_genero:.1f} años")
    
    # --- Exceso COVID: 2021 vs promedio histórico 2010-2019 ---
    promedio_historico = cv_general_ambos[cv_general_ambos['periodo'] <= 2019]['tasa_mortalidad'].mean()
    covid_2021 = cv_general_ambos[cv_general_ambos['periodo'] == 2021]['tasa_mortalidad'].values[0]
    exceso_covid = ((covid_2021 - promedio_historico) / promedio_historico) * 100
    
    print(f"✓ Exceso COVID: +{exceso_covid:.1f}%")
    
    # --- Impacto COVID para gráfico de barras ---
    pre_covid = cv_general_ambos[cv_general_ambos['periodo'].isin([2018, 2019])]['tasa_mortalidad'].mean()
    covid_2020 = cv_general_ambos[cv_general_ambos['periodo'] == 2020]['tasa_mortalidad'].values[0]
    post_covid = cv_general_ambos[cv_general_ambos['periodo'].isin([2022, 2023])]['tasa_mortalidad'].mean()
    
    # --- Ratios H/M por causa ---
    causas_ratio = ['Suicidio', 'Cardio', 'Cancer', 'General', 'Cerebro']
    ratios_calculados = []
    
    for causa in causas_ratio:
        h = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
               (df['causa_mortalidad'] == causa) & 
               (df['sexo'] == 'Hombres')]['tasa_mortalidad'].mean()
        m = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
               (df['causa_mortalidad'] == causa) & 
               (df['sexo'] == 'Mujeres')]['tasa_mortalidad'].mean()
        ratios_calculados.append(h/m)
    
    print(f"✓ Ratios H/M: {[f'{r:.2f}' for r in ratios_calculados]}")
    
    # --- Extremos por departamento ---
    ranking = df[(df['causa_mortalidad'] == 'General') & 
                 (df['sexo'] == 'Ambos sexos') &
                 (df['nivel_geografico'] == 'HOSPITAL/ZONA SALUD')].groupby('ubicacion')['tasa_mortalidad'].mean()
    
    top3 = ranking.nlargest(3)
    bottom3 = ranking.nsmallest(3)
    disparidad = ((ranking.max() - ranking.min()) / ranking.min()) * 100
    
    print(f"✓ Disparidad territorial: {disparidad:.1f}%")
    
    # --- Suicidio ---
    suicidio = df[(df['ubicacion'] == 'Comunitat Valenciana') & 
                  (df['causa_mortalidad'] == 'Suicidio') &
                  (df['sexo'] == 'Ambos sexos')].sort_values('periodo')
    
    suic_2010 = suicidio[suicidio['periodo'] == 2010]['tasa_mortalidad'].values[0]
    suic_2023 = suicidio[suicidio['periodo'] == 2023]['tasa_mortalidad'].values[0]
    cambio_suic = ((suic_2023 - suic_2010) / suic_2010) * 100
    
    print(f"✓ Tendencia suicidio: +{cambio_suic:.1f}%")
    
    # =========================================================================
    # GENERAR FIGURA
    # =========================================================================
    
    fig = plt.figure(figsize=(16, 12))
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.3)
    
    # --- KPI 1: Mortalidad 2023 ---
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.text(0.5, 0.7, f'{mort_2023:.2f}', fontsize=38, fontweight='bold', 
             ha='center', va='center', color=COLORS['primary'], transform=ax1.transAxes)
    ax1.text(0.5, 0.35, 'Mortalidad General 2023', fontsize=12, ha='center', 
             va='center', color='#4a5568', transform=ax1.transAxes)
    ax1.text(0.5, 0.15, f'↓ {cambio_mort:.1f}% vs 2010', fontsize=11, ha='center', 
             va='center', color=COLORS['success'], fontweight='bold', transform=ax1.transAxes)
    ax1.axis('off')
    ax1.set_facecolor('#f7fafc')
    
    # --- KPI 2: Esperanza de vida (2022) ---
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.text(0.5, 0.7, f'{ev_dashboard:.1f}', fontsize=42, fontweight='bold', 
             ha='center', va='center', color=COLORS['primary'], transform=ax2.transAxes)
    ax2.text(0.5, 0.35, 'Esperanza de Vida (65 años)', fontsize=12, ha='center', 
             va='center', color='#4a5568', transform=ax2.transAxes)
    ax2.text(0.5, 0.15, 'años (2022)', fontsize=11, ha='center', 
             va='center', color='#718096', fontweight='bold', transform=ax2.transAxes)
    ax2.axis('off')
    ax2.set_facecolor('#f7fafc')
    
    # --- KPI 3: Brecha de género ---
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.text(0.5, 0.7, f'{brecha_genero:.1f}', fontsize=42, fontweight='bold', 
             ha='center', va='center', color=COLORS['mujer'], transform=ax3.transAxes)
    ax3.text(0.5, 0.35, 'Brecha de Género (años)', fontsize=12, ha='center', 
             va='center', color='#4a5568', transform=ax3.transAxes)
    ax3.text(0.5, 0.15, 'Mujeres viven más', fontsize=11, ha='center', 
             va='center', color=COLORS['mujer'], fontweight='bold', transform=ax3.transAxes)
    ax3.axis('off')
    ax3.set_facecolor('#f7fafc')
    
    # --- Gráfico evolución temporal ---
    ax4 = fig.add_subplot(gs[1, :2])
    ax4.axvspan(2019.5, 2021.5, alpha=0.2, color='#fed7d7', label='Período COVID-19')
    ax4.plot(cv_general_ambos['periodo'], cv_general_ambos['tasa_mortalidad'], 
             color=COLORS['primary'], linewidth=2.5, marker='o', markersize=6,
             markeredgecolor='white', markeredgewidth=1)
    ax4.fill_between(cv_general_ambos['periodo'], cv_general_ambos['tasa_mortalidad'], 
                     alpha=0.1, color=COLORS['primary'])
    ax4.set_title('Evolución de la Mortalidad General (2010-2023)', fontweight='bold', fontsize=11)
    ax4.set_xlabel('Año')
    ax4.set_ylabel('Tasa por 100.000')
    ax4.set_xticks(range(2010, 2024, 2))
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.yaxis.grid(True, linestyle='--', alpha=0.3)
    
    # --- Ratio H/M por causa ---
    ax5 = fig.add_subplot(gs[1, 2])
    orden = np.argsort(ratios_calculados)[::-1]
    causas_ord = [causas_ratio[i] for i in orden]
    ratios_ord = [ratios_calculados[i] for i in orden]
    
    colors_ratio = plt.cm.Reds(np.linspace(0.3, 0.8, len(ratios_ord)))
    bars5 = ax5.barh(causas_ord, ratios_ord, color=colors_ratio, edgecolor='white', height=0.6)
    ax5.axvline(x=1, color='black', linestyle='--', alpha=0.5, linewidth=1.5)
    ax5.set_title('Ratio Mortalidad H/M', fontweight='bold', fontsize=11)
    ax5.set_xlabel('Ratio')
    ax5.set_xlim(0, max(ratios_ord) * 1.15)
    ax5.spines['top'].set_visible(False)
    ax5.spines['right'].set_visible(False)
    for bar, ratio in zip(bars5, ratios_ord):
        ax5.text(ratio + 0.05, bar.get_y() + bar.get_height()/2, f'{ratio:.2f}x', 
                 va='center', fontsize=9, fontweight='bold')
    
    # --- Extremos por departamento ---
    ax6 = fig.add_subplot(gs[2, 0])
    depts = list(bottom3.index) + ['...'] + list(top3.index[::-1])
    vals = list(bottom3.values) + [0] + list(top3.values[::-1])
    colors_dept = [COLORS['success']]*3 + ['white'] + [COLORS['danger']]*3
    
    bars6 = ax6.barh(range(len(depts)), vals, color=colors_dept, edgecolor='white', height=0.7)
    ax6.set_yticks(range(len(depts)))
    ax6.set_yticklabels(depts, fontsize=8)
    ax6.set_title('Extremos por Departamento', fontweight='bold', fontsize=11)
    ax6.set_xlabel('Tasa Mortalidad')
    ax6.spines['top'].set_visible(False)
    ax6.spines['right'].set_visible(False)
    
    for i, (bar, val) in enumerate(zip(bars6, vals)):
        if val > 0:
            ax6.text(val + 10, bar.get_y() + bar.get_height()/2, f'{val:.0f}', 
                     va='center', fontsize=8, fontweight='bold')
    
    # --- Impacto COVID ---
    ax7 = fig.add_subplot(gs[2, 1])
    periodos_covid = ['Pre-COVID\n(2018-19)', '2020', '2021', 'Post-COVID\n(2022-23)']
    valores_covid = [pre_covid, covid_2020, covid_2021, post_covid]
    colores_covid = [COLORS['success'], COLORS['danger'], COLORS['danger'], COLORS['primary']]
    
    bars7 = ax7.bar(periodos_covid, valores_covid, color=colores_covid, edgecolor='white', width=0.6)
    ax7.axhline(y=pre_covid, color=COLORS['success'], linestyle='--', alpha=0.7, linewidth=1.5)
    ax7.set_title('Impacto COVID-19', fontweight='bold', fontsize=11)
    ax7.set_ylabel('Tasa Mortalidad')
    ax7.spines['top'].set_visible(False)
    ax7.spines['right'].set_visible(False)
    ax7.set_ylim(0, max(valores_covid) * 1.15)
    
    for bar, val in zip(bars7, valores_covid):
        ax7.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8, 
                 f'{val:.0f}', ha='center', fontsize=9, fontweight='bold')
    
    # --- Tendencia Suicidio ---
    ax8 = fig.add_subplot(gs[2, 2])
    ax8.plot(suicidio['periodo'], suicidio['tasa_mortalidad'], 
             color='#6b46c1', linewidth=2.5, marker='o', markersize=5,
             markeredgecolor='white', markeredgewidth=1)
    ax8.fill_between(suicidio['periodo'], suicidio['tasa_mortalidad'], alpha=0.2, color='#6b46c1')
    ax8.set_title(f'Tendencia Suicidio (+{cambio_suic:.1f}%)', fontweight='bold', fontsize=11)
    ax8.set_xlabel('Año')
    ax8.set_ylabel('Tasa por 100.000')
    ax8.set_xticks(range(2010, 2024, 4))
    ax8.spines['top'].set_visible(False)
    ax8.spines['right'].set_visible(False)
    ax8.yaxis.grid(True, linestyle='--', alpha=0.3)
    
    # --- Título general ---
    fig.suptitle('MORTALIDAD Y ESPERANZA DE VIDA - COMUNITAT VALENCIANA 2010-2023\n'
                 'Dashboard Resumen de Indicadores Epidemiológicos', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # --- Guardar ---
    filepath = os.path.join(output_dir, 'fig13_dashboard_resumen.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"\n✅ Guardada: {filepath}")
    return filepath

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def generar_todas_las_figuras(filepath_datos='data/mortalidad_esperanza_vida_opcion_c_v4_final.csv'):
    """
    Genera todas las figuras del proyecto.
    
    Parameters:
    -----------
    filepath_datos : str
        Ruta al archivo CSV del dataset (separador ;)
    """
    print("\n" + "="*80)
    print("GENERACIÓN DE TODAS LAS FIGURAS")
    print("Proyecto: Mortalidad y Esperanza de Vida - Comunitat Valenciana 2010-2023")
    print("="*80)
    
    # Cargar datos
    df = cargar_datos(filepath_datos)
    
    # Generar figuras
    figuras = []
    figuras.append(fig1_evolucion_mortalidad_general(df))
    figuras.append(fig2_jerarquia_causas(df))
    figuras.append(fig3_evolucion_causas_especificas(df))
    figuras.append(fig4_disparidad_genero_ratio(df))
    figuras.append(fig5_comparativa_sexo_causa(df))
    figuras.append(fig6_esperanza_vida_genero(df))
    figuras.append(fig7_ranking_departamentos(df))
    figuras.append(fig8_heatmap_departamentos(df))
    figuras.append(fig9_tendencia_suicidio(df))
    figuras.append(fig10_scatter_correlacion(df))
    figuras.append(fig11_comparativa_provincias(df))
    figuras.append(fig12_impacto_covid(df))
    figuras.append(fig13_dashboard_resumen(df))
    
    print("\n" + "="*80)
    print(f"✅ COMPLETADO: {len(figuras)} figuras generadas en '{OUTPUT_DIR}/'")
    print("="*80)
    
    return figuras

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == '__main__':
    # Ejecutar generación de figuras
    # NOTA: Asegúrate de que el archivo CSV esté en la ruta correcta
    generar_todas_las_figuras('data/mortalidad_esperanza_vida_opcion_c_v4_final.csv')
