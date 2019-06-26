import datetime
import io
import sys
import typing

DEFAULT_STREAM = sys.stdout


def bprint(
        *values: typing.Any,
        stream: typing.Union[typing.TextIO, typing.Type[str]] = None,
        indent: typing.Union[str, typing.Tuple[str]] = '  ',
        start_indent_level: int = 0,
        maximum_depth: int = None,
        sort=True,
        max_str_len=256,
        max_bytes_len=64,
        truncate_suffix='…',
        human_bytes=True,
        skip_private=True,
        skip_builtin=True,
        skip_callable=True,
        skip_none=True,
        seq_bullet='- ',
        sep='\n\n'
):
    """
    Beautifully prints the given ``values``.

    Arguments
        values
            The object or objects to beautifully print.

        stream
            The output stream where the method should print to.

            If it's ``str``, it will be written to memory,
            and the printed results will be returned as a string.

        indent
            The string used for each indent level.

            If a tuple of two strings is passed, the first string
            will be used for the first indent, and the second string
            for the rest.

            If a tuple of three strings is passed, the first string
            will be used for the first indent, the third for the last,
            and the second for the rest.

        start_indent_level
            The starting indent level.

        maximum_depth
            The maximum depth to print. By default, all nesting
            levels will be printed.

        sort
            Whether key names should be sorted before printing.

        max_str_len
            The maximum length allowed for strings.

        max_bytes_len
            The maximum length allowed for bytes.

        truncate_suffix
            The suffix to use when truncating strings, bytes or iterables.

        human_bytes
            Whether bytes should be shown as readable strings if it contains
            only printable characters.

        skip_private
            Whether private members should be skipped or not.

        skip_builtin
            Whether builtin members should be skipped or not.

        skip_callable
            Whether callable members should be skipped or not.

        skip_none
            Whether ``None`` fields should be skipped or not.

        seq_bullet
            The bullet string to use for sequences like lists.

        sep
            The separator to use when there is more than one value.
    """
    if maximum_depth is None:
        maximum_depth = float('inf')
    elif maximum_depth <= 0:
        return
    else:
        maximum_depth -= 1

    if stream == str:
        out = io.StringIO()
    else:
        out = stream or DEFAULT_STREAM

    def should_skip(name, attr):
        if name.startswith('__'):
            return skip_builtin
        elif name.startswith('_'):
            return skip_private
        elif attr is None:
            return skip_none
        else:
            return skip_callable and callable(attr)

    def handle_kvp(level, kvp):
        if sort:
            kvp = sorted(kvp)

        ind = get_indent(level)
        for key, value in kvp:
            if not should_skip(key, value):
                out.write('\n')
                out.write(ind)
                out.write(key)
                out.write(':')
                fmt(value, level, ' ')

    if isinstance(indent, str):
        def get_indent(level):
            return indent * level
    else:
        def get_indent(level):
            if level == 0:
                return ''
            elif level == 1:
                return indent[0]
            else:
                return indent[0] + (indent[1] * (level - 2)) + indent[-1]

    def fmt(obj, level, space=''):
        """
        Pretty formats the given object as a YAML string which is returned.
        (based on TLObject.pretty_format)
        """
        if isinstance(obj, int):
            out.write(space)
            out.write(str(obj))

        elif isinstance(obj, float):
            out.write(space)
            out.write('{:.2f}'.format(obj))

        elif isinstance(obj, datetime.datetime):
            out.write(space)
            out.write(obj.strftime('%Y-%m-%d %H:%M:%S'))

        elif isinstance(obj, str):
            out.write(space)
            value = repr(obj[:max_str_len])[:-1]
            out.write(value)
            if len(obj) > max_str_len:
                out.write(truncate_suffix)

            out.write(value[0])

        elif isinstance(obj, bytes):
            out.write(space)
            if human_bytes and all(0x20 <= c < 0x7f for c in obj):
                value = repr(obj[:max_bytes_len])[:-1]
                out.write(value)
                if len(obj) > max_bytes_len:
                    out.write(truncate_suffix)

                out.write(value[1])
            else:
                out.write('<…>' if len(obj) > max_bytes_len else
                          ' '.join(f'{b:02X}' for b in obj))

        elif isinstance(obj, dict):
            out.write(space)
            out.write('dict')
            if level < maximum_depth:
                handle_kvp(level + 1, obj.items())

        elif hasattr(obj, '__iter__'):
            # Special case who wants no space before
            if level < maximum_depth:
                level += 1
                for attr in obj:
                    out.write('\n')
                    out.write(get_indent(level))
                    out.write(seq_bullet)
                    fmt(attr, level)

                level -= 1
            else:
                out.write(space)
                out.write('[…]')

        else:
            out.write(space)
            out.write(obj.__class__.__name__)
            if level < maximum_depth:
                out.write(':')
                handle_kvp(level + 1, ((name, getattr(obj, name)) for name in dir(obj)))

    for val in values:
        fmt(val, level=start_indent_level)
        out.write(sep)

    if stream == str:
        return out.value()
