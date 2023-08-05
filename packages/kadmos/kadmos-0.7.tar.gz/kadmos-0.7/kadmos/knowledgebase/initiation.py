import json
import logging
import networkx as nx
import os
import shutil
import re
from lxml import etree

from kadmos.graph import KadmosGraph, RepositoryConnectivityGraph
import kadmos.utilities.mapping as MU
from kadmos.utilities.prompting import user_prompt_yes_no, user_prompt_select_options
from kadmos.utilities.printing import print_indexed_list


# Settings for the logger
logger = logging.getLogger(__name__)


class KnowledgeBaseInitiator(object):
    """
    This class initiates the knowledge base for a given set of tool blueprints. The user is able to select tools from the
    database of blueprints.

    """


    def __init__(self, knowledge_base_path, schema_files_dir=None, specific_files_dir = None):
        """
        ADD DESCRIPTION
        """

        # save inputs as attributes
        self.kb_path = knowledge_base_path
        self.schema_files_dir = schema_files_dir
        self.specific_files_dir = specific_files_dir
        self.circularConnections= {}

        # ----> HARDCODE <----

        self.WORKDIR_SUB = ['SCHEMATIC_BASE', 'SPECIFIC_BASE'] # directories must be present in working directory

        self.GEN_INFO = ["name", "version", "creator", "description", "schema_input", "schema_output"] # prescribed general info

        self.EXEC_INFO = ["mode", "description", "prog_env", "toolspecific", "runtime", "precision", "fidelity"] # prescribed execution info

        self.STANDARD_KB_NAME = "UNNAMED_KB_DIR" # knowledge base folder name if none indicated at initiation

        self.FILEPATTERN = "(-input-schema.xml)$|(-output-schema.xml)$|(-info.json)$"  # file patterns for matching

        ##########  execute Class Methods ########

        # perform checks on kb schema directory and kb directory
        self.check_knowledge_base_schema()

        # get function files from schema directory and save in instance: self.function_files
        self._get_function_files()

        # read data from provided schema files and save them in instance: self.function_data
        self._get_function_data()

        # get function graphs in kb schema according to their execution modes
        self.get_function_graphs_in_kb_schema()


    def check_knowledge_base_schema(self):
        """
        This function checks whether the provided knowledge base schema directory exists or not. If not, error is thrown.
        It then proceeds to check the existence of the specified knowledge base directory, and creates a knowledge base
        directory based on user input.
        If initiation is done with a specified directory name, the user will be prompted about the decision to replace
        an existing directory, if one is found with the same name. Otherwise, the specified directory is created without
        prompts. If no knowledge base directory is given, the standard name will be used (self.STANDARD_KB_NAME).

        :return:    self.schema_files_dir_path: Full path to the schema files directory
        :return:    self.specific_files_dir: Depending on user-input, new or old kb directory name
        :return:    self.specific_files_dir_path: Full path to the created knowledge base
        """

        # assert that knowledge base dir and subdirs exist
        assert isinstance(self.kb_path, basestring), "Provided 'KB_path' argument must be of type string."
        assert os.path.exists(self.kb_path), "Provided 'KB_path' does not exist."
        assert os.path.isdir(self.kb_path), "Provided 'KB_path' must be a directory."
        assert all(os.path.isdir(os.path.join(self.kb_path, dir)) for dir in self.WORKDIR_SUB), \
            "All of the directories must be present in the working directory: {}".format(', '.join(self.WORKDIR_SUB))

        # define schematic and specific base paths
        self.schema_base_path = os.path.join(self.kb_path, 'SCHEMATIC_BASE')
        self.spec_base_path = os.path.join(self.kb_path, 'SPECIFIC_BASE')

        # check if schema files directory exist; if not, let user select one
        if self.schema_files_dir is not None:
            assert isinstance(self.schema_files_dir, basestring), \
                "The provided schematic base directory must be of type string."
            assert os.path.isdir(os.path.join(self.schema_base_path, self.schema_files_dir)), \
                "Could not find schema dir {} directory in {}".format(self.schema_files_dir, self.schema_base_path)
            self.schema_files_dir_path = os.path.join(self.schema_base_path, self.schema_files_dir)

        else: # if schema dir not provided

            # get schema file directories
            schema_dirs = [obj for obj in os.listdir(self.schema_base_path) if os.path.isdir(os.path.join(self.schema_base_path, obj))]
            assert schema_dirs, "No schema file directories found in {}".format(self.kb_path, 'SCHEMATIC_BASE')

            if len(schema_dirs) > 1:

                # print schema dirs and let user choose
                mssg = "\nThe following directories were found in {}: "
                print_indexed_list(*schema_dirs, message=mssg)
                user_sel = user_prompt_select_options(*schema_dirs, allow_multi=False)
                self.schema_files_dir = next(iter(user_sel))

            else: # if only one present, take that one
                self.schema_files_dir = next(iter(schema_dirs))

        # define path of schema files directory
        self.schema_files_dir_path = os.path.join(self.schema_base_path, self.schema_files_dir)

        # create new knowledge base directory
        if self.specific_files_dir is not None:
            assert isinstance(self.specific_files_dir, basestring), "The specific files directory must be a string."

            # make sure that name does not already exist, otherwise ask user if overwrite or not
            if os.path.exists(os.path.join(self.spec_base_path, self.specific_files_dir)):

                mssg = "The provided directory name '{}' already exists in:\n'{}'.\n\nWould you like to overwrite its contents?".format(self.specific_files_dir, self.spec_base_path)
                usr_sel = user_prompt_yes_no(message=mssg)
                # usr_sel = 0 #TODO:DEMO

                # either create a unique directory or delete directory contents
                if usr_sel:
                    shutil.rmtree(os.path.join(self.spec_base_path, self.specific_files_dir))
                    os.makedirs(os.path.join(self.spec_base_path, self.specific_files_dir))
                else:
                    self.specific_files_dir = self._create_unique_directory(self.spec_base_path, self.specific_files_dir)

            else: # create that directory
                os.makedirs(os.path.join(self.spec_base_path, self.specific_files_dir))

        else: # create dir with standard name
            if os.path.exists(os.path.join(self.spec_base_path, self.STANDARD_KB_NAME)):
                self.specific_files_dir = self._create_unique_directory(self.spec_base_path, self.STANDARD_KB_NAME)
            else:
                self.specific_files_dir = self.STANDARD_KB_NAME
                os.makedirs(os.path.join(self.spec_base_path, self.specific_files_dir))

        # store specific files dir
        self.specific_files_dir_path = os.path.join(self.spec_base_path, self.specific_files_dir)

        # print init message
        initString = "\nInitiating KADMOS for Knowledge Base Schema:  {}\n".format(self.schema_files_dir)
        print "\n{0}{1}{0}\n".format("#"*(len(initString)-2), initString)

        print "NOTE: Writing to {}.\n".format(self.specific_files_dir_path)

        return


    def _create_unique_directory(self, parent_dir_path, directory):
        """
        This helper function takes the desired name and adds squared brackets to its name containing an index, making the
        directory unique. The new directory is created in the provided parent path.

        :param      parent_dir_path: Path to parent directory
        :param      directory: Desired directory name
        :return:    alternate_dir: Alternative directory name
        """

        # loop through alternative names until a non-existing name is found; create dir
        kb_dir_idx = 0
        alternate_dir = ""
        while True:
            kb_dir_idx += 1
            alternate_dir = "{}[{}]".format(directory, kb_dir_idx)
            if not os.path.exists(os.path.join(parent_dir_path, alternate_dir)):
                break

        os.makedirs(os.path.join(parent_dir_path, alternate_dir))

        return alternate_dir


    def _get_function_files(self):
        """
        (PRIVATE) This function

        :return:
        """
        # TODO: function description!
        # TODO: MAKE SURE THAT (a) DIR IS NOT EMPTY and (b) FILE STRUCTURE IS THERE (INFO, INPUT, OUTPUT)!

        # Read input and output XML files and info json files, save them in self.function_files
        self.function_files = dict(input=[], output=[], info=[])
        self.function_list = []

        # setup pattern to match type of file (info, input, output)
        typePattern = "-[a-zA-Z]*."

        files_in_dir = os.listdir(self.schema_files_dir_path)

        listOfTools = []
        for file in files_in_dir:
            matchEnding = re.search(self.FILEPATTERN, file)
            if matchEnding:
                listOfTools.append(file[:-len(matchEnding.group())])
        listOfTools = list(set(listOfTools)) # make elements unique

        # prompt user for tools selection
        # ignoreTools = self._ignore_tools_for_kb(listOfTools)
        ignoreTools = [] #TODO:DEMO

        for file in files_in_dir:
            matchEnding = re.search(self.FILEPATTERN, file)  # match name ending
            if matchEnding:
                # if the file matches any in the ignoreList, skip
                if file[:-len(matchEnding.group())] in ignoreTools:
                    continue
                matchType = re.search(typePattern, matchEnding.group())
                self.function_files[matchType.group()[1:-1]].append(file)
            else:
                if not file.endswith("mapping.json"): # TODO: add mapping file properly
                    print "Could not identify the type of {}, please make sure files adhere to naming conventions".format(file)

        # assert that the correct function files present, not just amount
        redundantFiles = [] # contains functions with missing info-file
        infoFiles = [file[:-len('-info.json')] for file in self.function_files['info']]
        for inout in ['input', 'output']:
            removeList = [] # list used as cross check
            inOutFiles = [file[:-len("-{}-schema.xml".format(inout))] for file in self.function_files[inout]]
            for infoFile in infoFiles:
                if infoFile in inOutFiles:
                    removeList.append(infoFile)
                else:
                    raise ValueError, "Can not find {}-{}-schema.xml in '{}'. Please check for correct spelling of info, input and output files.".format(infoFile, inout, self.schema_files_dir)

            redundantFiles += [file for file in inOutFiles if file not in removeList]

        assert not redundantFiles, "The following tools have missing -info.json files: \n" + "\n".join(set(redundantFiles))

        return


    def _ignore_tools_for_kb(self, listOfTools):
        """
        (PRIVATE) This helper function prompts the user to make a selection from a given list of tools on which tools to
        ignore from this list for further analysis. It first lists the available tools in the console, and asks the user
        whether to ignore any of them. If "No" is chosen, the function is exited with an empty list. If "Yes", the user
        is asked to give the corresponding indices of the tools to remove.

        :param listOfTools: List of tools found in repository
        :return: ignoreTools: List of tools that will be ignored when functions are loaded into init-object
        """

        assert isinstance(listOfTools, list), "'listOfTools' argument must be of type 'list'."

        # print list of tools found in schema dir
        mssg = "The following tools have been found in the {} directory:".format(self.schema_files_dir)
        print_indexed_list(message=mssg, *listOfTools)

        ignoreTools = [] # initiate list of tools to ignore

        # prompt user to select tools to ignore, if user chooses to ignore tools
        mssg = "Would you like to ignore any of the listed tools?"
        user_input = user_prompt_yes_no(message=mssg)
        if user_input == 1:
            selectMssg = "Please select all tools you would like to ignore (separate by space):"
            ignoreTools = user_prompt_select_options(message=selectMssg, *listOfTools)

        if not ignoreTools or user_input == 0: # if empty list
            print "No tools are ignored."

        return ignoreTools


    def _get_function_data(self):
        """"
        (PRIVATE) This function adds a new attribute functionData to the class instance that contains all information in the knowledge base.

        functionData = [
            {
                "info": {
                                "general_info": {"name": str, "type": str, "version": float, "creator": str, "description": str},
                                "execution_info": [{"mode": str, "runtime": int, "precision": float, "fidelity": str}, # mode 1
                                    ... ]
                        }
                        ,
                "input": 	{
                                "leafNodes": 	[ {"xpath": str, "tag": str, "attributes": dict, "value": str, "level": int}, ...] # list of all input leafNodes
                                "completeNodeSet": [] # list of ALL nodes (for convenience)
                                "leafNodeSet": [] # list of all leaf nodes (for convenience)
                            },
                "output": 	{
                                "leafNodes": 	[ {"xpath": str, "tag": str, "attributes": dict, "value": str, "level": int}, ...], # list of all output leafNodes
                                "completeNodeSet": [] # list of ALL nodes (for convenience)
                                "leafNodeSet": [] # list of all leaf nodes (for convenience)

                            }
            }, # tool1
            ...
        ]

        :return self.function_data
        """

        self.function_data = []

        # loop through info-files and extract relevant information from info and corresponding input, output files
        for file in self.function_files["info"]:

            # initiate a dict for each function
            funcDict = {'info': {'general_info': {}, 'execution_info': [] }}

            # open -info.json to read data
            with open(os.path.join(self.schema_files_dir_path, file)) as info:
                print "loading {}".format(os.path.join(self.schema_files_dir_path, file))
                infoData = json.load(info)

            # make sure that execution and general info is provided in info-file
            for info in ["execution_info", "general_info"]:
                assert info in infoData, "{}-key is missing in {}. Please check for spelling errors.".format(info, file)

            # add function info from file to funcDict
            for inf in self.GEN_INFO: # looping through general info

                # make sure that function name and type is defined, is string
                if inf == 'name':
                    funcName = infoData["general_info"].get(inf)
                    assert isinstance(funcName, basestring), "Function name in {} must be of type 'string'!".format(file)
                    assert len(funcName)>0, "Function name in {} must be non-empty string!".format(file)

                # add general info if provided in file
                try: funcDict['info']['general_info'][inf] = infoData["general_info"].get(inf)
                except KeyError:
                    print "Function {} was not found for {} and not added to knowledge base.".format(inf, funcName)

            # assert that exection info is provided for at least one mode
            execInfo = infoData["execution_info"]
            assert isinstance(execInfo, list), "'execution_info' in info-file for {} must be a list (of dicts).".format(funcName)
            assert len(execInfo)>0, "The {} 'execution_info' must have at least one defined mode. Please add a function mode to the info-file.".format(funcName)

            # loop through execution info for each mode
            for dictIndex, modeDict in enumerate(execInfo):

                assert isinstance(modeDict, dict), "Each element in 'execution_info'-list in {} must be dictionary.".format(file)

                #add mode dict to exec info
                funcDict['info']['execution_info'].append({})

                # make sure mode name is defined
                mode = modeDict["mode"]
                assert isinstance(mode, basestring), "Execution mode names in {} must be defined string(s) in the info-file.".format(file)
                assert re.match("^[a-zA-Z0-9_]+$", mode), "Execution mode {} in {} must be non-empty string of alphanumeric characters (and underscore).".format(file)

                # add execution info by mode to function dictionary (if that information is provided)
                for inf in self.EXEC_INFO:
                    if inf in modeDict:
                        funcDict['info']['execution_info'][dictIndex][inf] = modeDict[inf]  # add the information to dictionary
                    else:
                        raise KeyError, "'{}'-information for mode {} of {} is not available in the info-file!".format(inf, mode, funcName)

            # ensure that the execution modes given in info-file are unique
            funcModes = [execDict['mode'] for execDict in funcDict['info']['execution_info']]
            if not len(funcModes) == len(set(funcModes)):
                duplicateModes = set([mode for mode in funcModes if funcModes.count(mode) > 1])
                raise ValueError, "Duplicate function mode(s) [{}] found in {}.".format(", ".join(duplicateModes), file)

            # get input and output data
            for inOut in ['input', 'output']:
                funcDict[inOut] = self._get_function_input_output_data(file, inOut, funcDict)

            # add function dictionary to list of function data
            self.function_data.append(funcDict)

            # check if circular coupling exists for this function
            outputSet = set(funcDict['output']['leafNodeSet'])
            for nodeDict in funcDict['input']["leafNodes"]:
                nodePath = nodeDict["xpath"]
                if nodePath in outputSet:
                    self.circularConnections[funcName] = []
                    self.circularConnections[funcName].append(nodePath)

        return


    def _get_function_input_output_data(self, file, inOut, functionDict):
        """
        (PRIVATE) This helper function writes the information on all leaf nodes from the input and output XML files to a dictionary. \
        If XML file is empty, it empty dict is returned. The element paths are checked for uniqueness.

        :param file: info-file corresponding to the analyzed function
        :param inOut: must be "input" or "output"
        :param functionDict:
        :return: dict: dictionary containing all XPaths and leaf nodes
        """
        # initiate data dictionary
        dataDict = {"leafNodes": [], "completeNodeSet": [],"leafNodeSet": []}

        # define file and file path to read data from (based on info-file)
        func = file[:-10] # remove -info.json to get file name
        mapFile = "{}-{}-schema.xml".format(func, inOut)
        parseFile = os.path.join(self.schema_files_dir_path, mapFile)

        # if XML file is empty, return empty dict, else parse file
        if os.stat(parseFile).st_size == 0: # check size of file
            return dataDict
        else:
            tree = etree.parse(parseFile)

        # remove comments from tree, if any present
        comments = tree.xpath("//comment()")
        for c in comments:
            p = c.getparent()
            p.remove(c)

        # iterate through tree and add data to dict, only touch leaf nodes
        leafNodesList = []
        completeNodeList = []
        for el in tree.iter():
            elemData = {}
            elemPath = MU.xpath_to_uid_xpath(tree.getpath(el), el)

            # check whether indices in path --> uniqueness
            indexPattern = ('\[[0-9]+\]')
            if re.search(indexPattern, elemPath):
                raise ValueError, "Element {} in {} has index and is not unique!".format(elemPath, mapFile)

            # append path to list of all nodes
            completeNodeList.append(elemPath)

            if not el.getchildren(): # if leaf node

                # append path to list of leaf nodes
                leafNodesList.append(elemPath)

                # add element data to function dict
                elemData['xpath'] = elemPath
                elemData['tag'] = el.tag
                elemData['attributes'] = el.attrib
                elemData['level'] = elemPath.count('/') - 1
                elemData['value'] = el.text  # adding None if empty

                # add 'modes' attribute if it does not exist
                elemData['modes'] = self._get_execution_modes_for_element(el, tree, mapFile, functionDict)

                # remove whitespace from start/end of string, or add None
                if el.text is not None:
                    elemData['value'] = el.text.strip()
                else:
                    elemData['value'] = el.text  # adding None if empty

                # add element data to data dict
                dataDict['leafNodes'].append(elemData)

        # add complete list of input/output nodes (for convenience, performance later on)
        dataDict["leafNodeSet"] = set(leafNodesList)

        # add list of ALL nodes to dictionary (for convenience, performance later on)
        dataDict["completeNodeSet"] = set(completeNodeList)

        # check if toolspecific nodes found in file
        if any("toolspecific" in node for node in dataDict["leafNodeSet"]):
            logger.waning("'toolspecific' nodes found in {}".format(mapFile))

        return dataDict


    def _get_execution_modes_for_element(self, element, tree, file, functionDict):
        """
        (PRIVATE) This function retrieves the modes attribute of the child node or of its ancestors. If multiple modes
        are defined in its ancestry, a warning is given and only the lowest modes definition is returned. Ancestry is
        checked for 'modes' attributes regardless of whether it is present in it leaf-node or not.
        Once the modes are retrieved, they are checked for validity (present in info-file) and "negativity" (mode
        attributes can either be positive or negative). NOTE: If no modes are given in a leaf-node, this node is applied
        to ALL function modes.

        :param element: xml element, leaf-node
        :param tree: element tree of the current element
        :param file: file that is currently analyzed
        :param functionDict: data dict containing execution and info data
        :return: execModes: string containing all function modes applied to this element
        """
        # get element xpath
        elementPath = tree.getpath(element)

        # get function modes from info file and assert that they are unique
        funcModes = [execDict['mode'] for execDict in functionDict['info']['execution_info']]
        execModes = '' # NOTE: if no modes indicated, all modes are applied to node
        modesFound = False

        if 'modes' in element.attrib and re.search("[^\s]", element.attrib['modes']): # if 'modes' key present and has characters
            assert isinstance(element.attrib['modes'], basestring), "If provided, modes-attribute of elemeent {} in {} must be of type string.".format(elementPath, file)
            execModes = element.attrib['modes']
            modesFound = True

        for anc in element.iterancestors():
            if 'modes' in anc.attrib  and re.search("[^\s]", anc.attrib['modes']):
                if not modesFound:
                    modesFound = True
                    execModes = anc.attrib['modes']
                else:
                    print "WARNING: Multiple 'modes' attributes found in ancestry of element {} in {}; lowest one is applied.".format(elementPath, file)
                    break

        if re.search("[^\s]", execModes):  # if contains any characters

            # get all modes
            modesList = execModes.split()

            # check if modes negative (all either negative or positive)
            modesNegative = False
            negPattern = "^-"
            if any(re.search(negPattern, mode) for mode in modesList):
                modesNegative = True

                assert all(re.search(negPattern, mode) for mode in modesList), \
                    "Either all or none of the 'modes'-attributes of element {} in {} must be negative!".format(elementPath, file)

            # check if each mode is valid (use its positive if modesNegative)
            for mode in modesList:
                if modesNegative:
                    assert mode[1:] in funcModes, "Execution mode '{}' of node {} (or its ancestor) in {} was not found in the info-file. Please check spelling or alter info-file.".format(mode[1:], elementPath, file)
                else:
                    assert mode in funcModes, "Execution mode '{}' of node {} (or its ancestor) in {} was not found in the info-file. Please check spelling or alter info-file.".format(mode, elementPath, file)

        return execModes


    def get_function_graphs_in_kb_schema(self):
        """
        This class method generates all graphs for all present functions in the knowledge base, and add these to
        the class instance as: self.functionGraphs.

        :return: self.functionGraphs
        """
        # get list of all functions in KB
        funcList = [self.function_data[i]['info']["general_info"]['name'] for i in range(len(self.function_data))]

        # initiate list of function graphs and add graphs to it
        graphList = []
        for func in funcList:
            graphList.append(self.get_function_graph(func))

        # add list of function graphs to class instance
        self.functionGraphs = graphList

        return


    def get_function_graph(self, funcName, inOut=None):
        """
        This function builds a directed graph (KadmosGraph object) for the specified function using the "networkx" package. If inOut
        argument is specified, only the input or output of the function will be included in the graph, otherwise both.

        The "modes" functionality enables the addition of function modes to certain nodes. If a node is required in certain
        execution modes for a tool, the attribute "modes" will indicate this in the CPACS element. When creating function graphs,
        graphs are created for EACH mode. Nodes that are only present in certain modes will therefore only be added to the
        corresponding function graph.

        :param: funcName: function name for which the graph is generated; must be present in knowledge base.
        :param: inOut: default = None; if specified, must be "input" or "output" string. Specification of this argument enables the generation of the function graph with only input or output variables.
        :return: functionGraph
        """

        assert isinstance(funcName, basestring), 'Provided function name must be a string!'

        # assert funcName exists and get index of function in self.function_data list
        funcIndex = None
        for idx, funcDict in enumerate(self.function_data):
            if funcDict['info']['general_info']['name'] == funcName:
                funcIndex = idx  # funcIndex is index of the function in list
                break
        assert funcIndex is not None, "The provided function name can not be found in knowledge base."

        # assert inOut, if defined, is string and either input or output
        if inOut is not None:
            assert isinstance(inOut, basestring), "inOut argument must be a string if specified."
            assert inOut.lower() in ["input", "output"], "inOut argument must be either 'input' or 'output'."
        else:
            inOut = ["input", "output"]

        # initiate directed graph and list of edges
        DG, edgeTpls = KadmosGraph(), []

        # get all execution modes for the function from function info
        funcModes = set([infoDict['mode'] for infoDict in funcDict['info']['execution_info']])

        # loop input and output elements
        for io in inOut:

            # loop through xml leaf-nodes and add them to function-tuples list, i.e output: (function, leaf-node)
            for nodeDict in funcDict[io]['leafNodes']:
                modesAttr = nodeDict['modes'] # modes-attrib always present
                node = nodeDict['xpath'] # will not contain any indeces

                if re.search("[^\s]", modesAttr):  # if contains any characters

                    # get all modes
                    nodeModes = modesAttr.split()

                    # check if modes negative (all either negative or positive)
                    modesNegative = False
                    negPattern = "^-"
                    if any(re.search(negPattern, mode) for mode in nodeModes):

                        # make sure that all modes in list "positive" for later processing; remove minus sign
                        # (modesNegative ensures that modes are still regarded as negative)
                        modesNegative = True
                        for i, mode in enumerate(nodeModes):
                            nodeModes[i] = mode[1:]

                    """
                    Add relevant modes to addModes list (modes that apply to the node). The addModes list plays an
                    important part in the creation of function graphs, since the creation of function-leafNode tuples
                    depends on it.
                    """
                    if modesNegative:
                        # add to all modes but the ones indicated
                        addModes = [mode for mode in funcModes if not mode in nodeModes]
                    else:
                        # add to all modes the ones indicated
                        addModes = list(set(nodeModes) & set(funcModes))

                else:
                    # add to all modes
                    addModes = list(funcModes)

                # add edge tuple for the node and function
                edgeTpls += self._create_edge_tuples(funcName, funcModes, io, node, addModes)

        # loop through all function-leafnode-tuples and add them to graph
        DG.add_edges_from(edgeTpls, coupling_strength = 1) # each edge has connection strength of one

        # add node attributes to each node in graph
        self._add_node_attribs(funcDict, funcName, funcModes, DG)

        DG.name = funcName

        return DG

    # TODO: (maybe?) add functionality to ignore certain running modes; similar to ignoreList function

    def _create_edge_tuples(self, funcName, funcModes, inOut, node, addModes):
        """
        (PRIVATE) This helper function creates a list of edge tuples in order to generate a graph. The function label
        depends on the mode that the edge tuple is applied to. If the list of modes is larger than one, the mode name
        is indicated in square brackets, i.e. Function[MODE].

        :param funcName: Function name
        :param funcModes: List of all modes that apply to that function
        :param inOut: Specifies whether input or output nodes
        :param node: Name (xpath) of the input or output node
        :param addModes: List of modes that the node is applied to
        :return: tpls: list of function-leafNode-tuples that will be added to graph
        """
        # initiate list of tuples
        tpls = []

        #make sure that at least one mode is present
        assert len(addModes)>0, "At least one mode must be present for node {} of {}!".format(node, funcName)

        for mode in addModes:

            # if more than one mode, use mode in brackets
            if len(funcModes) > 1:
                funcLabel = '{}[{}]'.format(funcName, mode)
            else:
                funcLabel = funcName

            # determine whether input or output node
            if inOut.lower() == 'input':
                tpl = (node, funcLabel)
            else:
                tpl = (funcLabel, node)

            tpls.append(tpl)

        return tpls


    def _add_node_attribs(self, funcDict, funcName, funcModes, G):
        """
        (PRIVATE) Function that adds node attributes to the nodes in the graph. If the node is

        :param funcDict: Dictionary conainting all function data
        :param funcName: Function name
        :param funcModes: List of modes applied to the nodes
        :param G: Function graph w/o attribs
        :return: G: Function graph w/ attribs
        """

        for node in G.nodes_iter():
            if re.match(funcName, node):  # if node matches function name

                # add attributes to node
                G.node[node]['shape'] = 's'  # square for functions
                G.node[node]['category'] = 'function'
                G.node[node]['label'] = node
                G.node[node]['name'] = funcName
                G.node[node]['level'] = None

                # check if node has brackets to retrieve execution mode
                modePattern = "\[.+\]"
                match = re.search(modePattern, node)
                if match:
                    fMode = match.group(0)[1:-1]  # take matching string and remove brackets
                    assert fMode in funcModes, 'Something went wrong! Could not find execution mode {} for {} in list of execution modes.'.format(
                        fMode, funcName)
                else:
                    fMode = next(iter(funcModes))  # get only execution mode in set

                # loop over execution modes of function and add execution info to graph node
                for execMode in funcDict['info']['execution_info']:
                    if fMode == execMode['mode']:

                        # loop over execution info and add the provided information to node; raise error if info missing
                        for info in self.EXEC_INFO:
                            G.node[node][info] = execMode[info]

            else: # otherwise variable node

                # add attributes to node
                G.node[node]['shape'] = 'o'  # circle for variables
                G.node[node]['category'] = 'variable'
                G.node[node]['label'] = node.split('/')[-1]
                G.node[node]['level'] = node.count('/') - 1
                G.node[node]['execution_time'] = 1  # TODO: this is not really needed for nodes

        return G


    def get_MCG(self, name='RCG-GRAPH'):
        """
        Function to create Maximal Connectivity Graph (Pate, 2014) by composing a list of graphs.

        :param: name: Name of the RCG
        :return: maximal connectivity graph (RCG)
        """
        # TODO: Check with get_rcg function of knowledgebase.py

        functionGraphs = self.functionGraphs

        MCG = RepositoryConnectivityGraph()  # initialize RCG

        logger.info('Composing RCG...')
        for g in functionGraphs:
            MCG = nx.compose(MCG, g)
        logger.info('Successfully composed RCG.')

        # Add kb_path and name attribute
        MCG.name = name
        MCG.kb_schema_path = self.schema_files_dir_path

        return MCG