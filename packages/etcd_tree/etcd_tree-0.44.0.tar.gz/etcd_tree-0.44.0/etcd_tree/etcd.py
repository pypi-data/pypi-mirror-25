# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals
##
##  This file is part of etcTree, a dynamic and Pythonic view of
##  whatever information you tend to store in etcd.
##
##  etcTree is Copyright © 2015 by Matthias Urlichs <matthias@urlichs.de>,
##  it is licensed under the GPLv3. See the file `README.rst` for details,
##  including optimistic statements by the author.
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License (included; see the file LICENSE)
##  for more details.
##
##  This header is auto-generated and may self-destruct at any time,
##  courtesy of "make update". The original is in ‘scripts/_boilerplate.py’.
##  Thus, do not remove the next line, or insert any blank lines above.
##
import logging
logger = logging.getLogger(__name__)
##BP

"""\
This is the etcd interface.
"""

import aio_etcd as etcd
from aio_etcd.client import Client
import asyncio
import weakref
import inspect
from contextlib import suppress
from itertools import chain

from .node import EtcRoot

__all__ = ("EtcClient","EtcTypes")

# Requiring a lock is bad for our health.

if not hasattr(asyncio.Condition,'notify_unlocked'):
	def notify_unlocked(self):
		for fut in self._waiters:
			if not fut.done():
				fut.set_result(False)
asyncio.Condition.notify_unlocked = notify_unlocked
del notify_unlocked

class _NOTGIVEN: pass

class WatchStopped(RuntimeError):
	"""Raised when calling sync() on a stopped EtcWatcher."""
	pass

class WatchError(RuntimeError):
	"""Used when an external error stops an EtcWatcher."""
	pass

async def retry_conn(p,*a,**k):
	n=0
	while True:
		try:
			res = await p(*a,**k)
		except etcd.EtcdConnectionFailed:
			if n >= 5:
				raise
			n += 1
		else:
			return res

class EtcClient(object):
	last_mod = None
	def __init__(self, root="", loop=None, **args):
		assert (root == '' or root[0] == '/')
		self.root = root
		self.args = args
		self._loop = loop if loop is not None else asyncio.get_event_loop()
		self.client = Client(loop=loop, **args)
		self._trees = set()
