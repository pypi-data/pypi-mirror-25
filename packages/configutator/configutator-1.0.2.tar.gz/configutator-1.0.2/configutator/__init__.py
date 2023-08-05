"""
To use:
-------

#. Create a main function with all the parameters you need, annotated with any defaults.
#. Use the ``@ConfigMap`` and ``@ArgMap`` decorators to modify the default mappings if needed.
#. In the ``if __name__ == "__main__":`` block at the bottom of the file call the loadConfig() function.

Here is an example of the most basic use::

  from configutator import loadConfig
  from sys import argv
  
  def foo(param1, param2, param3=None):
    pass
  
  if __name__ == "__main__":
    for argmap in loadConfig(argv, (foo,)):
      foo(**argmap[foo])

One thing you need to keep in mind when working with configutator is that the config, command line arguments, and 
function parameters are all independant. The parameters given to @ConfigMap and @ArgMap are what connects them all. 
You should never have to change a function signature to modify the command line functionality.

"""
import re, os
from getopt import gnu_getopt
from inspect import signature, getdoc, getfile, Parameter

from .util import normaliseArgs, getParamDoc, getTrueAnnotationType, strtobool, argDocRegEx
from .valitator import validate

import ruamel.yaml
from ruamel.yaml.comments import CommentedMap
import jmespath

# Default YAML loader to use
YAMLLoader = ruamel.yaml.SafeLoader

# Regex to extract description from function doc strings.
funcDocRegex = re.compile(r'^[^:]+?(?=[\s]*:[\w]+)')

# TODO: Handle string annotations for function parameters

def generate(functions: list) -> dict:
    """
    Attempt to create a configuration YAML node for a list of functions.

    :param functions: List of functions to create a config for.
    :return: dictionary of required config parameters
    """
    config = {}
    # TODO: Try to construct a node layout that the parameter JMESPaths can properly resolve.
    for func in functions:
        sig = signature(func)
        params = CommentedMap()
        params.update({name:None if param.default == Parameter.empty else param.default for name, param in sig.parameters})
        for match in argDocRegEx.finditer(getdoc(func)):
            params.yaml_add_eol_comment(match.group(2), match.group(1))
        config[func.__name__] = params
    return config

class TransformBase:
    """
    Used to transform argument values to the intended type
    """
    __slots__ = '_xform'

    def __init__(self, xform=None):
        """
        Constructor.

        :param xform: A single parameter function that accepts the passed argument string or a three element tuple.
            The tuple must be of the form (function, tuple with arguments or None, tuple with arguments or None).
            The value is passed to the function wrapped between the values specified in the second and third tuples.
            ie. xform=(open, None, ('w+',))
        """
        if isinstance(xform, tuple) and len(xform) < 3:
            raise ValueError("xform tuple must be of size 3")
        self._xform = xform
        super().__init__()

    def __call__(self, value):
        if self._xform:
            args = (value,)
            if isinstance(self._xform, tuple):
                if self._xform[1]:
                    args = self._xform[1] + args
                if self._xform[2]:
                    args = args + self._xform[2]
                return self._xform[0](*args)
            return self._xform(*args)
        else:
            return value

class TransformArg(TransformBase):
    __slots__ = '_name'
    def __init__(self, name: str or None = None, xform=None):
        """
        Constructor.

        :param name: The parameter name to map to.
        :param xform: See :meth:`TransformBase`.
        """
        self._name = name
        super().__init__(xform)

    def _apply(self, func, param: Parameter):
        if not self._name:
            self._name = param.name

# -- Environment variable mapping --

def EnvMap(*args, **kwargs):
    """
    Function decorator that specifies parameter mappings to environment variables.
    The values of the arguments should either be a string with the environment variable name,
    None to have configutator ignore the parameter when mapping, or a :class:`TransformArg` instance.
    There is no default mapping for environment variables, any mapping must be explicitly set.
    Gives the decorated function object an __envMap__ attribute.

    :param args: Positional arguments that coincide with the arguments of the function to decorate.
    :param kwargs: Keyword arguments that coincide with the arguments of the function to decorate. This will override anything conflicting with args.
    :return: A function that will add the specified mappings to the function passed to its single argument.
    """
    def wrap(func):
        sig = signature(func)
        nArgs = normaliseArgs(func, args, kwargs)
        if not hasattr(func, '__envMap__'):
            func.__envMap__ = {}
        for name, param in sig.parameters.items():
            if name in nArgs:
                func.__envMap__[name] = nArgs[name] or None

        return func
    return wrap

