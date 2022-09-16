"""
Simple implemenatation of Monads
https://www.philliams.com/monads-in-python/
"""

import traceback

from typing import Dict
from collections.abc import Callable


class MaybeMonad:

	def __init__(self, value: object = None, contains_value: bool = True):
		self.value = value
		self.contains_value = contains_value

	def bind(self, f: Callable) -> 'MaybeMonad':

		if not self.contains_value:
			return MaybeMonad(None, contains_value=False)

		try:
			result = f(self.value)
			return MaybeMonad(result)
		except:
			return MaybeMonad(None, contains_value=False)


class FailureMonad:

	def __init__(self, value: object = None, error_status: Dict = None):
		self.value = value
		self.error_status = error_status

	def bind(self, f: Callable, *args, **kwargs) -> 'FailureMonad':

		if self.error_status:
			return FailureMonad(None, error_status=self.error_status)

		try:
			result = f(self.value, *args, **kwargs)
			return FailureMonad(result)
		except Exception as e:

			failure_status = {
				'trace' : traceback.format_exc(),
				'exc' : e,
				'args' : args,
				'kwargs' : kwargs
			}

			return FailureMonad(None, error_status=failure_status)


class LazyMonad:

	def __init__(self, value: object):

		if isinstance(value, Callable):
			self.compute = value
		else:
			def return_val():
				return value

			self.compute = return_val

	def bind(self, f: Callable, *args, **kwargs) -> 'FailureMonad':

		def f_compute():
			return f(self.compute(), *args, **kwargs)

		return LazyMonad(f_compute)
