"""Containers for results from inference."""

import io
import logging
import sys
from collections import OrderedDict

import numpy as np
from matplotlib import pyplot as plt

import elfi.visualization.visualization as vis

logger = logging.getLogger(__name__)


class ParameterInferenceResult:
    """Base class for results."""

    def __init__(self, method_name, outputs, parameter_names, **kwargs):
        """Initialize result.

        Parameters
        ----------
        method_name : string
            Name of inference method.
        outputs : dict
            Dictionary with outputs from the nodes, e.g. samples.
        parameter_names : list
            Names of the parameter nodes
        **kwargs
            Any other information from the inference algorithm, usually from it's state.

        """
        self.method_name = method_name
        self.outputs = outputs.copy()
        self.parameter_names = parameter_names
        self.meta = kwargs


class OptimizationResult(ParameterInferenceResult):
    """Base class for results from optimization."""

    def __init__(self, x_min, **kwargs):
        """Initialize result.

        Parameters
        ----------
        x_min
            The optimized parameters
        **kwargs
            See `ParameterInferenceResult`

        """
        super(OptimizationResult, self).__init__(**kwargs)
        self.x_min = x_min


class Sample(ParameterInferenceResult):
    """Sampling results from inference methods."""

    def __init__(self,
                 method_name,
                 outputs,
                 parameter_names,
                 discrepancy_name=None,
                 weights=None,
                 **kwargs):
        """Initialize result.

        Parameters
        ----------
        method_name : string
            Name of inference method.
        outputs : dict
            Dictionary with outputs from the nodes, e.g. samples.
        parameter_names : list
            Names of the parameter nodes
        discrepancy_name : string, optional
            Name of the discrepancy in outputs.
        weights : array_like
        **kwargs
            Other meta information for the result

        """
        super(Sample, self).__init__(
            method_name=method_name, outputs=outputs, parameter_names=parameter_names, **kwargs)

        self.samples = OrderedDict()
        for n in self.parameter_names:
            self.samples[n] = self.outputs[n]

        self.discrepancy_name = discrepancy_name
        self.weights = weights

    def __getattr__(self, item):
        """Allow more convenient access to items under self.meta."""
        if item in self.meta.keys():
            return self.meta[item]
        else:
            raise AttributeError("No attribute '{}' in this sample".format(item))

    def __dir__(self):
        """Allow autocompletion for items under self.meta.

        http://stackoverflow.com/questions/13603088/python-dynamic-help-and-autocomplete-generation
        """
        items = dir(type(self)) + list(self.__dict__.keys())
        items.extend(self.meta.keys())
        return items

    @property
    def n_samples(self):
        """Return the number of samples."""
        return len(self.outputs[self.parameter_names[0]])

    @property
    def dim(self):
        """Return the number of parameters."""
        return len(self.parameter_names)

    @property
    def discrepancies(self):
        """Return the discrepancy values."""
        return None if self.discrepancy_name is None else \
            self.outputs[self.discrepancy_name]

    @property
    def samples_array(self):
        """Return the samples as an array.

        The columns are in the same order as in self.parameter_names.

        Returns
        -------
        list of np.arrays

        """
        return np.column_stack(tuple(self.samples.values()))

    def __str__(self):
        """Return a summary of results as a string."""
        # create a buffer for capturing the output from summary's print statement
        stdout0 = sys.stdout
        buffer = io.StringIO()
        sys.stdout = buffer
        self.summary()
        sys.stdout = stdout0  # revert to original stdout
        return buffer.getvalue()

    def __repr__(self):
        """Return a summary of results as a string."""
        return self.__str__()

    def summary(self):
        """Print a verbose summary of contained results."""
        # TODO: include __str__ of Inference Task, seed?
        desc = "Method: {}\nNumber of samples: {}\n" \
            .format(self.method_name, self.n_samples)
        if hasattr(self, 'n_sim'):
            desc += "Number of simulations: {}\n".format(self.n_sim)
        if hasattr(self, 'threshold'):
            desc += "Threshold: {:.3g}\n".format(self.threshold)
        print(desc, end='')
        self.sample_means_summary()

    def sample_means_summary(self):
        """Print a representation of sample means."""
        s = "Sample means: "
        s += ', '.join(["{}: {:.3g}".format(k, v) for k, v in self.sample_means.items()])
        print(s)

    @property
    def sample_means(self):
        """Evaluate weighted averages of sampled parameters.

        Returns
        -------
        OrderedDict

        """
        return OrderedDict([(k, np.average(v, axis=0, weights=self.weights))
                            for k, v in self.samples.items()])

    @property
    def sample_means_array(self):
        """Evaluate weighted averages of sampled parameters.

        Returns
        -------
        np.array

        """
        return np.array(list(self.sample_means.values()))

    def plot_marginals(self, selector=None, bins=20, axes=None, **kwargs):
        """Plot marginal distributions for parameters.

        Parameters
        ----------
        selector : iterable of ints or strings, optional
            Indices or keys to use from samples. Default to all.
        bins : int, optional
            Number of bins in histograms.
        axes : one or an iterable of plt.Axes, optional

        Returns
        -------
        axes : np.array of plt.Axes

        """
        return vis.plot_marginals(self.samples, selector, bins, axes, **kwargs)

    def plot_pairs(self, selector=None, bins=20, axes=None, **kwargs):
        """Plot pairwise relationships as a matrix with marginals on the diagonal.

        The y-axis of marginal histograms are scaled.

        Parameters
        ----------
        selector : iterable of ints or strings, optional
            Indices or keys to use from samples. Default to all.
        bins : int, optional
            Number of bins in histograms.
        axes : one or an iterable of plt.Axes, optional

        Returns
        -------
        axes : np.array of plt.Axes

        """
        return vis.plot_pairs(self.samples, selector, bins, axes, **kwargs)