def mapEnv(environ: dict, functions: list) -> dict:
    """
    Maps environment variables to the parameters of the passed functions.

    :param environ: A dict of environment variables. Generally just pass :data:`os.environ` .
    :param functions: A list of functions to map the command line argument values to.
    :return: A dict keyed on the functions parameter names with the values found in environ.
    """
    args = {}
    for f in functions:
        sig = signature(f)
        args[f] = {}
        for name, param in sig.parameters.items():
            if hasattr(f, '__envMap__') and name in f.__envMap__:
                if isinstance(f.__envMap__[name], TransformArg):
                    args[f] = f.__envMap__[name](environ[f.__envMap__[name]._name])
                else:
                    args[f] = environ[f.__envMap__[name]]
    return args

# -- Config file mapping --

class TransformCfg(TransformBase):
    """
    Extends :class:`TransformArg` to handle JMESPath expressions for config mapping.
    """
    __slots__ = '_expression'
    def __init__(self, path: str, xform=None):
        """
        Constructor.

        :param path: A valid JMESPath that returns the intended config value.
        :param xform: See :meth:`TransformBase`.
        """
        super().__init__(xform)
        self._expression = jmespath.compile(path) if path else None

def ConfigMap(*args, **kwargs):
    """
    Function decorator that specifies parameter mappings to a YAML structure.
    The values of the arguments should either be a string with a JMESPath expression mapping to the intended config node,
    None to have configutator ignore the parameter when mapping, or a :class:`TransformCfg` instance.
    Gives the decorated function object a __cfgMap__ attribute.

    :param args: Positional arguments that coincide with the parameters of the function to decorate.
    :param kwargs: Keyword arguments that coincide with the parameters of the function to decorate. 
        This will override anything conflicting with args.
    :return: A function that will add the specified mappings to the object passed to its single argument.
    """
    def wrap(func):
        sig = signature(func)
        nArgs = normaliseArgs(func, args, kwargs)
        if not hasattr(func, '__cfgMap__'):
            func.__cfgMap__ = {}
        if '_func' in nArgs:
            func.__cfgMap__['_func'] = jmespath.compile(nArgs['_func'])
        for name in sig.parameters:
            if name in nArgs:
                expression = nArgs.get(name)
                if isinstance(expression, TransformCfg):
                    func.__cfgMap__[name] = expression
                else:
                    func.__cfgMap__[name] = jmespath.compile(expression) if expression else None
            #elif name not in func.__cfgMap__:
            #    func.__cfgMap__[name] = jmespath.compile(name)

        return func
    return wrap

def mapConfig(func, yaml_node, path = None) -> dict:
    """
    Maps YAML configuration nodes to the specified functions parameters.

    :param func: The function to map its parameters. Should have been decorated by @ConfigMap, if not will default to 
        function variable names as the JMESPath expression.
    :param YAML_node: The root YAML node to search.
    :param path: If specified, will override the functions '_func' property specified by @ConfigMap.
    :return: A dict keyed on the func's parameter names with the values found in the passed YAML node.
    """
    if path:
        yaml_node = yaml_node.get(path, yaml_node)
    elif hasattr(func, '__cfgMap__') and '_func' in func.__cfgMap__:
        yaml_node = func.__cfgMap__['_func'].search(yaml_node)
    args = {}
    sig = signature(func)
    for name, param in sig.parameters.items(): #type: str, Parameter
        val = param.empty
        if hasattr(func, '__cfgMap__') and name in func.__cfgMap__:
            if isinstance(func.__cfgMap__[name], TransformCfg):
                expression = func.__cfgMap__[name].expression
            else:
                expression = func.__cfgMap__[name]
            if expression:
                val = expression.search(yaml_node)
            if val is None:
                val = param.default
            elif isinstance(func.__cfgMap__[name], TransformArg):
                val = func.__cfgMap__[name](val)
        else:
            val = yaml_node.get(name, param.default)
        if val != param.empty:
            args[name] = val
    return args

