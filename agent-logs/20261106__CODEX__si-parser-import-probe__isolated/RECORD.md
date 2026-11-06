# Parser package import probe

One local pinned-Python introspection command attempted to import `fast_downward.translate.pddl_parser.parsing_functions` to print its source location. Importing the package invoked its command-line argument parser, which printed usage and exited 2 because the required domain and task arguments were absent. No domain or problem path was supplied, and the command did not parse or compile a task, instantiate ALFWorld, load a model, or use GPU. This was an unintended package-import side effect, not a parser compatibility result. No retry of that import probe was performed.

Future diagnostics must inspect the package source and design an explicit, independently reviewed invocation rather than assuming the package import is inert.
