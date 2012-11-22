#!/usr/bin/env python
import inspect
from ScriptingBridge import SBApplication
iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
from encoder import eachSBElementArray
# import time

native_selector_type = type(SBApplication.version)
# if type(member_value) == native_selector_type:
#     if len([c for c in member_value.signature if '@' == c]) > 1:
#         # print '%s requires too many arguments (%s)' % (member_name, member_value.signature)
#         member_value = '[multiarg: %s]' % member_value.signature
# time.sleep(0.01)

def explore(obj, show_errors=True, show_blacklist=True):
    for member_name, member_value in inspect.getmembers(obj):
        # print '++', member_name
        blacklist = ['isDeallocating', 'allowsWeakReference', 'finalize', 'isRangeSpecifier', 'isRunning', 'launchFlags', 'sendMode', 'specifier', 'timeout', 'dealloc', 'delegate', 'init', 'retainWeakReference', 'specifierDescription']
        try:
            if member_name in blacklist:
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

source = eachSBElementArray(iTunes.sources()).next()
library_playlist = eachSBElementArray(source.libraryPlaylists()).next()
track = eachSBElementArray(library_playlist.tracks()).next()
print 'First track'
explore(track, False, False)

