# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from six import with_metaclass as _py_backwards_six_withmetaclass
import abc
from typing import *
import random
__all__ = (u'Input', u'Output', u'Params', u'PrimitiveBase', u'SamplingCompositionalityMixin',
           u'ProbabilisticCompositionalityMixin', u'Scores', u'Gradients', u'GradientCompositionalityMixin', u'InspectLossMixin')
Input = TypeVar(u'Input')
Output = TypeVar(u'Output')
Params = TypeVar(u'Params')


class PrimitiveBase(Generic[(Input, Output, Params)]):
    u'\n    A base class for all TA1 primitives.\n\n    Class is parametrized using three type variables, ``Input``, ``Output``, and ``Params``.\n    ``Params`` has to be a subclass of a `NamedTuple` and subclasses of this class should\n    define types for all fields of a provided named tuple.`\n\n    All arguments to all methods are keyword-only. In Python 3 this is enforced, in Python 2\n    this is not, but callers should still use only keyword-based arguments when calling to\n    be backwards and future compatible.\n\n    Subclasses of this class allow functional compositionality.\n    '

    def __init__(self):
        u"\n        All primitives should specify all the hyper-parameters that can be set at the class\n        level in their ``__init__`` as explicit typed keyword-only arguments\n        (no ``*args`` or ``**kwargs``).\n\n        Hyper-parameters are those primitive's parameters which are not changing during\n        a life-time of a primitive. Parameters which do are set using the ``set_params`` method.\n        "

    @abc.abstractmethod
    def produce(self, inputs):
        u"\n        Produce primitive's best choice of the output for each of the inputs.\n\n        Parameters\n        ----------\n        inputs : Sequence[Input]\n            The inputs of shape [num_inputs, ...].\n\n        Returns\n        -------\n        Sequence[Output]\n            The outputs of shape [num_inputs, ...].\n        "

    @abc.abstractmethod
    def fit(self, timeout=None, iterations=1):
        u"\n        Fits primitive using inputs and outputs (if any) using currently set training data.\n\n        If ``fit`` has already been called in the past on different training data,\n        this method fits it **again from scratch** using currently set training data.\n\n        On the other hand, caller can call ``fit`` multiple times on the same training data\n        to continue fitting.\n\n        If ``fit`` fully fits using provided training data, this method should return ``True``.\n        In this case there is no point in making further calls to this method with same training data,\n        and in fact further calls can be noops, or a primitive can decide to refit from scratch.\n\n        In the case fitting can continue with same training data, the method should return ``False``.\n        If ``fit`` is called again after that (without setting training data), the primitive has\n        to continue fitting.\n\n        Primitive can provide ``timeout`` information to guide the length of the fitting process. If primitive\n        reaches the timeout and was unable to fit, it should raise a ``TimeoutError`` exception to\n        signal that fitting was unsuccessful in the given time. Primitive should not be used anymore\n        after the exception because its state is undefined and can be broken.\n\n        Caller can provide how many of primitive's internal fitting iterations (for example, epochs)\n        should a primitive do before returning. Primitives should make iterations as small as reasonable.\n        If ``iterations`` is ``None``, then there is no limit no how many iterations the primitive should\n        do. This can be useful when combined with set ``timeout`` to allow for time-based only limit.\n\n        Subclasses can extend arguments of this method with explicit typed keyword arguments used during\n        the fitting process. For example, they can accept other primitives through an argument representing\n        a regularizer to use during fitting. The reason why those are not part of constructor arguments is\n        that one can create primitives in any order before having to invoke them or pass them to other\n        primitives.\n\n        Parameters\n        ----------\n        timeout : float\n            A maximum time this primitive should be fitting during this method call, in seconds.\n        iterations : int\n            How many of internal iterations should the primitive do.\n\n        Returns\n        -------\n        bool\n            Has fitting fully finished on current training data?\n        "

    @abc.abstractmethod
    def get_params(self):
        u'\n        Returns parameters of this primitive.\n\n        Parameters are all parameters of the primitive which can potentially change during a life-time of\n        a primitive. Parameters which cannot are passed through constructor.\n\n        Parameters should include all data which is necessary to create a new instance of this primitive\n        behaving exactly the same as this instance, when the new instance is created by passing the same\n        parameters to the class constructor and calling ``set_params``.\n\n        Returns\n        -------\n        Params\n            A named tuple of parameters.\n        '

    @abc.abstractmethod
    def set_params(self, params):
        u'\n        Sets parameters of this primitive.\n\n        Parameters are all parameters of the primitive which can potentially change during a life-time of\n        a primitive. Parameters which cannot are passed through constructor.\n\n        Parameters\n        ----------\n        params : Params\n            A named tuple of parameters.\n        '

    def set_random_seed(self, seed):
        u"\n        Sets a random seed for all operations from now on inside the primitive.\n\n        By default it sets numpy's and Python's random seed.\n\n        Parameters\n        ----------\n        seed : int\n            A random seed to use.\n        "
        try:
            import numpy
            numpy.random.seed(seed)
        except ImportError:
            pass
        random.seed(seed)


