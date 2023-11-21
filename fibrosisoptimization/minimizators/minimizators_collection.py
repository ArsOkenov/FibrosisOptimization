from fibrosisoptimization.minimizators.minimizator import Minimizator


class MinimizatorsCollection:
    """MinimizatorsCollection class for managing multiple minimizators.

    This class manages a collection of Minimizator instances for
    optimization purposes.

    Parameters
    ----------
    segments : list
        List of segment information.
    value_names : list, optional
        List of value names. Defaults to ['PtP', 'PtP', 'LAT'].
    density_step_tol : float, optional
        Tolerance for density step change. Defaults to 0.01.

    Attributes
    ----------
    density_step_tol : float
        Tolerance for density step change.
    minimizators : list
        List of Minimizator instances.
    """

    def __init__(self, segments, value_names, density_step_tol=0.01):
        """Initialize a MinimizatorsCollection object.

        Parameters
        ----------
        segments : list
            List of segment information.
        value_names : list, optional
            List of value names. Defaults to ['PtP', 'PtP', 'LAT'].
        density_step_tol : float, optional
            Tolerance for density step change. Defaults to 0.01.
        """
        self.density_step_tol = density_step_tol
        self.minimizators = self.make_minimizators(segments, value_names)

    @property
    def segments(self):
        """Get segment information for all Minimizator instances.

        Returns
        -------
        list
            List of segment information for each Minimizator.
        """
        return [minimizator.segment for minimizator in self.minimizators]

    @property
    def value_names(self):
        """Get value names for all Minimizator instances.

        Returns
        -------
        list
            List of value names for each Minimizator.
        """
        return [minimizator.value_name for minimizator in self.minimizators]

    def make_minimizators(self, segments, value_names):
        """Create Minimizator instances based on segment and value names.

        Parameters
        ----------
        segments : list
            List of segment information.
        value_names : list
            List of value names.

        Returns
        -------
        list
            List of Minimizator instances.
        """
        minimizators = []
        for segment, value_name in zip(segments, value_names):
            minimizators.append(Minimizator(segment, value_name))
        return minimizators

    def update_minimizator(self, minimizator, densities, surface_data):
        """Internal method to update Minimizator based on densities and
        surface data.

        Parameters
        ----------
        densities : list
            List of density values.
        surface_data : object
            Surface data object.

        Returns
        -------
        tuple
            Tuple of active minimizator density and new density value.
        """
        if minimizator.value_name == 'PtP':
            values = surface_data.ptp_mean_per_segment

        if minimizator.value_name == 'LAT':
            values = - surface_data.lat_mean_per_segment

        segment_ind = minimizator.segment - 1
        value = values[segment_ind]
        density = densities[segment_ind]

        density_new = minimizator.update(density, value)

        print('SEGMENT : {}'.format(minimizator.segment))
        print('    {} : {:.3f}'.format(minimizator.value_name, value))
        print('DENSITY : {:.3f} --> {:.3f}'.format(density, density_new))

        return density, density_new

    def update(self, densities, surface_data):
        """Update Minimizators based on densities and surface data.

        Parameters
        ----------
        densities : np.ndarray
            List of density values.
        surface_data : SurfaceData
            Surface data object.

        Returns
        -------
        np.ndarray
            Updated list of density values.
        """

        densities = densities.copy()

        for minimizator in self.minimizators:
            density, density_new = self.update_minimizator(minimizator,
                                                           densities,
                                                           surface_data)
            densities[minimizator.segment - 1] = density_new

        return densities
