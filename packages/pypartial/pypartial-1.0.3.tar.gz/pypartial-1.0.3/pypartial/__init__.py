import operator

class partializer(object):
  def __init__(self, *args, **kwargs):
    self.args=args
    self.kwargs=kwargs
    self.func=None
  
  def __gt__(self, b):
    self.func = b
    return self
  
  def __lt__(self, b):
    self.args+=b.args
    self.kwargs.update(b.kwargs)
    
    return self
  
  def __call__(self, *args, **kwargs):
    args=list(args)
    
    full_kwargs={}
    full_kwargs.update(kwargs)
    full_kwargs.update(self.kwargs)
    return self.func(*[args.pop(0) if arg==self.__class__ else arg for arg in self.args]+args, **full_kwargs)

  def __repr__(self):
    if self.func:
      return "partial function: " + self.func.__name__ + ", ".join(["(" + ", ".join('_' if arg==self.__class__ else str(arg) for arg in self.args), ", ".join( name+"="+('_' if arg==self.__class__ else str(arg)) for name, arg in self.kwargs.items())]).rstrip(", ") + ")"
    return "unbound partializer"

__builtins__['_']=partializer
