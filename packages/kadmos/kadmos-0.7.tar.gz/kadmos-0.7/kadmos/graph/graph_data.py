# Imports
import itertools
import copy
import logging
import distutils.util
import re

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from ..utilities import prompting
from ..utilities import printing
from ..utilities.general import make_camel_case, unmake_camel_case, make_plural, get_list_entries, translate_dict_keys
from ..utilities.testing import check
from ..utilities.plotting import AnnoteFinder
from ..utilities.xml import Element

from graph_kadmos import KadmosGraph

from mixin_mdao import MdaoMixin
from mixin_kechain import KeChainMixin


# Settings for the logger
logger = logging.getLogger(__name__)


class DataGraph(KadmosGraph):

    def __init__(self, *args, **kwargs):
        super(DataGraph, self).__init__(*args, **kwargs)

    def cleancopy(self):
        """Method to make a clean copy of a graph.

        This method can be used to avoid deep-copy problems in graph manipulation algorithms.
        The graph class is kept.

        :return: clean-copy of the graph
        :rtype: DataGraph
        """

        return DataGraph(self)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            CREATE METHODS                                                        #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _create_cmdows_problem_def(self):

        # Create problemDefinition
        cmdows_problem_definition = Element('problemDefinition')
        graph_problem_formulation = self.graph.get('problem_formulation')
        cmdows_problem_definition.set('uID', str(graph_problem_formulation.get('mdao_architecture')) +
                                      str(graph_problem_formulation.get('convergence_type')))

        # Create problemDefinition/problemFormulation
        cmdows_problem_formulation = cmdows_problem_definition.add('problemFormulation')
        graph_problem_formulation = self.graph.get('problem_formulation')
        cmdows_problem_formulation.add('mdaoArchitecture', graph_problem_formulation.get('mdao_architecture'))
        cmdows_problem_formulation.add('convergerType', graph_problem_formulation.get('convergence_type'))
        cmdows_executable_blocks_order = cmdows_problem_formulation.add('executableBlocksOrder')
        for index, item in enumerate(graph_problem_formulation.get('function_order')):
            # Create problemDefinition/problemFormulation/executableBlocksOrder/executableBlock
            cmdows_executable_blocks_order.add('executableBlock', item, attrib={'position': str(index + 1)})
        cmdows_problem_formulation.add('allowUnconvergedCouplings',
                                       str(graph_problem_formulation.get('allow_unconverged_couplings')).lower())

        # Create problemDefinition/problemFormulation/doeSettings
        graph_settings = graph_problem_formulation.get('doe_settings')
        if graph_settings is not None:
            cmdows_settings = cmdows_problem_formulation.add('doeSettings')
            cmdows_settings.add('doeMethod', graph_settings.get('doe_method'))
            cmdows_settings.add('doeSeeds', graph_settings.get('doe_seeds'))
            cmdows_settings.add('doeRuns', graph_settings.get('doe_runs'))

        # Create problemDefinition/problemRoles
        cmdows_problem_roles = cmdows_problem_definition.add('problemRoles')
        # Create problemDefinition/problemRoles/parameters
        cmdows_parameters = cmdows_problem_roles.add('parameters')
        # Create problemDefinition/problemRoles/parameters/...
        for cmdows_parameterIndex, cmdows_parameterDef in enumerate(self.CMDOWS_ROLES_DEF):
            cmdows_parameter = cmdows_parameters.add(cmdows_parameterDef[0] + 's')
            graph_attr_cond = ['problem_role', '==', self.PROBLEM_ROLES_VARS[cmdows_parameterIndex]]
            graph_parameter = self.find_all_nodes(category='variable', attr_cond=graph_attr_cond)
            for graph_problem_role in graph_parameter:
                cmdows_problem_role = cmdows_parameter.add(cmdows_parameterDef[0])
                cmdows_problem_role.set('uID',
                                        self.PROBLEM_ROLES_VAR_SUFFIXES[cmdows_parameterIndex] +
                                        str(graph_problem_role))
                cmdows_problem_role.add('parameterUID', graph_problem_role)
                for cmdows_problem_role_attr in cmdows_parameterDef[1]:
                    if cmdows_problem_role_attr == 'samples':
                        # Create problemDefinition/problemRoles/parameters/designVariables/designVariable/samples
                        cmdows_samples = cmdows_problem_role.add('samples')
                        if self.node[graph_problem_role].get(cmdows_problem_role_attr) is not None:
                            for idx, itm in enumerate(self.node[graph_problem_role].get(cmdows_problem_role_attr)):
                                cmdows_samples.add('sample', itm, attrib={'position': str(idx + 1)})
                    else:
                        cmdows_problem_role.add(self.CMDOWS_ATTRIBUTE_DICT[cmdows_problem_role_attr],
                                                self.node[graph_problem_role].get(cmdows_problem_role_attr),
                                                camel_case_conversion=True)

        # Create problemDefinition/problemRoles/executableBlocks
        cmdows_executable_blocks = cmdows_problem_roles.add('executableBlocks')
        graph_executable_blocks = self.graph['problem_formulation']['function_ordering']
        # Create problemDefinition/problemRoles/executableBlocks/...
        for executable_block in self.FUNCTION_ROLES:
            if graph_executable_blocks.get(executable_block) is not None:
                if len(graph_executable_blocks.get(executable_block)) != 0:
                    cmdows_key = cmdows_executable_blocks.add(make_camel_case(executable_block) + 'Blocks')
                    for graph_block in graph_executable_blocks.get(executable_block):
                        cmdows_key.add(make_camel_case(executable_block) + 'Block', graph_block)

        return cmdows_problem_definition

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                             LOAD METHODS                                                         #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _load_cmdows_problem_def(self, cmdows):

        graph_problem_form = {}

        cmdows_problem_formulation = cmdows.find('problemDefinition/problemFormulation')
        if cmdows_problem_formulation is not None:
            graph_problem_form['mdao_architecture'] = cmdows_problem_formulation.findtext('mdaoArchitecture')
            graph_problem_form['convergence_type'] = cmdows_problem_formulation.findtext('convergerType')
            cmdows_executable_blocks = cmdows_problem_formulation.find('executableBlocksOrder').findall(
                'executableBlock')
            cmdows_executable_blocks_order = [None] * len(list(cmdows_executable_blocks))
            for cmdows_executable_block in cmdows_executable_blocks:
                cmdows_executable_blocks_order[int(cmdows_executable_block.get('position')
                                                   ) - 1] = cmdows_executable_block.text
            graph_problem_form['function_order'] = cmdows_executable_blocks_order
            graph_problem_form['allow_unconverged_couplings'] = bool(distutils.util.strtobool(
                cmdows_problem_formulation.findtext('allowUnconvergedCouplings')))
            graph_problem_form['doe_settings'] = {}
            cmdows_doe_settings = cmdows_problem_formulation.find('doeSettings')
            if cmdows_doe_settings is not None:
                for cmdows_doe_setting in list(cmdows_doe_settings):
                    graph_problem_form['doe_settings'][unmake_camel_case(cmdows_doe_setting.tag
                                                                         )] = cmdows_doe_setting.text

        cmdows_problem_roles = cmdows.find('problemDefinition/problemRoles')
        if cmdows_problem_roles is not None:
            graph_problem_form['function_ordering'] = {}
            cmdows_executable_blocks = cmdows_problem_roles.find('executableBlocks')
            for role in self.FUNCTION_ROLES:
                cmdows_blocks = cmdows_executable_blocks.find(make_camel_case(role) + 'Blocks')
                if cmdows_blocks is None:
                    arr = list()
                else:
                    arr = list()
                    for cmdows_block in list(cmdows_blocks):
                        if self.node.get(cmdows_block.text) is None:
                            # Add node if it does not exist yet
                            self.add_node(cmdows_block.text, category='function')
                        self.node[cmdows_block.text]['problem_role'] = role
                        arr.append(cmdows_block.text)
                graph_problem_form['function_ordering'][role] = arr

            variable_types = [make_plural(role[0]) for role in self.CMDOWS_ROLES_DEF]
            for variable_type in variable_types:
                cmdows_variables = cmdows_problem_roles.find('parameters/' + variable_type)
                if cmdows_variables is not None:
                    for cmdows_variable in list(cmdows_variables):
                        cmdows_parameter_uid = cmdows_variable.findtext('parameterUID')
                        cmdows_suffix = '__' + re.findall(r'(?<=__).*?(?=__)', cmdows_variable.get('uID'))[0] + '__'
                        # Add problem role
                        try:
                            self.node[cmdows_parameter_uid]['problem_role'] = self.CMDOWS_ROLES_DICT_INV[cmdows_suffix]
                            # TODO: Find a more elegant way to handle samples and parameterUID
                            for attribute in cmdows_variable.getchildren():
                                if attribute.tag == 'samples':
                                    cmdows_samples = attribute.findall('sample')
                                    cmdows_sample_data = [None] * len(list(cmdows_samples))
                                    for cmdows_sample in cmdows_samples:
                                        cmdows_sample_data[int(cmdows_sample.get('position')) - 1] = float(cmdows_sample.text)
                                    self.node[cmdows_parameter_uid]['samples'] = cmdows_sample_data
                                    cmdows_variable.remove(attribute)
                            self.node[cmdows_parameter_uid].update(cmdows.finddict(cmdows_variable, camel_case_conversion=True))
                            del self.node[cmdows_parameter_uid]['parameter_u_i_d']
                        except KeyError:
                            pass

        self.graph['problem_formulation'] = graph_problem_form


