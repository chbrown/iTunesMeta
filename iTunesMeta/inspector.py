import inspect
# import time


hidden_blacklist = set([
    '__class__',
    '__cobject__',
    '__delattr__',
    '__dict__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__gt__',
    '__hash__',
    '__init__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__',
])

objc_blacklist = set([
    '_',
    '_pyobjc_performOnThread:',
    '_pyobjc_performOnThreadWithResult:',
    'activate',  # calling this brings iTunes to the front
    'clearProperties',
    'close',
    'delegate',
    'delete',
    'fastForward',  # fast-forwards the current track
    'mute',
    'NS_addTiledLayerDescendent_',
    'NS_removeTiledLayerDescendent_',
    'NS_tiledLayerVisibleRect',
    'pyobjc_ISA',
    'rewind',
    'setTo_',
])

segfault_blacklist = set([
    'conformsToProtocol_',
    'dealloc',
    'finalize',
    'forwardingTargetForSelector_',
    'forwardInvocation_',
    'handleQueryWithUnboundKey_',
    'handleTakeValue_forUnboundKey_',
    'implementsSelector_',
    'infoForBinding_',
    'init',
    'initWithApplication_specifier_',
    'initWithBundleIdentifier_',
    'initWithClass_properties_data_',
    'initWithCoder_',
    'initWithContext_',
    'initWithData_',
    'initWithProperties_',
    'isRunning',
    'launchFlags',
    'mutableArrayValueForKey_',
    'mutableOrderedSetValueForKey_',
    'mutableSetValueForKey_',
    'qualifiedSpecifier',
    'release',
    'replacementObjectForArchiver_',
    'replacementObjectForCoder_',
    'replacementObjectForKeyedArchiver_',
    'retain',
    'self',
    'setApplication:',
    'setDelegate_',
    'setNilValueForKey_',
    'specifierDescription',
    'storedValueForKey_',
    'unableToSetNilForKey_',
    'valueForKey_',
    'valueForUndefinedKey_',
])
inspect_blacklist = hidden_blacklist | objc_blacklist | segfault_blacklist


def dump_check(obj, blacklist=inspect_blacklist):
    for member_name, member_value in inspect.getmembers(obj):
        if member_name in blacklist:
            # type(member_name), member_name in blacklist
            # print '[member_name in blacklist]',
            # print type(member_name), len(member_name), repr(member_name)
            print '<BLACKLISTED>'
        else:
            # print '[member_name not in blacklist]',
            # print type(member_name), len(member_name), repr(member_name)
            # print member_name, type(member_name), 'not in', blacklist, member_name not in blacklist
            # if inspect.ismethod(member_value):
            # if hasattr(member_value, '__call__'):
            if hasattr(member_value, 'selector'):
                # print '(%s)' % ', '.join(argspec.args),
                n_args = member_value.selector.count(':')
                print '(%d)' % n_args,
                if n_args == 0:
                    result = member_value.__call__()
                elif n_args == 1:
                    result = member_value.__call__(obj)
                else:
                    result = '<NA>'
                # argspec = inspect.getargspec(member_value)
                # if len(argspec.args) == 1:
                # result = member_value.__call__(obj)
                # else:
            else:
                result = member_value
            print ':', result


def dump(obj, blacklist=inspect_blacklist):
    for member_name, member_value in inspect.getmembers(obj):
        if member_name not in blacklist:
            print member_name, '---'
            try:
                print '%s(self): %s' % (member_name, member_value.__call__(obj))
            except Exception:
                try:
                    print '%s(): %s' % (member_name, member_value.__call__())
                except Exception, exc2:
                    print '%s: %s' % (member_name, member_value), exc2
            # time.sleep(.1)

# inspector = IPython.core.oinspect.Inspector()
# inspector.info(s0)
# member_dict = dict(inspect.getmembers(iTunes))