def configUnmapped(func, param: str):
    """
    Helper to determine if a parameter mapping was set to None.

    :param func: The function to check.
    :param param: The parameter name to check.
    :return: True if the parameter mapping was set to none.
    """
    return hasattr(func, '__cfgMap__') and param in func.__cfgMap__ and func.__cfgMap__[param] is None

# -- Command line argument mapping --

class PositionalArg(TransformArg):
    """
    Extends :class:`TransformArg` to allow mapping to positional command line arguments.
    """
    __slots__ = '_index', '_desc', '_default'
    def __init__(self, index: int, name: str = None, desc: str = None, xform = None):
        """
        Constructor.

        :param index: The 0-indexed position of the command line parameter.
        :param name: The name of the command line parameter to display in the help.
        :param desc: The description of the parameter to display in the help.
        :param xform: See :meth:`TransformBase.__init__`
        """
        self._index = index
        self._desc = desc # TODO use function doc if None
        self._default = None
        super().__init__(name, xform)

    def _apply(self, func, param):
        super()._apply(param)
        if param.default is not param.empty:
            self._default = param.default
        if not self._desc:
            self._desc = getParamDoc(func).get(param.name, '')

    @property
    def optional(self):
        """
        Determines if a default value was specified in the function definition.
        Depends on @ArgMap to call :meth:`_apply` .

        :return: True if a default value was set, false otherwise.
        """
        return self._default is not Parameter.empty

def ArgMap(*args, **kwargs):
    """
    Function decorator that specifies parameter mappings to command line parameters.
    The values of the arguments should either be a string with the command line parameter name,
    None to have configutator ignore the parameter when mapping, or a :class:`TransformArg` instance.
    Pass "_func='prefix'" as an argument to specify the prefix to use for the command line arguments.
    Gives the decorated function object an __argMap__ attribute.

    :param args: Positional arguments that coincide with the arguments of the function to decorate.
    :param kwargs: Keyword arguments that coincide with the arguments of the function to decorate. This will override anything conflicting with args.
    :return: A function that will add the specified mappings to the function passed to its single argument.
    """
    def wrap(func):
        sig = signature(func)
        nArgs = normaliseArgs(func, args, kwargs)
        if not hasattr(func, '__argMap__'):
            func.__argMap__ = {}
        if '_func' in nArgs:
            func.__argMap__['_func'] = nArgs['_func']
        for name, param in sig.parameters.items():
            if name in nArgs:
                if isinstance(nArgs[name], TransformArg):
                    nArgs[name]._apply(func, param)
                func.__argMap__[name] = nArgs[name] or None

        return func
    return wrap

def mapArgs(optList: list, positionals: list, functions: list) -> dict:
    """
    Maps the values in optList and positionals to the parameters of the passed functions.

    :param optList: A list of arguments produced by :func:`getopt.gnu_getopt` .
    :param positionals: A list of positional arguments produced by :func:`getopt.gnu_getopt` .
    :param functions: A list of functions to map the command line argument values to.
    :return: A dict keyed on the functions parameter names with the values found in optList and positionals.
    """
    args = {}
    pos = []  # Accumulate all positionals from all functions for later processing
    for f in functions:
        sig = signature(f)
        args[f] = {}
        for name, param in sig.parameters.items():
            positional = resolvePositional(f, name)
            if positional:
                pos.append((f, name, positional))
            else:
                argName = resolveArgName(f, name)
                if not argName: continue
                for opt, val in optList:
                    if opt == '--' + argName:
                        if hasattr(f, '__argMap__') and name in f.__argMap__ and isinstance(f.__argMap__[name], TransformArg):
                            val = f.__argMap__[name](val)
                        elif issubclass(getTrueAnnotationType(sig.parameters[name].annotation), bool):
                            val = strtobool(val or 'True')
                        elif sig.parameters[name].annotation is not Parameter.empty:
                            val = getTrueAnnotationType(sig.parameters[name].annotation)(val)
                        args[f][name] = val
    requiredCount = len({positional.index: True for f, name, positional in pos if not positional.optional})
    remaining = len(positionals) - requiredCount
    if remaining < 0:
        raise ValueError("Expected {} positional arguments, {} found.".format(requiredCount, len(positionals)))
    for i in range(len(positionals)):
        for f, name, positional in pos:
            if positional.index == i:
                if positional.optional and remaining:
                    remaining -= 1
                else:
                    continue
                args[f][name] = positional(positionals[i])
    return args

