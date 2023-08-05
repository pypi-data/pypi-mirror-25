from inspect import getfullargspec
from numbers import Integral
from typing import Callable, Dict, Any, Set

from decorator import decorate

from autoclass.utils import _create_function_decorator__robust_to_args, apply_on_func_args


def validate(**validators: Dict[str, Callable[[Any], bool]]):
    """
    Defines a decorator with parameters, that will execute the provided input validators PRIOR to executing the 
    function. Specific entry 'returns' may contain validators executed AFTER executing the function.
    
    ```
    def is_even(x):
        return x % 2 == 0
    
    def gt(a):
        def gt(x):
            return x >= a
        return gt
    
    @validate(a=[is_even, gt(1)], b=is_even)
    def myfunc(a, b):
        print('hello')
    ```
    
    will generate the equivalent of :
    
    ```
    def myfunc(a, b):
        gt1 = gt(1)
        if is_even(a) and gt1(a) and is_even(b):
            print('hello')
        else:
            raise ValidationError(...)
    ```
    
    :param validators: 
    :return: 
    """
    return _create_function_decorator__robust_to_args(validate_decorate, **validators)


def validate_decorate(func: Callable, **validators: Dict[str, Callable[[Any], bool]]) -> Callable:
    """
    Defines a decorator with parameters, that will execute the provided input validators PRIOR to executing the 
    function. Specific entry 'returns' may contain validators executed AFTER executing the function.
    
    :param func: 
    :param include: 
    :param exclude: 
    :return: 
    """
    # (1) retrieve function signature
    # attrs, varargs, varkw, defaults = getargspec(func)
    signature_attrs, signature_varargs, signature_varkw, signature_defaults, signature_kwonlyargs, \
    signature_kwonlydefaults, signature_annotations = getfullargspec(func)
    # TODO better use signature(func) ? but that would be less compliant with python 2

    # (2) check that provided validators dont contain names that are incorrect
    if validators is not None:
        incorrect = set(validators.keys()) - set(signature_attrs)
        if len(incorrect) > 0:
            raise ValueError('@validate definition exception: validators are defined for \'' + str(incorrect) + '\' '
                             'that is/are not part of signature for ' + str(func))
    # for att_name, att_validators in validators.items():
    #     i = att_validators.index(not_none)
    #     if i > 0:
    #         raise ValueError('not_none is a special validator that can only be provided at the beginning of the'
    #                          ' validators list')

    # replace validators lists with explicit and_ if needed
    for att_name, att_validators in validators.items():
        att_validators = _assert_list_and_protect_not_none(att_validators, allow_not_none=True)
        if att_validators[0] != not_none:
            # att_validators is a list not containing not_none: wrap in an 'and_' and wrap with a none-ignoring checker
            validators[att_name] = _not_none_checker(and_(att_validators), ignore_none_silently=True)
        else:
            # first element of att_validators is not_none
            if len(att_validators) > 1:
                # remove not_none from the list, wrap witha and_, and wrap with the corresponding_not_none_checker
                validators[att_name] = _not_none_checker(and_(att_validators[1:]), ignore_none_silently=False)
            else:
                # one element in the list only (not_none): include it directly
                validators[att_name] = att_validators[0]

    # (3) create a wrapper around the function to add validation
    # -- old:
    # @functools.wraps(func) -> to make the wrapper function look like the wrapped function
    # def wrapper(self, *args, **kwargs):
    # -- new:
    # we now use 'decorate' at the end of this code to have a wrapper that has the same signature, see below
    def wrapper(func, *args, **kwargs):
        # apply _validate on all received arguments
        apply_on_func_args(func, args, kwargs, signature_attrs, signature_defaults, signature_varargs, signature_varkw,
                           _validate, validators)

        # finally execute the method
        return func(*args, **kwargs)

    a = decorate(func, wrapper)
    # save the validators somewhere for reference
    a.__validators__ = validators
    return a


def _not_none_checker(validator, ignore_none_silently: bool = True):
    """
    Generates a checker handling None values. When a None value is received, it is not passed to the validator.
    Instead this operator will either drop silently (ignore_none_silently = True) or return a False
    (ignore_none_silently=False)

    :param validator:
    :param ignore_none_silently:
    :return:
    """
    if ignore_none_silently:
        def drop_none_silently(x):
            if not_none(x):
                return validator(x)
            else:
                # value is None : skip validation (users should explicitly include 'not_none' as the first validator to
                # change this behaviour)
                return True
        return drop_none_silently
    else:
        def check_not_none(x):
            if not_none(x):
                return validator(x)
            else:
                return False
        return check_not_none