class RepositoryConnectivityGraph(DataGraph):

    PATHS_LIMIT = 1e4    # limit check for select_function_combination_from method
    WARNING_LIMIT = 3e6  # limit for _get_path_combinations method

    def __init__(self, *args, **kwargs):
        super(RepositoryConnectivityGraph, self).__init__(*args, **kwargs)

    def cleancopy(self):
        """Method to make a clean copy of a graph.

        This method can be used to avoid deep-copy problems in graph manipulation algorithms.
        The graph class is kept.

        :return: clean-copy of the graph
        :rtype: RepositoryConnectivityGraph
        """

        return RepositoryConnectivityGraph(self)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            CREATE METHODS                                                        #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _create_cmdows_problem_def(self):

        # Create problemDefinition
        cmdows_problem_definition = Element('problemDefinition')

        return cmdows_problem_definition

    # -----------------------------------------------------------------------------------------------------------------#
    #                                          GRAPH SPECIFIC METHODS                                                  #
    # -----------------------------------------------------------------------------------------------------------------#

    def get_function_paths_by_objective(self, *args, **kwargs):
        """This function takes an arbitrary amount of objective nodes as graph sinks and returns all path combinations
        of tools.

        If no arguments are given, user is prompted to select objectives from the graph.

        The tool combinations are found using the function itertools.product() and can lead to significant computation
        times for large graphs. If this is the case, the user is prompted whether to continue or not.

        A variety of filters can be applied to the search of possible tools combinations, some of which reduce the
        computation time.

        kwargs:
        obj_vars_covered - ensures that all objective variables are used in tool configurations
        ignore_funcs - ignores functions for the config
        source - source node; if provided, must be in config

        :param args: arbitrary amount of objective nodes
        :param kwargs: filter options to limit possible path combinations
        :return: all possible FPG path combinations for the provided objective nodes
        """

        # TODO: Add filters
        # Filters:
        # include_functions - returned path combinations must include the indicated functions
        # exclude_functions - returned path combinations must exclude the indicated functions
        # min_funcs - only returns paths that have a minimum amount if functions
        # max_funcs - only returns paths that have a maximum amount of functions
        # obj_vars_covered - only returns paths where ALL objective variables are covered

        # make copy of self
        graph = copy.deepcopy(self)

        # get and check keyword arguments
        obj_vars_covered = kwargs.get('objective_variables_covered', False)  # TODO: Implement this option
        assert isinstance(obj_vars_covered, bool)

        ignore_funcs = None
        if "ignore_funcs" in kwargs:
            ignore_funcs = kwargs["ignore_funcs"]
            for func in ignore_funcs:
                assert func in self, "Function node {} must be present in graph.".format(func)

        # source = None
        # if "source" in kwargs:
        #    source = kwargs["source"]
        #    assert graph.node_is_function(source), "Source node must be a function."

        min_funcs = None
        if "min_funcs" in kwargs:
            min_funcs = kwargs["min_funcs"]
            assert isinstance(min_funcs, int)

        max_funcs = float("inf")
        if "max_funcs" in kwargs:
            max_funcs = kwargs["max_funcs"]
            assert isinstance(max_funcs, int)

        # get all function nodes in graph
        # func_nodes = graph.get_function_nodes()

        # [step 1] check if function nodes provided
        if args:
            objs = list(args)
            for arg in objs:
                assert graph.node_is_function(arg), "Provided Objective must be function."

        else:  # if not provided, ask user to select
            objs = graph.select_objectives_from_graph()

        # intermediate check that OBJ function node given
        assert objs, "No valid Objective Functions provided."
        logger.info('Function configurations are considered for objective(s): [{}]'.format(
            ', '.join(str(x) for x in objs)))

        # [Step 2]: Get OBJ function variables in graph
        obj_variables = []
        for objFunc in objs:
            for u, v in graph.in_edges_iter(objFunc):
                obj_variables.append(u)

        # [Step 3]: Get function graph (remove all variable nodes and replace them with corresponding edges)
        if obj_vars_covered:
            # if obj_vars_covered, objective vars will be present in paths; easy to check their presence
            function_graph = graph.get_function_graph(keep_objective_variables=True)
        else:
            function_graph = graph.get_function_graph()

        # [Step 4]: get all (simple) paths to sinks
        all_simple_paths = set()  # making sure that no duplicate paths in list
        for sink in objs:
            anc_nodes = nx.ancestors(function_graph, sink)
            for anc in anc_nodes:
                if function_graph.node_is_function(anc):  # do not take objVars into account

                    # add every path to sink as frozenset
                    for path in nx.all_simple_paths(function_graph, anc, sink):  # TODO: Test for multiple sinks!
                        all_simple_paths.add(frozenset(path))

        # [Step 5]: Apply (some) filters
        # TODO: Apply some filters here

        # [Step 6]: group paths according into subsets
        path_subsets = self._group_elements_by_subset(*all_simple_paths)

        # [Step 7]: Get all combinations between all feedback tool combinations
        subsets_list = [subset for _, subset in path_subsets.iteritems()]

        # remove all paths that have ignore-functions
        if ignore_funcs:
            for subset in subsets_list:
                remove = []
                for path in subset:
                    if not ignore_funcs.isdisjoint(path):
                        remove.append(path)
                for p in remove:
                    subset.remove(p)

        all_fpg_paths = function_graph.get_path_combinations(*subsets_list, min_funcs=min_funcs, max_funcs=max_funcs)

        return all_fpg_paths

    def get_path_combinations(self, *args, **kwargs):
        """This function takes lists of subsets and generates all possible combinations between them.

        This is done by using the itertools.product() function. If the amount of expected evaluations exceeds a pre-set
        minimum, the user will be asked if to continue or not; because the process can take a long time and use up many
        resources.

        Optional arguments:
        min_func: minimum amount of functions in each configuration
        max_func: maximum amount of functions in each configuration

        :param args: lists of subsets that will be used to find configurations
        :type args: list
        :return: set of all unique path combinations
        """

        # get list of subsets
        subsets = list(args)

        # kwargs check
        # min_funcs = None
        # if "min_funcs" in kwargs:
        #     min_funcs = kwargs["min_funcs"]
        #     assert isinstance(min_funcs, int)

        max_funcs = kwargs.get('max_funcs', float("inf"))

        # append empty string to each list (to get ALL combinations; check itertools.product()) and count evaluations
        count = 1
        for subset in subsets:
            subset.append('')
            count *= len(subset)
        count -= 1

        # If many combinations are evaluated, warn user and ask if to continue
        if count > self.WARNING_LIMIT:
            logger.warning('Only ' + str(self.WARNING_LIMIT) + ' tool combinations can be evaluated with the current ' +
                           ' settings. However, ' + str(count) + ' evaluations are now selected. You can decrease ' +
                           'this number by applying filters. You could also increase the WARNING_LIMIT but be aware ' +
                           'that the process can take a considerable amount of time and resources then.')
            return list()

        # get all tool combinations using subsets
        all_path_combinations = set()

        for comb in itertools.product(*subsets):
            # combine separate lists into one for each combo
            # clean_comb = frozenset(itertools.chain.from_iterable(comb))
            clean_comb = frozenset().union(*comb)
            if len(clean_comb) > max_funcs or len(clean_comb) > max_funcs:
                continue
            # add to list if combo is not empty and does not yet exist in list
            if clean_comb and clean_comb not in all_path_combinations:
                all_path_combinations.add(clean_comb)

        return all_path_combinations

    def _get_feedback_paths(self, path, functions_only=True):
        # TODO: Add docstring

        # functions_only only passes on argument, not used in this function
        assert isinstance(functions_only, bool)

        # get feedback nodes if exist in path
        # empty strings in tpls are necessary for proper functioning
        feedback = self._get_feedback_nodes(path, functions_only=functions_only)

        # get path combinations in case feedback loops exist in path
        feedback_combis = []
        for prod in itertools.product([tuple(path)], *feedback):
            # remove all empty products
            removed_empty = (x for x in prod if x)  # remove empty strings
            # remove brackets created by product; create frozenset to make object immutable
            removed_brackets = frozenset(itertools.chain.from_iterable(removed_empty))

            # if combination is not empty and does not already exist in list, add to list
            if removed_brackets not in feedback_combis and removed_brackets:
                feedback_combis.append(removed_brackets)

        return feedback_combis

    def _get_feedback_nodes(self, main_path, functions_only=True):
        # TODO: Add docstring

        assert isinstance(functions_only, bool)
        feed_back = []  # contains feed_back nodes; each feed_back loop is in a separate list

        for main_path_idx, main_path_node in enumerate(main_path):
            search_loop = []
            start_index = -1

            if functions_only:
                if not self.node_is_function(main_path_node):
                    continue

            # iterate through edges recursively and add feed_back loops if they exist
            self._iter_out_edges(main_path_idx, main_path, main_path_node, start_index, search_loop, feed_back,
                                 functions_only)

        return feed_back

    def _iter_out_edges(self, main_path_idx, main_path, node, search_index, search_loop, feed_back,
                        functions_only=True):
        # TODO: Add docstring

        out_edges = self.out_edges(node)
        search_index += 1

        for edge in out_edges:
            if functions_only:
                if not self.node_is_function(edge[1]):
                    continue
            if edge[1] in search_loop:
                continue
            search_loop.insert(search_index, edge[1])
            if edge[1] in main_path and main_path.index(edge[1]) <= main_path_idx:
                feed_back.append(("", search_loop[:search_index]))
            elif edge[1] not in main_path:
                self._iter_out_edges(main_path_idx, main_path, edge[1], search_index, search_loop, feed_back,
                                     functions_only)

        return

    # noinspection PyMethodMayBeStatic
    def _group_elements_by_subset(self, *args):
        """This function takes arguments of type set/frozenset and groups them by subset.

        All elements that are subsets of another element are grouped together and returned in a dict with the longest
        superset as keywords.

        Example:
        >> list = [set([1]),set([1,2]),set([3]),set([0,1,2])]
        >> sub_sets = graph._group_elements_by_subset(*list)
        >> sub_sets
        >> {set([0,1,2]): [set([1]), set([1,2]),set([0,1,2])], set([3]):[set([3])]}

        :param args: arbitrary argument
        :type args: set, frozenset
        :return: dict with grouped arguments by longest subset in group
        :rtype: dict
        """

        for arg in args:
            assert isinstance(arg, (set, frozenset))
        set_list = list(args)

        sub_sets = {}
        skip = []
        for i, path in enumerate(set_list):
            if path in skip:
                continue

            set_found = False
            for comp in set_list[i + 1:]:
                if comp in skip:
                    continue

                if path == comp:
                    skip.append(comp)
                    continue

                if path.issubset(comp):
                    set_found = True

                    if comp not in sub_sets:
                        sub_sets[comp] = [comp]

                    if path in sub_sets:
                        sub_sets[comp] += sub_sets[path]
                        sub_sets.pop(path, None)
                    else:
                        sub_sets[comp].append(path)

                    skip.append(path)
                    break

                elif path.issuperset(comp):
                    set_found = True
                    skip.append(comp)

                    if path not in sub_sets:
                        sub_sets[path] = [path]
                    sub_sets[path].append(comp)

                    if comp in sub_sets:
                        sub_sets[path] += sub_sets[comp]
                        sub_sets.pop(comp, None)
                    continue

            if not set_found and path not in sub_sets:
                sub_sets[path] = []
                sub_sets[path].append(path)

        return sub_sets

    def select_function_combination_from(self, *args, **kwargs):
        """This function takes all provided workflow configurations and lists them according to their characteristics.

        The user can then choose the workflow configuration from the list.
        A warning is given to the user if the amount of total configurations exceeds n = 1e4.
        Print limit is set to [0-20] by default.
        sort_by must be one of ["couplings", "system_inputs", "edges", "nodes"].
        """

        # make sure arguments provided
        assert args, "At least one argument must be provided."

        # check number of arguments; prompt user to continue or not
        if len(args) > self.PATHS_LIMIT:
            msg = "More than {} workflow configurations provided; this could take a lot of time to analyze. Continue?"
            usr_sel = prompting.user_prompt_yes_no(message=msg)
            if not usr_sel:
                print "Combination selection cancelled."
                return

        # check if all arguments are non-string iterables (list, tuple, set, frozenset,...)
        assert all([hasattr(arg, '__iter__') for arg in args]), "All arguments must be non-string iterables."

        # check KWARGS HERE
        print_combos = True
        if "print_combos" in kwargs:
            print_combos = kwargs["print_combos"]
            assert isinstance(print_combos, bool)

        # if no limit given, limit for displaying combos is set to 10
        n_limit = 21
        if "n_limit" in kwargs:
            n_limit = kwargs["n_limit"]
            assert isinstance(n_limit, int)
            assert n_limit > 0, "Argument must be positive."

        # if no sort_by argument given, it sorts combos by "holes"
        sort_by = "functions"
        if "sort_by" in kwargs:
            sort_by = kwargs["sort_by"]
            assert isinstance(sort_by, basestring)
            assert sort_by in self.GRAPH_PROPERTIES, "Argument must be in self.GRAPH_PROPERTIES."

        sort_by_ascending = False
        if "sort_by_ascending" in kwargs:
            sort_by_ascending = kwargs["sort_by_ascending"]
            assert isinstance(sort_by_ascending, bool)

        plot_combos = True
        if "plot_combos" in kwargs:
            plot_combos = kwargs["plot_combos"]
            # TODO: Add assert for type of plot, plot variables etc

        # ------------------------------------------------------------- #

        # iterate through arguments and analyze their graphs
        graph_analysis = {}
        for arg in args:
            # TODO: Implement an option to get graph data from a db instead of analyzing each subgraph (if available)
            # TODO: This saves time in large graphs!

            # initiate dict to save subgraph data to
            graph_analysis[arg] = {}

            # get subgraph in order to get fast analysis
            sub_graph = self.get_subgraph_by_function_nodes(*arg)

            # subgraph analysis
            graph_analysis[arg] = sub_graph.get_graph_properties()

        # sort configuration list
        combo_list = list(graph_analysis.items())
        sorted_combos = sorted(combo_list, key=lambda x: x[1][sort_by], reverse=not sort_by_ascending)

        if plot_combos:

            # plot
            plt_x, plt_y, annotes = [], [], []
            for k, v in graph_analysis.iteritems():
                plt_y.append(v["system_inputs"])
                plt_x.append(v["functions"])
                annotes.append(str(list(k)))

            # TODO: Automate the plotting of graphs (data, labels, etc)!
            fig, ax = plt.subplots()
            ax.scatter(plt_x, plt_y)
            af = AnnoteFinder(plt_x, plt_y, annotes, ax=ax)
            fig.canvas.mpl_connect('button_press_event', af)
            plt.xlabel('Tools')
            plt.ylabel('System Inputs')
            plt.show()

        # print configs
        if print_combos:
            print_list = []
            for combo, properties in sorted_combos:
                prop_list = [properties[prop] for prop in self.GRAPH_PROPERTIES]
                prop_list.append(list(combo))
                print_list.append(prop_list)

            hdr = self.GRAPH_PROPERTIES + ["Configuration"]
            msg = "The following tool configurations were found in the graph:"
            printing.print_in_table(print_list[:n_limit], message=msg, headers=hdr, print_indeces=True)

        # select combo for FPG
        # TODO: finish!
        # sel_mssg = "Please select a tool combination from the list above:"
        sel_list = [sorted_combo[0] for sorted_combo in sorted_combos[:n_limit]]
        # user_sel= PRO.user_prompt_select_options(*sel_list, message=sel_mssg, allow_multi=False, allow_empty=False)
        user_sel = [sel_list[0]]

        return next(iter(user_sel))

    def get_fpg_by_function_nodes(self, *args):
        """This function creates a new (FPG)-graph based on the selected function nodes.

        :return: new fpg graph
        :rtype: FundamentalProblemGraph
        """

        # TODO: Assert that nodes are function nodes

        # get subgraph from function nodes
        sub_graph = self.get_subgraph_by_function_nodes(*args)

        # create FPG from sub-graph
        fpg = nx.compose(FundamentalProblemGraph(), sub_graph)
        # TODO: Make sure that the name of the graph is changed!

        return fpg

    def get_fpg_based_on_sinks(self, list_of_sinks, name='FPG'):
        """Function to get the a Fundamental Problem Graph based on a list of sinks/required output variables.

        :param list_of_sinks: list with strings that specify the desired output
        :type list_of_sinks: list
        :param name: name of the graph to be generated
        :type name: str
        :return: Fundamental Problem Graph object
        :rtype: FundamentalProblemGraph
        """

        fpg = FundamentalProblemGraph(sinks=list_of_sinks, name=name)
        for sink in list_of_sinks:
            ancestors = nx.ancestors(self, sink)
            ancestors.add(sink)
            fpg_sink = self.subgraph(ancestors)
            fpg = nx.compose(fpg, fpg_sink)

        return fpg

    def get_fpg_based_on_list_functions(self, list_of_functions, name='FPG'):
        """Function to get a Fundamental Problem Graph based on a list of functions.

        :param list_of_functions: list with strings that specify the desired functions
        :type list_of_functions: list
        :param name: name of the graph to be generated
        :type name: str
        :return: Fundamental Problem Graph object
        :rtype: FundamentalProblemGraph
        """

        # make empty copy
        fpg = FundamentalProblemGraph(self, based_on_functions=list_of_functions, kb_path=self.graph['kb_path'],
                                      name=name)

        # build fpg by first determining the required nodes
        required_nodes = set(list_of_functions)
        for function in list_of_functions:
            function_out_edges = fpg.out_edges(function)
            function_in_edges = fpg.in_edges(function)
            for edge in function_out_edges:
                required_nodes.add(edge[1])
            for edge in function_in_edges:
                required_nodes.add(edge[0])

        for node, data in fpg.nodes_iter(data=True):
            if node not in required_nodes:
                fpg.remove_node(node)

        return fpg

    def get_fpg_based_on_function_nodes(self, *args, **kwargs):
        """Function to get the Fundamental Problem Graph based on a list of (or a single) function.

        :param args: node names of functions of interest
        :type args: str
        :param kwargs: name: name of the graph to be generated
        :type kwargs: name: str
        :return: Fundamental Problem Graph object
        :rtype: FundamentalProblemGraph
        """

        # Input assertions
        name = kwargs.get('name', 'FPG')
        assert isinstance('name', str)
        list_of_functions = list(args)
        for function in list_of_functions:
            assert function in self.nodes(), 'Defined function node ' + str(function) + ' does not exist in the graph.'

        # make empty copy
        fpg = FundamentalProblemGraph(self, based_on_functions=list_of_functions, name=name)

        # build FPG by first determining the required nodes
        required_nodes = set(list_of_functions)
        for function in list_of_functions:
            function_out_edges = fpg.out_edges(function)
            function_in_edges = fpg.in_edges(function)
            for edge in function_out_edges:
                required_nodes.add(edge[1])
            for edge in function_in_edges:
                required_nodes.add(edge[0])

        for node, data in fpg.nodes_iter(data=True):
            if node not in required_nodes:
                fpg.remove_node(node)

        return fpg


