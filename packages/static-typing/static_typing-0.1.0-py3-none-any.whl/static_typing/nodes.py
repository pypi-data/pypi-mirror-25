
#import typing as t

import typed_ast.ast3

class Comment(typed_ast.ast3.Str):

    pass


class Docstring(typed_ast.ast3.Str):

    pass