def _validate(value_to_validate, validator_func, func, att_name):
    """
    Subroutine that actually executes validation

    :param value_to_validate: the value to validate
    :param validator_func: the validator function that will be applied on value_to_validate
    :param func: the method for which this validation is performed. This is used just for errors
    :param att_name: the name of the attribute that is being validated
    :return:
    """
    # new: validator_func should always be a single element here
    res = validator_func(value_to_validate)
    if res not in {None, True}:
        raise ValidationError.create(func, att_name, validator_func, value_to_validate)


class ValidationError(Exception):
    """
    Exception raised whenever validation fails. It may be directly triggered by Validators, or it is raised if 
    validator returns false
    """

    def __init__(self, contents):
        """
        We actually can't put more than 1 argument in the constructor, it creates a bug in Nose tests
        https://github.com/nose-devs/nose/issues/725
        
        Please use ValidationError.create() instead

        :param contents:
        """
        super(ValidationError, self).__init__(contents)

    @staticmethod
    def create(func, att_name, validator_func, item, extra_msg: str = None):
        """
        
        :param func:
        :param att_name:
        :param validator_func: 
        :param item: 
        :param extra_msg
        :return: 
        """
        return ValidationError('Error validating input ' + str(att_name) + '=\'' + str(item) + '\' for function \''
                               + str(func) + '\' with validator ' + (validator_func.__name__ or str(validator_func))
                               + (('.\n  ' + extra_msg) if extra_msg else ''))


def get_names(validators):
    return ', '.join([val.__name__ for val in validators])


# ----------- some convenient validators ...
def not_none(x: Any):
    """ 'Is not None' validator """
    return x is not None


def and_(validators):
    """
    An 'and' validator: returns True if all of the provided validators are happy with the input. This method will
    raise a ValidationException on the first False received or Exception caught

    :param validators:
    :return:
    """

    validators = _assert_list_and_protect_not_none(validators)

    if len(validators) == 1:
        return validators[0]  # simplification for single validator case
    else:
        def and_v_(x):
            for validator in validators:
                res = validator(x)
                if res not in {None, True}:
                    # one validator was unhappy > raise
                    raise ValidationError('and(' + get_names(validators) + '): Validator ' + str(validator)
                                          + ' failed validation for input ' + str(x))
            return True

        return and_v_


def or_(validators):
    """
    An 'or' validator: returns True if at least one of the provided validators is happy with the input. All exceptions
    will be silently caught. In case of failure, a global ValidationException will be raised, together with the first
    exception message if any.

    :param validators:
    :return:
    """

    validators = _assert_list_and_protect_not_none(validators)

    if len(validators) == 1:
        return validators[0]  # simplification for single validator case
    else:
        def or_v_(x):
            err = None
            for validator in validators:
                try:
                    res = validator(x)
                    if res in {None, True}:
                        # we can return : one validator was happy
                        return True
                except Exception as e:
                    if err is None:
                        err = e  # remember the first exception

            # no validator accepted: raise
            msg = 'or(' + get_names(validators) + '): All validators failed validation for input \'' + str(x) + '\'. '
            if err is not None:
                msg += 'First exception caught was: \'' + str(err) + '\''
            raise ValidationError(msg)

        return or_v_


def xor_(validators):
    """
    A 'xor' validator: returns True if exactly one of the provided validators is happy with the input. All
    exceptions will be silently caught. In case of failure, a global ValidationException will be raised, together with
    the first exception message if any.

    :param validators:
    :return:
    """

    validators = _assert_list_and_protect_not_none(validators)

    if len(validators) == 1:
        return validators[0]  # simplification for single validator case
    else:
        def xor_v_(x):
            ok_validator = None
            sec_validator = None
            err = None
            for validator in validators:
                try:
                    res = validator(x)
                    if res in {None, True}:
                        if ok_validator is not None:
                            sec_validator = validator
                        else:
                            # we found the first one happy
                            ok_validator = validator
                except Exception as e:
                    if err is None:
                        err = e  # remember the first exception

            # return if were happy or not
            if ok_validator is not None:
                if sec_validator is None:
                    # one unique validator happy: success
                    return True
                else:
                    # second validator happy : fail, too many validators happy
                    raise ValidationError('xor(' + get_names(validators) + ') : Too many validators succeeded : '
                                          + str(ok_validator) + ' + ' + str(sec_validator))
            else:
                # no validator happy
                msg = 'xor(' + get_names(validators) + '): All validators failed validation for input \'' + str(x) + '\'. '
                if err is not None:
                    msg += 'First exception caught was: \'' + str(err) + '\''
                raise ValidationError(msg)

        return xor_v_