class FundamentalProblemGraph(DataGraph, KeChainMixin):

    OPTIONS_FUNCTION_ORDER_METHOD = ['manual', 'minimum feedback']

    def __init__(self, *args, **kwargs):
        super(FundamentalProblemGraph, self).__init__(*args, **kwargs)

    def cleancopy(self):
        """Method to make a clean copy of a graph.

        This method can be used to avoid deep-copy problems in graph manipulation algorithms.
        The graph class is kept.

        :return: clean-copy of the graph
        :rtype: FundamentalProblemGraph
        """

        return FundamentalProblemGraph(self)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            CHECKING METHODS                                                      #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _check_category_a(self):
        """Extended method to perform a category A check on the graph.

        :return: result of the check and index
        :rtype: bool, int
        """

        # Set check
        category_check, i = super(FundamentalProblemGraph, self)._check_category_a()

        # Get nodes
        func_nodes = self.find_all_nodes(category='function')
        var_nodes = self.find_all_nodes(category='variable')
        out_nodes = self.find_all_nodes(subcategory='all outputs')

        # Get information
        n_nodes = self.number_of_nodes()
        n_functions = len(func_nodes)
        n_variables = len(var_nodes)

        # Checks on nodes
        category_check, i = check(n_nodes != (n_functions+n_variables),
                                  'The number of total nodes does not match number of function and variable nodes.',
                                  status=category_check,
                                  category='A',
                                  i=i)
        for out_node in out_nodes:
            category_check, i_not = check('problem_role' not in self.node[out_node],
                                          'The attribute problem_role is missing on the output node %s.'
                                          % str(out_node),
                                          status=category_check,
                                          category='A',
                                          i=i)
        i += 1
        for func_node in func_nodes:
            category_check, i_not = check('problem_role' not in self.node[func_node],
                                          'The attribute problem_role is missing on the function node %s.'
                                          % str(func_node),
                                          status=category_check,
                                          category='A',
                                          i=i)
        i += 1

        # Return
        return category_check, i

    def _check_category_b(self):
        """Extended method to perform a category B check on the graph.

        :return: result of the check and index
        :rtype: bool, int
        """

        # Set check
        category_check, i = super(FundamentalProblemGraph, self)._check_category_b()

        # Get nodes
        func_nodes = self.find_all_nodes(category='function')

        # Checks
        category_check, i = check('problem_formulation' not in self.graph,
                                  'The problem formulation attribute is missing on the graph.',
                                  status=category_check,
                                  category='B',
                                  i=i)
        if category_check:
            category_check, i = check('mdao_architecture' not in self.graph['problem_formulation'],
                                      'The mdao_architecture attribute is missing in the problem formulation.',
                                      status=category_check,
                                      category='B',
                                      i=i)
            if category_check:
                category_check, i = check(self.graph['problem_formulation']['mdao_architecture'] not in
                                          self.OPTIONS_ARCHITECTURES,
                                          'Invalid mdao_architecture attribute in the problem formulation.',
                                          status=category_check,
                                          category='B',
                                          i=i)
            category_check, i = check('convergence_type' not in self.graph['problem_formulation'],
                                      'The convergence_type attribute is missing in the problem formulation.',
                                      status=category_check,
                                      category='B',
                                      i=i)
            if category_check:
                category_check, i = check(self.graph['problem_formulation']['convergence_type'] not in
                                          self.OPTIONS_CONVERGERS,
                                          'Invalid convergence_type %s in the problem formulation.'
                                          % self.graph['problem_formulation']['convergence_type'],
                                          status=category_check,
                                          category='B',
                                          i=i)
            category_check, i = check('function_order' not in self.graph['problem_formulation'],
                                      'The function_order attribute is missing in the problem formulation.',
                                      status=category_check,
                                      category='B',
                                      i=i)
            if category_check:
                func_order = self.graph['problem_formulation']['function_order']
                category_check, i = check(len(func_order) != len(func_nodes),
                                          'There is a mismatch between the FPG functions and the given function_order, '
                                          + 'namely: %s.' % set(func_nodes).symmetric_difference(set(func_order)),
                                          status=category_check,
                                          category='B',
                                          i=i)
            category_check, i = check('function_ordering' not in self.graph['problem_formulation'],
                                      'The function_ordering attribute is missing in the problem formulation.',
                                      status=category_check,
                                      category='B',
                                      i=i)
            if 'allow_unconverged_couplings' in self.graph['problem_formulation']:
                allow_unconverged_couplings = self.graph['problem_formulation']['allow_unconverged_couplings']
                category_check, i = check(not isinstance(allow_unconverged_couplings, bool),
                                          'The setting allow_unconverged_couplings should be of type boolean.',
                                          status=category_check,
                                          category='B',
                                          i=i)
            if self.graph['problem_formulation']['mdao_architecture'] in get_list_entries(self.OPTIONS_ARCHITECTURES, 5,
                                                                                          6):  # DOE
                category_check, i = check('doe_settings' not in self.graph['problem_formulation'],
                                          'The doe_settings attribute is missing in the problem formulation.',
                                          status=category_check,
                                          category='B',
                                          i=i)
                if category_check:
                    category_check, i = check('doe_method' not in self.graph['problem_formulation']['doe_settings'],
                                              'The doe_method attribute is missing in the doe_settings.',
                                              status=category_check,
                                              category='B',
                                              i=i)
                    if category_check:
                        doe_method = self.graph['problem_formulation']['doe_settings']['doe_method']
                        category_check, i = check(self.graph['problem_formulation']['doe_settings']['doe_method'] not
                                                  in self.OPTIONS_DOE_METHODS,
                                                  'Invalid doe_method (%s) specified in the doe_settings.' % doe_method,
                                                  status=category_check,
                                                  category='B',
                                                  i=i)
                        if doe_method in get_list_entries(self.OPTIONS_DOE_METHODS, 0, 1, 2):  # FF, LHC, Monte Carlo
                            category_check, i = check('doe_runs' not in
                                                      self.graph['problem_formulation']['doe_settings'],
                                                      'The doe_runs attribute is missing in the doe_settings.',
                                                      status=category_check,
                                                      category='B',
                                                      i=i)
                            if category_check:
                                test = not isinstance(self.graph['problem_formulation']['doe_settings']['doe_runs'],
                                                      int) or \
                                       self.graph['problem_formulation']['doe_settings']['doe_runs'] < 0
                                category_check, i = check(test,
                                                          'Invalid doe_runs (%s) specified in the doe_settings.' %
                                                          self.graph['problem_formulation']['doe_settings']['doe_runs'],
                                                          status=category_check,
                                                          category='B',
                                                          i=i)
                        if doe_method in get_list_entries(self.OPTIONS_DOE_METHODS, 1, 2):  # LHC, Monte Carlo
                            category_check, i = check('doe_seed' not in
                                                      self.graph['problem_formulation']['doe_settings'],
                                                      'The doe_seed attribute is missing in the doe_settings.',
                                                      status=category_check,
                                                      category='B',
                                                      i=i)
                            if category_check:
                                test = not isinstance(self.graph['problem_formulation']['doe_settings']['doe_seed'],
                                                      int) or \
                                       self.graph['problem_formulation']['doe_settings']['doe_seed'] < 0
                                category_check, i = check(test,
                                                          'Invalid doe_seed (%s) specified in the doe_settings.' %
                                                          self.graph['problem_formulation']['doe_settings']['doe_seed'],
                                                          status=category_check,
                                                          category='B',
                                                          i=i)

        # Return
        return category_check, i

    def _check_category_c(self):
        """Extended method to perform a category C check on the graph.

        :return: result of the check and index
        :rtype: bool, int
        """

        # Set check
        category_check, i = super(FundamentalProblemGraph, self)._check_category_c()

        # Get information
        mdao_arch = self.graph['problem_formulation']['mdao_architecture']
        conv_type = self.graph['problem_formulation']['convergence_type']
        allow_unconverged_couplings = self.graph['problem_formulation']['allow_unconverged_couplings']

        # Check if architecture and convergence_type match
        # -> match for converged-MDA, MDF, converged-DOE
        if mdao_arch in [self.OPTIONS_ARCHITECTURES[1], self.OPTIONS_ARCHITECTURES[3], self.OPTIONS_ARCHITECTURES[6]]:
            category_check, i = check(conv_type not in self.OPTIONS_CONVERGERS[:2],
                                      'Convergence type %s does not match with architecture %s.'
                                      % (conv_type, mdao_arch),
                                      status=category_check,
                                      category='C',
                                      i=i)
        # -> match IDF
        if mdao_arch in [self.OPTIONS_ARCHITECTURES[2]]:
            category_check, i = check(conv_type is not self.OPTIONS_CONVERGERS[2],
                                      'Convergence type %s does not match with architecture %s.'
                                      % (conv_type, mdao_arch),
                                      status=category_check,
                                      category='C',
                                      i=i)
        # -> match for unconverged-MDA, IDF, unconverged-OPT, unconverged-DOE
        # TODO: Sort out unconverged coupling mess
        # if mdao_arch in [self.OPTIONS_ARCHITECTURES[0], self.OPTIONS_ARCHITECTURES[4], self.OPTIONS_ARCHITECTURES[5]]:
        #     if allow_unconverged_couplings:
        #         category_check, i = check(conv_type is not self.OPTIONS_CONVERGERS[2],
        #                                   'Convergence type %s does not match with architecture %s. As unconverged '
        #                                   'couplings are allowed, the convergence method None has to be selected.'
        #                                   % (conv_type, mdao_arch),
        #                                   status=category_check,
        #                                   category='C',
        #                                   i=i)
        #     else:
        #         category_check, i = check(conv_type not in self.OPTIONS_CONVERGERS[:2],
        #                                   'Convergence type %s does not match with architecture %s. As unconverged '
        #                                   'couplings are not allowed, a convergence method has to be selected.'
        #                                   % (conv_type, mdao_arch),
        #                                   status=category_check,
        #                                   category='C',
        #                                   i=i)

        # For architectures using convergence, check whether this is necessary
        if category_check:
            coup_funcs = self.graph['problem_formulation']['function_ordering'][self.FUNCTION_ROLES[1]]
            if mdao_arch == self.OPTIONS_ARCHITECTURES[1]:  # converged-MDA
                category_check, i = check(not self.check_for_coupling(coup_funcs, only_feedback=True if
                                          conv_type == self.OPTIONS_CONVERGERS[1] else 0),
                                          'Inconsistent problem formulation, expected coupling missing. Architecture '
                                          'should be set to "unconverged-MDA".',
                                          status=category_check,
                                          category='C',
                                          i=i)
            if mdao_arch == self.OPTIONS_ARCHITECTURES[3]:  # MDF
                category_check, i = check(not self.check_for_coupling(coup_funcs, only_feedback=True if
                                          conv_type == self.OPTIONS_CONVERGERS[1] else 0),
                                          'Inconsistent problem formulation, expected coupling missing. Architecture '
                                          'should be set to "unconverged-OPT".',
                                          status=category_check,
                                          category='C',
                                          i=i)
            if mdao_arch == self.OPTIONS_ARCHITECTURES[2]:  # IDF
                category_check, i = check(not self.check_for_coupling(coup_funcs, only_feedback=False),
                                          'Inconsistent problem formulation, expected coupling missing. Architecture '
                                          'should be set to "unconverged-OPT".',
                                          status=category_check,
                                          category='C',
                                          i=i)
            if mdao_arch == self.OPTIONS_ARCHITECTURES[6]:  # converged-DOE
                category_check, i = check(not self.check_for_coupling(coup_funcs, only_feedback=True if
                                          conv_type == self.OPTIONS_CONVERGERS[1] else 0),
                                          'Inconsistent problem formulation, expected coupling missing. Architecture '
                                          'should be set to "unconverged-DOE".',
                                          status=category_check,
                                          category='C',
                                          i=i)

        # For architectures not using convergence, check whether this is allowed
        if category_check:
            coup_funcs = self.graph['problem_formulation']['function_ordering'][self.FUNCTION_ROLES[1]]
            # unconverged-MDA, unconverged-OPT, unconverged-DOE
            if mdao_arch in get_list_entries(self.OPTIONS_ARCHITECTURES, 0, 4, 5):
                if not allow_unconverged_couplings:
                    category_check, i = check(self.check_for_coupling(coup_funcs, only_feedback=True),
                                              'Inconsistent problem formulation, no feedback coupling was expected. '
                                              'Architecture should be set to something using convergence (e.g. MDF). '
                                              'Or setting allow_unconverged_couplings should be set to True.',
                                              status=category_check,
                                              category='C',
                                              i=i)
                if category_check and conv_type is not self.OPTIONS_CONVERGERS[2]:
                    category_check, i = check(not self.check_for_coupling(coup_funcs, only_feedback=True if
                                              conv_type == self.OPTIONS_CONVERGERS[1] else False),
                                              'Inconsistent problem formulation, expected coupling missing. '
                                              'Architecture should be unconverged variant with convergence type None.',
                                              status=category_check,
                                              category='C',
                                              i=i)

        # Check the feedforwardness of the pre-coupling functions
        if category_check:
            precoup_funcs = self.graph['problem_formulation']['function_ordering'][self.FUNCTION_ROLES[0]]
            category_check, i = check(self.check_for_coupling(precoup_funcs, only_feedback=True),
                                      'Pre-coupling functions contain feedback variables. '
                                      'Pre-coupling functions should be adjusted.',
                                      status=category_check,
                                      category='C',
                                      i=i)

        # Check whether the necessary variables have been marked with the problem_role attribute
        if category_check:
            if mdao_arch in self.OPTIONS_ARCHITECTURES[2:5]:  # IDF, MDF, unconverged-OPT
                des_var_nodes = self.find_all_nodes(attr_cond=['problem_role', '==', self.PROBLEM_ROLES_VARS[0]])
                category_check, i = check(len(des_var_nodes) == 0,
                                          'No design variables are specified. Use the problem_role attribute for this.',
                                          status=category_check,
                                          category='C',
                                          i=i)
                # Check the design variables connections
                for des_var_node in des_var_nodes:
                    des_var_sources = self.get_sources(des_var_node)
                    # noinspection PyUnboundLocalVariable
                    category_check, i_not = check(not set(des_var_sources).issubset(precoup_funcs),
                                                  'Design variable %s has a source after the pre-coupling functions. '
                                                  'Adjust design variables or function order to solve this.'
                                                  % des_var_node,
                                                  status=category_check,
                                                  category='C',
                                                  i=i)
                    category_check, i_not = check(self.out_degree(des_var_node) == 0,
                                                  'Design variable %s does not have any targets. Reconsider design '
                                                  'variable selection.' % des_var_node,
                                                  status=category_check,
                                                  category='C',
                                                  i=i+1)
                i += 2
                constraint_nodes = self.find_all_nodes(attr_cond=['problem_role', '==', self.PROBLEM_ROLES_VARS[2]])
                objective_node = self.find_all_nodes(attr_cond=['problem_role', '==', self.PROBLEM_ROLES_VARS[1]])
                category_check, i = check(len(objective_node) != 1,
                                          '%d objective variables are specified. Only one objective node is allowed. '
                                          'Use the problem_role attribute for this.' % len(objective_node),
                                          status=category_check,
                                          category='C',
                                          i=i)
                constraint_functions = list()
                for idx, node in enumerate(objective_node + constraint_nodes):
                    category_check, i_not = check(self.in_degree(node) != 1,
                                                  'Invalid in-degree of ' + str(self.in_degree(node)) +
                                                  ', while it should be 1 of node: ' + str(node),
                                                  status=category_check,
                                                  category='C',
                                                  i=i)
                    category_check, i_not = check(self.out_degree(node) != 0,
                                                  'Invalid out-degree of '+ str(self.out_degree(node))
                                                  + ', while it should be 0 of node: ' + str(node),
                                                  status=category_check,
                                                  category='C',
                                                  i=i+1)
                    if idx == 0:
                        objective_function = self.in_edges(node)[0][0]
                    elif not (self.in_edges(node)[0][0] in set(constraint_functions)):
                        constraint_functions.append(self.in_edges(node)[0][0])
                i += 2
                if category_check:
                    # Check that the objective function is unique (not also a constraint function)
                    # noinspection PyUnboundLocalVariable
                    category_check, i = check(objective_function in constraint_functions,
                                              'Objective function should be a separate function.',
                                              status=category_check,
                                              category='C',
                                              i=i)
                    optimizer_functions = [objective_function] + constraint_functions
                    # Check that all optimizer function are post-coupling functions for IDF and MDF
                    if mdao_arch in self.OPTIONS_ARCHITECTURES[2:4]:
                        func_cats = self.graph['problem_formulation']['function_ordering']
                        diff = set(optimizer_functions).difference(func_cats[self.FUNCTION_ROLES[2]])
                        coup_check = self.check_for_coupling(optimizer_functions, only_feedback=False)
                        category_check, i = check(diff,
                                                  'Not all optimizer functions are not post-coupling functions, '
                                                  'namely: %s' % diff,
                                                  status=category_check,
                                                  category='C',
                                                  i=i)
                        category_check, i = check(coup_check,
                                                  'The optimizer functions %s are not independent of each other.'
                                                  % optimizer_functions,
                                                  status=category_check,
                                                  category='C',
                                                  i=i)
            if mdao_arch in self.OPTIONS_ARCHITECTURES[:2] + self.OPTIONS_ARCHITECTURES[5:7]:
                # unc-MDA, con-MDA, unc-DOE, con-DOE
                # Check whether quantities of interest have been defined.
                qoi_nodes = self.find_all_nodes(attr_cond=['problem_role', '==', self.PROBLEM_ROLES_VARS[3]])
                category_check, i = check(len(qoi_nodes) == 0,
                                          'No quantities of interest are specified. Use the problem_role attribute for '
                                          'this.',
                                          status=category_check,
                                          category='C',
                                          i=i)
            if mdao_arch in self.OPTIONS_ARCHITECTURES[5:7]:  # unc-DOE, con-DOE
                des_var_nodes = self.find_all_nodes(attr_cond=['problem_role', '==', self.PROBLEM_ROLES_VARS[0]])
                category_check, i = check(len(des_var_nodes) == 0,
                                          'No design variables are specified. Use the problem_role attribute for this.',
                                          status=category_check,
                                          category='C',
                                          i=i)
                if category_check:
                    # If custom table, check the samples
                    if self.graph['problem_formulation']['doe_settings']['doe_method'] == self.OPTIONS_DOE_METHODS[3]:
                        all_samples = []
                        for des_var_node in des_var_nodes:
                            category_check, i_not = check('samples' not in self.node[des_var_node],
                                                          'The samples attributes is missing for design variable node'
                                                          ' %s.' % des_var_node,
                                                          status=category_check,
                                                          category='C',
                                                          i=i)
                            if category_check:
                                all_samples.append(self.node[des_var_node]['samples'])
                        i += 1
                        sample_lengths = [len(item) for item in all_samples]
                        # Check whether all samples have the same length
                        category_check, i = check(not sample_lengths.count(sample_lengths[0]) == len(sample_lengths),
                                                  'Not all given samples have the same length, this is mandatory.',
                                                  status=category_check,
                                                  category='C',
                                                  i=i)

        # Return
        return category_check, i

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                          GRAPH SPECIFIC METHODS                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #

    # TODO: mark_as_abc functions can be all combined in one function mark_as(abc, *kwargs)

    def mark_as_design_variable(self, nodes, lower_bounds=None, nominal_values=None, upper_bounds=None, samples=None):
        """Method to mark a list of nodes as design variable and add metadata.

        :param nodes: list of nodes present in the graph
        :type nodes: list
        :param lower_bounds: list of lower bound values
        :type lower_bounds: list
        :param nominal_values: list of nominal values
        :type nominal_values: list
        :param upper_bounds: list of upper bounds
        :type upper_bounds: list
        :param samples: nested list of kadmos values
        :type samples: list
        """

        # Input assertions
        assert isinstance(nodes, list)
        for node in nodes:
            assert self.has_node(node), 'Node %s is not present in the graph.' % node
        if lower_bounds:
            assert isinstance(lower_bounds, list)
            assert len(nodes) == len(lower_bounds), 'Amount of lower_bounds does not match the amount of nodes.'
        if nominal_values:
            assert isinstance(nominal_values, list)
            assert len(nodes) == len(nominal_values), 'Amount of nominal_values does not match the amount of nodes.'
        if upper_bounds:
            assert isinstance(upper_bounds, list)
            assert len(nodes) == len(upper_bounds), 'Amount of upper_bounds does not match the amount of nodes.'
        if samples:
            assert isinstance(samples, list)
            assert len(nodes) == len(samples), 'Amount of samples does not match the amount of nodes.'

        # Mark nodes
        for idx, node in enumerate(nodes):
            self.node[node]['problem_role'] = self.PROBLEM_ROLES_VARS[0]
            if lower_bounds:
                self.node[node]['lower_bound'] = lower_bounds[idx]
            if nominal_values:
                self.node[node]['nominal_value'] = nominal_values[idx]
            if upper_bounds:
                self.node[node]['upper_bound'] = upper_bounds[idx]
            if samples:
                self.node[node]['samples'] = samples[idx]

        return

    def mark_as_objective(self, node):
        """Method to mark a single node as objective.

        :param node: variable node
        :type node: basestring
        """

        # Input assertions
        assert self.has_node(node), 'Node %s is not present in the graph.' % node

        # Mark node
        self.node[node]['problem_role'] = self.PROBLEM_ROLES_VARS[1]

        return

    def mark_as_constraint(self, nodes, lower_bounds=None, upper_bounds=None):
        """Method to mark a list of nodes as constraint.

        :param nodes: list of nodes present in the graph
        :type nodes: list
        :param lower_bounds: list of lower bound values
        :type lower_bounds: list
        :param upper_bounds: list of upper bound values
        :type upper_bounds: list
        """

        # Input assertions
        assert isinstance(nodes, list)
        for node in nodes:
            assert self.has_node(node), 'Node %s is not present in the graph.' % node
        if lower_bounds:
            assert isinstance(lower_bounds, list)
            assert len(nodes) == len(lower_bounds), 'Amount of lower_bounds does not match the amount of nodes.'
        if upper_bounds:
            assert isinstance(upper_bounds, list)
            assert len(nodes) == len(upper_bounds), 'Amount of upper_bounds does not match the amount of nodes.'

        # Mark nodes
        for idx, node in enumerate(nodes):
            self.node[node]['problem_role'] = self.PROBLEM_ROLES_VARS[2]
            if lower_bounds:
                self.node[node]['lower_bound'] = lower_bounds[idx]
            if upper_bounds:
                self.node[node]['upper_bound'] = upper_bounds[idx]

        return

    def mark_as_qoi(self, nodes):
        """Function to mark a list of nodes as quantity of interest.

        :param nodes: list of nodes present in the graph
        :type nodes: list
        """

        # Input assertions
        assert isinstance(nodes, list)
        for node in nodes:
            assert self.has_node(node), 'Node %s is not present in the graph.' % node

        # Mark nodes
        for node in nodes:
            self.node[node]['problem_role'] = self.PROBLEM_ROLES_VARS[3]

        return

    def add_function_problem_roles(self, function_order_method='manual'):
        """
        Method to add the function problem roles (pre-coupled, coupled, post-coupled functions).

        :param function_order_method: algorithm to be used for the order in which the functions are executed.
        :type function_order_method: basestring
        """

        logger.info('Adding function problem roles...')

        # Determine and check function ordering method
        assert function_order_method in self.OPTIONS_FUNCTION_ORDER_METHOD
        if function_order_method == 'manual':
            assert 'function_order' in self.graph['problem_formulation'], 'function_order must be given as attribute.'
            function_order = self.graph['problem_formulation']['function_order']
        elif function_order_method == 'random':
            raise IOError('Random function ordering method not allowed for adding function problem roles.')

        # Determine the coupling matrix
        coupling_matrix = self.get_coupling_matrix()

        # Determine the different function roles
        # determine non-zero values in the coupling matrix
        non_zeros = np.transpose(np.nonzero(coupling_matrix))
        # remove upper triangle and diagonal elements
        lower_zeros = []
        left_ind = None
        low_ind = None
        for pos in non_zeros:
            if pos[1] < pos[0]:
                lower_zeros.append(pos)
                # Assess left-most feedback coupling node position -> first coupled function
                if not left_ind:
                    left_ind = pos[1]
                elif pos[1] < left_ind:
                    left_ind = pos[1]
                # Assess lowest feedback coupling node position -> last coupled function
                if not low_ind:
                    low_ind = pos[0]
                elif pos[0] > low_ind:
                    low_ind = pos[0]

        # Enrich graph function nodes and create dictionary with ordering results
        function_ordering = dict()
        function_ordering[self.FUNCTION_ROLES[0]] = list()
        function_ordering[self.FUNCTION_ROLES[1]] = list()
        function_ordering[self.FUNCTION_ROLES[2]] = list()
        if left_ind is not None:
            for i in range(0, left_ind):
                self.node[function_order[i]]['problem_role'] = self.FUNCTION_ROLES[0]
                function_ordering[self.FUNCTION_ROLES[0]].append(function_order[i])
            for i in range(left_ind, low_ind+1):
                self.node[function_order[i]]['problem_role'] = self.FUNCTION_ROLES[1]
                function_ordering[self.FUNCTION_ROLES[1]].append(function_order[i])
            if low_ind < len(function_order)-1:
                for i in range(low_ind+1, len(function_order)):
                    self.node[function_order[i]]['problem_role'] = self.FUNCTION_ROLES[2]
                    function_ordering[self.FUNCTION_ROLES[2]].append(function_order[i])
        else:
            # noinspection PyUnboundLocalVariable
            for function in function_order:
                self.node[function]['problem_role'] = self.FUNCTION_ROLES[0]
                function_ordering[self.FUNCTION_ROLES[0]].append(function)

        # Add function ordering to the graph as well
        self.graph['problem_formulation']['function_ordering'] = function_ordering

        logger.info('Successfully added function problem roles...')

        return

    def get_coupling_matrix(self, function_order_method='manual'):
        """Function to determine the role of the different functions in the FPG.

        :param function_order_method: algorithm to be used for the order in which the functions are executed.
        :type function_order_method: basestring
        :return: graph with enriched function node attributes and function problem role dictionary
        :rtype: FundamentalProblemGraph
        """

        # Make a copy of the graph, check it and remove all inputs and outputs
        graph = self.cleancopy()
        nodes_to_remove = list()
        # TODO: Consider using the check function
        assert not graph.find_all_nodes(subcategory='all problematic variables')
        nodes_to_remove.extend(graph.find_all_nodes(subcategory='all inputs'))
        nodes_to_remove.extend(graph.find_all_nodes(subcategory='all outputs'))
        graph.remove_nodes_from(nodes_to_remove)

        # Determine and check function ordering method
        assert function_order_method in self.OPTIONS_FUNCTION_ORDER_METHOD
        if function_order_method == 'manual':
            assert 'function_order' in graph.graph['problem_formulation'], 'function_order must be given as attribute.'
            function_order = graph.graph['problem_formulation']['function_order']
        elif function_order_method == 'random':
            function_order = graph.find_all_nodes(category='function')

        # First store all the out- and in-edge variables per function
        function_var_data = dict()
        # noinspection PyUnboundLocalVariable
        for function in function_order:
            function_var_data[function] = dict(in_vars=set(), out_vars=set())
            function_var_data[function]['in_vars'] = [edge[0] for edge in graph.in_edges(function)]
            function_var_data[function]['out_vars'] = [edge[1] for edge in graph.out_edges(function)]
        # Create an empty matrix
        coupling_matrix = np.zeros((len(function_order), len(function_order)), dtype=np.int)
        # Create the coupling matrix (including circular dependencies)
        for idx1, function1 in enumerate(function_order):
            for idx2, function2 in enumerate(function_order):
                n_coupling_vars = len(set(function_var_data[function1]['out_vars']).
                                      intersection(set(function_var_data[function2]['in_vars'])))
                coupling_matrix[idx1, idx2] = n_coupling_vars

        return coupling_matrix

    def get_mg_function_ordering(self):
        """Method to determine the function ordering for MDAO graphs (FPG and MDG) based on an FPG.

        Function ordering has to be adjusted when design variables are used. In that case, the pre-coupling functions
        have to be divided in  two parts: the first part does not use the design variables yet, while the second does.

        :return: function ordering dictionary
        :rtype: dict
        """

        mdao_arch = self.graph['problem_formulation']['mdao_architecture']
        pre_functions = self.graph['problem_formulation']['function_ordering'][self.FUNCTION_ROLES[0]]
        mg_function_ordering = dict(self.graph['problem_formulation']['function_ordering'])

        if mdao_arch in self.OPTIONS_ARCHITECTURES[2:7]:  # IDF, MDF, unc-OPT, unc-DOE, con-DOE
            del mg_function_ordering[self.FUNCTION_ROLES[0]]
            if pre_functions:
                target_set = set()
                des_var_nodes = self.find_all_nodes(attr_cond=['problem_role', '==', self.PROBLEM_ROLES_VARS[0]])
                for des_var in des_var_nodes:
                    # Find targets
                    des_var_targets = self.get_targets(des_var)
                    target_set.update(des_var_targets)
                post_desvars_idx = len(pre_functions)
                for idx, func in enumerate(pre_functions):
                    # Check if the function is in the target set
                    if func in target_set:
                        post_desvars_idx = idx
                        break
                pre_desvars_funcs = pre_functions[:post_desvars_idx]
                post_desvars_funcs = pre_functions[post_desvars_idx:]
            else:
                pre_desvars_funcs = []
                post_desvars_funcs = []
            mg_function_ordering[self.FUNCTION_ROLES[3]] = pre_desvars_funcs
            mg_function_ordering[self.FUNCTION_ROLES[4]] = post_desvars_funcs
            if mdao_arch == self.OPTIONS_ARCHITECTURES[2]:  # IDF
                mg_function_ordering[self.FUNCTION_ROLES[2]].append(self.CONSCONS_STRING)

        return mg_function_ordering

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            CONVERSION METHODS                                                    #
    # ---------------------------------------------------------------------------------------------------------------- #

    def create_mpg(self, mg_function_ordering, name='MPG'):
        """Function to automatically create a MPG based on a FPG.

        :param mg_function_ordering: dictionary with MDAO graph function ordering
        :type mg_function_ordering: dict
        :param name: name for the MPG graph
        :type name: basestring
        :return: unconnected FPG (only action blocks and their diagonal position)
        :rtype: MdaoProcessGraph
        """

        from graph_process import MdaoProcessGraph
        mpg = MdaoProcessGraph(kb_path=self.graph.get('kb_path'), name=name,
                               fpg=self, mg_function_ordering=mg_function_ordering)
        mpg.graph['problem_formulation'] = self.graph['problem_formulation']

        return mpg

    def create_mdg(self, mg_function_ordering, name='MDG'):
        """Function to automatically create an MDG based on an FPG.

        :param mg_function_ordering: dictionary with MDAO graph function ordering
        :type mg_function_ordering: dict
        :param name: name for the MDG graph
        :type name: basestring
        :return: baseline MDG (only added additional action blocks, no changed connections)
        :rtype: MdaoDataGraph
        """

        mdg = MdaoDataGraph(self, name=name, mg_function_ordering=mg_function_ordering)

        return mdg

    def get_mpg(self, name='MPG', mdg=None):
        """Create the MDAO process graph for a given FPG.

        :param name: name of the new graph
        :type name: basestring
        :param mdg: data graph to be used for process optimization
        :type mdg: MdaoDataGraph
        :return: MDAO process graph
        :rtype: MdaoProcessGraph
        """

        # Start-up checks
        logger.info('Composing MPG...')
        assert isinstance(name, basestring)
        self.add_function_problem_roles()
        self.check(raise_error=True)

        # Make clean copy of the graph to avoid unwanted links and updates
        graph = self.cleancopy()

        # Local variables
        coor = graph.COORDINATOR_STRING
        mdao_arch = graph.graph['problem_formulation']['mdao_architecture']
        conv_type = graph.graph['problem_formulation']['convergence_type']

        # Get the function ordering for the FPG and assign function lists accordingly.
        mg_function_ordering = graph.get_mg_function_ordering()
        if graph.FUNCTION_ROLES[0] in mg_function_ordering:
            pre_functions = mg_function_ordering[graph.FUNCTION_ROLES[0]]
        elif graph.FUNCTION_ROLES[3] in mg_function_ordering:
            pre_desvars_funcs = mg_function_ordering[graph.FUNCTION_ROLES[3]]
            post_desvars_funcs = mg_function_ordering[graph.FUNCTION_ROLES[4]]
        coup_functions = mg_function_ordering[graph.FUNCTION_ROLES[1]]
        post_functions = mg_function_ordering[graph.FUNCTION_ROLES[2]]

        # Set up MDAO process graph
        mpg = graph.create_mpg(mg_function_ordering, name=name)

        # Make process step of the coordinator equal to zero
        mpg.node[coor]['process_step'] = 0

        # Add process edges for each architecture
        if mdao_arch == graph.OPTIONS_ARCHITECTURES[0]:  # unconverged-MDA
            # noinspection PyUnboundLocalVariable
            sequence1 = [coor] + pre_functions
            mpg.add_simple_sequential_process(sequence1, mpg.node[coor]['process_step'],
                                              end_in_iterative_node=sequence1[0] if
                                              conv_type == graph.OPTIONS_CONVERGERS[2] else None)
            if conv_type == graph.OPTIONS_CONVERGERS[0]:  # Jacobi
                # Then run coupled and post-coupling functions in parallel
                start_node = sequence1[-1]
                mpg.add_parallel_process(start_node, coup_functions,
                                         mpg.node[start_node]['process_step'],
                                         end_node=sequence1[0] if not post_functions else None,
                                         end_in_converger=True if not post_functions else None,
                                         use_data_graph=None)
                start_nodes_post = coup_functions
            elif conv_type == graph.OPTIONS_CONVERGERS[1]:  # Gauss-Seidel
                sequence2 = [sequence1[-1]] + coup_functions
                mpg.add_simple_sequential_process(sequence2, mpg.node[sequence1[-1]]['process_step'],
                                                  end_in_iterative_node=sequence1[0] if not post_functions else None)
                start_nodes_post = [sequence2[-1]]
            if conv_type in graph.OPTIONS_CONVERGERS[0:2] and post_functions:  # Jacobi or Gauss-Seidel
                # noinspection PyUnboundLocalVariable
                mpg.add_parallel_process(start_nodes_post, post_functions,
                                         start_step=mpg.node[start_nodes_post[0]]['process_step'],
                                         end_node=coor, end_in_converger=True, use_data_graph=mdg)
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[1]:  # converged-MDA
            conv = graph.CONVERGER_STRING
            # noinspection PyUnboundLocalVariable
            sequence = [coor] + pre_functions + [conv]
            mpg.add_simple_sequential_process(sequence, mpg.node[coor]['process_step'])
            if conv_type == graph.OPTIONS_CONVERGERS[1]:  # Gauss-Seidel
                sequence2 = [graph.CONVERGER_STRING] + coup_functions
                mpg.add_simple_sequential_process(sequence2, mpg.node[conv]['process_step'], end_in_iterative_node=conv)
            elif conv_type == graph.OPTIONS_CONVERGERS[0]:  # Jacobi
                mpg.add_parallel_process(conv, coup_functions, mpg.node[conv]['process_step'],
                                         end_node=conv, end_in_converger=True, use_data_graph=None)
            if post_functions:
                mpg.add_parallel_process(conv, post_functions, mpg.node[conv]['converger_step'],
                                         end_node=coor, end_in_converger=True, use_data_graph=None)
            else:
                mpg.add_edge(conv, coor)
                mpg.edge[conv][coor]['process_step'] = mpg.node[conv]['converger_step'] + 1
                mpg.node[coor]['converger_step'] = mpg.node[conv]['converger_step'] + 1
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[2]:  # IDF
            opt = graph.OPTIMIZER_STRING
            # noinspection PyUnboundLocalVariable
            sequence1 = [coor] + pre_desvars_funcs + [opt]
            mpg.add_simple_sequential_process(sequence1, mpg.node[coor]['process_step'])
            # noinspection PyUnboundLocalVariable
            sequence2 = [opt] + post_desvars_funcs
            mpg.add_simple_sequential_process(sequence2, mpg.node[opt]['process_step'])
            mpg.add_parallel_process(sequence2[-1], coup_functions, mpg.node[sequence2[-1]]['process_step'],
                                     use_data_graph=None)
            mpg.add_parallel_process(coup_functions, post_functions, mpg.node[coup_functions[0]]['process_step'],
                                     end_node=opt, end_in_converger=True, use_data_graph=mdg)
            mpg.connect_nested_iterators(coor, opt)
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[3]:  # MDF
            opt = graph.OPTIMIZER_STRING
            conv = graph.CONVERGER_STRING
            # noinspection PyUnboundLocalVariable
            sequence1 = [coor] + pre_desvars_funcs + [opt]
            mpg.add_simple_sequential_process(sequence1, mpg.node[coor]['process_step'])
            # noinspection PyUnboundLocalVariable
            sequence2 = [opt] + post_desvars_funcs + [conv]
            mpg.add_simple_sequential_process(sequence2, mpg.node[opt]['process_step'])
            if conv_type == graph.OPTIONS_CONVERGERS[0]:  # Jacobi
                mpg.add_parallel_process(conv, coup_functions, mpg.node[conv]['process_step'],
                                         end_node=conv, end_in_converger=True, use_data_graph=None)
            elif conv_type == graph.OPTIONS_CONVERGERS[1]:  # Gauss-Seidel
                sequence3 = [conv] + coup_functions
                mpg.add_simple_sequential_process(sequence3, mpg.node[conv]['process_step'],
                                                  end_in_iterative_node=sequence3[0])
            mpg.add_parallel_process(conv, post_functions, mpg.node[conv]['converger_step'],
                                     end_node=opt, end_in_converger=True, use_data_graph=None)
            mpg.connect_nested_iterators(coor, opt)
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[4]:  # unconverged-OPT
            opt = graph.OPTIMIZER_STRING
            # noinspection PyUnboundLocalVariable
            sequence1 = [coor] + pre_desvars_funcs + [opt]
            mpg.add_simple_sequential_process(sequence1, mpg.node[coor]['process_step'])
            # noinspection PyUnboundLocalVariable
            sequence2 = [opt] + post_desvars_funcs
            mpg.add_simple_sequential_process(sequence2, mpg.node[opt]['process_step'],
                                              end_in_iterative_node=sequence2[0] if
                                              conv_type == graph.OPTIONS_CONVERGERS[2] else None)
            if conv_type == graph.OPTIONS_CONVERGERS[0]:  # Jacobi
                # Then run coupled and post-coupling functions in parallel
                start_node = sequence2[-1]
                mpg.add_parallel_process(start_node, coup_functions,
                                         mpg.node[start_node]['process_step'], use_data_graph=None)
                start_nodes_post = coup_functions
            elif conv_type == graph.OPTIONS_CONVERGERS[1]:  # Gauss-Seidel
                sequence = [sequence2[-1]]+coup_functions
                mpg.add_simple_sequential_process(sequence, mpg.node[sequence2[-1]]['process_step'])
                start_nodes_post = [sequence[-1]]
            if conv_type in graph.OPTIONS_CONVERGERS[0:2]:  # Jacobi or Gauss-Seidel
                # noinspection PyUnboundLocalVariable
                mpg.add_parallel_process(start_nodes_post, post_functions,
                                         start_step=mpg.node[start_nodes_post[0]]['process_step'],
                                         end_node=opt, end_in_converger=True, use_data_graph=mdg)
            mpg.connect_nested_iterators(coor, opt)
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[5]:  # unconverged-DOE
            doe = graph.DOE_STRING
            # noinspection PyUnboundLocalVariable
            sequence1 = [coor] + pre_desvars_funcs + [doe]
            mpg.add_simple_sequential_process(sequence1, mpg.node[coor]['process_step'])
            # noinspection PyUnboundLocalVariable
            sequence2 = [doe] + post_desvars_funcs
            mpg.add_simple_sequential_process(sequence2, mpg.node[doe]['process_step'],
                                              end_in_iterative_node=sequence2[0] if
                                              conv_type == graph.OPTIONS_CONVERGERS[2] else None)
            if conv_type == graph.OPTIONS_CONVERGERS[0]:  # Jacobi
                # Then run coupled and post-coupling functions in parallel
                start_node = sequence2[-1]
                mpg.add_parallel_process(start_node, coup_functions,
                                         mpg.node[start_node]['process_step'], use_data_graph=None)
                start_nodes_post = coup_functions
            elif conv_type == graph.OPTIONS_CONVERGERS[1]:  # Gauss-Seidel
                sequence = [sequence2[-1]] + coup_functions
                mpg.add_simple_sequential_process(sequence, mpg.node[sequence2[-1]]['process_step'])
                start_nodes_post = [sequence[-1]]
            if conv_type in graph.OPTIONS_CONVERGERS[0:2]:  # Jacobi or Gauss-Seidel
                # noinspection PyUnboundLocalVariable
                mpg.add_parallel_process(start_nodes_post, post_functions,
                                         start_step=mpg.node[start_nodes_post[0]]['process_step'],
                                         end_node=doe, end_in_converger=True, use_data_graph=mdg)
            mpg.connect_nested_iterators(coor, doe)
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[6]:  # converged-DOE
            doe = graph.DOE_STRING
            conv = graph.CONVERGER_STRING
            # noinspection PyUnboundLocalVariable
            sequence1 = [coor] + pre_desvars_funcs + [doe]
            mpg.add_simple_sequential_process(sequence1, mpg.node[coor]['process_step'])
            # noinspection PyUnboundLocalVariable
            sequence2 = [doe] + post_desvars_funcs + [conv]
            mpg.add_simple_sequential_process(sequence2, mpg.node[doe]['process_step'])
            if conv_type == graph.OPTIONS_CONVERGERS[0]:  # Jacobi
                mpg.add_parallel_process(conv, coup_functions, mpg.node[conv]['process_step'],
                                         end_node=conv, end_in_converger=True, use_data_graph=None)
            elif conv_type == graph.OPTIONS_CONVERGERS[1]:  # Gauss-Seidel
                sequence3 = [conv] + coup_functions
                mpg.add_simple_sequential_process(sequence3, mpg.node[conv]['process_step'],
                                                  end_in_iterative_node=sequence3[0])
            mpg.add_parallel_process(conv, post_functions, mpg.node[conv]['converger_step'],
                                     end_node=doe, end_in_converger=True, use_data_graph=None)
            mpg.connect_nested_iterators(coor, doe)

        logger.info('Composed MPG.')

        return mpg

    def get_mdg(self, name='MDG'):
        """
        Create the MDAO data graph for a given FPG.

        :param name: name of the new graph
        :type name: basestring
        :return: MDAO data graph
        :rtype: MdaoDataGraph
        """

        # Start-up checks
        logger.info('Composing MDG...')
        assert isinstance(name, basestring)
        self.add_function_problem_roles()
        self.check(raise_error=True)

        # Make clean copy of the graph to avoid unwanted links and updates
        graph = self.cleancopy()

        # Load variables from FPG
        mdao_arch = graph.graph['problem_formulation']['mdao_architecture']
        conv_type = graph.graph['problem_formulation']['convergence_type']
        if 'allow_unconverged_couplings' in graph.graph['problem_formulation']:
            allow_unconverged_couplings = graph.graph['problem_formulation']['allow_unconverged_couplings']
        else:
            allow_unconverged_couplings = False

        # Determine special variables and functions
        if mdao_arch in graph.OPTIONS_ARCHITECTURES[2:7]:  # IDF, MDF, unc-OPT, unc-DOE, con-DOE
            des_var_nodes = graph.find_all_nodes(attr_cond=['problem_role', '==', graph.PROBLEM_ROLES_VARS[0]])
        if mdao_arch in graph.OPTIONS_ARCHITECTURES[2:5]:  # IDF, MDF, unconverged-OPT
            constraint_nodes = graph.find_all_nodes(attr_cond=['problem_role', '==', graph.PROBLEM_ROLES_VARS[2]])
            objective_node = graph.find_all_nodes(attr_cond=['problem_role', '==', graph.PROBLEM_ROLES_VARS[1]])[0]
        qoi_nodes = graph.find_all_nodes(attr_cond=['problem_role', '==', graph.PROBLEM_ROLES_VARS[3]])

        # Get the function ordering for the FPG and assign coupling function lists accordingly.
        mg_function_ordering = graph.get_mg_function_ordering()
        coup_functions = mg_function_ordering[graph.FUNCTION_ROLES[1]]

        # Set up MDAO data graph
        mdg = graph.create_mdg(mg_function_ordering, name=name)

        # Manipulate data graph
        if mdao_arch == graph.OPTIONS_ARCHITECTURES[0]:  # unconverged-MDA
            if allow_unconverged_couplings:
                # Manipulate the coupling variables based on the architecture
                if conv_type == graph.OPTIONS_CONVERGERS[0]:  # Jacobi
                    mdg.manipulate_coupling_nodes(coup_functions, remove_feedback=True, remove_feedforward=True,
                                                  converger=None, include_couplings_as_final_output=False)
                elif conv_type == graph.OPTIONS_CONVERGERS[1]:  # Gauss-Seidel
                    mdg.manipulate_coupling_nodes(coup_functions, remove_feedback=True, remove_feedforward=False,
                                                  converger=None, include_couplings_as_final_output=False)
            # Connect QOIs to the coordinator
            mdg.connect_qoi_nodes_as_input(qoi_nodes, graph.COORDINATOR_STRING, True)
            # Connect system inputs and outputs to the coordinator
            mdg.connect_coordinator()
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[1]:  # converged-MDA
            conv = graph.CONVERGER_STRING
            # Connect converger
            mdg.connect_converger(conv, conv_type, coup_functions, True)
            # Connect QOIs to the coordinator
            mdg.connect_qoi_nodes_as_input(qoi_nodes, graph.COORDINATOR_STRING, True)
            # Connect remaining system inputs and outputs to the coordinator
            mdg.connect_coordinator()
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[2]:  # IDF
            opt = graph.OPTIMIZER_STRING
            # Connect optimizer as a converger using the consistency constraint function
            mdg.connect_converger(opt, graph.OPTIONS_ARCHITECTURES[2], coup_functions, True)
            # Connect optimizer w.r.t. design variables, objective, contraints
            # noinspection PyUnboundLocalVariable
            mdg.connect_optimizer(opt, des_var_nodes, objective_node, constraint_nodes)
            # Connect QOIs to the coordinator
            mdg.connect_qoi_nodes_as_input(qoi_nodes, graph.COORDINATOR_STRING, True)
            # Connect remaining system inputs and outputs to the coordinator
            mdg.connect_coordinator()
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[3]:  # MDF
            opt = graph.OPTIMIZER_STRING
            conv = graph.CONVERGER_STRING
            # Connect converger
            mdg.connect_converger(conv, conv_type, coup_functions, True)
            # Connect optimizer
            # noinspection PyUnboundLocalVariable
            mdg.connect_optimizer(opt, des_var_nodes, objective_node, constraint_nodes)
            # Connect QOIs to the coordinator
            mdg.connect_qoi_nodes_as_input(qoi_nodes, graph.COORDINATOR_STRING, True)
            # Connect remaining system inputs and outputs to the coordinator
            mdg.connect_coordinator()
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[4]:  # unconverged-OPT
            opt = graph.OPTIMIZER_STRING
            if allow_unconverged_couplings:
                # Manipulate the coupling variables based on the architecture
                if conv_type == graph.OPTIONS_CONVERGERS[0]:  # Jacobi
                    mdg.manipulate_coupling_nodes(coup_functions, remove_feedback=True, remove_feedforward=True,
                                                  converger=None, include_couplings_as_final_output=True)
                elif conv_type == graph.OPTIONS_CONVERGERS[1]:  # Gauss-Seidel
                    mdg.manipulate_coupling_nodes(coup_functions, remove_feedback=True, remove_feedforward=False,
                                                  converger=None, include_couplings_as_final_output=True)
            # Connect optimizer
            # noinspection PyUnboundLocalVariable
            mdg.connect_optimizer(opt, des_var_nodes, objective_node, constraint_nodes)
            # Connect QOIs to the coordinator
            mdg.connect_qoi_nodes_as_input(qoi_nodes, graph.COORDINATOR_STRING, True)
            # Connect remaining system inputs and outputs to the coordinator
            mdg.connect_coordinator()
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[5]:  # unconverged-DOE
            doe = graph.DOE_STRING
            if allow_unconverged_couplings:
                # Manipulate the coupling variables based on the architecture
                if conv_type == graph.OPTIONS_CONVERGERS[0]:  # Jacobi
                    mdg.manipulate_coupling_nodes(coup_functions, remove_feedback=True, remove_feedforward=True,
                                                  converger=None, include_couplings_as_final_output=False)
                elif conv_type == graph.OPTIONS_CONVERGERS[1]:  # Gauss-Seidel
                    mdg.manipulate_coupling_nodes(coup_functions, remove_feedback=True, remove_feedforward=False,
                                                  converger=None, include_couplings_as_final_output=False)
            # Connect doe block
            # noinspection PyUnboundLocalVariable
            mdg.connect_doe_block(doe, des_var_nodes, qoi_nodes)
            # Connect remaining system inputs and outputs to the coordinator
            mdg.connect_coordinator()
        elif mdao_arch == graph.OPTIONS_ARCHITECTURES[6]:  # converged-DOE
            doe = graph.DOE_STRING
            conv = graph.CONVERGER_STRING
            # Connect converger
            mdg.connect_converger(conv, conv_type, coup_functions, False)
            # Connect doe block
            # noinspection PyUnboundLocalVariable
            mdg.connect_doe_block(doe, des_var_nodes, qoi_nodes)
            # Connect remaining system inputs and outputs to the coordinator
            mdg.connect_coordinator()

        logger.info('Composed MDG.')

        return mdg