#		self.watched = weakref.WeakValueDictionary()

	async def start(self):
		if self.last_mod is not None: # pragma: no cover
			return
		try:
			self.last_mod = (await retry_conn(self.client.read,self.root)).etcd_index
		except etcd.EtcdKeyNotFound:
			self.last_mod = (await retry_conn(self.client.write,self.root, value=None, dir=True)).etcd_index

	def __del__(self):
		self._kill()

	def _kill(self):
		try:
			if self._trees:
				raise RuntimeError("Clients not closed cleanly",self,self._trees)
			del self.client
		except AttributeError: pass

	async def stop(self):
		self.close()

	def close(self):
		try: c = self.client
		except AttributeError: pass # pragma: no cover
		else: c.close()
		self._kill()

	def _extkey(self, key, sub=(), _prefix=False):
		if isinstance(key,str):
			key = str(key)
			if key == '/':
				key = ''
			elif key != '':
				assert key[0] == '/'
				assert key[-1] != '/'
				assert '//' not in key
			if sub:
				key += '/'+'/'.join(sub)
		else:
			if key or sub:
				key = '/'+'/'.join((str(x) for x in chain(key,sub)))
			else:
				key = ''
		if _prefix:
			assert (key+'/').startswith(self.root+'/')
			return key
		else:
			return self.root+key

	async def get(self, key, _prefix=False, **kw):
		key = self._extkey(key, _prefix=_prefix)
		logger.debug("get %s %s",key, repr(kw))
		return (await retry_conn(self.client.get,key, **kw))

	async def read(self, key, _prefix=False, **kw):
		return (await retry_conn(self.client.read,self._extkey(key,_prefix=_prefix), **kw))

	async def delete(self, key, prev=_NOTGIVEN, _prefix=False, index=None, **kw):
		"""\
			Delete a value.

			@recursive: delete a whole tree.

			@index: current mod stamp

			@prev: current value
			"""
		key = self._extkey(key, _prefix=_prefix)
		logger.debug("del %s prev=%s index=%s %s",key, prev,index, repr(kw))
		if prev is not _NOTGIVEN:
			kw['prevValue'] = prev
		if index is not None:
			kw['prevIndex'] = index
		res = await retry_conn(self.client.delete,key,**kw)
		self.last_mod = res.modifiedIndex
		return res

	async def set(self, key, value, prev=None, create=None, _prefix=False, index=None, **kw):
		"""\
			Either create or update a value.

			@key: the object path.

			@value: the value of the node, for non-directories

			@create: new entry? True:yes / False:no / None:doesn't matter

			@ttl: time-to-live in seconds.

			@append=True: generate a new guaranteed-unique and sequential entry.

			@dir=True: generate/update a directory entry

			@prev: the previous value; only when @dir=False and @create!=True

			@index: the previous modification stamp; only when @dir=False and @create!=True

			"""
		key = self._extkey(key, _prefix=_prefix)
		logger.debug("set %s to %s prev=%s index=%s %s",value,key, prev,index, repr(kw))
		if kw.get('append',False):
			assert prev is None, prev
			assert index is None, index
			assert create is not False, create
		elif create is True:
			kw['prevExist'] = False
			assert prev is None
			assert index is None
		else:
			if create is False:
				kw['prevExist'] = True
			if index is not None:
				kw['prevIndex'] = index
			if prev is not None:
				kw['prevValue'] = prev

		res = await retry_conn(self.client.write,key, value=value, **kw)
		self.last_mod = res.modifiedIndex
		return res

	async def tree(self, key, sub=_NOTGIVEN, _prefix=False, root_cls=None, types=None, immediate=True, static=False, create=None, **kw):
		"""\
			Generate an object tree, populate it, and update it.
			if @create is True, create the directory node.
			@sub can be a prefix that's added to the key; in that case,
			both the "real" root and the prefixed root are returned.

			If @immediate is set, run a recursive query and grab everything now.
			Otherwise fill the tree in the background.
			@static=True turns off the tree's auto-update.

			*Warning*: If you update the tree by direct assignment, you
			must call its `wait()` coroutine before you can depend on them 
			actually being present.
			"""

		if isinstance(key,str):
			key = tuple((k for k in key.split('/') if k != ""))
		xkey = self._extkey(key, _prefix=_prefix)

		if isinstance(sub,str):
			sub = tuple(sub.split('/'))

		if sub is _NOTGIVEN:
			rec = immediate
		else:
			rec = None

		if create is False:
			res = await retry_conn(self.client.read,xkey, recursive=rec)
		elif create is True:
			res = await retry_conn(self.client.write,xkey, prevExist=False, dir=True, value=None)
		else:
			# etcd can't do "create-directory-if-it-does-not-exist", so
			# if two jobs with create=None attempt this at the same time
			# the whole thing gets interesting.
			try:
				res = await retry_conn(self.client.read,xkey, recursive=rec)
			except etcd.EtcdKeyNotFound:
				try:
					res = await retry_conn(self.client.write,xkey, prevExist=False, dir=True, value=None)
				except etcd.EtcdAlreadyExist: # pragma: no cover
					res = await retry_conn(self.client.read,xkey, recursive=rec)

		w = None if static else EtcWatcher(self,xkey,seq=res.etcd_index)
		if root_cls is None and types is not None:
			root_cls = types.type[True]
		if root_cls is None or sub is not _NOTGIVEN:
			root_cls = EtcRoot
		else:
			if isinstance(root_cls,str):
				root_cls = import_string(root_cls)
			assert issubclass(root_cls,EtcRoot)
		root = await root_cls._new(conn=self, watcher=w, key=key, pre=res,
				recursive=rec, types=types, **kw)

		if w is not None:
			w._set_root(root)

		if sub is _NOTGIVEN:
			return root

		r = await root.subdir(*sub,create=create)
		# re-attach the watcher to the new root
		if w is not None:
			w._set_root(r)
		return root,r