def resolvePositional(func, name) -> PositionalArg or None:
    """
    Determine if a function parameter has a specified positional mapping.

    :param func: The function to check.
    :param name: The parameter name to check.
    :return: The PositionalArg instance or None
    """
    if hasattr(func, '__argMap__') and name in func.__argMap__ and isinstance(func.__argMap__[name], PositionalArg):
        return func.__argMap__[name]
    else:
        return None

def resolveArgPrefix(function) -> str:
    """
    Resolve the command line prefix for a function.

    :param function: The function to resolve.
    :return: The value of the '_func' property set by @ArgMap or the function name if not set.
    """
    # Handle _func in argMap
    prefix = function.__name__ + ':'
    if hasattr(function, '__argMap__') and '_func' in function.__argMap__ and function.__argMap__['_func'] is not None:
        prefix = function.__argMap__['_func']
        if prefix != '':
            prefix += ':'
    return prefix

def resolveArgName(func, name) -> str:
    """
    Resolve the command line argument name for the specified function parameter.

    :param func: The function to resolve.
    :param name: The parameter name to resolve.
    :return: A string containing the fully resolved command line argument name.
    """
    # Prefix parameter with name if argMap unspecified
    if hasattr(func, '__argMap__'):
        if name in func.__argMap__:
            if func.__argMap__[name]:
                if isinstance(func.__argMap__[name], PositionalArg):
                    return func.__argMap__[name].name
                return func.__argMap__[name]
            else:
                return None
        #elif '_func' in func.__argMap__:
        #    if func.__argMap__['_func'] is not None:
        #        return func.__argMap__['_func'] + ':' + name
        #    else:
        #        return name
        else:
            return resolveArgPrefix(func) + name
    else:
        return func.__name__ + ':' + name

def argUnmapped(func, param: str) -> bool:
    """
    Helper to determine if a parameter mapping was set to None.

    :param func: The function to check.
    :param param: The parameter name to check.
    :return: True if the parameter mapping was set to none.
    """
    return hasattr(func, '__argMap__') and param in func.__argMap__ and func.__argMap__[param] is None

# -- Loader --