class MdaoDataGraph(DataGraph, MdaoMixin):

    def __init__(self, *args, **kwargs):
        super(MdaoDataGraph, self).__init__(*args, **kwargs)
        if 'mg_function_ordering' in kwargs:
            mg_function_ordering = kwargs['mg_function_ordering']
            self._add_action_blocks_and_roles(mg_function_ordering)
            self.graph['function_ordering'] = mg_function_ordering

    def cleancopy(self):
        """Method to make a clean copy of a graph.

        This method can be used to avoid deep-copy problems in graph manipulation algorithms.
        The graph class is kept.

        :return: clean-copy of the graph
        :rtype: MdaoDataGraph
        """

        return MdaoDataGraph(self)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            CHECKING METHODS                                                      #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _check_category_a(self):
        """Extended method to perform a category A check on the graph.

        :return: result of the check and index
        :rtype: bool, int
        """

        # Set check
        category_check, i = super(MdaoDataGraph, self)._check_category_a()

        # Get nodes
        func_nodes = self.find_all_nodes(category='function')
        var_nodes = self.find_all_nodes(category='variable')

        # Get information
        n_nodes = self.number_of_nodes()
        n_functions = len(func_nodes)
        n_variables = len(var_nodes)

        # Checks on nodes
        category_check, i = check(n_nodes != (n_functions+n_variables),
                                  'The number of total nodes does not match number of function and variable nodes.',
                                  status=category_check,
                                  category='A',
                                  i=i)
        for node in var_nodes:
            category_check, i_not = check(self.in_degree(node) == 0,
                                          'The node %s has in-degree 0.' % node,
                                          status=category_check,
                                          category='A',
                                          i=i)
            category_check, i_not = check(self.out_degree(node) == 0,
                                          'The node %s has out-degree 0.' % node,
                                          status=category_check,
                                          category='A',
                                          i=i+1)
        i += 1
        category_check, i = check(not self.has_node(self.COORDINATOR_STRING),
                                  'The %s node is missing in the graph.' % self.COORDINATOR_STRING,
                                  status=category_check,
                                  category='A',
                                  i=i)
        for node in func_nodes:
            category_check, i_not = check('architecture_role' not in self.node[node],
                                          'The architecture_role attribute is missing on the node %s.' % node,
                                          status=category_check,
                                          category='A',
                                          i=i)
        i += 1

        # Return
        return category_check, i

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            CREATE METHODS                                                        #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _create_cmdows_workflow_problem_def(self):

        # Create workflow/problemDefinitionUID
        cmdows_workflow_problem_def = Element('problemDefinitionUID')
        cmdows_workflow_problem_def.text = (str(self.graph['problem_formulation'].get('mdao_architecture')) +
                                            str(self.graph['problem_formulation'].get('convergence_type')))

        return cmdows_workflow_problem_def

    def _create_cmdows_architecture_elements(self):

        # Create architectureElement
        cmdows_architecture_elements = Element('architectureElements')

        # Create architectureElements/parameters
        cmdows_parameters = cmdows_architecture_elements.add('parameters')
        # Create architectureElements/parameters/instances
        # noinspection PyUnusedLocal
        cmdows_instances = cmdows_parameters.add('instances')
        # TODO: Implement this
        # Create architectureElements/parameters/...
        for architecture_roles_var in self.ARCHITECTURE_ROLES_VARS:
            cmdows_parameter = cmdows_parameters.add(make_camel_case(architecture_roles_var, make_plural_option=True))
            graph_parameter_nodes = self.find_all_nodes(attr_cond=['architecture_role', '==', architecture_roles_var])
            for graph_parameter_node in graph_parameter_nodes:
                cmdows_parameter_node = cmdows_parameter.add(make_camel_case(architecture_roles_var))
                cmdows_parameter_node.set('uID', graph_parameter_node)
                cmdows_parameter_node.add('relatedParameterUID',
                                          self.node[graph_parameter_node].get('related_to_schema_node'))
                cmdows_parameter_node.add('label',
                                          self.node[graph_parameter_node].get('label'))

        # Create architectureElements/executableBlocks
        cmdows_executable_blocks = cmdows_architecture_elements.add('executableBlocks')
        # Create architectureElements/executableBlocks/...
        for architecture_roles_fun in self.CMDOWS_ARCHITECTURE_ROLE_SPLITTER:
            graph_nodes = self.find_all_nodes(attr_cond=['architecture_role', '==', architecture_roles_fun])
            cmdows_executable_block = cmdows_executable_blocks.add(make_camel_case(architecture_roles_fun,
                                                                                   make_plural_option=True))
            # Create architectureElements/executableBlocks/.../...
            for graph_node in graph_nodes:

                cmdows_executable_block_elem = cmdows_executable_block.add(make_camel_case(architecture_roles_fun))
                cmdows_executable_block_elem.set('uID', graph_node)
                cmdows_executable_block_elem.add('label', self.node[graph_node].get('label'))

                if architecture_roles_fun == 'optimizer':
                    cmdows_executable_block_elem.add('settings', self.node[graph_node].get('settings'))
                    graph_des_vars = [{'designVariableUID': self.PROBLEM_ROLES_VAR_SUFFIXES[0]+var} for var in
                                      self.node[graph_node].get('design_variables')]
                    cmdows_executable_block_elem.add('designVariables', graph_des_vars)
                    graph_obj_vars = [{'objectiveVariableUID': self.PROBLEM_ROLES_VAR_SUFFIXES[1] + var} for var in
                                      self.node[graph_node].get('objective_variable')]
                    cmdows_executable_block_elem.add('objectiveVariables', graph_obj_vars)
                    graph_con_vars = [{'constraintVariableUID': self.PROBLEM_ROLES_VAR_SUFFIXES[2] + var} for var in
                                      self.node[graph_node].get('constraint_variables')]
                    cmdows_executable_block_elem.add('constraintVariables', graph_con_vars)

                elif architecture_roles_fun == 'doe':
                    graph_settings = self.node[graph_node].get('settings')
                    cmdows_settings = cmdows_executable_block_elem.add('settings')
                    if graph_settings.get('doe_table') is not None:
                        cmdows_table = cmdows_settings.add('doeTable')
                        for graph_row_index, graph_row in enumerate(graph_settings.get('doe_table_order')):
                            cmdows_row = cmdows_table.add('tableRow', attrib={'relatedParameterUID': str(graph_row)})
                            for graph_element_index, graph_element in enumerate(graph_settings.get('doe_table')):
                                cmdows_row.add('tableElement', graph_element[graph_row_index],
                                               attrib={'experimentID': str(graph_element_index)})
                    cmdows_settings.add('doeMethod', graph_settings.get('doe_method'))
                    graph_des_vars = [{'designVariableUID': self.PROBLEM_ROLES_VAR_SUFFIXES[0] + var} for var in
                                      self.node[graph_node].get('design_variables')]
                    cmdows_executable_block_elem.add('designVariables', graph_des_vars)

                else:
                    cmdows_executable_block_elem.add('settings', self.node[graph_node].get('settings'))

        # Create architectureElements/executableBlocks/...Analyses/...
        architecture_roles_funs = np.setdiff1d(self.ARCHITECTURE_ROLES_FUNS, self.CMDOWS_ARCHITECTURE_ROLE_SPLITTER,
                                               assume_unique=True)
        for architecture_roles_fun in architecture_roles_funs:
            nodes = self.find_all_nodes(attr_cond=['architecture_role', '==', str(architecture_roles_fun)])
            cmdows_analyses = cmdows_executable_blocks.add(make_camel_case(architecture_roles_fun,
                                                                           make_plural_option=True))
            for node in nodes:
                cmdows_analysis = cmdows_analyses.add(make_camel_case(architecture_roles_fun))
                cmdows_analysis.add('relatedExecutableBlockUID', node)

        return cmdows_architecture_elements

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                             LOAD METHODS                                                         #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _load_cmdows_architecture_elements(self, cmdows):

        # Create architecture element nodes
        cmdows_architecture_parameters = cmdows.find('architectureElements/parameters')
        for cmdows_architecture_parameter in list(cmdows_architecture_parameters):
            for cmdows_single_architecture_parameter in list(cmdows_architecture_parameter):
                cmdows_uid = cmdows_single_architecture_parameter.get('uID')
                attrb = cmdows.finddict(cmdows_single_architecture_parameter, ordered=False, camel_case_conversion=True)
                attrb = translate_dict_keys(attrb, {'related_parameter_u_i_d': 'related_to_schema_node'})
                self.add_node(cmdows_uid,
                              attrb,
                              category='variable',
                              architecture_role=unmake_camel_case(cmdows_single_architecture_parameter.tag, ' '))
        cmdows_architecture_exe_blocks = cmdows.find('architectureElements/executableBlocks')
        for cmdows_architecture_exe_block in list(cmdows_architecture_exe_blocks):
            for cmdows_single_architecture_exe_block in list(cmdows_architecture_exe_block):
                cmdows_uid = cmdows_single_architecture_exe_block.get('uID')

                if cmdows_uid is not None:
                    role = unmake_camel_case(cmdows_single_architecture_exe_block.tag, ' ')
                    self.add_node(cmdows_uid,
                                  category='function',
                                  architecture_role=role,
                                  label=cmdows_single_architecture_exe_block.findasttext('label'),
                                  settings=cmdows_single_architecture_exe_block.findasttext('settings'))
                    if role == 'optimizer' or role == 'doe':
                        cmdows_des_vars = cmdows_single_architecture_exe_block.findall('designVariables/designVariable')
                        graph_des_vars = [var.findtext('designVariableUID')[10:] for var in list(cmdows_des_vars)]
                        self.node[cmdows_uid]['design_variables'] = graph_des_vars
                    if role == 'optimizer':
                        cmdows_des_vars = cmdows_single_architecture_exe_block.findall('objectiveVariables/objectiveVariable')
                        graph_des_vars = [var.findtext('objectiveVariableUID')[10:] for var in list(cmdows_des_vars)]
                        self.node[cmdows_uid]['objective_variable'] = graph_des_vars
                        cmdows_des_vars = cmdows_single_architecture_exe_block.findall('constraintVariables/constraintVariable')
                        graph_des_vars = [var.findtext('constraintVariableUID')[10:] for var in list(cmdows_des_vars)]
                        self.node[cmdows_uid]['constraint_variables'] = graph_des_vars
                    elif role == 'doe':
                        cmdows_rows = list(cmdows_single_architecture_exe_block.findall('settings/doeTable/tableRow'))
                        graph_rows = [cmdows_row.get('relatedParameterUID') for cmdows_row in cmdows_rows]
                        graph_table = []
                        for cmdows_row in cmdows_rows:
                            def get_experiment_id(elem):
                                return float(elem.get('experimentID'))
                            elements = sorted(cmdows_row, key=get_experiment_id)
                            graph_table.append([element.findasttext() for element in elements])
                        graph_table = map(list, zip(*graph_table))
                        if 'settings' not in self.node[cmdows_uid] or self.node[cmdows_uid]['settings'] is None:
                            self.node[cmdows_uid]['settings'] = {}
                        self.node[cmdows_uid]['settings']['doe_table_order'] = graph_rows
                        self.node[cmdows_uid]['settings']['doe_table'] = graph_table
                        self.node[cmdows_uid]['settings']['doe_method'] = cmdows_single_architecture_exe_block.findtext('settings/doeMethod')

                else:
                    for role in self.ARCHITECTURE_ROLES_FUNS:
                        cmdows_role_name = make_camel_case(role)
                        if cmdows_single_architecture_exe_block.tag == cmdows_role_name:
                            cmdows_uid = cmdows_single_architecture_exe_block.find('relatedExecutableBlockUID').text
                            self.node[cmdows_uid]['architecture_role'] = role

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                          GRAPH SPECIFIC METHODS                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _add_action_blocks_and_roles(self, mg_function_ordering):
        """Method to add function blocks to the MDG based on the FPG function ordering

        :param mg_function_ordering: ordered list of functions to be added
        :type mg_function_ordering: list
        """

        # Set input settings
        mdao_arch = self.graph['problem_formulation']['mdao_architecture']

        # Add coordinator node
        assert not self.has_node(self.COORDINATOR_STRING), 'Coordinator name already in use in FPG.'
        self.add_node(self.COORDINATOR_STRING,
                      category='function',
                      architecture_role=self.ARCHITECTURE_ROLES_FUNS[0],
                      shape='8',
                      label=self.COORDINATOR_LABEL,
                      level=None)

        # No optimizer present
        if self.FUNCTION_ROLES[0] in mg_function_ordering:
            functions = mg_function_ordering[self.FUNCTION_ROLES[0]]
            for func in functions:
                self.node[func]['architecture_role'] = self.ARCHITECTURE_ROLES_FUNS[4]

        # Optimizer / DOE present
        if self.FUNCTION_ROLES[3] in mg_function_ordering:
            # Add pre-optimizer functions
            functions = mg_function_ordering[self.FUNCTION_ROLES[3]]
            for func in functions:
                self.node[func]['architecture_role'] = 'pre-iterator analysis'
            # Add optimizer / DOE
            if mdao_arch in self.OPTIONS_ARCHITECTURES[2:5]:  # IDF, MDF, unc-OPT
                assert not self.has_node(self.OPTIMIZER_STRING), 'Optimizer name already in use in FPG.'
                self.add_node(self.OPTIMIZER_STRING,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[1],
                              shape='8',
                              label=self.OPTIMIZER_LABEL,
                              level=None)
            elif mdao_arch in self.OPTIONS_ARCHITECTURES[5:7]:  # unc-DOE, con-DOE
                assert not self.has_node(self.DOE_STRING), 'DOE name already in use in FPG.'
                self.add_node(self.DOE_STRING,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[3],  # doe
                              shape='8',
                              label=self.DOE_LABEL,
                              level=None,
                              settings=self.graph['problem_formulation']['doe_settings'])
            # Add architecture role to post-iterator functions
            functions = mg_function_ordering[self.FUNCTION_ROLES[4]]
            for func in functions:
                self.node[func]['architecture_role'] = self.ARCHITECTURE_ROLES_FUNS[6]

        # Converger required
        if mdao_arch in [self.OPTIONS_ARCHITECTURES[1]] + [self.OPTIONS_ARCHITECTURES[3]] + \
                [self.OPTIONS_ARCHITECTURES[6]]:  # con-MDA, MDF, con-DOE
            # Add converger
            assert not self.has_node(self.CONVERGER_STRING), 'Converger name already in use in FPG.'
            self.add_node(self.CONVERGER_STRING,
                          category='function',
                          architecture_role=self.ARCHITECTURE_ROLES_FUNS[2],
                          shape='8',
                          label=self.CONVERGER_LABEL,
                          level=None)

        # Add architecture role to coupled functions
        for func in mg_function_ordering[self.FUNCTION_ROLES[1]]:
            self.node[func]['architecture_role'] = self.ARCHITECTURE_ROLES_FUNS[7]

        # Add post-coupling functions
        for func in mg_function_ordering[self.FUNCTION_ROLES[2]]:
            if func != self.CONSCONS_STRING:
                self.node[func]['architecture_role'] = self.ARCHITECTURE_ROLES_FUNS[8]
            else:
                assert not self.has_node(self.CONSCONS_STRING), 'Consistency constraint name already in use in FPG.'
                self.add_node(self.CONSCONS_STRING,
                              label=self.CONSCONS_LABEL,
                              level=None,
                              shape='s',
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[9])

        return

    def copy_node_as(self, node, architecture_role):
        """Method to copy a given node for an architecture role.

        :param node: node to be copied
        :type node: str
        :param architecture_role: architecture role of the copied node
        :type architecture_role: basestring
        :return: modified node
        """

        assert self.has_node(node), "Node %s is not present in the graph." % node
        assert architecture_role in self.ARCHITECTURE_ROLES_VARS, "Invalid architecture role %s specified." % \
                                                                  architecture_role
        xpath_nodes = node.split('/')
        root = xpath_nodes[1]
        if architecture_role == self.ARCHITECTURE_ROLES_VARS[6]:  # consistency constraint variable
            new_node = '/' + root + '/architectureNodes/' + make_camel_case(architecture_role) + 's' + \
                       '/' + root + 'Copy/' + '/'.join(xpath_nodes[2:-1]) + '/gc_' + xpath_nodes[-1]
            # TODO: This needs to be fixed, now used to make RCE WF work for IDF (g_y1) instead of (y1)
        else:
            new_node = '/' + root + '/architectureNodes/' + make_camel_case(architecture_role) + 's' + \
                       '/' + root + 'Copy/' + '/'.join(xpath_nodes[2:])
        if architecture_role == self.ARCHITECTURE_ROLES_VARS[0]:  # initial guess coupling variable
            label_prefix = ''
            label_suffix = '^{c0}'
        elif architecture_role in [self.ARCHITECTURE_ROLES_VARS[1],
                                   self.ARCHITECTURE_ROLES_VARS[5]]:  # final coupling/output variable
            label_prefix = ''
            label_suffix = '^*'
        elif architecture_role == self.ARCHITECTURE_ROLES_VARS[2]:  # coupling variable
            label_prefix = ''
            label_suffix = '^c'
        elif architecture_role == self.ARCHITECTURE_ROLES_VARS[3]:  # initial guess design variable
            label_prefix = ''
            label_suffix = '^0'
        elif architecture_role == self.ARCHITECTURE_ROLES_VARS[4]:  # final design variable
            label_prefix = ''
            label_suffix = '^*'
        elif architecture_role == self.ARCHITECTURE_ROLES_VARS[6]:  # consistency constraint variable
            label_prefix = 'gc_'
            label_suffix = ''
        elif architecture_role == self.ARCHITECTURE_ROLES_VARS[7]:  # doe input samples
            label_prefix = 'DOE_'
            label_suffix = '_inp'
        elif architecture_role == self.ARCHITECTURE_ROLES_VARS[8]:  # doe output samples
            label_prefix = 'DOE_'
            label_suffix = '_out'
        else:
            raise IOError('Label extension could not be found.')

        node_data_dict = dict(self.node[node])

        # Determine the related schema node
        if 'related_to_schema_node' in node_data_dict:
            related_schema_node = node_data_dict['related_to_schema_node']
        else:
            related_schema_node = node

        if not self.has_node(new_node):
            self.add_node(new_node,
                          category=node_data_dict['category'],
                          related_to_schema_node=related_schema_node,
                          architecture_role=architecture_role,
                          shape=node_data_dict.get('shape'),
                          label=label_prefix+node_data_dict['label']+label_suffix)
        return new_node

    def connect_qoi_nodes_as_input(self, nodes, function, override_with_final_outputs):
        """Method to connect a list of qoi nodes as input to a given function node.

        :param nodes: list of nodes to be connected as input
        :type nodes: list
        :param function: function to which the nodes are connected
        :type function: basestring
        :param override_with_final_outputs: setting on whether to override the use of final outputs
        :type override_with_final_outputs: bool
        """

        for node in nodes:
            assert self.has_node(node)
            # Check if there is a final output node as well and use that one instead.
            if override_with_final_outputs:
                schema_related_nodes = self.find_all_nodes(category='variable',
                                                           attr_cond=['related_to_schema_node', '==', node])
                for schema_related_node in schema_related_nodes:
                    if 'architecture_role' in self.node[schema_related_node]:
                        if self.node[schema_related_node]['architecture_role'] in \
                                get_list_entries(self.ARCHITECTURE_ROLES_VARS, 1, 4, 5):
                            node = schema_related_node
            self.add_edge(node, function)

        return

    def connect_nodes_as_output(self, nodes, function):
        """Method to connect a list of nodes as output to a function node.

        :param nodes: list of nodes to be connected as output
        :type nodes: list
        :param function: function to which the nodes are connected
        :type function: basestring
        """

        for node in nodes:
            assert self.has_node(node)
            self.add_edge(function, node)

        return

    def connect_coordinator(self):
        """Method to automatically connect all system inputs and outputs of a graph to the coordinator node."""

        # Get system inputs and outputs
        input_nodes = self.find_all_nodes(subcategory='all inputs')
        output_nodes = self.find_all_nodes(subcategory='all outputs')

        # Connect the nodes to the coordinator
        for input_node in input_nodes:
            self.add_edge(self.COORDINATOR_STRING, input_node)
        for output_node in output_nodes:
            self.add_edge(output_node, self.COORDINATOR_STRING)

        return

    def connect_converger(self, converger, conv_type, coupling_functions, include_couplings_as_final_output):
        """Method to automatically connect a converger around a collection of coupled functions.

        :param converger: name of the converger to be connected
        :type converger: basestring
        :param conv_type: setting for the type of convergence (Jacobi, Gauss-Seidel)
        :type conv_type: basestring
        :param coupling_functions: list of coupled functions
        :type coupling_functions: list
        :param include_couplings_as_final_output: setting on whether coupling variables should always be added as output
        :type include_couplings_as_final_output: bool
        """

        # Input assertions
        assert self.has_node(converger), 'Converger is not present in the graph.'
        assert conv_type in self.OPTIONS_CONVERGERS + [self.OPTIONS_ARCHITECTURES[2]], \
            'Invalid converger type %s specified.' % conv_type
        assert isinstance(coupling_functions, list)
        for coupling_function in coupling_functions:
            assert self.has_node(coupling_function), 'Missing coupling function %s in the graph.' % coupling_function

        # Manipulate the coupling variables based on the architecture
        if conv_type == self.OPTIONS_CONVERGERS[0]:  # Jacobi
            self.manipulate_coupling_nodes(coupling_functions, remove_feedback=True, remove_feedforward=True,
                                           converger=converger,
                                           include_couplings_as_final_output=include_couplings_as_final_output)
        elif conv_type == self.OPTIONS_CONVERGERS[1]:  # Gauss-Seidel
            self.manipulate_coupling_nodes(coupling_functions, remove_feedback=True, remove_feedforward=False,
                                           converger=converger,
                                           include_couplings_as_final_output=include_couplings_as_final_output)
        elif conv_type == self.OPTIONS_ARCHITECTURES[2]:  # IDF
            self.manipulate_coupling_nodes(coupling_functions, remove_feedback=True, remove_feedforward=True,
                                           converger=converger,
                                           include_couplings_as_final_output=include_couplings_as_final_output)

        return

    def connect_optimizer(self, optimizer, design_variable_nodes, objective_node, constraint_nodes):
        """Method to automatically connect an optimizer w.r.t. the design variables, objective, and constraints.

        :param optimizer: name of the optimizer to be connected
        :type optimizer: basestring
        :type design_variable_nodes: list
        :param objective_node: node used as objective by the optimizer
        :type objective_node: basestring
        :param constraint_nodes: list of constraint nodes
        :type constraint_nodes: list
        :return: enriched MDAO data graph with connected optimizer
        :rtype: MdaoDataGraph
        """

        # Input assertions
        assert self.has_node(optimizer), 'Optimizer is not present in the graph.'
        assert isinstance(design_variable_nodes, list)
        for des_var in design_variable_nodes:
            assert self.has_node(des_var), 'Design variable %s is missing in the graph.' % des_var
        assert isinstance(objective_node, basestring)
        assert self.has_node(objective_node), 'Objective node %s is missing in the graph.' % objective_node
        assert isinstance(constraint_nodes, list)
        for con_var in constraint_nodes:
            assert self.has_node(con_var), 'Constraint variable %s is missing in the graph.' % con_var

        # Add attributes to the optimizer block
        self.node[optimizer]['design_variables'] = dict()
        for des_var in design_variable_nodes:
            self.node[optimizer]['design_variables'][des_var] = dict()
            if 'upper_bound' in self.node[des_var]:
                self.node[optimizer]['design_variables'][des_var]['upper_bound'] = self.node[des_var]['upper_bound']
            else:
                self.node[optimizer]['design_variables'][des_var]['upper_bound'] = None
            if 'lower_bound' in self.node[des_var]:
                self.node[optimizer]['design_variables'][des_var]['lower_bound'] = self.node[des_var]['lower_bound']
            else:
                self.node[optimizer]['design_variables'][des_var]['lower_bound'] = None
            if 'nominal_value' in self.node[des_var]:
                self.node[optimizer]['design_variables'][des_var]['nominal_value'] = self.node[des_var]['nominal_value']
            else:
                self.node[optimizer]['design_variables'][des_var]['nominal_value'] = None
        self.node[optimizer]['objective_variable'] = [objective_node]
        self.node[optimizer]['constraint_variables'] = dict()
        for con_var in constraint_nodes:
            self.node[optimizer]['constraint_variables'][con_var] = dict()
            if 'upper_bound' in self.node[con_var]:
                self.node[optimizer]['constraint_variables'][con_var]['upper_bound'] = self.node[con_var]['upper_bound']
            else:
                self.node[optimizer]['constraint_variables'][con_var]['upper_bound'] = None
            if 'lower_bound' in self.node[con_var]:
                self.node[optimizer]['constraint_variables'][con_var]['lower_bound'] = self.node[con_var]['lower_bound']
            else:
                self.node[optimizer]['constraint_variables'][con_var]['lower_bound'] = None

        # Manipulate the graph based on the architecture
        # Connect design variables to the optimizer
        pre_opt_funcs = self.graph['function_ordering'][self.FUNCTION_ROLES[3]]
        for des_var in design_variable_nodes:
            # Create initial guess design variable
            ini_guess_node = self.copy_node_as(des_var, architecture_role=self.ARCHITECTURE_ROLES_VARS[3])
            # If des_var comes from pre-des-var function, then reconnect (remove previous connection, connect to guess)
            des_var_sources = self.get_sources(des_var)
            if des_var_sources:
                pre_des_var_func = list(set(des_var_sources).intersection(pre_opt_funcs))[0]
                if pre_des_var_func:
                    self.remove_edge(pre_des_var_func, des_var)
                    self.add_edge(pre_des_var_func, ini_guess_node)
            # Connect initial guess design variable to optimizer
            self.add_edge(ini_guess_node, optimizer)
            # Connect design variable as output from optimizer
            self.add_edge(optimizer, des_var)
            # Create final design variable
            fin_value_node = self.copy_node_as(des_var, architecture_role=self.ARCHITECTURE_ROLES_VARS[4])
            # Connect final design variable as output from optimizer
            self.add_edge(optimizer, fin_value_node)
        # Connect objective and constraint nodes to the optimizer
        for var in [objective_node] + constraint_nodes:
            # Connect regular variable version to optimizer
            self.add_edge(var, optimizer)
            # Create a final value copy and connect it as output of the associated functions
            fin_value_node = self.copy_node_as(var, architecture_role=self.ARCHITECTURE_ROLES_VARS[5])
            self.add_edge(self.get_sources(var)[0], fin_value_node)
        # If the graph contains consistency constraint variables, then connect these to the optimizer as well
        consconcs_nodes = self.find_all_nodes(category='variable',
                                              attr_cond=['architecture_role', '==', self.ARCHITECTURE_ROLES_VARS[6]])
        for node in consconcs_nodes:
            rel_node = self.node[node]['related_to_schema_node']
            # Add constraint variables to optimizer attributes
            self.node[optimizer]['constraint_variables'][node] = dict()
            self.node[optimizer]['constraint_variables'][node]['upper_bound'] = 1e-6
            self.node[optimizer]['constraint_variables'][node]['lower_bound'] = -1e-6
            # Add design variables to optimizer attributes
            self.node[optimizer]['design_variables'][rel_node] = dict()
            if 'upper_bound' in self.node[rel_node]:
                self.node[optimizer]['design_variables'][rel_node]['upper_bound'] = self.node[rel_node]['upper_bound']
            else:
                self.node[optimizer]['design_variables'][rel_node]['upper_bound'] = None
            if 'lower_bound' in self.node[rel_node]:
                self.node[optimizer]['design_variables'][rel_node]['lower_bound'] = self.node[rel_node]['lower_bound']
            else:
                self.node[optimizer]['design_variables'][rel_node]['lower_bound'] = None
            self.add_edge(node, optimizer)

    def connect_doe_block(self, doe_block, design_variable_nodes, qoi_nodes):
        """Method to automatically connect an doe_block w.r.t. the design variables, objective, and constraints.

        :param doe_block: name of the doe_block to be connected
        :type doe_block: basestring
        :param design_variable_nodes: list of design variables
        :type design_variable_nodes: list
        :param qoi_nodes: list of constraint nodes
        :type qoi_nodes: list
        :return: enriched MDAO data graph with connected doe_block
        :rtype: MdaoDataGraph
        """

        # Input assertions
        assert self.has_node(doe_block), 'DOE is not present in the graph.'
        assert isinstance(design_variable_nodes, list)
        for des_var in design_variable_nodes:
            assert self.has_node(des_var), 'Design variable %s is missing in the graph.' % des_var
        assert isinstance(qoi_nodes, list)
        for qoi_var in qoi_nodes:
            assert self.has_node(qoi_var), 'Q.O.I. variable %s is missing in the graph.' % qoi_var

        # Add attributes to the doe block
        self.node[doe_block]['design_variables'] = dict()
        for des_var in design_variable_nodes:
            self.node[doe_block]['design_variables'][des_var] = dict()
            if 'upper_bound' in self.node[des_var]:
                self.node[doe_block]['design_variables'][des_var]['upper_bound'] = self.node[des_var]['upper_bound']
            else:
                self.node[doe_block]['design_variables'][des_var]['upper_bound'] = None
            if 'lower_bound' in self.node[des_var]:
                self.node[doe_block]['design_variables'][des_var]['lower_bound'] = self.node[des_var]['lower_bound']
            else:
                self.node[doe_block]['design_variables'][des_var]['lower_bound'] = None
            if 'nominal_value' in self.node[des_var]:
                self.node[doe_block]['design_variables'][des_var]['nominal_value'] = self.node[des_var][
                    'nominal_value']
            else:
                self.node[doe_block]['design_variables'][des_var]['nominal_value'] = None
            if 'samples' in self.node[des_var]:
                self.node[doe_block]['design_variables'][des_var]['samples'] = self.node[des_var]['samples']
            else:
                self.node[doe_block]['design_variables'][des_var]['samples'] = None
        self.node[doe_block]['quantities_of_interest'] = qoi_nodes

        # For the custom design table, add the table with values to the settings
        if self.graph['problem_formulation']['doe_settings']['doe_method'] == 'Custom design table':
            n_samples = len(self.node[doe_block]['design_variables'][design_variable_nodes[-1]]['samples'])
            doe_table = []
            for idj in range(n_samples):
                doe_table.append([])
                for des_var in design_variable_nodes:
                    doe_table[idj].append(self.node[des_var]['samples'][idj])
            self.graph['problem_formulation']['doe_settings']['doe_table'] = doe_table
            self.graph['problem_formulation']['doe_settings']['doe_table_order'] = design_variable_nodes

        # Manipulate the graph based on the architecture
        # Connect design variables to the doe_block
        pre_doe_funcs = self.graph['function_ordering'][self.FUNCTION_ROLES[3]]
        for des_var in design_variable_nodes:
            # Create DOE input samples
            doe_input_node = self.copy_node_as(des_var, architecture_role=self.ARCHITECTURE_ROLES_VARS[7])
            # If des_var comes from pre-des-var function then remove this connection (DOE uses separate list of samples)
            des_var_sources = self.get_sources(des_var)
            pre_des_var_funcs = list(set(des_var_sources).intersection(pre_doe_funcs))
            if pre_des_var_funcs:
                pre_des_var_func = pre_des_var_funcs[0]
                self.remove_edge(pre_des_var_func, des_var)
                # If des_var has become a hole, remove it
                if self.node_is_hole(des_var):
                    self.add_edge(pre_des_var_func, doe_input_node)
            # Connect DOE input samples to doe_block
            self.add_edge(doe_input_node, doe_block)
            # Connect design variable as output from doe_block
            self.add_edge(doe_block, des_var)
        # Connect QOI nodes to the doe_block
        for var in qoi_nodes:
            # Connect regular variable version to doe_block
            self.add_edge(var, doe_block)
            # Create a DOE output samples node and connect it as output of the DOE
            doe_output_node = self.copy_node_as(var, architecture_role=self.ARCHITECTURE_ROLES_VARS[8])
            self.add_edge(doe_block, doe_output_node)

        return

    def manipulate_coupling_nodes(self, func_order, remove_feedback, remove_feedforward, converger=None,
                                  include_couplings_as_final_output=False):
        """Method to manipulate the coupling nodes in a data graph in order to remove unwanted feedback/feedforward.

        :param func_order: the order of the functions to be analyzed
        :type func_order: list
        :param remove_feedback: setting on whether feedback coupling should be removed
        :type remove_feedback: bool
        :param remove_feedforward: setting on whether feedforward coupling should be removed
        :type remove_feedforward: bool
        :param converger: setting on whether the couplings should be linked to a converger
        :type converger: basestring or None
        :param include_couplings_as_final_output: setting on whether coupling variables should always be added as output
        :type include_couplings_as_final_output: bool
        """

        # Get all the relevant couplings
        if remove_feedback and remove_feedforward:
            direction = "both"
        elif remove_feedback and not remove_feedforward:
            direction = "backward"
        elif not remove_feedback and remove_feedforward:
            direction = "forward"
        else:
            raise IOError("Invalid settings on feedback and feedforward specific.")
        couplings = self.get_direct_coupling_nodes(func_order, direction=direction, print_couplings=False)

        # Manipulate the coupling nodes accordingly
        for coupling in couplings:
            # Remove coupling edge between coupling variable -> function
            self.remove_edge(coupling[2], coupling[1])
            # Create initial guess coupling variable node
            ini_guess_node = self.copy_node_as(coupling[2], self.ARCHITECTURE_ROLES_VARS[0])
            # If there is no converger node, then just add an initial guess of the coupled node
            if converger is None:
                # Connect initial guess as input to coupled function
                self.add_edge(ini_guess_node, coupling[1])
            # If there is a converger node, then connect it accordingly
            elif converger == self.CONVERGER_STRING:
                # Connect initial guess as input to the converger
                self.add_edge(ini_guess_node, converger)
                # Create coupling copy variable (coming from converger) and connect it accordingly
                coupling_copy_node = self.copy_node_as(coupling[2], self.ARCHITECTURE_ROLES_VARS[2])
                if not self.has_edge(converger, coupling_copy_node):
                    self.add_edge(converger, coupling_copy_node)
                self.add_edge(coupling_copy_node, coupling[1])
                # Connect original coupling node to the converger
                self.add_edge(coupling[2], self.CONVERGER_STRING)
            # If the converger node in an optimizer (IDF), then connect it accordingly
            elif converger == self.OPTIMIZER_STRING:
                # Connect initial guess as input to the optimizer
                self.add_edge(ini_guess_node, converger)
                # Create coupling copy variable (coming from converger/optimizer) and connect it accordingly
                coupling_copy_node = self.copy_node_as(coupling[2], self.ARCHITECTURE_ROLES_VARS[2])
                if not self.has_edge(converger, coupling_copy_node):
                    self.add_edge(converger, coupling_copy_node)
                self.add_edge(coupling_copy_node, coupling[1])
                # Connect original and copied coupling node to the consistency constraint function
                self.add_edge(coupling[2], self.CONSCONS_STRING)
                self.add_edge(coupling_copy_node, self.CONSCONS_STRING)
                # Create consistency constraint variables for each coupling and make them output of the function
                consistency_node = self.copy_node_as(coupling[2], self.ARCHITECTURE_ROLES_VARS[6])
                self.add_edge(self.CONSCONS_STRING, consistency_node)
                if 'consistency_nodes' in self.node[self.CONSCONS_STRING]:
                    self.node[self.CONSCONS_STRING]['consistency_nodes'].append(consistency_node)
                else:
                    self.node[self.CONSCONS_STRING]['consistency_nodes'] = [consistency_node]
            # If required, create final coupling variable node and let it come from the coupled function
            if converger and ('problem_role' in self.node[coupling[2]] or include_couplings_as_final_output):
                final_node = self.copy_node_as(coupling[2], self.ARCHITECTURE_ROLES_VARS[1])
                self.add_edge(coupling[0], final_node)
                keep_original_coupling_node = False
            elif not converger and ('problem_role' in self.node[coupling[2]] or include_couplings_as_final_output):
                keep_original_coupling_node = True
            else:
                keep_original_coupling_node = False
            # Remove original coupling node if it has become an output
            if self.node_is_output(coupling[2]) and not keep_original_coupling_node:
                self.remove_node(coupling[2])

        return
