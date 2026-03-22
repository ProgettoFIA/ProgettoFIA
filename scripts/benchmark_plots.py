import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

def load_benchmark_results(filename="benchmark_results.json"):
    """Carica i risultati del benchmark da file JSON"""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Errore: {filename} non trovato. Esegui main.py prima.")
        return None

def plot_algoritmi_comparison(results):
    """Confronto tempi esecuzione A* vs GREEDY vs CU"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Tempi di esecuzione
    algoritmi = ['A*', 'GREEDY', 'CU']
    exec_times = [
        results["astar"]["medie_esecuzione"]["euclidea"],
        results["greedy"]["medie_esecuzione"]["euclidea"],
        results["cu"]["media_esecuzione"]
    ]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    ax1.bar(algoritmi, exec_times, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Tempo (s)', fontsize=12, fontweight='bold')
    ax1.set_title('Confronto Tempo Esecuzione Algoritmi', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    for i, v in enumerate(exec_times):
        ax1.text(i, v + max(exec_times)*0.02, f'{v:.4f}s', ha='center', fontweight='bold')
    
    # Tempi percorrenza
    perc_times = [
        results["astar"]["medie_percorrenza"]["euclidea"],
        results["greedy"]["medie_percorrenza"]["euclidea"],
        results["cu"]["media_percorrenza"]
    ]
    
    ax2.bar(algoritmi, perc_times, color=colors, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Tempo (min)', fontsize=12, fontweight='bold')
    ax2.set_title('Confronto Tempo Percorrenza Algoritmi', fontsize=13, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    for i, v in enumerate(perc_times):
        ax2.text(i, v + max(perc_times)*0.02, f'{v:.2f} min', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig("plots/01_algoritmi_comparison.png", dpi=300, bbox_inches='tight')
    print("✅ Salvato: 01_algoritmi_comparison.png")
    plt.close()

def plot_astar_euristiche(results):
    """Confronto euristiche A*"""
    euristiche = list(results["astar"]["medie_esecuzione"].keys())
    exec_times = [results["astar"]["medie_esecuzione"][e] for e in euristiche]
    perc_times = [results["astar"]["medie_percorrenza"][e] for e in euristiche]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Tempo esecuzione
    colors_eu = ['#FF6B6B', '#FFA502', '#FFD93D']
    ax1.bar(euristiche, exec_times, color=colors_eu, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Tempo (s)', fontsize=12, fontweight='bold')
    ax1.set_title('A* - Confronto Euristiche (Tempo Esecuzione)', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    for i, v in enumerate(exec_times):
        ax1.text(i, v + max(exec_times)*0.02, f'{v:.4f}s', ha='center', fontweight='bold')
    
    # Tempo percorrenza
    ax2.bar(euristiche, perc_times, color=colors_eu, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Tempo (min)', fontsize=12, fontweight='bold')
    ax2.set_title('A* - Confronto Euristiche (Tempo Percorrenza)', fontsize=13, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    for i, v in enumerate(perc_times):
        ax2.text(i, v + max(perc_times)*0.02, f'{v:.2f} min', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig("plots/02_astar_euristiche.png", dpi=300, bbox_inches='tight')
    print("✅ Salvato: 02_astar_euristiche.png")
    plt.close()

def plot_greedy_euristiche(results):
    """Confronto euristiche GREEDY"""
    euristiche = list(results["greedy"]["medie_esecuzione"].keys())
    exec_times = [results["greedy"]["medie_esecuzione"][e] for e in euristiche]
    perc_times = [results["greedy"]["medie_percorrenza"][e] for e in euristiche]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Tempo esecuzione
    colors_eu = ['#4ECDC4', '#44A08D', '#0B8E7F']
    ax1.bar(euristiche, exec_times, color=colors_eu, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Tempo (s)', fontsize=12, fontweight='bold')
    ax1.set_title('GREEDY - Confronto Euristiche (Tempo Esecuzione)', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    for i, v in enumerate(exec_times):
        ax1.text(i, v + max(exec_times)*0.02, f'{v:.4f}s', ha='center', fontweight='bold')
    
    # Tempo percorrenza
    ax2.bar(euristiche, perc_times, color=colors_eu, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Tempo (min)', fontsize=12, fontweight='bold')
    ax2.set_title('GREEDY - Confronto Euristiche (Tempo Percorrenza)', fontsize=13, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    for i, v in enumerate(perc_times):
        ax2.text(i, v + max(perc_times)*0.02, f'{v:.2f} min', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig("plots/03_greedy_euristiche.png", dpi=300, bbox_inches='tight')
    print("✅ Salvato: 03_greedy_euristiche.png")
    plt.close()

def plot_efficiency_pie(results):
    """Grafico a torta: efficienza relativa"""
    # Normalizza i tempi di esecuzione
    times = [
        results["astar"]["medie_esecuzione"]["euclidea"],
        results["greedy"]["medie_esecuzione"]["euclidea"],
        results["cu"]["media_esecuzione"]
    ]
    
    algoritmi = ['A*', 'GREEDY', 'CU']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    wedges, texts, autotexts = ax.pie(times, labels=algoritmi, autopct='%1.1f%%',
                                        colors=colors, startangle=90,
                                        textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    ax.set_title('Distribuzione Tempo Esecuzione', fontsize=14, fontweight='bold', pad=20)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    plt.savefig("plots/04_efficiency_pie.png", dpi=300, bbox_inches='tight')
    print("✅ Salvato: 04_efficiency_pie.png")
    plt.close()

def plot_all_algorithms_line(results):
    """Grafico a linee: tutte le euristiche e algoritmi"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    euristiche_astar = list(results["astar"]["medie_esecuzione"].keys())
    exec_astar = [results["astar"]["medie_esecuzione"][e] for e in euristiche_astar]
    exec_greedy = [results["greedy"]["medie_esecuzione"][e] for e in euristiche_astar]
    
    x = np.arange(len(euristiche_astar))
    
    ax.plot(x, exec_astar, marker='o', linewidth=2.5, markersize=10, 
            label='A*', color='#FF6B6B')
    ax.plot(x, exec_greedy, marker='s', linewidth=2.5, markersize=10,
            label='GREEDY', color='#4ECDC4')
    ax.axhline(y=results["cu"]["media_esecuzione"], linestyle='--', linewidth=2.5,
               label='CU (Uniform Cost)', color='#45B7D1')
    
    ax.set_xlabel('Euristica', fontsize=12, fontweight='bold')
    ax.set_ylabel('Tempo Esecuzione (s)', fontsize=12, fontweight='bold')
    ax.set_title('Confronto Tempo Esecuzione - Tutti gli Algoritmi', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([e.capitalize() for e in euristiche_astar])
    ax.legend(fontsize=11, loc='best')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("plots/05_all_algorithms_line.png", dpi=300, bbox_inches='tight')
    print("✅ Salvato: 05_all_algorithms_line.png")
    plt.close()

def main():
    """Esegui la generazione di tutti i grafici"""
    # Crea cartella plots se non esiste
    Path("plots").mkdir(exist_ok=True)
    
    results = load_benchmark_results()
    if results is None:
        return
    
    print("\n" + "-"*50)
    print("🎨 Generazione grafici benchmark...")
    print("-"*50)
    
    plot_algoritmi_comparison(results)
    plot_astar_euristiche(results)
    plot_greedy_euristiche(results)
    plot_efficiency_pie(results)
    plot_all_algorithms_line(results)
    
    print("-"*50)
    print("✅ Tutti i grafici generati in /plots/")
    print("-"*50)

if __name__ == "__main__":
    main()