import torch
from oggm.core.massbalance import MassBalanceModel

from oggm.cfg import SEC_IN_YEAR, SEC_IN_MONTH, RHO

# @torch.no_grad()
class LinearMassBalance(MassBalanceModel):
    """Constant mass-balance as a linear function of altitude.
    """

    def __init__(self, ela_h, grad=3., max_mb=None):
        """ Initialize.

        Parameters
        ----------
        ela_h: float
            Equilibrium line altitude (units: [m])
        grad: float
            Mass-balance gradient (unit: [mm w.e. yr-1 m-1])
        max_mb: float
            Cap the mass balance to a certain value (unit: [mm w.e. yr-1])

        Attributes
        ----------
        temp_bias : float, default 0
            A "temperature bias" doesn't makes much sense in the linear MB
            context, but we implemented a simple empirical rule:
            + 1K -> ELA + 150 m
        """
        super(LinearMassBalance, self).__init__()
        self.valid_bounds = [-1e4, 2e4]  # in m
        self.orig_ela_h = ela_h
        self.ela_h = ela_h
        self.grad = grad
        self.max_mb = max_mb
        self._temp_bias = 0

    @property
    def temp_bias(self):
        """Temperature bias to add to the original series."""
        return self._temp_bias

    @temp_bias.setter
    def temp_bias(self, value):
        """Temperature bias to change the ELA."""
        self.ela_h = self.orig_ela_h + value * 150
        self._temp_bias = value

    def get_monthly_mb(self, heights, year=None):
        mb = (heights - self.ela_h) * self.grad
        if self.max_mb is not None:
            mb = mb.clip(None, self.max_mb)
        return mb / SEC_IN_YEAR / RHO

    def get_annual_mb(self, heights, year=None):
        return self.get_monthly_mb(heights, year=year)