# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  performer_desks.py                         (\(\
# Func:    Accessing a set of available performers    (^.^)
# # ## ### ##### ######## ############# #####################

from typing import Dict, List, Tuple
import sys, os, pathlib, importlib
import workers, desks, performer_shortcuts, performers
sys.path.append(os.path.abspath(str(pathlib.Path(__file__).parent.parent.absolute()) + "/performers"))


class PerformerDesk(desks.Desk):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.performer_shortcuts, self.performer_shortcuts_by_names = self.load_performer_shortcuts()


    def load_performer_shortcuts(self) -> Tuple[List, Dict]:

        loaded_performer_shortcuts = performer_shortcuts.PerformerShortcut(self).load_all() 

        performer_shortcuts_by_names = {}

        for performer_shortcut in loaded_performer_shortcuts:
            performer_shortcuts_by_names[performer_shortcut.get_performer_name()] = performer_shortcut

        return loaded_performer_shortcuts, performer_shortcuts_by_names


    def get_performer_names(self) -> List:

        return self.performer_shortcuts_by_names.keys()


    def has_performer(self, performer_name: str) -> bool:

        return performer_name in self.performer_shortcuts_by_names


    def get_performer_shortcut(self, performer_name: str) -> performer_shortcuts.PerformerShortcut:

        return self.performer_shortcuts_by_names.get(performer_name)
    

    def involve_admin(self, performer_name: str) -> performers.Reporter:
        
        if self.has_performer(performer_name):

            shortcut = self.get_performer_shortcut(performer_name)
            
            admin_module_full_name = shortcut.get_admin_module_full_name()
            
            try:
                admin_module = importlib.import_module(admin_module_full_name)
                performer_admin = admin_module.new_admin(shortcut)
            except:
                performer_admin = None

        else:
            performer_admin = None

        return performer_admin
    

    def involve_processor(self, performer_name: str) -> performers.Reporter:
        
        if self.has_performer(performer_name):

            shortcut = self.get_performer_shortcut(performer_name)
            processor_module_full_name = shortcut.get_processor_module_full_name()
            
            try:
                processor_module = importlib.import_module(processor_module_full_name)
                performer_processor = processor_module.new_processor(shortcut)
            except:
                performer_processor = None

        else:
            performer_processor = None

        return performer_processor


    def involve_reporter(self, performer_name: str) -> performers.Reporter:
        
        if self.has_performer(performer_name):

            shortcut = self.get_performer_shortcut(performer_name)
            reporter_module_full_name = shortcut.get_reporter_module_full_name()
            
            try:
                performer_module = importlib.import_module(reporter_module_full_name)
                performer_reporter = performer_module.new_reporter(shortcut)
            except:
                performer_reporter = None

        else:
            performer_reporter = None

        return performer_reporter