import logging
import os

from pyjade import Compiler as _Compiler, Parser, register_filter
from pyjade.runtime import attrs
from pyjade.exceptions import CurrentlyNotSupported
from pyjade.utils import process, odict

from django.conf import settings
import six
import contextlib
import re


class Defs(object):
    RE_INTERPOLATE_ARG = re.compile(r'(\\)?(\$){(.*?)}')

    def __init__(self, visit_block, var_processor, buffer):
        self.__args = []
        self.defs = {}
        self.__visit_block = visit_block
        self.__var_processor = var_processor
        self.__buffer = buffer

    @property
    def visiting(self):
        return len(self.__args) > 0

    def _make_def(self, mixin):

        def split_parameter(value):
            result = value.split('=', 1)
            if len(result) == 1:
                return result[0], None
            assert len(result) == 2
            return tuple(result)

        def split_argument(value):
            # Ignores the equal sign IF the value is quoted.
            unquoted_value = unquote_value(value)
            if value.strip() != unquoted_value:
                return None, unquoted_value

            result = value.split('=', 1)
            if len(result) == 1:
                return None, result[0]
            assert len(result) == 2
            return tuple(result)

        def split_args(args):
            import re
            PATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')
            return PATTERN.split(args)[1::2]

        def unquote_value(arg):
            arg = arg.strip()
            if len(arg) > 1 and arg[0] == arg[-1] and arg[0] in ['\'', '\"']:
                return arg[1:-1]
            return arg

        parameters = odict(
            split_parameter(arg.strip())
            for arg in mixin.args.split(',')
        )

        def _def(self, raw_args):
            # Obtain args and kwargs from the raw_args.
            args = []
            kwargs = {}
            for i_raw_name, i_raw_value in map(split_argument, split_args(raw_args)):
                if i_raw_name is None:
                    args.append(i_raw_value)
                else:
                    kwargs[i_raw_name.strip()] = i_raw_value

            arguments = []
            for i, (i_parameter_name, i_default_value) in enumerate(parameters.iteritems()):
                try:
                    arg = kwargs[i_parameter_name]
                except KeyError:
                    try:
                        arg = args.pop(0)
                    except IndexError:
                        if i_default_value is not None:
                            arg = i_default_value
                        else:
                            arg = ''
                arguments.append(six.text_type(unquote_value(arg)))
            self.__args.append(dict(zip(parameters.keys(), arguments)))
            try:
                self.__visit_block(mixin.block)
            finally:
                self.__args.pop()

        return _def

    def visit_mixin(self, mixin):
        if mixin.block:
            self.defs[mixin.name] = self._make_def(mixin)
        else:
            self.defs[mixin.name](self, mixin.args)

    def interpolate_arg(self, arg):
        args = self.__args[-1]

        result = self.RE_INTERPOLATE_ARG.sub(
            lambda matchobj:args.get(matchobj.group(3)),
            arg
        )
        return result