class SmcSample(Sample):
    """Container for results from SMC-ABC."""

    def __init__(self, method_name, outputs, parameter_names, populations, *args, **kwargs):
        """Initialize result.

        Parameters
        ----------
        method_name : str
        outputs : dict
        parameter_names : list
        populations : list[Sample]
            List of Sample objects
        args
        kwargs

        """
        super(SmcSample, self).__init__(
            method_name=method_name,
            outputs=outputs,
            parameter_names=parameter_names,
            *args,
            **kwargs)
        self.populations = populations

        if self.weights is None:
            raise ValueError("No weights provided for the sample")

    @property
    def n_populations(self):
        """Return the number of populations."""
        return len(self.populations)

    def summary(self, all=False):
        """Print a verbose summary of contained results.

        Parameters
        ----------
        all : bool, optional
            Whether to print the summary for all populations separately,
            or just the final population (default).

        """
        super(SmcSample, self).summary()

        if all:
            for i, pop in enumerate(self.populations):
                print('\nPopulation {}:'.format(i))
                pop.summary()

    def sample_means_summary(self, all=False):
        """Print a representation of sample means.

        Parameters
        ----------
        all : bool, optional
            Whether to print the means for all populations separately,
            or just the final population (default).

        """
        if all is False:
            super(SmcSample, self).sample_means_summary()
            return

        out = ''
        for i, pop in enumerate(self.populations):
            out += "Sample means for population {}: ".format(i)
            out += ', '.join(["{}: {:.3g}".format(k, v) for k, v in pop.sample_means.items()])
            out += '\n'
        print(out)

    def plot_marginals(self, selector=None, bins=20, axes=None, all=False, **kwargs):
        """Plot marginal distributions for parameters for all populations.

        Parameters
        ----------
        selector : iterable of ints or strings, optional
            Indices or keys to use from samples. Default to all.
        bins : int, optional
            Number of bins in histograms.
        axes : one or an iterable of plt.Axes, optional
        all : bool, optional
            Plot the marginals of all populations

        """
        if all is False:
            super(SmcSample, self).plot_marginals()
            return

        fontsize = kwargs.pop('fontsize', 13)
        for i, pop in enumerate(self.populations):
            pop.plot_marginals(selector=selector, bins=bins, axes=axes)
            plt.suptitle("Population {}".format(i), fontsize=fontsize)

    def plot_pairs(self, selector=None, bins=20, axes=None, all=False, **kwargs):
        """Plot pairwise relationships as a matrix with marginals on the diagonal.

        The y-axis of marginal histograms are scaled.

        Parameters
        ----------
        selector : iterable of ints or strings, optional
            Indices or keys to use from samples. Default to all.
        bins : int, optional
            Number of bins in histograms.
        axes : one or an iterable of plt.Axes, optional
        all : bool, optional
            Plot for all populations

        """
        if all is False:
            super(SmcSample, self).plot_marginals()
            return

        fontsize = kwargs.pop('fontsize', 13)
        for i, pop in enumerate(self.populations):
            pop.plot_pairs(selector=selector, bins=bins, axes=axes)
            plt.suptitle("Population {}".format(i), fontsize=fontsize)


class BolfiSample(Sample):
    """Container for results from BOLFI."""

    def __init__(self, method_name, chains, parameter_names, warmup, **kwargs):
        """Initialize result.

        Parameters
        ----------
        method_name : string
            Name of inference method.
        chains : np.array
            Chains from sampling, warmup included. Shape: (n_chains, n_samples, n_parameters).
        parameter_names : list : list of strings
            List of names in the outputs dict that refer to model parameters.
        warmup : int
            Number of warmup iterations in chains.

        """
        chains = chains.copy()
        shape = chains.shape
        n_chains = shape[0]
        warmed_up = chains[:, warmup:, :]
        concatenated = warmed_up.reshape((-1, ) + shape[2:])
        outputs = dict(zip(parameter_names, concatenated.T))

        super(BolfiSample, self).__init__(
            method_name=method_name,
            outputs=outputs,
            parameter_names=parameter_names,
            chains=chains,
            n_chains=n_chains,
            warmup=warmup,
            **kwargs)

    def plot_traces(self, selector=None, axes=None, **kwargs):
        """Plot MCMC traces."""
        return vis.plot_traces(self, selector, axes, **kwargs)