def _assert_list_and_protect_not_none(validators, allow_not_none: bool = False):
    """
     * if validators is an empty list, throw error
     * If validators is a singleton, turns it into a list.
     * If validators contains not_none and allow_not_none is set to True, asserts that not_none is first in the list
     * If validators contains not_none and allow_not_none is set to False, asserts that not_none is not present at all
     in the list

    :param validators:
    :param allow_not_none:
    :return:
    """
    i = -1
    try:
        i = validators.index(not_none)
    except ValueError:
        # not_none not found in validators list : ok
        pass
    except AttributeError:
        # validators is not a list (no attribute 'index'): turn it into a list
        validators = [validators]

    # not_none ?
    if i > 0 or (i == 0 and not allow_not_none):
        raise ValueError('not_none is a special validator that can only be provided at the beginning of the'
                         ' global validators list')
    # empty list ?
    if len(validators) == 0:
        raise ValueError('provided validators list is empty')

    return validators


def not_(validator, catch_all: bool = False):
    """
    Generates the inverse of the provided validator: when the validator returns False or raises a `ValidationError`,
    this validator returns True. Otherwise it returns False. If the `catch_all` parameter is set to `True`, any
    exception will be caught instead of just `ValidationError`s.

    Note that you may provide a list of validators to `not_()`. It will be interpreted as `not_(and_(<valiators_list>))`

    :param validator:
    :param catch_all: an optional boolean flag. By default, only ValidationError are silently catched and turned into
    a 'ok' result. Turning this flag to True will assume that all exceptions should be catched and turned to a
    'ok' result
    :return:
    """

    # in case this is a validator list, create a 'and_' around it (otherwise this returns the validator)
    validator = and_(validator)

    def not_v_(x):
        if catch_all:
            try:
                res = validator(x)
                if res not in {None, True}:  # inverse the result
                    return True
            except:
                return True  # caught exception: return True

            # if we're here that's a failure
            raise ValidationError('not(' + str(validator) + '): Validator validated input \'' + str(x) + '\' with success, '
                                  'therefore the not() is a failure')
        else:
            try:
                res = validator(x)
                if res not in {None, True}:  # inverse the result
                    return True
            except ValidationError:
                return True  # caught exception: return True

            # if we're here that's a failure
            raise ValidationError('not(' + str(validator) + '): Validator validated input \'' + str(x) + '\' with success, '
                                  'therefore the not() is a failure')
    return not_v_


# ------------- orderables ----------------
def gt(min_value: Any, strict: bool = False):
    """
    'Greater than' validator generator.
    Returns a validator to check that x >= min_value (strict=False, default) or x > min_value (strict=True)

    :param min_value: minimum value for x
    :param strict: Boolean flag to switch between x >= min_value (strict=False) and x > min_value (strict=True)
    :return:
    """
    if strict:
        def gt(x):
            if x > min_value:
                return True
            else:
                raise ValidationError('gt: x > ' + str(min_value) + ' does not hold for x=' + str(x))
    else:
        def gt(x):
            if x >= min_value:
                return True
            else:
                raise ValidationError('gt: x >= ' + str(min_value) + ' does not hold for x=' + str(x))
    return gt


def gts(min_value_strict: Any):
    """ Alias for 'greater than' validator generator in strict mode """
    return gt(min_value_strict, True)


def lt(max_value: Any, strict: bool = False):
    """
    'Lesser than' validator generator.
    Returns a validator to check that x <= max_value (strict=False, default) or x < max_value (strict=True)

    :param max_value: maximum value for x
    :param strict: Boolean flag to switch between x <= max_value (strict=False) and x < max_value (strict=True)
    :return:
    """
    if strict:
        def lt(x):
            if x < max_value:
                return True
            else:
                raise ValidationError('lt: x < ' + str(max_value) + ' does not hold for x=' + str(x))
    else:
        def lt(x):
            if x <= max_value:
                return True
            else:
                raise ValidationError('lt: x <= ' + str(max_value) + ' does not hold for x=' + str(x))
    return lt


def lts(max_value_strict: Any):
    """ Alias for 'lesser than' validator generator in strict mode """
    return gt(max_value_strict, True)


def between(min_val: Any, max_val: Any, open_left: bool = False, open_right: bool = False):
    """
    'Is between' validator generator.
    Returns a validator to check that min_val <= x <= max_val (default). open_right and open_left flags allow to
    transform each side into strict mode. For example setting open_left=True will enforce min_val < x <= max_val

    :param min_val: minimum value for x
    :param max_val: maximum value for x
    :param open_left: Boolean flag to turn the left inequality to strict mode
    :param open_right: Boolean flag to turn the right inequality to strict mode
    :return:
    """
    if open_left and open_right:
        def between(x):
            if (min_val < x) and (x < max_val):
                return True
            else:
                raise ValidationError('between: ' + str(min_val) + ' < x < ' + str(max_val) + ' does not hold for x='
                                      + str(x))
    elif open_left:
        def between(x):
            if (min_val < x) and (x <= max_val):
                return True
            else:
                raise ValidationError('between: ' + str(min_val) + ' < x <= ' + str(max_val) + ' does not hold for x='
                                      + str(x))
    elif open_right:
        def between(x):
            if (min_val <= x) and (x < max_val):
                return True
            else:
                raise ValidationError('between: ' + str(min_val) + ' <= x < ' + str(max_val) + ' does not hold for x='
                                      + str(x))
    else:
        def between(x):
            if (min_val <= x) and (x <= max_val):
                return True
            else:
                raise ValidationError('between: ' + str(min_val) + ' <= x <= ' + str(max_val) + ' does not hold for x='
                                      + str(x))
    return between


