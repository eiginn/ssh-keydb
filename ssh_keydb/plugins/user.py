# ssh-keydb - http://ssh-keydb.googlecode.com/
#
# Copyright (C) 2010 Fabien Bouleau
#
# This file is part of ssh-keydb.
#
# ssh-keydb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ssh-keydb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ssh-keydb.  If not, see <http://www.gnu.org/licenses/>.

import sys
from model import *
from controller import Controller
from key import KeyController

__all__ = [ 'UserController' ]

class UserController(Controller):
    def list(self, *kargs, **kwargs):
        args = kargs
        opts = kwargs

        lst = self.filter(*kargs, **kwargs)

        if len(lst) == 0: 
            return

        hdr = { 'user': 'user', 'section': 'section','key': 'key','location': 'location' }

        nl = {}
        for user in lst:
            nl['user'] = max(nl.get('user', len(hdr['user'])), len(user.user))
            nl['section'] = max(nl.get('section', len(hdr['section'])), len(user.section or ''))
            if user.location is not None: nl['location'] = max(nl.get('location', len(hdr['location'])), len(user.location.location or ''))
            for k in user.keys:
                nl['key'] = max(nl.get('key', len(hdr['key'])), len(k.key_name))
            
        fmt = '%%(user)-%(user)is %%(section)-%(section)is %%(location)-%(location)is' % nl
        n = sum(nl.values()) - nl['key'] + len(nl) - 2

        if 'long' in opts:
            fmt = '%%(user)-%(user)is %%(section)-%(section)is %%(location)-%(location)is %%(key)-%(key)is' % nl
            n = sum(nl.values()) + len(nl) - 1

        print fmt % hdr
        print '-' * n

        for user in lst:
            kl = dict(enumerate(user.keys))
            k = kl.get(0)
            kn = ''
            if k: kn = k.key_name
            print fmt % { 'user': user.user, 'section': user.section or '', 'key': kn, 'location': user.location.location or '' }
            if 'long' in opts:
                for ii in range(1, len(kl)):
                    k = kl[ii]
                    print fmt % { 'user': '', 'section': '', 'location': '', 'key': k.key_name }


    def filter(self, *kargs, **kwargs):
        if len(kargs) > 0:
            return None

        args = kargs
        opts = kwargs

        userlist = User.query.filter(None)

        if 'user' in opts: 
            userlist = userlist.filter_by(user = opts['user'])

        if 'section' in opts: 
            sectionname = None
            if opts['section'] != '':
                sectionname = opts['section']
            userlist = userlist.filter_by(section = sectionname)

        if 'location' in opts: 
            loc = None
            if opts['location'] != '':
                loc = Location.get_by(location = opts['location'])
            userlist = userlist.filter_by(location = loc)

        return userlist.all()

    def set(self, *kargs, **kwargs):
        args = kargs
        opts = kwargs

        if len(args) < 2:
            raise SyntaxError()

        username = args[0]
        location = args[1]
        sectionname = None

        if len(args) > 2: sectionname = args[2]

        user = User.get_by(user = username)
        location = Location.get_by(location = location)

        if location is None:
            print 'Error: location does not exist.'
            sys.exit(1)

        if user is None:
            user = User(user = username, section = sectionname, location = location)
        else:
            if len(args) > 1:
                user.location = location
            if len(args) > 2:
                user.section = sectionname

        if 'keyfile' in opts: 
            KeyController().setkeyfile(user, opts['keyfile'])
        elif 'keystring' in opts: 
            KeyController().setkeystring(user, opts['keystring'])

        session.flush()
        session.commit()

        return True

    def remove(self, *kargs, **kwargs):
        userlist = self.filter(*kargs, **kwargs)

        if userlist is None:
            return
        
        n = len(userlist)

        if n > 2:
            ch = raw_input('Warning: remove all %i users (Y/n)? ' % n)
            if ch != 'Y':
                print 'Cancelled.'
                sys.exit(1)

        for user in userlist:
            section = user.section or ''
            if section != '':
                section = section + ', '
            for key in user.keys:
                key.delete()
            user.delete()

        session.flush()
        session.commit()

        return True

    list.usage = {        
        'shortdesc': 'Manage users',        
        'usage': [ '%(exec)s user list [--user=<user>] [--section=<section>] [--location=<location>] [--long]' ],
        'options': {             
            'help': 'displays the current help',        
            'user=': 'filter by user',
            'section=': 'filter by section',
            'location=': 'filter by location',
            'long': 'long display',
        },        
        'shortopts': { 'help': 'h', 'long': 'l' }    
    }    

    set.usage = {        
        'shortdesc': 'Manage users',        
        'usage': [ '%(exec)s user set <user> <location> [<section>] [--keyfile=<keyfile>] [--keystring=<string>]' ],
        'options': {             
            'help': 'displays the current help',        
            'keyfile=': 'set/filter by key from file',
            'keystring=': 'set/filter by key from string',
        },        
        'shortopts': { 'help': 'h', }    
    }    

    remove.usage = {        
        'shortdesc': 'Manage users',        
        'usage': [ '%(exec)s user remove [--user=<user>] [--section=<section>] [--key=<key>]' ],
        'options': {             
            'help': 'displays the current help',        
            'section=': 'filter by section name',
            'user=': 'filter by user name',
            'key=': 'set/filter by key name',
        },        
        'shortopts': { 'help': 'h', }    
    }    

    usage = {         
        'command': [ 'user' ],
        'shortdesc': 'Manage users',    
    } 

UserController()

if __name__ == '__main__':
    c = UserController()
    c.list()