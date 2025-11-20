"""
Partial Differential Equation solver.
"""

from typing import Callable, Dict, List
import numpy as np

class PDESolver:
    def solve(
        self,
        pde: Callable[[float, float, float], float],
        domain: Dict[str, float],
        nx: int = 10,
        nt: int = 10
    ) -> List[List[float]]:
        """
        Solve PDE using explicit finite difference (1D heat equation style).

        Args:
            pde (callable): Function f(t, x, u) representing du/dt = f(t, x, u)
            domain (dict): {'x_start': float, 'x_end': float, 't_start': float, 't_end': float}
            nx (int): Number of spatial points
            nt (int): Number of time points

        Returns:
            list: 2D solution grid (time x space)
        """
        required_keys = ['x_start', 'x_end', 't_start', 't_end']
        for key in required_keys:
            if key not in domain:
                raise ValueError(f"Domain missing required key: {key}")

        x_start, x_end = domain['x_start'], domain['x_end']
        t_start, t_end = domain['t_start'], domain['t_end']

        x = np.linspace(x_start, x_end, nx)
        t = np.linspace(t_start, t_end, nt)
        dx = (x_end - x_start) / (nx - 1)
        dt = (t_end - t_start) / (nt - 1)

        u = np.zeros((nt, nx))

        # Initial condition: u[0, :] = pde(t_start, x, 0)
        for i in range(nx):
            u[0, i] = pde(t_start, x[i], 0)

        # Explicit finite difference time stepping
        for n in range(0, nt - 1):
            for i in range(1, nx - 1):
                # du/dt = f(t, x, u) -> u_new = u_old + dt * f
                u[n+1, i] = u[n, i] + dt * pde(t[n], x[i], u[n, i])

            # Boundary conditions: assume Dirichlet u=0 at boundaries
            u[n+1, 0] = 0
            u[n+1, -1] = 0

        return u.tolist()
