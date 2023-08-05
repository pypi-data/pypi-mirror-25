# Imports
import logging

import networkx as nx

from ..utilities.general import format_string_for_d3js, remove_if_exists
from ..utilities.testing import check
from ..utilities.xml import Element

from graph_kadmos import KadmosGraph
from mixin_mdao import MdaoMixin


# Settings for the logger
logger = logging.getLogger(__name__)


class ProcessGraph(KadmosGraph, MdaoMixin):

    def __init__(self, *args, **kwargs):
        super(ProcessGraph, self).__init__(*args, **kwargs)

    def cleancopy(self):
        """Method to make a clean copy of a graph.

        This method can be used to avoid deep-copy problems in graph manipulation algorithms.
        The graph class is kept.

        :return: clean-copy of the graph
        :rtype: ProcessGraph
        """

        return ProcessGraph(self)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            CREATE METHODS                                                        #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _create_cmdows_workflow_process_graph(self):

        # Create workflow/processGraph
        cmdows_process_graph = Element('processGraph')
        cmdows_process_graph.add('name', self.graph.get('name'))

        # Create workflow/processGraph/edges
        cmdows_edges = cmdows_process_graph.add('edges')
        for u, v, w in self.edges_iter(data=True):
            # Create workflow/dataGraph/edges/edge
            cmdows_edge = cmdows_edges.add('edge')
            cmdows_edge.add('fromExecutableBlockUID', u)
            cmdows_edge.add('toExecutableBlockUID', v)
            cmdows_edge.add('processStepNumber', w.get('process_step'))

        # Create workflow/processGraph/nodes
        cmdows_nodes = cmdows_process_graph.add('nodes')
        for n, data in self.nodes_iter(data=True):
            # Create workflow/dataGraph/nodes/node
            cmdows_node = cmdows_nodes.add('node')
            cmdows_node.add('referenceUID', n)
            cmdows_node.add('processStepNumber', data.get('process_step'))
            cmdows_node.add('convergerStepNumber', data.get('converger_step'))
            cmdows_node.add('diagonalPosition', data.get('diagonal_position'))

        # Create workflow/processGraph/metadata
        cmdows_meta = cmdows_process_graph.add('metadata')
        graph_process_ordering = self.get_nested_process_ordering()[1]
        if len(graph_process_ordering.get('iter_nesting')):
            cmdows_loop_nesting = cmdows_meta.add('loopNesting')
            cmdows_loop_nesting.addloop(graph_process_ordering['iter_nesting'],
                                        graph_process_ordering['function_grouping'])

        return cmdows_process_graph

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                             LOAD METHODS                                                         #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _load_cmdows_workflow_process_graph(self, cmdows, nodes):

        cmdows_process_graph = cmdows.find('workflow/processGraph')
        cmdows_nodes = cmdows_process_graph.find('nodes')
        if cmdows_nodes is not None:
            for node in list(cmdows_nodes):
                # Get new node info
                new_attr_dict = {'process_step': node.findasttext('processStepNumber'),
                                 'converger_step': node.findasttext('convergerStepNumber'),
                                 'diagonal_position': node.findasttext('diagonalPosition')}
                # Copy other node info
                attr_dict = nodes[node.findtext('referenceUID')]
                attr_dict.update(new_attr_dict)
                self.add_node(node.findtext('referenceUID'), attr_dict=attr_dict)
        cmdows_edges = cmdows_process_graph.find('edges')
        if cmdows_edges is not None:
            for edge in list(cmdows_edges):
                self.add_edge(edge.findtext('fromExecutableBlockUID'), edge.findtext('toExecutableBlockUID'),
                              attr_dict={'process_step': int(edge.findtext('processStepNumber'))})


