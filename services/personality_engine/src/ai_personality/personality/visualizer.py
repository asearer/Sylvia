"""
visualizer.py - Provides visualization utilities for Personality objects.

Uses matplotlib to graphically display trait distributions, comparisons,
and hybridizations.
"""
import matplotlib.pyplot as plt
from typing import Dict, Any

class PersonalityVisualizer:
    """
    Visualizes the trait profiles or comparisons of Personality objects.
    """

    @staticmethod
    def plot_traits(personality, title: str = None, ax: Any = None):
        """
        Plot the trait weights for a given Personality (or trait dict).
        Args:
            personality: Personality object or dict of trait->value
            title: Optional plot title.
            ax: Optional matplotlib axis to plot into.
        """
        # Accept class or dict
        traits = getattr(personality, 'traits', personality)
        labels = list(traits.keys())
        values = [traits[k] for k in labels]
        ax = ax or plt.gca()
        bars = ax.bar(labels, values, color='teal')
        ax.set_ylim(0, 1)
        ax.set_ylabel('Weight')
        ax.set_xlabel('Trait')
        if title:
            ax.set_title(title)
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2., val + 0.01, f'{val:.2f}', ha='center', va='bottom')
        plt.tight_layout()
        return ax

    @staticmethod
    def compare(p1, p2, labels=None, ax: Any = None):
        """
        Plot a side-by-side comparison of two personalities' trait profiles.
        Args:
            p1, p2: Personality objects or dicts.
            labels: Optional, force order of comparison.
            ax: matplotlib axis (optional).
        """
        t1 = getattr(p1, 'traits', p1)
        t2 = getattr(p2, 'traits', p2)
        all_keys = sorted(set(t1) | set(t2) if labels is None else labels)
        v1 = [t1.get(k, 0.0) for k in all_keys]
        v2 = [t2.get(k, 0.0) for k in all_keys]
        x = range(len(all_keys))
        ax = ax or plt.gca()
        ax.bar([i - 0.2 for i in x], v1, width=0.4, label=getattr(p1, 'name', 'p1'))
        ax.bar([i + 0.2 for i in x], v2, width=0.4, label=getattr(p2, 'name', 'p2'))
        ax.set_xticks(list(x))
        ax.set_xticklabels(all_keys)
        ax.set_ylim(0, 1)
        ax.set_ylabel('Weight')
        ax.legend()
        plt.tight_layout()
        return ax

# Example usage
if __name__ == '__main__':
    from personality import Personality
    p1 = Personality('friendly', {'openness': 0.9, 'sociability': 0.8})
    p2 = Personality('serious', {'openness': 0.4, 'discipline': 0.85})
    PersonalityVisualizer.plot_traits(p1, title='Friendly Personality')
    plt.show()
    PersonalityVisualizer.compare(p1, p2)
    plt.show()
