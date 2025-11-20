"""
Ordinary Differential Equation solver.
"""

from typing import Callable, List, Tuple, Union
import numpy as np
from scipy.integrate import solve_ivp

class ODESolver:
    def solve(
        self,
        equation: Union[str, Callable[[float, float], float]],
        t_span: Tuple[float, float],
        y0: float = 0.0,
        num_points: int = 100
    ) -> List[Tuple[float, float]]:
        """
        Solve ODE.

        Args:
            equation (str or callable): ODE in symbolic form (lambda t, y: dy/dt) or callable.
            t_span (tuple): (t_start, t_end)
            y0 (float, optional): Initial condition
            num_points (int, optional): Number of points to evaluate solution

        Returns:
            list of tuples: [(t0, y0), (t1, y1), ...]
        """
        t_start, t_end = t_span
        if t_end <= t_start:
            raise ValueError("t_end must be greater than t_start.")

        if isinstance(equation, str):
            # Convert string to lambda safely (expects 't' and 'y')
            try:
                func = eval(equation, {"__builtins__": {}}, {})
            except Exception as e:
                raise ValueError(f"Invalid equation string: {e}")
        elif callable(equation):
            func = equation
        else:
            raise TypeError("Equation must be a string or callable.")

        t_eval = np.linspace(t_start, t_end, num_points)
        sol = solve_ivp(fun=func, t_span=t_span, y0=[y0], t_eval=t_eval)

        if not sol.success:
            raise RuntimeError(f"ODE solver failed: {sol.message}")

        return list(zip(sol.t, sol.y[0]))