class Compiler(_Compiler):
    autocloseCode = 'if,ifchanged,ifequal,ifnotequal,for,block,filter,autoescape,with,trans,blocktrans,spaceless,comment,cache,localize,compress,verbatim'.split(',')
    useRuntime = True

    def __init__(self, node, **options):
        if settings.configured:
            options.update(getattr(settings,'PYJADE',{}))
        super(Compiler, self).__init__(node, **options)
        self.defs = Defs(self.visitBlock, self.var_processor, self.buffer)

    def visitInclude(self, node):

        def find_filename(filename, directories, extensions):
            filenames = []
            for i_extension in extensions:
                for j_directory in directories:
                    filenames.append(
                        os.path.join(j_directory, filename) + i_extension
                    )

            valid_filenames = [i for i in filter(os.path.exists, filenames)]

            if len(valid_filenames) == 0:
                raise Exception(
                    "Include path doesn't exists: {}".format(filenames)
                )

            return valid_filenames[0]

        include_dirs = []
        if self.filename is not None:
            include_dirs += [os.path.dirname(self.filename)]
        include_dirs += self.include_dirs if self.include_dirs else []
        if self.filename is None:
            include_dirs += [os.getcwd()]

        import_filename = node.path.strip('\"\'')
        import_filename = find_filename(
            import_filename,
            directories=include_dirs,
            extensions=('', '.jade')
        )
        src = open(import_filename, 'r').read()

        parser = Parser(src)
        block = parser.parse()
        self.visit(block)

    def visitCodeBlock(self,block):
        self.buffer('{%% block %s %%}'%block.name)
        if block.mode=='append': self.buffer('{{block.super}}')
        self.visitBlock(block)
        if block.mode=='prepend': self.buffer('{{block.super}}')
        self.buffer('{% endblock %}')

    def visitAssignment(self,assignment):
        self.buffer('{%% __pyjade_set %s = %s %%}'%(assignment.name,assignment.val))

    def visitMixin(self,mixin):
        if mixin.name.startswith('__'):
            return self.defs.visit_mixin(mixin)

        self.mixing += 1
        if not mixin.call:
            self.buffer('{%% __pyjade_kwacro %s %s %%}'%(mixin.name,mixin.args))
            self.visitBlock(mixin.block)
            self.buffer('{% end__pyjade_kwacro %}')
        elif mixin.block:
            raise CurrentlyNotSupported("The mixin blocks are not supported yet.")
        else:
            self.buffer('{%% __pyjade_usekwacro %s %s %%}'%(mixin.name,mixin.args))
        self.mixing -= 1

    def visitCode(self,code):
        if code.buffer:
            val = code.val.lstrip()
            val = self.var_processor(val)
            self.buf.append('{{%s%s}}'%(val,'|force_escape' if code.escape else ''))
        else:
            self.buf.append('{%% %s %%}'%code.val)

        if code.block:
            self.visit(code.block)

        codeTag = code.val.strip().split(' ',1)[0]
        if codeTag in self.autocloseCode:
            self.buf.append('{%% end%s %%}'%codeTag)

    def attributes(self,attrs):
        return "{%% __pyjade_attrs %s %%}"%attrs


    def visitConditional(self,conditional):
        #print('****** visitConditional')
        if self.defs.visiting:
            old_sentence = conditional.sentence
            conditional.sentence = self.defs.interpolate_arg(old_sentence)
        try:
            return super(Compiler, self).visitConditional(conditional)
        finally:
            if self.defs.visiting:
                conditional.sentence = old_sentence

    def visitAttributes(self,attrs):
        '''
        Override visitAttributes in order to interpolate DEFs arguments in tag
        arguments values.
        For now, DEFs do not support replacing tag-name or attribute name.
        '''
        #print('****** visitAttributes')
        if self.defs.visiting:
            for i_attr in attrs:
                i_attr['val'] = self.defs.interpolate_arg(i_attr['val'])
        return super(Compiler, self).visitAttributes(attrs)

    def interpolate(self, text, escape=True):
        '''
        Override to try to interpolate values found in any text.
        Only interpolate in we're inside a DEF.
        '''
        #print('****** interpolate')
        if self.defs.visiting:
            text = self.defs.interpolate_arg(text)
        return super(Compiler, self).interpolate(text, escape=escape)


try:
    try:
        from django.template.base import add_to_builtins
    except ImportError: # Django < 1.8
        from django.template import add_to_builtins
    add_to_builtins('pyjade.ext.django.templatetags')
except ImportError:
    # Django 1.9 removed add_to_builtins and instead
    # provides a setting to specify builtins:
    # TEMPLATES['OPTIONS']['builtins'] = ['pyjade.ext.django.templatetags']
    pass

from django.utils import translation

try:
    from django.utils.encoding import force_text as to_text
except ImportError:
    from django.utils.encoding import force_unicode as to_text

def decorate_templatize(func):
    def templatize(src, origin=None):
        src = to_text(src, settings.FILE_CHARSET)
        if origin.endswith(".jade"):
            html = process(src,compiler=Compiler)
        else:
            html = src
        return func(html, origin)

    return templatize

translation.templatize = decorate_templatize(translation.templatize)

try:
    from django.contrib.markup.templatetags.markup import markdown

    @register_filter('markdown')
    def markdown_filter(x,y):
        return markdown(x)

except ImportError:
    pass
