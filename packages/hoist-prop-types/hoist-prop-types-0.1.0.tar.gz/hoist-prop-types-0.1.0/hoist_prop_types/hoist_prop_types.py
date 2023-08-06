'''
Rewrites React components to hoist the proptypes to
the top of the file
'''
import argparse
import sys
import codemod

__version__ = '0.1.0'


PROP_TYPES_LINE_REG = 'propTypes'
DEFAULT_PROP_TYPES_LINE = 'defaultProps'


def suggestor_insert_prop_types(replace_type, replace_const):
    def build_prop_type_insert_const_patch(lines):
        first_non_import_line_number, prop_type_start, prop_type_end = get_line_numbers(lines, replace_type)
        if prop_type_end is None or prop_type_start is None:
            return []

        current_line_number = prop_type_start
        assign_start = lines[current_line_number].find('=')
        new_lines = [lines[first_non_import_line_number - 1]]
        new_lines.append(
            'const %s %s ' % (
                replace_const,
                lines[current_line_number][assign_start:]
            )
        )

        print('WHATE', new_lines)
        while current_line_number < prop_type_end:
            current_line_number = current_line_number + 1
            new_lines.append(lines[current_line_number])
        new_lines.append('\n')

        new = ''.join([str(x) for x in new_lines])
        return [codemod.Patch(first_non_import_line_number - 1, None, new)]

    return build_prop_type_insert_const_patch


def get_line_numbers(lines, replace_type):
    first_non_import_line_number = None
    prop_type_start = None
    prop_type_end = None
    import_open_params = 0

    prop_type_open_params = 0

    for line_number, line in enumerate(lines):
        has_import = 'import' in line
        blank_line = line.strip() == ''

        if not first_non_import_line_number:
            if has_import:
                import_open_params = line.count('{') - line.count('}')

            elif import_open_params > 0:
                open_close_diff = line.count('{') - line.count('}')
                import_open_params = import_open_params + open_close_diff

            elif not has_import and import_open_params == 0 and not blank_line:
                first_non_import_line_number = line_number

        # If we haven't found the proptype declaration yet, 
        # lets keep looking
        if not prop_type_start and replace_type in line:
            prop_type_start = line_number
            prop_type_open_params = line.count('{') - line.count('}');

        # We've found the prop type start, lets find the end.
        elif prop_type_open_params != 0:
            open_close_diff = line.count('{') - line.count('}')
            prop_type_open_params = prop_type_open_params + open_close_diff

            if prop_type_open_params == 0:
                prop_type_end = line_number
    return first_non_import_line_number, prop_type_start, prop_type_end


def suggestor_replace_props_with_const(replace_type, replace_const):
    def build_prop_types_patch_replace_with_const(lines):
        '''
        Build the Patch that replaces the current propType assignement with
        the new const variable PROPS

        @param lines    The line where the prop definition started
        '''
        first_non_import_line_number, prop_type_start, prop_type_end = get_line_numbers(lines, replace_type)
        if prop_type_end is None or prop_type_start is None:
            return []

        assign_start = lines[prop_type_start].find('=')
        semicolon = ''
        if lines[prop_type_end].strip()[-1:] == ';':
            semicolon = ';'

        new_lines = '%s %s%s\n' % (
            lines[prop_type_start][:assign_start + 1],
            replace_const,
            semicolon
        )

        return [codemod.Patch(prop_type_start, prop_type_end + 1, new_lines)]
    return build_prop_types_patch_replace_with_const


def main():
    parser = argparse.ArgumentParser(
        description='Hoist prop type shapes to the top ' +
                    'of a file, below the last import'
    )
    parser.add_argument(
        'directory',
        metavar='DIR',
        default='.',
        help='The directory that you want to hoist the prop types for.'
    )
    args = parser.parse_args()
    directory = args.directory

    print('Executing hoist-prop-types %s.' % __version__)
    print('directory: %s' % directory)

    extension_filter = codemod.path_filter(['js', 'jsx'])

    codemod.Query(
        suggestor_insert_prop_types(DEFAULT_PROP_TYPES_LINE, 'DEFAULT_PROPS'),
        None,
        None,
        directory,
        extension_filter
    ).run_interactive()
    codemod.Query(
        suggestor_replace_props_with_const(
            DEFAULT_PROP_TYPES_LINE,
            'DEFAULT_PROPS'
        ),
        None,
        None,
        directory,
        extension_filter
    ).run_interactive()

    codemod.Query(
        suggestor_insert_prop_types(PROP_TYPES_LINE_REG, 'PROPS'),
        None,
        None,
        directory,
        extension_filter
    ).run_interactive()
    codemod.Query(
        suggestor_replace_props_with_const(PROP_TYPES_LINE_REG, 'PROPS'),
        None,
        None,
        directory,
        extension_filter
    ).run_interactive()
