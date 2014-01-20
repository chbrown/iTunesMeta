#!/usr/bin/env python
# import re
import inspect
# import time

# native_selector_type = type(SBApplication.version)
# if type(member_value) == native_selector_type:
#     if len([c for c in member_value.signature if '@' == c]) > 1:
#         # print '%s requires too many arguments (%s)' % (member_name, member_value.signature)
#         member_value = '[multiarg: %s]' % member_value.signature
# time.sleep(0.01)

def explore(obj, show_errors=True, show_blacklist=True, ignore=None):
    blacklist = ['isDeallocating', 'allowsWeakReference', 'finalize', 'isRangeSpecifier', 'isRunning', 'launchFlags', 'sendMode', 'specifier', 'timeout', 'dealloc', 'delegate', 'init', 'retainWeakReference', 'specifierDescription', 'copyWithZone']
    # these won't break anything, but they don't provide any helpful info
    blacklist += ['retain', 'scriptingProperties', 'self', 'superclass', 'toManyRelationshipKeys', 'toOneRelationshipKeys', 'userInterfaceItemIdentifier', 'zone', 'persistentID', 'pyobjc_instanceMethods', 'release', 'exposedBindings', 'flushKeyBindings', 'hash', 'autorelease', 'allPropertyKeys', 'autoContentAccessingProxy', 'lastError', 'delete', 'id', 'get', 'index', 'retainCount']
    for member_name, member_value in inspect.getmembers(obj):
        # print '++', member_name
        try:
            if ignore and ignore.search(member_name):
                pass
            elif member_name in blacklist:
                if show_blacklist:
                    print '%s = [blacklisted]' % member_name
            elif hasattr(member_value, '__call__'):
                print '%s() = %s' % (member_name, member_value())
            else:
                print '%s = %s' % (member_name, member_value)
        except Exception, exc:
            if show_errors:
                member_value = '[Error: %s]' % exc
        except ValueError, exc:
            member_value = '[ValueError: %s]' % exc



# print 'Here are all the application level variables:'
# explore(iTunes)
# explore(iTunes.sources().objectAtIndex_(0))


# source = eachSBElementArray(iTunes.sources()).next()
# print 'First source playlists'
# for playlist in eachSBElementArray(source.playlists()):
#     print
#     explore(playlist, False, False, re.compile('^(_|accessibility|to|is|class|CA|CI)'))
# track = eachSBElementArray(library_playlist.tracks()).next()