# Helpers for constructing a self-typed sub-tree from a recursive sub(?)-listing

async def build_typed(node,name,cls,t,rec):
	obj = cls(parent=node, pre=td, recursive=rec)
	await obj._fill_result(t,recursive=rec)
	return obj

##############################################################################

class SkipAhead(BaseException):
	pass

class EtcWatcher(object):
	"""\
		Runs a watcher on a (sub)tree.

		@conn: the EtcClient to monitor.
		@key: the path to monitor, relative to conn.
		@seq: etcd_index to start monitoring from.
		"""
	_reader = None
	_writer = None
	root = None
	def __init__(self, conn,key,seq=0, types=None):
		self.conn = conn
		self.extkey = key
		self.last_read = seq
		self.last_seen = seq

		self.q = asyncio.Queue(loop=conn._loop)
		self.uptodate = asyncio.Condition(loop=conn._loop)
		self._reader = asyncio.ensure_future(self._watch_read(), loop=conn._loop)
		self._writer = asyncio.ensure_future(self._watch_write(), loop=conn._loop)
		self.stopped = asyncio.Future(loop=conn._loop)
		self.stopped.add_done_callback(lambda _: self.uptodate.notify_unlocked())
		self.conn._trees.add(self)

	def stop(self, exc,cause):
		if not self.stopped.done():
			err = WatchError(cause)
			err.__cause__ = exc
			self.stopped.set_exception(err)
		try:
			self._reader.cancel()
		except Exception:
			pass
		try:
			self._writer.cancel()
		except Exception:
			pass

	@property
	def running(self):
		return not self.stopped.done()

	def __del__(self): # pragma: no cover
		self._kill()

	def _kill(self): # pragma: no cover
		"""Tear down everything"""
		#logger.warning("_KILL")
		if not self.stopped.done():
			try:
				self.stopped.set_result("_kill")
			except RuntimeError: # pragma: no cover ## event loop might be closed
				pass
		for k in ("_reader","_writer"):
			r = getattr(self,k)
			if r is not None:
				setattr(self,k, None)
				try:
					r.cancel()
				except RuntimeError: # pragma: no cover ## event loop might be closed
					pass

	async def close(self):
		self.conn._trees.remove(self)
		if not self.stopped.done():
			self.stopped.set_result("close")
		for k in ("_reader","_writer"):
			r = getattr(self,k)
			if r is not None:
				setattr(self,k, None)
				r.cancel()
				try:
					await r
				except asyncio.CancelledError: # pragma: no cover
					pass

	def _set_root(self, root):
		self.root = weakref.ref(root)
		self.extkey = self.conn._extkey(root.path)

	async def sync(self, mod=None):
		"""Wait for pending updates"""
		root = self.root
		if root is None:
			return
		root = root()
		if root is not None:
			root = root.root # may be a subdir
		if root is None:
			return
		if mod is None or (root.last_mod is not None and mod < root.last_mod):
			mod = root.last_mod
		if mod is None: # nothing has yet happened
			return
		if self._reader is not None and self.last_seen < mod:
			logger.debug("Syncing, wait for %d: %s",mod, id(self))
			w = None
			async with self.uptodate:
				while self._reader is not None and self.last_seen < mod:
					if self.stopped.done():
						raise WatchStopped() from self.stopped.exception()
					await self.uptodate.wait()
													# processing got done during .acquire()
			logger.debug("Syncing, done, at %d: %s",self.last_seen, id(self))
		if self.stopped.done():
			raise WatchStopped() from self.stopped.exception()

	async def _watch_read(self): # pragma: no cover
		"""\
			Task which reads from etcd and processes the events received.
			"""
		logger.debug("READER started")
		conn = Client(loop=self.conn._loop, **self.conn.args)

		key = self.extkey
		# Initially, if creating a sub-tree, the watcher is attached to
		# the main tree until looking up / creating the intermediate nodes
		# is completed. Thus we need to restart watching at the subtree.
		try:
			def cb(x):
				logger.debug("IN: %s %s",id(self),repr(x.__dict__))
				if self.root is None or self.stopped.done():
					raise etcd.StopWatching
				if x.modifiedIndex <= self.last_read:
					raise RuntimeError("not in sequence: %s %s",self.last_read,x.modifiedIndex)
				self.last_read = x.modifiedIndex
				self.q.put_nowait(x)

			while not self.stopped.done():
				logger.debug("INW: %s after %s",id(self),self.last_read)
				await conn.eternal_watch(key, index=self.last_read+1, recursive=True, callback=cb)
				# restart at the subtree
				key = self.extkey

		except GeneratorExit:
			logger.debug("READER GenEx: %s",id(self))
			raise
		except asyncio.CancelledError:
			logger.debug("READER cancelled: %s", id(self))
			raise
		except BaseException as e:
			if type(e) is not RuntimeError or "Event loop is closed" not in str(e):
				logger.exception("READER died: %s", id(self))
			if not self.stopped.done():
				self.stopped.set_exception(e)
			raise
		else:
			logger.debug("READER ended: %s", id(self))
			if not self.stopped.done():
				self.stopped.set_result("end")
		finally:
			conn.close()

	async def _watch_write(self):
		"""\
			Callback which processes incoming events
			"""
		from .node import EtcAwaiter

		# Drop references so that termination works

		while True:
			try:
				x = await self.q.get()
				if not x.key.startswith(self.extkey+'/') and x.key != self.extkey:
					raise SkipAhead # sometimes we get the parent
				r = self.root()
				if r is None: # pragma: no cover
					return

				key = x.key[len(self.extkey):]
				key = tuple(k for k in key.split('/') if k != '')

				if x.action in {'compareAndDelete','delete','expire'}:
					for k in key:
						try:
							r = r._get(k)
							# will not create an EtcAwaiter
						except KeyError:
							raise SkipAhead
					await r._ext_delete(seq=x.modifiedIndex)
				else:
