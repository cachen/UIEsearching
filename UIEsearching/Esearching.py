#!/usr/bin/env python
import sys
import getopt
import os
import re
import pyatspi

"""
Search for application's element
"""

def abort(status):
    ''' exit according to status '''
    sys.exit(status)

def output(s=(), newline=True):
    format = "ControlName: %-20s ElementName: %-20s Parent: %-20s Children:\n"
    if not Settings.is_quiet:
        if newline:
            info = format % (s)
    return info

def help():
    help_info = """Usage: Esearching.py [options]
    For example: Esearching.py -a gedit -t findAll -c PushButton -n Undo -C 0
    Options:
          -h | --help        Print help information (this message)
          -a | --appname     Give application's name (Firefox, gedit....)
          -t | --findtype    'findAll' or 'find'
          -c | --ctrlname    Give the control's name you want to find (PushButton, Menu....)
          -n | --elementname Give the element's name you want to find (Open, Edit....)
          -C | --children    Whether print out element's children"""
    return help_info

def acc_status():
    '''
    Check accessibility status
    '''
    acc_status = os.popen('gconftool-2 -g /desktop/gnome/interface/accessibility').read().strip()
    return acc_status

def acc_active(status):
    '''
    Setup accessibility status
    '''
    os.system('gconftool-2 -s --type=bool /desktop/gnome/interface/accessibility %s' % status)

def spi_status():
    '''
    Check at-spi-registryd process
    '''
    process = os.popen('pgrep at-spi').read().strip()
    if process:
        spi_status = "running"
    else:
        spi_status = "not running"
    return spi_status

def spi_active():
    '''
    Make at-spi-registryd process running
    '''
    os.system('/usr/lib/at-spi/at-spi-registryd &')

class Settings(object):

    # static variable
    is_quiet = False
    list_children = None
    appname = None
    findtype = 'findAll'
    ctrlname = None
    elementname = None

    def argument_parser(self):
        opts = []
        args = []
        try:
            opts, args = getopt.getopt(sys.argv[1:],"ha:t:c:n:C:",["appname=","findtype=","ctrlname=","elementname=","help", "children"])
        except getopt.GetoptError:
            print help()
            abort(1)

        for o,a in opts:
            if o in ("-h","--help"):
                print help()
                abort(0)

            if o in ("-a", "--appname"):
                Settings.appname = a

            if o in ("-t", "--findtype"):
                Settings.findtype = a
                if Settings.findtype != "find" and Settings.findtype != "findAll":
                  print help()
                  abort(0)

            if o in ("-c", "--ctrlname"):
                Settings.ctrlname = a.lower()

            if o in ("-n", "--elementname"):
                Settings.elementname = a

            if o in ("-C", "--children"):
                if a is None:
                    Settings.list_children = 0
                else:
                    Settings.list_children = int(a)

class Searching(object):

    def __init__(self, findtype, appname, ctrlname, elementname, list_children):
        self.appname = appname
        self.findtype = findtype
        self.ctrlname = ctrlname
        self.elementname = elementname
        self.list_children = list_children

        if self.ctrlname != None and not self.ctrlname.startswith("application") and self.appname == None:
            print "Usage: Please give application's name, for example: -a gedit"
            abort(1)
        if self.ctrlname == None and self.elementname == None:
            print "Usage: Please give control name or element name, for example: -c PushButton, or -n Save"
            abort(1)

    def findFunc(self):
        if self.findtype == 'find':
            searchings = [pyatspi.findDescendant(self.appname, lambda x: x.getRoleName() == self.ctrlname)]
        elif self.findtype == 'findAll':
            searchings = pyatspi.findAllDescendants(self.appname, lambda x: x.getRoleName() == self.ctrlname)

        return searchings

    def searchObj(self, appname, ctrlname, elementname):
        reg = pyatspi.Registry
        desktop = reg.getDesktop(0)
        app = pyatspi.findDescendant(desktop, lambda x: x.name == self.appname)
        self.appname = app

        if self.ctrlname != None and self.ctrlname.startswith("application"):
            searchings = []
            for i in desktop:
                if i is not None:
                    searchings.append(i)
        elif self.ctrlname == None:
            searchings = pyatspi.findAllDescendants(self.appname, lambda x: x.name == self.elementname)
        elif self.ctrlname == None and self.findtype == "find":
            searchings = pyatspi.findDescendant(self.appname, lambda x: x.name == self.elementname)
        else:
            searchings = self.findFunc()

        return searchings

    def getChildren(self,obj, child_count):
        children = []
        children_name = []
        children_role = []
        children_info = {}

        accessible = obj
        for n in range(child_count):
            children.append(accessible.getChildAtIndex(n))
            children_name.append(accessible.getChildAtIndex(n).name)
            children_role.append(accessible.getChildAtIndex(n).getRoleName())
            children_info = zip(children_name, children_role)
        return children, children_info

    def run(self):
        output_info = []
        if self.list_children is not None:
            searchings = self.searchObj(self.appname, self.ctrlname, self.elementname)

            for obj in searchings:
                child_count = obj.childCount
                (children, children_info) = self.getChildren(obj, child_count)

                if self.list_children == 0:
                    output_info.append("="*80)
                    output_info.append(output(([obj.getRoleName()], [obj.name], obj.parent)))
                else:
                    for c in children:
                        child_count = c.childCount
                        (children, children_info) = self.getChildren(c, child_count)
                        if self.list_children == 1:
                            output_info.append("="*80)
                            output_info.append(output(([c.getRoleName()], [c.name], c.parent)))
                        elif self.list_children > 1:
                            for c1 in children:
                                if c1.childCount > 0:
                                    (children, children_info) = self.getChildren(c1, c1.childCount)
                                    output_info.append("="*80)
                                    output_info.append(output(([c1.getRoleName()], [c1.name], c1.parent)))

                for i in enumerate(children_info):
                    output_info.append(i)
        else:
            searchings = self.searchObj(self.appname, self.ctrlname, self.elementname)
            for i in searchings:
                output_info.append("="*80)
                output_info.append(output(([i.getRoleName()], [i.name], i.parent)))

        return output_info

if __name__ == '__main__':
  st = Settings()
  st.argument_parser()
  s = Searching(Settings.findtype, Settings.appname, Settings.ctrlname, Settings.elementname, Settings.list_children)

  for i in s.run():
    print i