class ContinueFitMixin(Generic[(Input, Output, Params)]):

    @abc.abstractmethod
    def continue_fit(self, timeout=None, iterations=1):
        u'\n        Similar to base ``fit``, this method fits the primitive using inputs and outputs (if any)\n        using currently set training data.\n\n        The difference is what happens when currently set training data is different from\n        what the primitive might have already been fitted on. ``fit`` fits the primitive from\n        scratch, while ``continue_fit`` fits it further and does **not** start from scratch.\n\n        Caller can still call ``continue_fit`` multiple times on the same training data as well,\n        in which case primitive should try to improve the fit in the same way as with ``fit``.\n\n        From the perspective of a caller of all other methods, the training data in effect\n        is still just currently set training data. If a caller wants to call ``gradient_output``\n        on all data on which the primitive has been fitted through multiple calls of ``continue_fit``\n        on different training data, the caller should pass all this data themselves through\n        another call to ``set_training_data``, do not call ``fit`` or ``continue_fit`` again,\n        and use ``gradient_output`` method. In this way primitives which truly support\n        continuation of fitting and need only the latest data to do another fitting, do not\n        have to keep all past training data around themselves.\n\n        If a primitive supports this mixin, then both ``fit`` and ``continue_fit`` can be\n        called. ``continue_fit`` always continues fitting, if it was started through ``fit``\n        or ``continue_fit``. And ``fit`` always restarts fitting, even if previously\n        ``continue_fit`` was used.\n\n        Parameters\n        ----------\n        timeout : float\n            A maximum time this primitive should be fitting during this method call, in seconds.\n        iterations : int\n            How many of internal iterations should the primitive do.\n\n        Returns\n        -------\n        bool\n            Has fitting fully finished on current training data?\n        '


class SamplingCompositionalityMixin(Generic[(Input, Output, Params)]):
    u'\n    This mixin signals to a caller that the primitive is probabilistic but\n    may be likelihood free.\n\n    Mixin should be used together with the ``PrimitiveBase`` class.\n    '

    @abc.abstractmethod
    def sample_one(self, input, num_samples=1):
        u'\n        Sample ``num_samples`` outputs for one input ``input``.\n\n        Parameters\n        ----------\n        input : Input\n            The input.\n        num_samples : int\n            The number of samples to return.\n\n        Returns\n        -------\n        Sequence[Output]\n            The set of samples of shape [num_samples, ...].\n        '

    def sample_multiple(self, inputs, num_samples=1):
        u'\n        Sample multiple inputs at once.\n\n        Parameters\n        ----------\n        inputs : Sequence[Input]\n            The inputs of shape [num_inputs, ...].\n        num_samples : int\n            The number of samples to return in a set of samples.\n\n        Returns\n        -------\n        Sequence[Sequence[Output]]\n            The multiple sets of samples of shape [num_inputs, num_samples, ...].\n        '
        return [self.sample_one(input=input, num_samples=num_samples) for input in inputs]


class ProbabilisticCompositionalityMixin(Generic[(Input, Output, Params)]):
    u'\n    This mixin provides additional abstract methods which primitives should implement to\n    help callers with doing various end-to-end refinements using probabilistic\n    compositionality.\n\n    This mixin adds methods to support at least:\n\n    * Metropolis-Hastings\n\n    Mixin should be used together with the ``PrimitiveBase`` class and ``SamplingCompositionalityMixin`` mixin.\n    '

    @abc.abstractmethod
    def log_likelihood(self, output, input):
        u'\n        Returns log probability of output given input and params under this primitive:\n\n        log(p(output | input, params))\n\n        Parameters\n        ----------\n        output : Output\n            The output.\n        input : Input\n            The input.\n\n        Returns\n        -------\n        float\n            log(p(output | input, params))\n        '


