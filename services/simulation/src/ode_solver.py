"""
Ordinary Differential Equation solver.
"""

class ODESolver:
    def solve(self, equation, t_span):
        """
        Solve ODE.

        Args:
            equation (str): ODE in symbolic form.
            t_span (tuple): Start and end time.

        Returns:
            list: Solution over time.
        """
        # TODO: Implement solver using scipy.integrate or sympy
        return [0] * (t_span[1] - t_span[0])
