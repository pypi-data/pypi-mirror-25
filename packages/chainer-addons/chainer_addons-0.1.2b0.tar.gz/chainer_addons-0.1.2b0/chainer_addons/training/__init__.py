from enum import Enum
import chainer

class OptimizerType(Enum):
	SGD = 1
	RMSPROP = 2
	Default = SGD

	@classmethod
	def as_choices(cls):
		return {e.name.lower(): e for e in cls}

	@classmethod
	def get(cls, key):
		key = key.lower()
		choices = cls.as_choices()
		return choices.get(key) if key in choices else cls.Default

def optimizer(opt_type_name, model, lr=1e-4, decay=9e-1, *args, **kw):
	opt_cls = {
		OptimizerType.SGD: chainer.optimizers.MomentumSGD,
		OptimizerType.RMSPROP: chainer.optimizers.RMSprop,
	}.get(OptimizerType.get(opt_type_name))

	opt = opt_cls(lr=lr, *args, **kw)
	opt.setup(model)
	if decay:
		opt.add_hook(chainer.optimizer.WeightDecay(decay))

	return opt