# ------------- integers ------------------
def is_even(x: Integral):
    """ Validates that x is even (`x % 2 == 0`) """
    return x % 2 == 0


def is_odd(x: Integral):
    """ Validates that x is odd (`x % 2 != 0`) """
    return x % 2 != 0


def is_mod(ref):
    """ Validates that x is a multiple of the reference (`x % ref == 0`) """
    def is_mod(x):
        if x % ref == 0:
            return True
        else:
            raise ValidationError('is_mod: x % ' + str(ref) + ' == 0 does not hold for x=' + str(x))
    return is_mod


# ------------- collections ----------------
def minlen(min_length: Integral, strict: bool = False):
    """
    'Minimum length' validator generator.
    Returns a validator to check that len(x) >= min_length (strict=False, default) or len(x) > min_length (strict=True)

    :param min_length: minimum length for x
    :param strict: Boolean flag to switch between len(x) >= min_length (strict=False) and len(x) > min_length
    (strict=True)
    :return:
    """
    if strict:
        def minlen(x):
            if len(x) > min_length:
                return True
            else:
                raise ValidationError('minlen: len(x) > ' + str(min_length) + ' does not hold for x=' + str(x))
    else:
        def minlen(x):
            if len(x) >= min_length:
                return True
            else:
                raise ValidationError('minlen: len(x) >= ' + str(min_length) + ' does not hold for x=' + str(x))
    return minlen


def minlens(min_length_strict: Integral):
    """ Alias for 'Minimum length' validator generator in strict mode """
    return minlen(min_length_strict, True)


def maxlen(max_length: Integral, strict: bool = False):
    """
    'Maximum length' validator generator.
    Returns a validator to check that len(x) <= max_length (strict=False, default) or len(x) < max_length (strict=True)

    :param max_length: maximum length for x
    :param strict: Boolean flag to switch between len(x) <= max_length (strict=False) and len(x) < max_length
    (strict=True)
    :return:
    """
    if strict:
        def maxlen(x):
            if len(x) < max_length:
                return True
            else:
                raise ValidationError('maxlen: len(x) < ' + str(max_length) + ' does not hold for x=' + str(x))
    else:
        def maxlen(x):
            if len(x) <= max_length:
                return True
            else:
                raise ValidationError('maxlen: len(x) <= ' + str(max_length) + ' does not hold for x=' + str(x))
    return maxlen


def maxlens(max_length_strict: Integral):
    """ Alias for 'Maximum length' validator generator in strict mode """
    return maxlen(max_length_strict, True)


def is_in(allowed_values: Set):
    """
    'Values in' validator generator.
    Returns a validator to check that x is in the provided set of allowed values

    :param allowed_values: a set of allowed values
    :return:
    """
    def valin(x):
        if x in allowed_values:
            return True
        else:
            raise ValidationError('is_in: x in ' + str(allowed_values) + ' does not hold for x=' + str(x))
    return valin


def is_subset(reference_set: Set):
    """
    'Is subset' validator generator.
    Returns a validator to check that x is a subset of reference_set

    :param reference_set: the reference set
    :return:
    """
    def is_subset(x):
        missing = x - reference_set
        if len(missing) == 0:
            return True
        else:
            raise ValidationError('is_subset: len(x - reference_set) == 0 does not hold for x=' + str(x)
                                  + ' and reference_set=' + str(reference_set) + '. x contains unsupported '
                                  'elements ' + str(missing))
    return is_subset


def is_superset(reference_set: Set):
    """
    'Is superset' validator generator.
    Returns a validator to check that x is a superset of reference_set

    :param reference_set: the reference set
    :return:
    """
    def is_superset(x):
        missing = reference_set - x
        if len(missing) == 0:
            return True
        else:
            raise ValidationError('is_superset: len(reference_set - x) == 0 does not hold for x=' + str(x)
                                  + ' and reference_set=' + str(reference_set) + '. x does not contain required '
                                  'elements ' + str(missing))
    return is_superset
