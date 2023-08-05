from decorator import decorate, decorator
from datetime import datetime
import sys
import traceback

from peewee import SqliteDatabase, Model, JOIN, fn, OperationalError
from peewee import CharField, SmallIntegerField, DateTimeField
from peewee import ForeignKeyField, FloatField, TextField


DB_FILENAME = 'pystas.db'
ALLOW_CUSTOM_DB = False

if ALLOW_CUSTOM_DB:
    if '-f' in sys.argv:
        idx = sys.argv.index('-f')
        sys.argv.pop(idx)
        DB_FILENAME = sys.argv.pop(idx)
DB = SqliteDatabase(DB_FILENAME)


@decorator
def retry(f, *args, **kw):
    ok = False
    while not ok:
        try:
            # with DB.transaction() as txn:
            #    ret = f(*args, **kw)
            #    txn.commit()
            with DB.atomic():
                ret = f(*args, **kw)
            ok = True
        except OperationalError, e:
            msg = e.message
            if not (msg.startswith("database is locked") or
                        msg.startswith("no such savepoint:")):
                raise
    return ret


class BaseModel(Model):
    @retry
    def save(self, *args, **kw):
        return super(BaseModel, self).save(*args, **kw)

    @classmethod
    @retry
    def get_or_create(cls, **kwargs):
        return super(BaseModel, cls).get_or_create(**kwargs)

    class Meta:
        database = DB


class PreFunctionSave:
    def __init__(self, module, name):
        self.name = name
        self.klass = None
        self.module = module

    @classmethod
    def For(cls, _function):
        _module = getattr(_function, '__module__', '')
        name = getattr(_function, 'func_name', '')
        return cls(module=_module, name=name)

    def getFunc(self, klass, arg_string):
        classname = None if klass is None else klass.__name__
        return Function.get_or_create(module=self.module, klass=classname,
                                      name=self.name, args=arg_string)


class Function(BaseModel):
    module = CharField(db_column='package')
    klass = CharField(db_column='class', null=True) # actually, classname or..
    name = CharField(db_column='function')
    args = CharField(null=True)

    def __repr__(self):
        klass = '' if self.klass is None else self.klass+'.'
        args = ' (%s)' % self.args if self.args is not None else ''
        return '%s:%s%s%s' % (self.module, klass, self.name, args)


class Src(BaseModel):
    name = CharField(db_column='filename')
    line = SmallIntegerField()

    @classmethod
    def For(cls, _function):
        func_code = _function.func_code
        name = getattr(func_code, 'co_filename', '')
        line = getattr(func_code, 'co_firstlineno', -1)
        ent, created = cls.get_or_create(name=name, line=line)
        return ent

    def __repr__(self):
        return '<%s:%d>' % (self.name, self.line)


class ProgExecution(BaseModel):
    start = DateTimeField()

    def __repr__(self):
        return '#%d' % self.id


class Errors(BaseModel):
    excep = CharField(db_column='Exception')
    error = TextField(db_column='Data')

    @classmethod
    def For(cls, exc):
        ent, create = cls.get_or_create(excep=exc.__class__.__name__,
                                        error=traceback.format_exc())
        return ent

    def __repr__(self):
        return self.excep


class Execution(BaseModel):
    function = ForeignKeyField(Function, related_name='executions')
    src = ForeignKeyField(Src, related_name='executions')
    prg = ForeignKeyField(ProgExecution, related_name='executions')
    start = DateTimeField(default=datetime.now)
    duration = FloatField(null=True)
    error = ForeignKeyField(Errors, related_name='executions', null=True)

    def __repr__(self):
        excp = '[%r]' % self.error if self.error else ''
        duration = self.duration if self.duration is not None else -1
        return '%s| %3.02fs. %s %s' % (self.prg, duration, self.function, excp)


ExecutionStart = None


class Pistas(object):
    @staticmethod
    def save_1_arg(is_func, args, kw):
        _args = args if is_func else args[1:]
        return repr(_args[0])

    @staticmethod
    def save_all_args(is_func, args, kw):
        _args = args if is_func else args[1:]
        return repr((_args, kw))[1:-1]

    @classmethod
    def log(cls, f, fargs=lambda have_self, args, kw: None):
        f.dbsrc = Src.For(f)
        f.dbfunc = PreFunctionSave.For(f)
        f.fargs = fargs
        return decorate(f, cls.log_decorator)

    @classmethod
    def get_class(cls, fname, args):
        if len(args) > 0:
            call_self = args[0]
            bound = getattr(call_self, fname, None)
            if not bound is None:
                return bound.im_class
        return

    @classmethod
    def log_decorator(cls, f, *args, **kw):
        klass = cls.get_class(f.dbfunc.name, args)
        x, _ = f.dbfunc.getFunc(klass, f.fargs(klass is None, args, kw))
        x.save()
        execution = Execution(function=x, src=f.dbsrc, prg=ExecutionStart)
        execution.save()
        try:
            return f(*args, **kw)
        except Exception, exc:
            execution.error = Errors.For(exc)
            execution.save()
            raise
        finally:
            end = datetime.now()
            execution.duration = (end-execution.start).total_seconds()
            execution.save()

    def __init__(self):
        raise RuntimeError("No instances of this class are required!")


logpista = Pistas.log
logw1arg = lambda f: Pistas.log(f, Pistas.save_1_arg)
logwargs = lambda f: Pistas.log(f, Pistas.save_all_args)


@retry
def init():
    try:
        DB.create_tables([Function, Src, Execution, Errors, ProgExecution])
    except OperationalError, e:
        msg = e.message
        if not (msg.startswith("table ") and msg.endswith(" already exists")):
            raise


if not __name__ == "__main__":
    # loaded as helper module..
    init()
    ExecutionStart = ProgExecution(start=datetime.now())
    ExecutionStart.save()
else:
    from texttable import Texttable

    def get_last_exec():
        for prgexec in ProgExecution.select().order_by(
                ProgExecution.start.desc()).limit(1):
            return prgexec

    def show_stats(condition, title):
        print
        print title
        table = Texttable(100)
        table.set_deco(Texttable.HEADER)
        table.set_chars(['', '', '+', '-'])
        #table.set_cols_dtype(['i', 'i', 'f', 'f', 't'])
        table.set_cols_dtype(['i', 'i', 't', 't', 't'])
        table.set_cols_align(["r", "r", "r", "r", "l"])
        table.header(['calls', 'excp.', 't.total', 'media', 'function'])
        table.set_precision(2)
        fs = lambda x: '%3.02fs' % x
        for _function in Function.select(Function,
                                         fn.Count(Execution.id).alias('count'),
                                         fn.SUM(Execution.duration).alias(
                                             'total'),
                                         fn.Count(Errors.id).alias('errors'),
                                         ).join(Execution
                                         ).join(Errors, JOIN.LEFT_OUTER
                                         ).where(
                                         condition).group_by(Function):
            table.add_row([
                _function.count, _function.errors, fs(_function.total),
                fs(_function.total / _function.count), _function
            ])
        print table.draw()


    # loaded as executable..
    lastprg = get_last_exec()
    print ('last execution is: %r started: %s complete dump:' % (lastprg,
                                                                 lastprg.start))
    for _execution in Execution.select(
                        ).where(Execution.prg == lastprg
                        ).order_by(Execution.start.desc()):
        print _execution

    show_stats(Function.id == Function.id, "all-history")
    show_stats(Execution.prg == lastprg, "last-exec")