#					if not x.createdIndex:
#						pn = getattr(x,'_prev_node',None)
#						if pn is not None:
#							x.createdIndex = pn.createdIndex
					if key:
						for k in key[:-1]:
							async with r._lock:
								try:
									r = r[k]
								except KeyError:
									r = await r._new(parent=r,key=k,recursive=None)
						async with r._lock:
							try:
								# don't resolve EtcValue or EtcAwaiter
								r = r._get(key[-1])
							except KeyError:
								r = await r._new(parent=r,key=key,pre=x,recursive=False)
						if type(r) is EtcAwaiter:
							await r.load(pre=x,recursive=False)
						else:
							await r._ext_update(x)
					else:
						await r._ext_update(x)

			except SkipAhead:
				pass
			except asyncio.CancelledError as e:
				logger.debug("Write watcher cancelled")
				raise
			except Exception as e:
				logger.exception("Error in write watcher")
				if not self.stopped.done():
					self.stopped.set_exception(e)
				return

			async with self.uptodate:
				self.last_seen = x.modifiedIndex
				self.uptodate.notify_all()
				logger.debug("DONE %d: %s",x.modifiedIndex,id(self))

class EtcTypes(object):
	doc = None
	pri = 0

	def __init__(self):
		self.type = [None,None]
		self.nodes = {}

	def __repr__(self): # pragma: no cover
		return "<%s:%s>" % (self.__class__.__name__,repr(self.type))

	def __call__(self, cls):
		"""\
			For usage as a class decorator.
			"""
		from .node import EtcDir,EtcXValue
		if issubclass(cls,EtcDir):
			dir = True
		elif issubclass(cls,EtcXValue):
			dir = False
		else:
			raise RuntimeError("%s: not an EtcDir/Value type" % (repr(cls),))

		if self.type[dir] is not None:
			raise RuntimeError("already registered")
		self.type[dir] = cls
		return cls

	def step(self,*key, dest=None):
		"""\
			Lookup a path, with auto-generation of new nodes.
			This is for registration only! For discovery, use
			.lookup(raw=True).

			You can set @dest to an existing EtcTypes object if you want to
			prepend to an existing tree.
			"""
		if len(key) == 1:
			key = key[0]
		if not key:
			assert dest is None or dest is self
			return self
		if isinstance(key,str):
			key = key.split('/')
		for k in key[:-1]:
			assert k != ''
			res = self.nodes.get(k,None)
			if res is None:
				res = EtcTypes()
				self.nodes[k] = res
			self = res
		k = key[-1]
		assert k != ''
		res = self.nodes.get(k,None)
		if res is None:
			if dest is None:
				dest = EtcTypes()
			self.nodes[k] = res = dest
		else:
			assert dest is None or dest is res
		return res

	def items(self,key=None):
		"""\
			Enumerate sub-entries matching this key.
			Yields (name,sub-entry) tuples.
			Note that a name of "**" is supposed to match a whole subtree,
			so the matching algorithm in .lookup() carries it over.

			If no key is given, enumerate all of this node's entries.
			"""
		if key is None:
			yield from self.nodes.items()
			return

		res = self.nodes.get(key,None)
		if res is not None:
			yield key,res
		if key[0] == ':':
			w1 = ':*'
			w2 = None
		else:
			w1 = '*'
			w2 = '**'
		res = self.nodes.get(w1,None)
		if res is not None:
			yield w1,res
		if w2 is not None:
			res = self.nodes.get(w2,None)
			if res is not None:
				yield w2,res

	def __getitem__(self,path):
		"""Shortcut to directly lookup a non-directory node"""
		self = self.step(path)
		return self.type[0]

	def __setitem__(self,path,value):
		"""Shortcut to register a non-directory node"""
		self = self.step(path)
		self._register(value)

	def register(self, *path, dir=None, cls=None, **kw):
		"""\
			Teach this node that a sub-node named @name is to be of type @sub.

			Set @doc to some doc string.
			Set @pri to the priority of this entry. Higher is better.
			"""
		self = self.step(*path)
		if cls is None:
			assert not kw
			return self._register
		else:
			return self._register(cls,**kw)

	def _register(self, cls,doc=None,pri=0):
		"""Register a class for this node"""
		from .node import EtcDir,EtcXValue
		done = False

		if doc is None:
			doc = cls.__doc__
		if doc:
			self.doc = doc
		if pri:
			self.pri = pri
		if issubclass(cls,EtcXValue):
			self.type[0] = cls
			done = True
		if issubclass(cls,EtcDir):
			self.type[1] = cls
			done = True
		if not done:
			raise RuntimeError("What exactly are you trying to register?")
		return cls

	def lookup(self, *path, dir, raw=False):
		"""\
			Find the node type that's to be associated with a path below me.

			This is called on the root node.
			@dir must be True (a directory) or False (an end node).
			If @raw is True, returns the EtcTypes entry instead of the class.
			"""
		from .node import EtcDir,EtcXValue

		if len(path) == 1:
			path = path[0]
			if isinstance(path,str):
				path = path.split('/')
		nodes = [(".",self)]
		for i,p in enumerate(path):
			d = dir if i == len(path)-1 else True
			assert p != ''
			cn = []
			for k,n in nodes:
				for nk,nn in n.items(p):
					cn.append((nk,nn))
					nn = getattr(nn.type[d],'_types',None)
					if nn is not None:
						cn.append((nk,nn))
				if k == '**':
					cn.append((k,n))
			if not cn:
				return None
			nodes = cn

		def by_pri(k):
			k=k[1].type
			if k[0] is None or not hasattr(k[0],'pri'):
				return -getattr(k[1],'pri',0)
			elif k[1] is None or not hasattr(k[1],'pri'):
				return -k[0].pri
			else:
				return -max(k[0].pri, k[1].pri)
		for p,n in sorted(nodes, key=by_pri):
			t = n.type[dir]
			if t is not None:
				if isinstance(t,str):
					n.type[dir] = t = import_string(t)
				if dir is True:
					assert issubclass(t,EtcDir)
				elif dir is False:
					assert issubclass(t,EtcXValue),t
				return n if raw else t
		return None

