import sys

def construct_trees(code):
	trees = []
	while code:
		inner = code[0]
		code  = code[1:]
		while sum(map(inner.count, '([{<')) != sum(map(inner.count, '>}])')):
			inner += code[0]
			code   = code[1:]
		trees.append(('([{<>}])'.find(inner[0]), construct_trees(inner[1:-1])))
	return trees

class BrainFlex:
	def __init__(self, left, right):
		self.data = [left, right]
		self.active = 0
	def interpret(self, code):
		code = ''.join(char for char in code if char in '([{<>}])')
		return self.evaluate(construct_trees(code))
	def evaluate(self, trees):
		value = 0
		for tree in trees:
			if tree[1]:
				value += self.monad(tree[0], tree[1])
			else:
				value += self.nilad(tree[0])
		return value
	def nilad(self, type):
		if type == 0:
			return 1
		elif type == 1:
			return self.data[self.active].size()
		elif type == 2:
			return self.pop()
		elif type == 3:
			self.swap()
			return 0
	def monad(self, type, argument):
		if type == 0:
			value = self.evaluate(argument)
			self.push(value)
			return value
		elif type == 1:
			return -self.evaluate(argument)
		elif type == 2:
			runsum = 0
			while self.peek():
				runsum += self.evaluate(argument)
			return runsum
		elif type == 3:
			self.evaluate(argument)
			return 0
	def pop(self):
		try:
			return self.data[self.active].pop()
		except:
			return 0
	def push(self, value):
		self.data[self.active].push(value)
		return value
	def peek(self):
		try:
			return self.data[self.active].peek()
		except:
			return 0
	def swap(self):
		self.active ^= 1

def output(trees, indent = 0):
	for tree in trees:
		print('    ' * indent + str(tree[0]))
		output(tree[1], indent + 1)

def run(left, right, code, args):
	flex = BrainFlex(left, right)
	for arg in args:
		flex.push(int(arg))
	flex.interpret(code)
	return flex.data[flex.active]

def flex(name, designer, filename, left, right):
	usage = '''
BrainFlex - %s - Turing Tarpit designed by %s, implemented by HyperNeutrino
Usage:

%s e <code> <arg1> <arg2> <args...> - Execute code directly

%s f <code> <arg1> <arg2> <args...> - Execute code from a file
	''' % (name, designer, filename, filename)
	if len(sys.argv) < 3:
		raise SystemExit(usage)
	else:
		if sys.argv[1] == 'e':
			code = sys.argv[2]
		elif args[1] == 'f':
			code = open(sys.argv[2], 'r').read()
		else:
			raise SystemExit(usage)
		run(left, right, code, sys.argv[3:]).output()
