from functools import wraps
from datetime import datetime
from loguru import logger


def name_decor(fun):
    """
        This function wraps a function and logs the full name of called function.

        Parameters
        ----------
        fun : function
            The function to be wrapped.

        Returns
        -------
        function
            The wrapped function.

        """
    @wraps(fun)
    def wrapper(*args, **kwargs):
        logger.info(fun.__qualname__)
        return fun(*args, **kwargs)
    return wrapper


def time_decor(fun):
    """
        This function wraps a function and logs the time it took to execute.

        Parameters
        ----------
        fun : function
            The function to be wrapped.

        Returns
        -------
        function
            The wrapped function.

        """
    @wraps(fun)
    def wrapper(*args, **kwargs):

        t0 = datetime.now()
        res = fun(*args, **kwargs)
        t1 = datetime.now()
        logger.info(f"{fun.__name__} time execution: {t1-t0}.")
        return res
    return wrapper


class NameMetaclass(type):
    """
    Metaclass for classes that can be used as a decorator. This metaclass is used
    to decorate the functions that are going to be called. The decorator prints logs with the name
    of executed function.
    """
    def __new__(cls, clsnames, clsbases, clsdict, *args, **kwargs):
        """
        This method is called when a new class is being created.

        Parameters
        ----------
        cls : type
            The class that is being created.
        clsnames : tuple
            The tuple of class names.
        clsbases : tuple
            The tuple of base classes.
        clsdict : dict
            The dictionary containing the class's namespace.
        *args : tuple
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        type
            The new class.

        """
        new_cls_dict = clsdict
        for key, val in clsdict.items():
            if callable(val):
                new_cls_dict[key] = name_decor(val)
        return super(NameMetaclass, cls).__new__(cls, clsnames, clsbases, new_cls_dict)


class TimeMetaclass(type):
    """
    Metaclass for classes that can be used as a decorator. This metaclass is used
    to decorate the functions that are going to be called.
    The decorator prints time of execution of the called method
    """
    def __new__(cls, clsnames, clsbases, clsdict):
        new_cls_dict = clsdict
        for key, val in clsdict.items():
            if callable(val):
                new_cls_dict[key] = time_decor(val)
        return super(TimeMetaclass, cls).__new__(cls, clsnames, clsbases, new_cls_dict)


class LoguruMetaclass(type):
    """
    Metaclass for classes that can be used as a decorator. This metaclass is used
    to decorate the functions that are going to be called. The decorator prints logs from the loguru module in case
    of an exception, warnings or errors.
    """
    def __new__(cls, clsnames, clsbases, clsdict):
        """
        This method is called when a new class is being created.

        Parameters
        ----------
        cls : type
            The class that is being created.
        clsnames : tuple
            The tuple of class names.
        clsbases : tuple
            The tuple of base classes.
        clsdict : dict
            The dictionary containing the class's namespace.

        Returns
        -------
        type
            The new class.

        """
        new_cls_dict = clsdict
        for key, val in clsdict.items():
            if callable(val):
                new_cls_dict[key] = logger.catch(val)
        return super(LoguruMetaclass, cls).__new__(cls, clsnames, clsbases, new_cls_dict)


class CallBlockerMetaclass(type):
    """
        Metaclass for classes that can have only one instance.

        This metaclass overrides the __call__ method to check if there is only one instance of the class and if so, returns it.
        If there are multiple instances, a warning is logged and the first instance is returned.
    """
    counter = 0

    def __new__(cls, clsnames, clsbases, clsdict):
        return super(CallBlockerMetaclass, cls).__new__(cls, clsnames, clsbases, clsdict)

    def __call__(cls, *args, **kwargs):
        """
        Call the object instance.

        This method is called when an instance of the class is called as a function.
        It checks if there is only one instance of the class and if so, returns it.
        If there are multiple instances, a warning is logged and the first instance is returned.

        Parameters
        ----------
        args : tuple
            Positional arguments passed to the instance when called as a function.
        kwargs : dict
            Keyword arguments passed to the instance when called as a function.

        Returns
        -------
        object
            The instance of the class.

        """

        cls.counter += 1
        if cls.counter < 2:
            return super(CallBlockerMetaclass, cls).__call__(*args, **kwargs)
        else:
            logger.warning("Objects from a class possessing CallBlockerMetaclass can have only one instance called!")


if __name__ == "__main__":
    pass
