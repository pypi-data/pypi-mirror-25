import abc
from typing import *
import random

import numpy

__all__ = (
    'Input', 'Output', 'Params', 'PrimitiveBase', 'SamplingCompositionalityMixin',
    'ProbabilisticCompositionalityMixin', 'Scores', 'Gradients', 'GradientCompositionalityMixin',
    'InspectLossMixin',
)


Input = TypeVar('Input')
Output = TypeVar('Output')
Params = TypeVar('Params', bound=NamedTuple)


class PrimitiveBase(Generic[Input, Output, Params]):
    """
    A base class for all TA1 primitives.

    Class is parametrized using three type variables, ``Input``, ``Output``, and ``Params``.
    ``Params`` has to be a subclass of a `NamedTuple` and subclasses of this class should
    define types for all fields of a provided named tuple.`

    All arguments to all methods should be keyword-only.

    Subclasses of this class allow functional compositionality.
    """

    def __init__(self) -> None:
        """
        All primitives should specify all the hyper-parameters that can be set at the class
        level in their ``__init__`` as explicit typed keyword-only arguments
        (no ``*args`` or ``**kwargs``).

        Hyper-parameters are those primitive's parameters which are not changing during
        a life-time of a primitive. Parameters which do are set using the ``set_params`` method.
        """

    @abc.abstractmethod
    def produce(self, *, inputs: Sequence[Input] = None) -> Sequence[Output]:
        """
        Produce primitive's best choice of the output for each of the inputs.

        Parameters
        ----------
        inputs : Sequence[Input]
            The inputs of shape [num_inputs, ...].

        Returns
        -------
        Sequence[Output]
            The outputs of shape [num_inputs, ...].
        """

    @abc.abstractmethod
    def set_training_data(self, *, inputs: Sequence[Input] = None, outputs: Sequence[Output] = None) -> None:
        """
        Sets training data of this primitive.

        Both inputs and outputs are optional in the base class, but subclasses can require one
        or both of them. For example, supervised learning subclass requires both.

        Parameters
        ----------
        inputs : Sequence[Input]
            The inputs.
        outputs : Sequence[Output]
            The outputs.
        """

    @abc.abstractmethod
    def fit(self, *, timeout: float = None, iterations: Optional[int] = 1) -> bool:
        """
        Fits primitive using inputs and outputs (if any) using currently set training data.

        If ``fit`` has already been called in the past on different training data,
        this method fits it **again from scratch** using currently set training data.

        On the other hand, caller can call ``fit`` multiple times on the same training data
        to continue fitting.

        If ``fit`` fully fits using provided training data, this method should return ``True``.
        In this case there is no point in making further calls to this method with same training data,
        and in fact further calls can be noops, or a primitive can decide to refit from scratch.

        In the case fitting can continue with same training data, the method should return ``False``.
        If ``fit`` is called again after that (without setting training data), the primitive has
        to continue fitting.

        Primitive can provide ``timeout`` information to guide the length of the fitting process. If primitive
        reaches the timeout and was unable to fit, it should raise a ``TimeoutError`` exception to
        signal that fitting was unsuccessful in the given time. Primitive should not be used anymore
        after the exception because its state is undefined and can be broken.

        Caller can provide how many of primitive's internal fitting iterations (for example, epochs)
        should a primitive do before returning. Primitives should make iterations as small as reasonable.
        If ``iterations`` is ``None``, then there is no limit no how many iterations the primitive should
        do. This can be useful when combined with set ``timeout`` to allow for time-based only limit.

        Subclasses can extend arguments of this method with explicit typed keyword arguments used during
        the fitting process. For example, they can accept other primitives through an argument representing
        a regularizer to use during fitting. The reason why those are not part of constructor arguments is
        that one can create primitives in any order before having to invoke them or pass them to other
        primitives.

        Parameters
        ----------
        timeout : float
            A maximum time this primitive should be fitting, in seconds.
        iterations : int
            How many of internal iterations should the primitive do.

        Returns
        -------
        bool
            Has fitting fully finished on current training data?
        """

    @abc.abstractmethod
    def get_params(self) -> Params:
        """
        Returns parameters of this primitive.

        Parameters are all parameters of the primitive which can potentially change during a life-time of
        a primitive. Parameters which cannot are passed through constructor.

        Parameters should include all data which is necessary to create a new instance of this primitive
        behaving exactly the same as this instance, when the new instance is created by passing the same
        parameters to the class constructor and calling ``set_params``.

        Returns
        -------
        Params
            A named tuple of parameters.
        """

    @abc.abstractmethod
    def set_params(self, *, params: Params) -> None:
        """
        Sets parameters of this primitive.

        Parameters are all parameters of the primitive which can potentially change during a life-time of
        a primitive. Parameters which cannot are passed through constructor.

        Parameters
        ----------
        params : Params
            A named tuple of parameters.
        """

    def set_random_seed(self, *, seed: int) -> None:
        """
        Sets a random seed for all operations from now on inside the primitive.

        By default it sets numpy's and Python's random seed.

        Parameters
        ----------
        seed : int
            A random seed to use.
        """

        numpy.random.seed(seed)
        random.seed(seed)