class MdaoProcessGraph(ProcessGraph):

    ARCHITECTURE_CATS = {'all iterative blocks': ['optimizer', 'converger', 'doe'],
                         'all design variables': ['initial guess design variable', 'final design variable'],
                         'all pre-iter analyses': ['pre-coupling analysis', 'pre-iterator analysis']}

    def __init__(self, *args, **kwargs):
        super(MdaoProcessGraph, self).__init__(*args, **kwargs)
        if 'fpg' in kwargs and 'mg_function_ordering' in kwargs:
            fpg = kwargs['fpg']
            mg_function_ordering = kwargs['mg_function_ordering']
            from graph_data import FundamentalProblemGraph
            assert isinstance(fpg, FundamentalProblemGraph)
            fpg.check(raise_error=True)
            self._add_action_blocks(fpg, mg_function_ordering)
            self.graph['function_ordering'] = mg_function_ordering
            del self.graph['fpg']

    def cleancopy(self):
        """Method to make a clean copy of a graph.

        This method can be used to avoid deep-copy problems in graph manipulation algorithms.
        The graph class is kept.

        :return: clean-copy of the graph
        :rtype: MdaoProcessGraph
        """

        return MdaoProcessGraph(self)

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                            CHECKING METHODS                                                      #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _check_category_a(self):
        """Extended method to perform a category A check on the graph.

        :return: result of the check and index
        :rtype: bool, int
        """

        # Set check
        category_check, i = super(MdaoProcessGraph, self)._check_category_a()

        # Get nodes
        func_nodes = self.find_all_nodes(category='function')
        var_nodes = self.find_all_nodes(category='variable')

        # Get information
        n_nodes = self.number_of_nodes()
        n_functions = len(func_nodes)
        n_variables = len(var_nodes)

        # Checks on nodes
        category_check, i = check(n_variables != 0,
                                  'There are variable nodes present in the graph, namely: %s.' % str(var_nodes),
                                  status=category_check,
                                  category='A',
                                  i=i)
        category_check, i = check(n_nodes != n_functions,
                                  'The number of total nodes does not match number of function nodes.',
                                  status=category_check,
                                  category='A',
                                  i=i)
        for node in func_nodes:
            category_check, i_not = check('process_step' not in self.node[node],
                                          'The process_step attribute is missing on the node %s.' % node,
                                          status=category_check,
                                          category='A',
                                          i=i)
            category_check, i_not = check('architecture_role' not in self.node[node],
                                          'The architecture_role attribute is missing on the node %s.' % node,
                                          status=category_check,
                                          category='A',
                                          i=i+1)
            category_check, i_not = check(not self.has_node(self.COORDINATOR_STRING),
                                          'The %s node is missing in the graph.' % self.COORDINATOR_STRING,
                                          status=category_check,
                                          category='A',
                                          i=i+2)
        i += 3

        # Check on edges
        for u, v, d in self.edges_iter(data=True):
            category_check, i_not = check('process_step' not in d,
                                          'The process_step attribute missing for the edge %s --> %s.' % (u, v),
                                          status=category_check,
                                          category='A',
                                          i=i)
        i += 1

        # Return
        return category_check, i

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                              PRINTING METHODS                                                    #
    # ---------------------------------------------------------------------------------------------------------------- #

    def inspect_process(self):
        """Method to print the MPG."""

        print '\n- - - - - - - - - - -'
        print ' PROCESS INSPECTION  '
        print '- - - - - - - - - - -\n'
        print '\nNODES\n'
        for idx in range(0, self.number_of_nodes()):
            nodes = self.find_all_nodes(attr_cond=['diagonal_position', '==', idx])
            for node in nodes:
                print '- - - - -'
                print node
                print 'process step: ' + str(self.node[node]['process_step'])
                print 'diag pos: ' + str(self.node[node]['diagonal_position'])
                if 'converger_step' in self.node[node]:
                    print 'converger step: ' + str(self.node[node]['converger_step'])
        print '\nEDGES\n'
        for idx in range(0, self.number_of_edges() + 1):
            for u, v, d in self.edges_iter(data=True):
                if d['process_step'] == idx:
                    print '- - - - -'
                    print u + ' ---> ' + v
                    print d['process_step']
        print '- - - - - - - - - - -\n'

    # ---------------------------------------------------------------------------------------------------------------- #
    #                                          GRAPH SPECIFIC METHODS                                                  #
    # ---------------------------------------------------------------------------------------------------------------- #

    def _add_action_blocks(self, fpg, mg_function_ordering):
        """Method to add the different action blocks to the MPG based on the FPG and based on FPG function ordering.

        :param fpg: fundamental problem graph
        :type fpg: FundamentalProblemGraph
        :param mg_function_ordering: ordered list of functions to be added
        :type mg_function_ordering: list
        """

        # TODO: Check if this method can be combined with _add_action_blocks_and_roles method in the mixin_mdao
        # Is the only difference the diagonal position?

        # Load/set input settings
        diag_pos = 0
        mdao_arch = fpg.graph['problem_formulation']['mdao_architecture']

        # Add coordinator node
        assert not fpg.has_node(self.COORDINATOR_STRING), 'Coordinator name already in use in FPG.'
        self.add_node(self.COORDINATOR_STRING,
                      category='function',
                      architecture_role=self.ARCHITECTURE_ROLES_FUNS[0],
                      shape='8',
                      label=self.COORDINATOR_LABEL,
                      level=None,
                      diagonal_position=diag_pos)
        diag_pos += 1

        # No optimizer present
        if self.FUNCTION_ROLES[0] in mg_function_ordering:
            functions = mg_function_ordering[self.FUNCTION_ROLES[0]]
            for func in functions:
                self.add_node(func, fpg.node[func],
                              diagonal_position=diag_pos,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[4])
                diag_pos += 1

        # Optimizer / DOE present
        if self.FUNCTION_ROLES[3] in mg_function_ordering:
            # Add pre-optimizer functions
            functions = mg_function_ordering[self.FUNCTION_ROLES[3]]
            for func in functions:
                self.add_node(func, fpg.node[func],
                              diagonal_position=diag_pos,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[5])
                diag_pos += 1
            # Add optimizer / DOE
            if mdao_arch in self.OPTIONS_ARCHITECTURES[2:5]:  # IDF, MDF, unc-OPT
                assert not fpg.has_node(self.OPTIMIZER_STRING), 'Optimizer name already in use in FPG.'
                self.add_node(self.OPTIMIZER_STRING,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[1],
                              shape='8',
                              label=self.OPTIMIZER_LABEL,
                              level=None,
                              diagonal_position=diag_pos)
            elif mdao_arch in self.OPTIONS_ARCHITECTURES[5:7]:  # unc-DOE, con-DOE
                assert not fpg.has_node(self.DOE_STRING), 'DOE name already in use in FPG.'
                self.add_node(self.DOE_STRING,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[3],
                              shape='8',
                              label=self.DOE_LABEL,
                              level=None,
                              diagonal_position=diag_pos)
            diag_pos += 1
            # Add post-optimizer functions
            functions = mg_function_ordering[self.FUNCTION_ROLES[4]]
            for func in functions:
                self.add_node(func, fpg.node[func],
                              diagonal_position=diag_pos,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[6])
                diag_pos += 1

        # Converger required
        if mdao_arch in [self.OPTIONS_ARCHITECTURES[1]] + [self.OPTIONS_ARCHITECTURES[3]] + \
                [self.OPTIONS_ARCHITECTURES[6]]:  # con-MDA, MDF, con-DOE
            # Add converger
            assert not fpg.has_node(self.CONVERGER_STRING), 'Converger name already in use in FPG.'
            self.add_node(self.CONVERGER_STRING,
                          category='function',
                          architecture_role=self.ARCHITECTURE_ROLES_FUNS[2],
                          shape='8',
                          label=self.CONVERGER_LABEL,
                          level=None,
                          diagonal_position=diag_pos)
            diag_pos += 1

        # Add coupled functions
        for func in mg_function_ordering[self.FUNCTION_ROLES[1]]:
            self.add_node(func, fpg.node[func],
                          diagonal_position=diag_pos,
                          category='function',
                          architecture_role=self.ARCHITECTURE_ROLES_FUNS[7])
            diag_pos += 1

        # Add post-coupling functions
        for func in mg_function_ordering[self.FUNCTION_ROLES[2]]:
            if func != self.CONSCONS_STRING:
                self.add_node(func, fpg.node[func],
                              diagonal_position=diag_pos,
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[8])
            else:
                assert not fpg.has_node(self.CONSCONS_STRING), 'Consistency constraint name already in use in FPG.'
                self.add_node(self.CONSCONS_STRING,
                              label=self.CONSCONS_LABEL,
                              diagonal_position=diag_pos,
                              level=None,
                              shape='s',
                              category='function',
                              architecture_role=self.ARCHITECTURE_ROLES_FUNS[9])
            diag_pos += 1

        return

    def add_simple_sequential_process(self, functions, start_step, end_in_iterative_node=None):
        """Method to add a simple sequential process to a list of functions.

        The sequence is assumed to be the order of the functions in the input list. The sequence is considered simple,
        since it is not analyzed for the possibility to run functions in parallel.

        :param functions: list of functions in the required sequence
        :type functions: list
        :param start_step:
        :type start_step:
        :param end_in_iterative_node: (optional) iterative node to which the last function should go
        :type end_in_iterative_node: basestring
        """

        # Input assertions and checks
        assert isinstance(functions, list)
        assert len(functions) > 0, 'Sequence cannot be an empty list.'
        assert len(functions) == len(set(functions))
        assert isinstance(start_step, int) and start_step >= 0, 'Start step should be a positive integer.'
        if end_in_iterative_node:
            assert self.has_node(end_in_iterative_node), 'Node %s is not present in the graph' % end_in_iterative_node

        # Add sequence process lines
        from_node = functions[0]
        step = start_step + 1

        if len(functions) > 1:
            for node in functions[1:]:
                self.node[node]['process_step'] = step
                self.add_edge(from_node, node, process_step=step)
                from_node = node
                step += 1

        # Add process edge back to first function if loop needs to be closed
        if end_in_iterative_node:
            self.add_edge(from_node, end_in_iterative_node, process_step=step)
            self.node[end_in_iterative_node]['converger_step'] = step

        return

    def add_optimal_sequential_process(self):

        # TODO: Add this method (as an option?)!!!

        pass

    def add_parallel_process(self, start_nodes, parallel_functions, start_step, end_node=None, end_in_converger=False,
                             use_data_graph=None):
        """Method to add a process to run multiple functions in parallel from a single start node.

        :param start_nodes: node or list of nodes from which all the functions are executed in parallel
        :type start_nodes: basestring or list
        :param parallel_functions: list of function to be run in parallel from the start node
        :type parallel_functions: list
        :param start_step: process step number of the start_node
        :type start_step: int
        :param end_node: (optional) node to which all the parallel functions go after execution
        :type end_node: basestring
        :param end_in_converger: (optional) indicate whether the end node finishes a convergence loop
        :type end_in_converger: bool
        :param use_data_graph: (optional) use data graph to assess whether nodes are actually coupled
        :type use_data_graph: MdaoDataGraph or None
        """

        # Input assertions and checks
        if isinstance(start_nodes, list):
            for node in start_nodes:
                assert self.has_node(node), 'Start node %s not present in the graph.' % start_nodes
        else:
            assert self.has_node(start_nodes), 'Start node %s not present in the graph.' % start_nodes
            start_nodes = [start_nodes]
        assert self.has_nodes(parallel_functions), 'One of the parallel nodes is not present in the graph.'
        assert len(parallel_functions) > 1, 'Parallel functions list should have more than one function.'
        assert len(parallel_functions) == len(set(parallel_functions)), 'Parallel list can only have unique functions.'
        assert isinstance(start_step, int) and start_step >= 0, 'Start step should be a positive integer.'
        if end_node:
            assert self.has_node(end_node), 'End node %s is not present in the graph.' % end_node
            assert isinstance(end_in_converger, bool)
        if use_data_graph:
            assert isinstance(use_data_graph, KadmosGraph)

        # Add parallel process lines
        for node in parallel_functions:
            for start_node in start_nodes:
                if use_data_graph:
                    if use_data_graph.get_direct_coupling_nodes(start_node, node, direction='forward'):
                        make_connection = True
                    else:
                        make_connection = False
                else:
                    make_connection = True
                if make_connection:
                    self.node[node]['process_step'] = start_step + 1
                    self.add_edge(start_node, node, process_step=start_step + 1)
            # Add process edge back to end node if one is given
            if end_node:
                self.add_edge(node, end_node, process_step=start_step + 2)
        if end_node:
            if end_in_converger:
                self.node[end_node]['converger_step'] = start_step + 2
            else:
                self.node[end_node]['process_step'] = start_step + 2

        return

    def connect_nested_iterators(self, master, slave):
        """Method to connect a slave iterator to a master iterator in a nested configuration.

        An example is if a converger inside an optimizer in MDF needs to be linked back.

        :param master: upper iterator node in the nested configuration
        :type master: basestring
        :param slave: lower iterator node in the nested configuration
        :type slave: basestring
        """

        assert self.has_node(master), 'Node %s not present in the graph.' % master
        assert self.has_node(slave), 'Node %s not present in the graph.' % slave
        assert 'converger_step' in self.node[slave], 'Slave node %s needs to have a converger_step.' % slave
        self.add_edge(slave, master, process_step=self.node[slave]['converger_step'] + 1)
        self.node[master]['converger_step'] = self.node[slave]['converger_step'] + 1

        return

    def get_node_text(self, node):
        """Method to determine the text of a function node (for use in a XDSM diagram).

        :param node: node
        :type node: basestring
        :return: node text for in the XDSM function box
        :rtype: basestring
        """

        if 'converger_step' in self.node[node] and node != self.COORDINATOR_STRING:
            node_text = ('$' + str(self.node[node]['process_step']) + ',' + str(self.node[node]['converger_step']) +
                         '\to' + str(self.node[node]['process_step'] + 1) +
                         '$:\\' + self.node[node].get('label', str(node)))
        elif 'converger_step' in self.node[node] and node == self.COORDINATOR_STRING:
            node_text = ('$' + str(self.node[node]['process_step']) + ',' + str(self.node[node]['converger_step']) +
                         '$:\\' + self.node[node].get('label', str(node)))
        elif 'process_step' in self.node[node]:
            node_text = ('$' + str(self.node[node]['process_step']) + '$:\\' + self.node[node].get('label', str(node)))
        else:
            node_text = self.node[node].get('label', str(node))

        return node_text

    def get_process_list(self, use_d3js_node_ids=True):
        """Method to get the xdsm workflow process list (for use in dynamic visualizations).

        :param use_d3js_node_ids: setting whether node names should be changed into node ids according to D3js notation.
        :type use_d3js_node_ids: bool
        :return: process list
        :rtype: list
        """

        # Input assertions
        assert isinstance(use_d3js_node_ids, bool)

        # Find first diagonal node
        first_nodes = self.find_all_nodes(attr_cond=['diagonal_position', '==', 0])
        assert len(first_nodes) == 1, 'Only one node per diagonal position is allowed.'
        first_node = first_nodes[0]
        assert 'converger_step' in self.node[first_node], 'First diagonal node should have a converger_step attribute.'
        max_step = self.node[first_node]['converger_step']
        process_list = []
        for step in range(0, max_step+1):
            process_list.append({'step_number': step,
                                 'process_step_blocks': [],
                                 'converger_step_blocks': [],
                                 'edges': []})
            process_step_nodes = self.find_all_nodes(attr_cond=['process_step', '==', step])
            converger_step_nodes = self.find_all_nodes(attr_cond=['converger_step', '==', step])
            if not process_step_nodes and not converger_step_nodes:
                raise IOError('Process block data missing for step %d.' % step)
            elif process_step_nodes and converger_step_nodes:
                raise IOError('Invalid process block data for step %d.' % step)
            # In case of regular process steps, determine their list positions
            for step_node in process_step_nodes:
                if use_d3js_node_ids:
                    node_name = format_string_for_d3js(step_node, prefix='id_')
                else:
                    node_name = step_node
                process_list[step]['process_step_blocks'].append(node_name)
            for step_node in converger_step_nodes:
                if use_d3js_node_ids:
                    node_name = format_string_for_d3js(step_node, prefix='id_')
                else:
                    node_name = step_node
                process_list[step]['converger_step_blocks'].append(node_name)
            for edge in self.edges_iter(data=True):
                if edge[2]['process_step'] == step:
                    if use_d3js_node_ids:
                        edge0_name = format_string_for_d3js(edge[0], prefix='id_')
                        edge1_name = format_string_for_d3js(edge[1], prefix='id_')
                    else:
                        edge0_name = edge[0]
                        edge1_name = edge[1]
                    process_list[step]['edges'].append((edge0_name, edge1_name))

        return process_list

    def get_nested_process_ordering(self):
        """Method to determine the nesting of iterative elements in the process graph.

        :return: tuple with iterative_nodes, process_info dictionary, and nested_functions list
        :rtype: tuple
        """

        # Local variables
        coor_str = self.COORDINATOR_STRING

        # Make cleancopy of the graph
        graph = self.cleancopy()

        # Determine the iterative nodes present in the graph (coordinator, optimizer, doe, converger)
        iterative_nodes = graph.find_all_nodes(attr_cond=['architecture_role', 'in',
                                                          graph.ARCHITECTURE_CATS['all iterative blocks']])

        # Get the precoup and preiter functions and remove them
        ignored_funcs = graph.find_all_nodes(attr_cond=['architecture_role', 'in',
                                                        graph.ARCHITECTURE_CATS['all pre-iter analyses']])

        # Use the MPG to find the architecture of iterative nodes (nested, parallel, etc)
        mpg_cycles = nx.simple_cycles(nx.DiGraph(graph))
        ini_cycles = []
        top_level_iterators = set()
        for node_list in mpg_cycles:
            # Find the cycles that have the Coordinator object in them
            if coor_str in node_list:
                assert graph.node[coor_str]['diagonal_position'] == 0, "Position of coordinator is expected at 0."
                ini_cycles.append(node_list)
            # Find the top-level iterators (these are iterators that are in a cycle with the Coordinator)
            if coor_str in node_list and set(node_list).intersection(set(iterative_nodes)):
                tli = list(set(node_list).intersection(set(iterative_nodes)))
                top_level_iterators.update(tli)
        # If an iterators is not top level, then it should be nested somehow
        nested_iterators = set(iterative_nodes).difference(top_level_iterators)

        # As the top-level and nested iterators have been found, we can now use a new loop to identify which nodes
        # belong to each other. So how the nested iterators belong to top-level iterators and which nodes are part of
        # the nested iterators.
        process_iter_nesting = dict()
        process_func_nesting = dict()
        mpg_cycles = nx.simple_cycles(nx.DiGraph(graph))
        for node_list in mpg_cycles:
            nested_iter = set(node_list).intersection(nested_iterators)
            top_iter = set(node_list).intersection(top_level_iterators)
            if nested_iter and top_iter:
                assert len(top_iter) == 1, 'Only one top-level iterator can be in a cycle.'
                assert len(nested_iter) == 1, 'Only one nested iterator can be in a cycle (for now).'
                if list(top_iter)[0] in process_iter_nesting and list(nested_iter)[0] not in \
                        process_iter_nesting[list(top_iter)[0]]:
                    process_iter_nesting[list(top_iter)[0]].append(list(nested_iter)[0])
                else:
                    process_iter_nesting[list(top_iter)[0]] = [list(nested_iter)[0]]
                # Add the functions on these cycles to the top-level iterator
                function_nodes = node_list
                function_nodes.remove(list(top_iter)[0])
                function_nodes.remove(list(nested_iter)[0])
                function_nodes = remove_if_exists(function_nodes, ignored_funcs)
                if list(top_iter)[0] in process_func_nesting:
                    process_func_nesting[list(top_iter)[0]].update(function_nodes)
                else:
                    process_func_nesting[list(top_iter)[0]] = set(function_nodes)

            # For the internal cycles of the nested loop, add the functions that are part of the nested iterator to
            # a dict
            elif nested_iter and not top_iter:
                assert len(nested_iter) == 1, 'Only one nested iterator can be in a cycle (for now).'
                function_nodes = node_list
                function_nodes.remove(list(nested_iter)[0])
                function_nodes = remove_if_exists(function_nodes, ignored_funcs)
                if list(nested_iter)[0] in process_func_nesting:
                    process_func_nesting[list(nested_iter)[0]].update(function_nodes)
                else:
                    process_func_nesting[list(nested_iter)[0]] = set(function_nodes)
            # For the top-level iterators, also add the functions associated with the iterator
            elif not nested_iter and top_iter:
                assert len(top_iter) == 1, 'Only one nested iterator can be in a cycle (for now).'
                function_nodes = node_list
                function_nodes.remove(list(top_iter)[0])
                function_nodes = remove_if_exists(function_nodes, ignored_funcs)
                if coor_str in function_nodes:
                    function_nodes.remove(coor_str)
                if list(top_iter)[0] in process_func_nesting:
                    process_func_nesting[list(top_iter)[0]].update(function_nodes)
                else:
                    process_func_nesting[list(top_iter)[0]] = set(function_nodes)

        # Make functions sets into lists
        for key, item in process_func_nesting.iteritems():
            process_func_nesting[key] = list(item)

        # Create final dictionary with process info
        process_info = dict(iter_nesting=process_iter_nesting, function_grouping=process_func_nesting)

        # Determine all the functions that are nested into a nested iterator
        nested_functions = []
        for top_iter, nested_iters in process_info['iter_nesting'].iteritems():
            for nested_iter in nested_iters:
                nested_functions.extend(process_info['function_grouping'][nested_iter])

        return iterative_nodes, process_info, nested_functions