class Scores(Generic[Params]):
    u'\n    A type representing a named tuple which holds all the differentiable fields from ``Params``.\n    Their values are of type ``float``.\n    '


class Gradients(Generic[Output]):
    u'\n    A type representing a structure of ``Output``, but the values are of type ``Optional[float]``.\n    Value is ``None`` if gradient for that part of the structure is not possible.\n    '


class GradientCompositionalityMixin(Generic[(Input, Output, Params)]):
    u'\n    This mixin provides additional abstract methods which primitives should implement to\n    help callers with doing various end-to-end refinements using gradient-based\n    compositionality.\n\n    This mixin adds methods to support at least:\n\n    * gradient-based, compositional end-to-end training\n    * regularized pre-training\n    * multi-task adaptation\n    * black box variational inference\n    * Hamiltonian Monte Carlo\n    '

    @abc.abstractmethod
    def gradient_output(self, outputs, inputs):
        u'\n        Returns the gradient of loss sum_i(L(output_i, produce_one(input_i))) with respect to output.\n\n        When fit term temperature is set to non-zero, it should return the gradient with respect to output of:\n\n        sum_i(L(output_i, produce_one(input_i))) + temperature * sum_i(L(training_output_i, produce_one(training_input_i)))\n\n        When used in combination with the ``ProbabilisticCompositionalityMixin``, it returns gradient\n        of sum_i(log(p(output_i | input_i, params))) with respect to output.\n\n        When fit term temperature is set to non-zero, it should return the gradient with respect to output of:\n\n        sum_i(log(p(output_i | input_i, params))) + temperature * sum_i(log(p(training_output_i | training_input_i, params)))\n\n        Parameters\n        ----------\n        outputs : Sequence[Output]\n            The outputs.\n        inputs : Sequence[Input]\n            The inputs.\n\n        Returns\n        -------\n        Gradients[Output]\n            Gradients.\n        '

    @abc.abstractmethod
    def gradient_params(self, outputs, inputs):
        u'\n        Returns the gradient of loss sum_i(L(output_i, produce_one(input_i))) with respect to params.\n\n        When fit term temperature is set to non-zero, it should return the gradient with respect to params of:\n\n        sum_i(L(output_i, produce_one(input_i))) + temperature * sum_i(L(training_output_i, produce_one(training_input_i)))\n\n        When used in combination with the ``ProbabilisticCompositionalityMixin``, it returns gradient of\n        log(p(output | input, params)) with respect to params.\n\n        When fit term temperature is set to non-zero, it should return the gradient with respect to params of:\n\n        sum_i(log(p(output_i | input_i, params))) + temperature * sum_i(log(p(training_output_i | training_input_i, params)))\n\n        Parameters\n        ----------\n        outputs : Sequence[Output]\n            The outputs.\n        inputs : Sequence[Input]\n            The inputs.\n\n        Returns\n        -------\n        Scores[Params]\n            A named tuple with all fields from ``Params`` and values set to gradient for each parameter.\n        '

    @abc.abstractmethod
    def set_fit_term_temperature(self, temperature=0):
        u'\n        Sets the temperature used in ``gradient_output`` and ``gradient_params``.\n\n        Parameters\n        ----------\n        temperature : float\n            The temperature to use, [0, inf), typically, [0, 1].\n        '


class InspectLossMixin(
        _py_backwards_six_withmetaclass(abc.ABCMeta, *[object])):
    u'\n    Mixin which provides an abstract method for a caller to call to inspect which\n    loss function a primitive is using internally.\n    '

    @abc.abstractmethod
    def get_loss_function(self):
        u'\n        Returns a D3M standard name of the loss function used by the primitive, or ``None`` if using\n        a non-standard loss function or if the primitive does not use a loss function at all.\n\n        Returns\n        -------\n        str\n            A D3M standard name of the loss function used.\n        '
