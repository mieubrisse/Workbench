'''
Created on Feb 1, 2013
Installs a Minecraft jar and provides jar-switching functionality
@author: Kevin Today
'''

import json
import os
import shutil
import sys
import urllib2

class JarDispenser:
    
    _APP_DIRNAME = "JarDispenser"
    
    _BACKUP_BINS_DIRNAME = "backup_bins"                # Name of dir where bins are stored
    _BACKUP_WORLDSAVES_DIRNAME = "backup_worldsaves"    # Name of dir where worldsaves are stored
    _DATA_JSON_FILENAME = "user_data.json"              # JSON file containing all data that should be persisted across runs
    _BIN_VERSION_AT_INSTALL = "VERS_AT_INSTALL"         # Version name to give the minecraft.jar binary at time of install
    ### TODO Examine the jar to find the version number
    
    # Keys for the main data structure
    _MINECRAFT_ASSETS_URL_KEY = "minecraft_assets_url"          # Key to URL of site where minecraft jars are uploaded (<http://assets.minecraft.net> at the moment)
    _MINECRAFT_FOLDER_DIRPATH_KEY = "minecraft_folder_dirpath"  # Key for dirpath to .minecraft folder containing all minecraft data
    _CURRENT_BIN_VERSION_KEY = "current_bin_version"            # Key for the version of the current binary being used
    _VERSIONS_LIST_KEY = "versions_list"                        # Key for the list of all versions stored in JarDispenser
    
    
    
    """ Initialize the app's folders if this is the user's first run, otherwise load data from disk """
    def __init__(self):
        self._user_data = dict()
        
        # Perform first-time setup actions if needed
        if not os.path.isfile(self._DATA_JSON_FILENAME):
            self._setup()
        else:
            self._load_user_data()

    
    """ Called when the user first runs JarInstaller. Creates necessary files and directories """
    def _setup(self):
        # Find .minecraft folder on Windows
        minecraft_dirpath = "C:\\Users\\" + os.environ.get("USERNAME") + "\\AppData\\Roaming\\.minecraft"
        if not os.path.isdir(minecraft_dirpath):
            raise OSError("Unable to find .minecraft folder at '" + minecraft_dirpath + "'; please be sure it exists")
        bin_dirpath = os.path.join(minecraft_dirpath, "bin")
        if not os.path.isdir(minecraft_dirpath):
            raise OSError("Unable to find .minecraft folder at '" + minecraft_dirpath + "'; please be sure it exists")
            
        # Create application directories
        if not os.path.exists(self._BACKUP_BINS_DIRNAME):
            os.mkdir(self._BACKUP_BINS_DIRNAME)
        if not os.path.exists(self._BACKUP_WORLDSAVES_DIRNAME):
            os.mkdir(self._BACKUP_WORLDSAVES_DIRNAME)
        ### TODO: Read into dict currently-existing world saves
        
        ### TODO: Load current version into system
        current_bin_src_filepath = os.path.join(minecraft_dirpath,"bin","minecraft.jar")
        current_bin_dest_filepath = os.path.join(self._BACKUP_BINS_DIRNAME, self._BIN_VERSION_AT_INSTALL + ".jar")
        shutil.copyfile(current_bin_src_filepath, current_bin_dest_filepath)
        versions_list = [self._BIN_VERSION_AT_INSTALL]
        
        #### TODO: Backup current saves
        
        # Initialize user_data
        self._user_data[self._MINECRAFT_ASSETS_URL_KEY] = "http://assets.minecraft.net"
        self._user_data[self._MINECRAFT_FOLDER_DIRPATH_KEY] = minecraft_dirpath
        self._user_data[self._CURRENT_BIN_VERSION_KEY] = self._BIN_VERSION_AT_INSTALL
        self._user_data[self._VERSIONS_LIST_KEY] = versions_list
        self._save_user_data()
        
        
        
    """ Loads user settings from disk  """
    def _load_user_data(self):
        data_file = open(self._DATA_JSON_FILENAME, "r")
        self._user_data = json.load(data_file)
        data_file.close()
    
    
    
    
    """ Writes user settings to disk in form of JSON file """
    def _save_user_data(self):
        data_file = open(self._DATA_JSON_FILENAME, "w+")
        json.dump(self._user_data, data_file, indent=4)
        data_file.close()
        
        
    
    
    """ Downloads the minecraft.jar with the given version from the assets site in user_data """
    def download_jar(self, version_name):      
        # Don't do anything if a jar of the specified version is already present
        bin_versions_list = self._user_data[self._VERSIONS_LIST_KEY]
        if version_name in bin_versions_list:
            return
        
        # Download jar if it can be located
        jar_url = self._user_data[self._MINECRAFT_ASSETS_URL_KEY] + "/" + version_name + "/minecraft.jar"
        jar_src = urllib2.urlopen(jar_url)
            
        # Move jar into JarInstaller's directory
        dest_filepath = os.path.join(self._BACKUP_BINS_DIRNAME, version_name + ".jar")
        jar_dest = open(dest_filepath, "w")
        shutil.copyfileobj(jar_src, jar_dest)
        bin_versions_list.append(version_name)
        self._save_user_data()
            
        jar_dest.close()
        jar_src.close()
        
        
        
    """ Uses the jar with the given version for Minecraft """
    def use_jar(self, version_name):
        version_list = self._user_data[self._VERSIONS_LIST_KEY]
        if version_name not in version_list:
            raise ValueError("No version with the name '" + version_name + "' exists")
        
        src_bin_filepath = os.path.join(self._BACKUP_BINS_DIRNAME, version_name + ".jar")
        dest_bin_filepath = os.path.join(self._user_data[self._MINECRAFT_FOLDER_DIRPATH_KEY], "bin", "minecraft.jar")
        shutil.copy(src_bin_filepath, dest_bin_filepath)
    
    
    
    """ Gets the version of the binary currently in use """
    def current_version(self):
        return self._user_data[self._CURRENT_BIN_VERSION_KEY]
    
    
    """ Gets the list of downloaded versions """
    def list_versions(self):
        return self._user_data[self._VERSIONS_LIST_KEY]
    
    

    


    