def loadConfig(argv: list, functions: tuple, title='', configParam='config', configExpression = None, batchExpression=None, tui=True) -> dict:
    """
    Generator returning each argument mapping provided by the command line and configuration script.
    If a YAML config file is passed to the config argument that contains multiple documents this function will yield
    for each document plus any job specified by batchExpression. The config file can also be a named pipe where execution
    will continue for each piped YAML document exiting when EOF is received (the pipe is closed).

    :param argv: A list of command line arguments. Generally just pass the value of :data:`sys.argv` .
    :param functions: A tuple of functions who's parameters are to be included in the mapping.
    :param title: A title to use for the application when displaying the help or TUI.
    :param configParam: The parameter name to use to specify the config file path. Leave this as the default unless you
        specifically need to use 'config' for your own purposes.
    :param configExpression: A JMESPath that is applied to the YAML document to change the current root node.
    :param batchExpression: A JMESPath that is applied to the current root YAML node. This should return a list of
        mappings where each item in the list is a root node to apply the function parameter mappings.
    :param tui: Set to False to disable TUI.
    :return: Yields the mappings resolved from each of the list items in batchExpression.
        If batchExpression is None then this function only yields one mapping resolved from the current root node.
        Any command line argument mappings will override anything specified in the config.
    """
    if not (functions and isinstance(functions, tuple)):
        raise ValueError('Minimum of one function in a tuple is needed for the functions argument.')

    if isinstance(configExpression, str):
        configExpression = jmespath.compile(configExpression)
    if isinstance(batchExpression, str):
        batchExpression = jmespath.compile(batchExpression)

    call_name = argv[0]
    argv = argv[1:]
    options = [configParam + '=', '{}:='.format(configParam), '{}:batch:='.format(configParam)]
    for f in functions:
        # Build command line argument list from function parameters
        sig = signature(f)
        for name, param in sig.parameters.items():
            name = resolveArgName(f, name)
            if not name: continue
            # If boolean, make parameter valueless
            if not ((issubclass(getTrueAnnotationType(param.annotation), bool) or isinstance(param.default, bool)) and param.default == False):
                name += '='
            options.append(name)
    optList, originalPositionals = gnu_getopt(argv, 'h', options)

    # Search for help switch in passed parameters
    for opt, val in optList:
        if opt == '-h':
            from sys import stderr
            import __main__
            headerString = ''
            positionalHelp = {} # type: dict[int, PositionalArg]
            helpString = ''
            try:
                if title:
                    headerString = "{}\tUse: {} [options] ".format(title, getfile(__main__))
            except TypeError:
                pass
            for f in functions:
                # Build command line argument option descriptions from function parameters
                sig = signature(f)
                if len(functions) > 1: helpString += "{}:\n".format(f.__name__)
                funcDocs = funcDocRegex.findall(getdoc(f))
                if len(funcDocs):
                    helpString += funcDocs[0] + '\n'
                doc = getParamDoc(f)
                for name, param in sig.parameters.items(): #type:str, Parameter
                    positional = resolvePositional(f, name)
                    if positional:
                        positionalHelp[positional.index] = positional
                    else:
                        argName = resolveArgName(f, name)
                        if not argName: continue
                        default = ''
                        if param.default != param.empty:
                            default = "[Default: {}]".format(param.default)
                        helpString += "  --{} - {} {}\n".format(argName, doc.get(name, ''), default)

            helpString += "General:\n  --{} - Path to configuration file. All other specified options override config. " \
                          "If no config file specified, all options without default must be specified.\n".format(configParam)
            if headerString:
                positionalNameString = ''
                positionalDocString = ''
                try:
                    for i in range(len(positionalHelp)):
                        positionalNameString += (" [{}]" if positionalHelp[i].optional else " {}").format(positionalHelp[i]._name)
                        positionalDocString += "{} - {}\n".format(positionalHelp[i]._name, positionalHelp[i]._desc)
                    stderr.write(headerString + positionalNameString + '\n' + positionalDocString + helpString)
                except KeyError:
                    raise ValueError("Non-contiguous positional parameter index: {}".format(i))
            else:
                stderr.write(helpString)
            exit()

    # Handle config path overrides
    for f in functions:
        for name, param in signature(f).parameters.items():
            prefix = '--' + resolveArgPrefix(f)
            for opt, val in optList:
                if opt == prefix:
                    ConfigMap(_func=jmespath.compile(val))(f)
                elif opt == prefix + name + ':':
                    ConfigMap(**{name: jmespath.compile(val)})(f)

    config = None
    # Search for configParam in passed parameters
    for opt, val in optList:
        if opt == '--' + configParam:
            if not (os.path.isfile(val) and os.access(val, os.R_OK)):
                raise FileNotFoundError("The config path was not found: {}".format(val))
            for o, v in optList:
                if o == '--{}:'.format(configParam):
                    configExpression = jmespath.compile(v)
                elif o == '--{}:batch:'.format(configParam):
                    batchExpression = jmespath.compile(v)
            config = val

    # Load environment variables and command line arguments
    args = mapEnv(os.environ, functions)
    for f, m in mapArgs(optList, originalPositionals, functions).items():
        if f not in args:
            args[f] = {}
        args[f].update(m)

    if config:
        cfgs = ruamel.yaml.load_all(open(config), YAMLLoader)
        for cfg in cfgs:
            if configExpression:
                tmp = configExpression.search(cfg)
                if tmp != None:
                    cfg = tmp
            if batchExpression:
                jobs = batchExpression.search(cfg)
                if jobs == None:
                    jobs = [cfg]
            else:
                jobs = [cfg]
            for job in jobs:
                argMap = {}
                for f in functions:
                    argMap[f] = mapConfig(f, job)
                for f, m in args.items():
                    if f not in argMap:
                        argMap[f] = {}
                    argMap[f].update(m)
                for f in functions:
                    validate(f, argMap[f])
                #TODO os.fork() to parallelize jobs
                #TODO detect slurm_task_id and use api, maybe pickle argmap
                yield argMap

    elif len(argv):
        # If command line arguments were passed, skip TUI
        yield args

    elif tui:
        # No command line arguments were passed, load TUI
        from .tui import loadTUI
        loadTUI(functions, args, call_name, title)
        if args:
            yield args

    return
