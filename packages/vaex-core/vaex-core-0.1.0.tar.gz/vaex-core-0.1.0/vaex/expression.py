import operator
import six
from future.utils import with_metaclass
from vaex.dataset import function_mapping

_binary_ops = [
    dict(code="+", name='add',  op=operator.add),
    dict(code="in", name='contains',  op=operator.contains),
    dict(code="/", name='truediv',  op=operator.truediv),
    dict(code="//", name='floordiv',  op=operator.floordiv),
    dict(code="&", name='and',  op=operator.and_),
    dict(code="^", name='xor',  op=operator.xor),

    dict(code="|", name='or',  op=operator.or_),
    dict(code="**", name='pow',  op=operator.pow),
    dict(code="is", name='is',  op=operator.is_),
    dict(code="is not", name='is_not',  op=operator.is_not),

    dict(code="<<", name='lshift',  op=operator.lshift),
    dict(code="%", name='mod',  op=operator.mod),
    dict(code="*", name='mul',  op=operator.mul),

    dict(code=">>", name='rshift',  op=operator.rshift),
    dict(code="-", name='sub',  op=operator.sub),

    dict(code="<",  name='lt',   op=operator.lt),
    dict(code="<=", name='le',  op=operator.le),
    dict(code="==", name='eq',  op=operator.eq),
    dict(code="!=", name='ne',  op=operator.ne),
    dict(code=">=", name='ge',  op=operator.ge),
    dict(code=">",  name='gt',  op=operator.gt),
]
#    dict(code="@", name='matmul',  op=operator.matmul),

reversable = 'add sub mul matmul truediv floordiv mod divmod pow lshift rshift and xor or'.split()

_unary_ops = [
    dict(code="~", name='invert',  op=operator.invert),
    dict(code="-", name='neg',  op=operator.neg),
    dict(code="+", name='pos',  op=operator.pos),
]
class Meta(type):
	def __new__(upperattr_metaclass, future_class_name,
				future_class_parents, attrs):
		#attrs = {}
		for op in _binary_ops:
			def wrap(op=op):
				def f(a, b):
					self = a
					#print(op, a, b)
					if isinstance(b, Expression):
						assert b.ds == a.ds
						b = b.expression
					expression = '({0}) {1} ({2})'.format(a.expression, op['code'], b)
					return Expression(self.ds, expression=expression, selection=self.selection)
				attrs['__%s__' % op['name']] = f
				if op['name'] in reversable:
					def f(a, b):
						self = a
						#print(op, a, b)
						if isinstance(b, Expression):
							assert b.ds == a.ds
							b = b.expression
						expression = '({2}) {1} ({0})'.format(a.expression, op['code'], b)
						return Expression(self.ds, expression=expression, selection=self.selection)
					attrs['__r%s__' % op['name']] = f

			wrap(op)
		for op in _unary_ops:
			def wrap(op=op):
				def f(a):
					self = a
					expression = '{0}({1})'.format(op['code'], a.expression)
					return Expression(self.ds, expression=expression, selection=self.selection)
				attrs['__%s__' % op['name']] = f
			wrap(op)
		for name, __ in function_mapping:
			def wrap(name=name):
				def f(*args, **kwargs):
					self = args[0]
					def to_expression(expression):
						if isinstance(expression, Expression):
							assert expression.ds == self.ds
							expression = expression.expression
						return expression
					expressions = [to_expression(e) for e in args]
					#print(name, expressions)
					expression = '{0}({1})'.format(name, ", ".join(expressions))
					return Expression(self.ds, expression=expression, selection=self.selection)
				attrs['%s' % name] = f
			if name not in attrs:
				wrap(name)
		return type(future_class_name, future_class_parents, attrs)

class Expression(with_metaclass(Meta)):
	def __init__(self, ds, expression, selection=False):
		self.ds = ds
		self.expression = expression
		self.selection = selection

	def __repr__(self):
		name = self.__class__.__module__ + "." +self.__class__.__name__
		return "<%s(expressions=%r, selections=%r)> instance at 0x%x" % (name, self.expression, self.selection, id(self))
	def count(self):
		return self.ds.count(self.expression, selection=self.selection)
	def sum(self):
		return self.ds.sum(self.expression, selection=self.selection)

	#def optmized_tensorflow(self):


	def optimized(self):
		import pythran
		import imp
		import hashlib
		#self._import_all(module)
		names =  []
		funcs = set(vaex.dataset.expression_namespace.keys())
		vaex.expresso.validate_expression(self.expression, self.ds.get_column_names(virtual=True, strings=True), funcs, names)
		names = list(set(names))
		types = ", ".join(str(self.ds.dtype(name)) + "[]" for name in names)
		argstring = ", ".join(names)
		code = '''
from numpy import *
#pythran export f({2})
def f({0}):
	return {1}'''.format(argstring, self.expression, types)
		print(code)
		m = hashlib.md5()
		m.update(code.encode('utf-8'))
		module_name = "pythranized_" + m.hexdigest()
		print(m.hexdigest())
		module_path = pythran.compile_pythrancode(module_name, code, extra_compile_args=["-DBOOST_SIMD", "-march=native"])
		module = imp.load_dynamic(module_name, module_path)
		function_name = "f_" +m.hexdigest()
		vaex.dataset.expression_namespace[function_name] = module.f

		return Expression(self.ds, "{0}({1})".format(function_name, argstring), selection=self.selection)

	def 	__lt__(self, other):
		#self._binop()
		if isinstance(other, Expression):
			assert other.ds == self.ds
			other = other.expression
		return Expression(self.ds, "({} < {})".format(self.expression, other))