class SamplingCompositionalityMixin(Generic[Input, Output, Params]):
    """
    This mixin signals to a caller that the primitive is probabilistic but
    may be likelihood free.

    Mixin should be used together with the ``PrimitiveBase`` class.
    """

    @abc.abstractmethod
    def sample_one(self, *, input: Input = None, num_samples: int = 1) -> Sequence[Output]:
        """
        Sample ``num_samples`` outputs for one input ``input``.

        Parameters
        ----------
        input : Input
            The input.
        num_samples : int
            The number of samples to return.

        Returns
        -------
        Sequence[Output]
            The set of samples of shape [num_samples, ...].
        """

    def sample_multiple(self, *, inputs: Sequence[Input], num_samples: int = 1) -> Sequence[Sequence[Output]]:
        """
        Sample multiple inputs at once.

        Parameters
        ----------
        inputs : Sequence[Input]
            The inputs of shape [num_inputs, ...].
        num_samples : int
            The number of samples to return in a set of samples.

        Returns
        -------
        Sequence[Sequence[Output]]
            The multiple sets of samples of shape [num_inputs, num_samples, ...].
        """

        return [self.sample_one(input, num_samples) for input in inputs]


class ProbabilisticCompositionalityMixin(Generic[Input, Output, Params]):
    """
    This mixin provides additional abstract methods which primitives should implement to
    help callers with doing various end-to-end refinements using probabilistic
    compositionality.

    This mixin adds methods to support at least:

    * Metropolis-Hastings

    Mixin should be used together with the ``PrimitiveBase`` class and ``SamplingCompositionalityMixin`` mixin.
    """

    @abc.abstractmethod
    def log_likelihood(self, *, output: Output, input: Input = None) -> float:
        """
        Returns log probability of output given input and params under this primitive:

        log(p(output | input, params))

        Parameters
        ----------
        output : Output
            The output.
        input : Input
            The input.

        Returns
        -------
        float
            log(p(output | input, params))
        """


class Scores(Generic[Params]):
    """
    A type representing a named tuple which holds all the differentiable fields from ``Params``
    """


class Gradients(Generic[Output]):
    """
    A type representing a structure of ``Output``, but the values are of type ``Optional[float]``.
    """


class GradientCompositionalityMixin(Generic[Input, Output, Params]):
    """
    This mixin provides additional abstract methods which primitives should implement to
    help callers with doing various end-to-end refinements using gradient-based
    compositionality.

    This mixin adds methods to support at least:

    * gradient-based, compositional end-to-end training
    * regularized pre-training
    * multi-task adaptation
    * black box variational inference
    * Hamiltonian Monte Carlo
    """

    @abc.abstractmethod
    def gradient_output(self, *, outputs: Sequence[Output], inputs: Sequence[Input] = None) -> Gradients[Output]:
        """
        Returns the gradient of loss sum_i(L(output_i, produce_one(input_i))) with respect to output.

        When fit term temperature is set to non-zero, it should return the gradient with respect to output of:

        sum_i(L(output_i, produce_one(input_i))) + temperature * sum_i(L(training_output_i, produce_one(training_input_i)))

        When used in combination with the ``ProbabilisticCompositionalityMixin``, it returns gradient
        of sum_i(log(p(output_i | input_i, params))) with respect to output.

        When fit term temperature is set to non-zero, it should return the gradient with respect to output of:

        sum_i(log(p(output_i | input_i, params))) + temperature * sum_i(log(p(training_output_i | training_input_i, params)))

        Parameters
        ----------
        outputs : Sequence[Output]
            The outputs.
        inputs : Sequence[Input]
            The inputs.

        Returns
        -------
        Gradients[Output]
            Gradients.
        """

    @abc.abstractmethod
    def gradient_params(self, *, outputs: Sequence[Output], inputs: Sequence[Input] = None) -> Scores[Params]:
        """
        Returns the gradient of loss sum_i(L(output_i, produce_one(input_i))) with respect to params.

        When fit term temperature is set to non-zero, it should return the gradient with respect to params of:

        sum_i(L(output_i, produce_one(input_i))) + temperature * sum_i(L(training_output_i, produce_one(training_input_i)))

        When used in combination with the ``ProbabilisticCompositionalityMixin``, it returns gradient of
        log(p(output | input, params)) with respect to params.

        When fit term temperature is set to non-zero, it should return the gradient with respect to params of:

        sum_i(log(p(output_i | input_i, params))) + temperature * sum_i(log(p(training_output_i | training_input_i, params)))

        Parameters
        ----------
        outputs : Sequence[Output]
            The outputs.
        inputs : Sequence[Input]
            The inputs.

        Returns
        -------
        Scores[Params]
            A named tuple with all fields from ``Params`` and values set to gradient for each parameter.
        """

    @abc.abstractmethod
    def set_fit_term_temperature(self, *, temperature: float = 0) -> None:
        """
        Sets the temperature used in ``gradient_output`` and ``gradient_params``.

        Parameters
        ----------
        temperature : float
            The temperature to use, [0, inf), typically, [0, 1].
        """


class InspectLossMixin(abc.ABC):
    """
    Mixin which provides an abstract method for a caller to call to inspect which
    loss function a primitive is using internally.
    """

    @abc.abstractmethod
    def get_loss_function(self) -> Optional[str]:
        """
        Returns a D3M standard name of the loss function used by the primitive, or ``None`` if using
        a non-standard loss function or if the primitive does not use a loss function at all.

        Returns
        -------
        str
            A D3M standard name of the loss function used.
        """
