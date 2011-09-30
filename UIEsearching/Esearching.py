#!/usr/bin/env python

import sys
import getopt
import os
import re
import pyatspi
import strongwind

"""
Search for application's element
"""

def abort(status):
    ''' exit according to status '''
    sys.exit(status)

def output(s, newline=True):
    if not Settings.is_quiet:
        if newline:
            print s
        else:
            print s

def toControlName(str):
    if str.isalnum() and str[0].islower():
        words = ''
        for c in str:
            if c.isupper():
                words += ' '
            words += c
        name = ''
        for word in words.split(' '):
            name += word.capitalize()
    else:
        name = ''
        for word in re.split('[^a-zA-Z0-9]', str):
            if len(re.split('[^a-zA-Z0-9]', str)) > 1:
                name = name + word.capitalize()
            else:
                name = name + word
    return name

class Settings(object):

    # static variable
    is_quiet = False
    list_children = None
    appname = None
    findtype = 'findAll'
    ctrlname = None
    elementname = None

    def __init__(self):
        self.argument_parser()

    def argument_parser(self):
        opts = []
        args = []
        try:
            opts, args = getopt.getopt(sys.argv[1:],"ha:t:c:n:C:",["appname=","findtype=","ctrlname=","elementname=","help", "children"])
        except getopt.GetoptError:
            self.help()
            abort(1)

        for o,a in opts:
            if o in ("-h","--help"):
                self.help()
                abort(0)
            if o in ("-a", "--appname"):
                Settings.appname = a
            if o in ("-t", "--findtype"):
                Settings.findtype = a
                if Settings.findtype != "find" and Settings.findtype != "findAll":
                  self.help()
                  abort(0)

            if o in ("-c", "--ctrlname"):
                Settings.ctrlname = a
                if Settings.findtype == "findAll":
                    Settings.ctrlname = a + 's'
                Settings.ctrlname = toControlName(Settings.ctrlname)

            if o in ("-n", "--elementname"):
                Settings.elementname = a

            if o in ("-C", "--children"):
                if a is None:
                    Settings.list_children = 0
                else:
                    Settings.list_children = int(a)

    def help(self):
      output("Usage: searching.py [options]")
      output("For example: searching.py -a gedit -t findAll -c PushButton -n Undo -C 0")
      output("Options:")
      output("  -h | --help        Print help information (this message)")
      output("  -a | --appname     Give application's name")
      output("  -t | --findtype    'findAll' or 'find'")
      output("  -c | --ctrlname    Give the control's name you want to find")
      output("  -n | --elementname Give the element's name you want to find")
      output("  -C | --children    Whether print out element's children")

class Searching(object):

    def __init__(self):
        if Settings.ctrlname != None and not Settings.ctrlname.startswith("Application") and Settings.appname == None:
            print "Usage: Please give application's name, for example: -a gedit"
            abort(1)
        if Settings.ctrlname == None and Settings.elementname == None:
            print "Usage: Please give control name or element name, for example: -c PushButton, or -n Save"
            abort(1)

    def findFunc(self):
        func = getattr(Settings.appname, Settings.findtype + Settings.ctrlname)
        searchings = func(name=Settings.elementname, checkShowing=False)
        if Settings.findtype == 'find':
            searchings = [searchings]
        return searchings

    def searchObj(self, appname, ctrlname, elementname):
        app = strongwind.cache._desktop.findApplication(Settings.appname, checkShowing=False)
        Settings.appname = app

        if Settings.ctrlname != None and Settings.ctrlname.startswith("Application"):
            Settings.appname = strongwind.cache._desktop
            searchings = self.findFunc()
        elif Settings.ctrlname == None:
            searchings = pyatspi.findAllDescendants(Settings.appname, lambda x: x.name == Settings.elementname)
        elif Settings.ctrlname == None and Settings.findtype == "find":
            searchings = pyatspi.findDescendant(Settings.appname, lambda x: x.name == Settings.elementname)
        else:
            searchings = self.findFunc()
        return searchings

    def getChildren(self,obj, child_count):
        children = []
        children_name = []
        children_role = []
        children_info = {}
        if isinstance(obj, strongwind.accessibles.Accessible):
            accessible = obj._accessible
        else:
            accessible = obj
        for n in range(child_count):
            children.append(accessible.getChildAtIndex(n))
            children_name.append(accessible.getChildAtIndex(n).name)
            children_role.append(accessible.getChildAtIndex(n).getRoleName())
            children_info = zip(children_name, children_role)
        return children, children_info

    def run(self):
        if Settings.list_children is not None:
            searchings = self.searchObj(Settings.appname, Settings.ctrlname, Settings.elementname)

            for obj in searchings:
                child_count = obj._accessible.childCount
                (children, children_info) = self.getChildren(obj, child_count)

                if Settings.list_children == 0:
                    output("======================================================")
                    output("ControlName: %s	ElementName: %s		Parent: %s	Children:\n" % \
                                      ([obj._accessible.getRoleName()], [obj.name], obj._accessible.parent))
                    for i in enumerate(children_info):
                        output(i)
                else:
                    for c in children:
                        child_count = c.childCount
                        (children, children_info) = self.getChildren(c, child_count)
                        if Settings.list_children == 1:
                            output("======================================================")
                            output("ControlName: %s	ElementName: %s		Parent: %s	Children:\n" % \
                                       ([c.getRoleName()], [c.name], c.parent))
                            for i in enumerate(children_info):
                                output(i)
                        elif Settings.list_children > 1:
                            for c1 in children:
                                if c1.childCount > 0:
                                    (children, children_info) = self.getChildren(c1, c1.childCount)
                                    output("======================================================")
                                    output("ControlName: %s	ElementName: %s		Parent: %s	Children:\n" % \
                                                ([c1.getRoleName()], [c1.name], c1.parent))
                                    for i in enumerate(children_info):
                                        output(i)
        else:
            searchings = self.searchObj(Settings.appname, Settings.ctrlname, Settings.elementname)
            for i in searchings:
                output("======================================================")
                output("ControlName: %s	ElementName: %s		Parent: %s" % \
                                      ([i._accessible.getRoleName()], [i.name], i._accessible.parent))

class Main(object):

  def main(self, argv=None):
    s = Searching()
    r = None
    if r is None or r == 0:
      r = s.run()
    return r

if __name__ == '__main__':
  Settings()
  main_obj = Main();
  sys.exit(main_obj.main())
