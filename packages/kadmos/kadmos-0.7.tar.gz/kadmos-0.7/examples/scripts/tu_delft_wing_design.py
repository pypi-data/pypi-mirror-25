# Imports
import os
import logging

from collections import OrderedDict

from kadmos.knowledgebase import KnowledgeBase
from kadmos.graph import FundamentalProblemGraph
from kadmos.utilities.general import get_mdao_setup


# Settings for logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)

# List of MDAO definitions that can be wrapped around the problem
mdao_definitions = ['unconverged-MDA-GS',  # 0
                    'unconverged-MDA-J',   # 1
                    'converged-MDA-GS',    # 2
                    'converged-MDA-J',     # 3
                    'unconverged-DOE-GS',  # 4
                    'unconverged-DOE-J',   # 5
                    'converged-DOE-GS',    # 6
                    'converged-DOE-J',     # 7
                    'unconverged-OPT-GS',  # 8
                    'unconverged-OPT-J',   # 9
                    'MDF-GS',              # 10
                    'MDF-J',               # 11
                    'IDF']                 # 12

# Settings for scripting
mdao_definitions_loop_all = True      # Option for looping through all MDAO definitions
mdao_definition_id = 12               # Option for selecting a MDAO definition (in case mdao_definitions_loop_all=False)

# Settings for creating the CMDOWS files
create_rcg_cmdows = True              # Option for creating the RCG CMDOWS file, set to False to save time

# Settings for creating visualizations
create_vis = True                     # Create visualisations
create_rcg_vis = True                 # Create RCG visualizations, set to False after first execution to save time

# Settings for loading and saving
kb_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../knowledgebases')
pdf_dir = 'tu_delft_wing_design/(X)DSM'
cmdows_dir = 'tu_delft_wing_design/CMDOWS'
kdms_dir = 'tu_delft_wing_design/KDMS'
vistoms_dir = 'tu_delft_wing_design/VISTOMS'


print 'Loading knowledge base...'

kb = KnowledgeBase(kb_dir, 'tu_delft_wing_design')


print 'Loading repository connectivity graph...'

rcg = kb.get_rcg()


print 'Scripting RCG...'

# A name and a description are added to the graph
rcg.graph['name'] = 'RCG'
rcg.graph['description'] = 'Repository of aircraft design tools from Delft University of Technology.'

# Add some (optional) organization information
contacts = [{'attrib': {'uID': 'ivangent'}, 'name': 'Imco van Gent', 'email': 'i.vangent@tudelft.nl', 'company': 'TU Delft'},
            {'attrib': {'uID': 'lmuller'}, 'name': 'Lukas Muller', 'email': 'l.muller@student.tudelft.nl', 'company': 'TU Delft'}]
architects = [{'contactUID': 'ivangent'}, {'contactUID': 'lmuller'}]
integrators = [{'contactUID': 'lmuller'}]
rcg.graph['organization'] = OrderedDict([('contacts', contacts),
                                         ('organigram', {'architects': architects,
                                                         'integrators': integrators})])
rcg.node['MTOW']['general_info'].update({'owner': {'contact_u_i_d': 'ivangent'}})

# Add some (optional) equations
rcg.add_equation_labels(rcg.get_function_nodes())
rcg.remove_edge('OBJ', '/cpacs/mdodata/objectives/mtow/normalized_mtow_list')
rcg.add_equation('OBJ', 'mass/mtow_ref', 'Python')
rcg.add_equation('OBJ', 'mass/mtow\_ref', 'LaTeX')
rcg.add_equation('OBJ', '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>m</mi><mi>a</mi><mi>s</mi><mi>s</mi><mo>/</mo><mi>m</mi><mi>t</mi><mi>o</mi><mi>w</mi><mi>_</mi><mi>r</mi><mi>e</mi><mi>f</mi></math>', 'MathML')

# Define function order for visualization (otherwise the functions will be placed randomly on the diagonal)
functions = ['HANGAR[AGILE_DC1_WP6_wing_startpoint]',
             'HANGAR[AGILE_DC1_L0_MDA]',
             'HANGAR[AGILE_DC1_L0_wing]',
             'HANGAR[Boxwing_AGILE_Hangar]',
             'HANGAR[D150_AGILE_Hangar]',
             'HANGAR[NASA_CRM_AGILE_Hangar]',
             'HANGAR[ATR72_AGILE_Hangar]',
             'INITIATOR',
             'SCAM[wing_taper_morph]',
             'SCAM[wing_sweep_morph]',
             'SCAM[wing_dihedral_morph]',
             'SCAM[wing_root_chord_morph]',
             'SCAM[wing_length_morph]',
             'GACA[mainWingRefArea]',
             'GACA[mainWingFuelTankVol]',
             'Q3D[VDE]',
             'Q3D[FLC]',
             'Q3D[APM]',
             'EMWET',
             'SMFA',
             'PHALANX[Full_Lookup]',
             'PHALANX[Full_Simple]',
             'PHALANX[Symmetric_Lookup]',
             'PHALANX[Symmetric_Simple]',
             'PROTEUS',
             'MTOW',
             'OBJ',
             'CNSTRNT[wingLoading]',
             'CNSTRNT[fuelTankVolume]']

# Create a DSM and a VISTOMS visualization of the RCG
if create_vis and create_rcg_vis:
    rcg.create_dsm('RCG', include_system_vars=True, summarize_vars=True, function_order=functions,
                   destination_folder=pdf_dir)
    rcg.vistoms_create(vistoms_dir, function_order=functions)

# Save CMDOWS file
if create_rcg_cmdows:
    rcg.save('RCG',
             file_type='cmdows',
             description='RCG CMDOWS file of the repository of aircraft design tools from Delft University of Technology',
             creator='Lukas Mueller',
             version='0.1',
             destination_folder=cmdows_dir,
             pretty_print=True,
             integrity=True)


# On to the wrapping of the MDAO architectures
# Get iterator (all or single one)
if not mdao_definitions_loop_all:
    mdao_definitions = [mdao_definitions[mdao_definition_id]]

for mdao_definition in mdao_definitions:

    print 'Scripting ' + str(mdao_definition) + '...'

    # Reset FPG
    fpg = FundamentalProblemGraph(rcg)
    fpg.graph['name'] = rcg.graph['name'] + ' - ' + mdao_definition + ' - FPG'
    fpg.graph['description'] = 'Fundamental problem graph to solve the wing design problem using the strategy: ' \
                               + mdao_definition + '.'

    # Remove the functions from the FPG that are not needed
    fpg.remove_function_nodes('INITIATOR', 'PROTEUS', 'PHALANX[Symmetric_Lookup]', 'PHALANX[Full_Lookup]',
                              'PHALANX[Full_Simple]', 'PHALANX[Symmetric_Simple]',
                              'HANGAR[AGILE_DC1_L0_wing]',
                              'HANGAR[AGILE_DC1_L0_MDA]',
                              'HANGAR[ATR72_AGILE_Hangar]',
                              'HANGAR[Boxwing_AGILE_Hangar]',
                              'HANGAR[D150_AGILE_Hangar]',
                              'HANGAR[NASA_CRM_AGILE_Hangar]',
                              'Q3D[APM]')

    # Contract the FPG to the smallest graph size possible for wrapping the architectures
    # Contract SCAM function modes into one node
    fpg = fpg.merge_function_modes('SCAM', 'wing_length_morph', 'wing_taper_morph', 'wing_root_chord_morph',
                                   'wing_sweep_morph', 'wing_dihedral_morph')
    if mdao_definition in ['unconverged-MDA-GS', 'unconverged-MDA-J', 'converged-MDA-GS', 'converged-MDA-J']:
        fpg.remove_function_nodes('SCAM-merged[5modes]')

    # Contract GAGA function modes into one node
    fpg = fpg.merge_function_modes('GACA', 'mainWingFuelTankVol', 'mainWingRefArea')

    # Contract CNSTRNT function modes into one node
    fpg = fpg.merge_function_modes('CNSTRNT', 'fuelTankVolume', 'wingLoading')

    # Add some (optional) equations (this time without MathML)
    # This is only done here as merging functions with equations does not yet work in KADMOS
    # TODO: Include this functionality in the merge_function_nodes method
    fpg.add_equation_labels(fpg.get_function_nodes())
    fpg.remove_edge('CNSTRNT-merged[2modes]', '/cpacs/mdodata/constraints/wingLoading/listOfValues')
    fpg.remove_edge('CNSTRNT-merged[2modes]', '/cpacs/mdodata/constraints/fuelTankVolume/listOfValues')
    fpg.add_equation(('CNSTRNT-merged[2modes]', '/cpacs/mdodata/constraints/fuelTankVolume/latestValue'), 'mass_mtow*9.81/area/maxWingLoading-1.0', 'Python')
    fpg.add_equation(('CNSTRNT-merged[2modes]', '/cpacs/mdodata/constraints/fuelTankVolume/latestValue'), 'mass\_mtow\times9.81/area/maxWingLoading-1.0', 'LaTeX'),
    fpg.add_equation(('CNSTRNT-merged[2modes]', '/cpacs/mdodata/constraints/wingLoading/latestValue'), '(mass_fuel/fuelDensity)/(optimalVolume*fuelTankEfficiencyFactor)-1.0', 'Python')
    fpg.add_equation(('CNSTRNT-merged[2modes]', '/cpacs/mdodata/constraints/wingLoading/latestValue'), '(mass\_fuel/fuelDensity)/(optimalVolume\times fuelTankEfficiencyFactor)-1.0', 'LaTeX'),

    # Group Q3D[APM] and SMFA
    fpg = fpg.merge_sequential_functions('Q3D[VDE]', 'SMFA')

    # Group Q3D[FLC] and EMWET into a service
    fpg = fpg.merge_sequential_functions('Q3D[FLC]', 'EMWET')

    # Find and fix problematic nodes w.r.t. HANGAR tool
    fpg.disconnect_problematic_variables_from('HANGAR[AGILE_DC1_WP6_wing_startpoint]')

    # Define FPG function order after function contractions and export visualizations
    function_order = ['HANGAR[AGILE_DC1_WP6_wing_startpoint]',
                      'SCAM-merged[5modes]',
                      'GACA-merged[2modes]',
                      'Q3D[FLC]-EMWET--seq',
                      'Q3D[VDE]-SMFA--seq',
                      'MTOW',
                      'OBJ',
                      'CNSTRNT-merged[2modes]']
    if mdao_definition in ['unconverged-MDA-GS', 'unconverged-MDA-J', 'converged-MDA-GS', 'converged-MDA-J']:
        function_order.remove('SCAM-merged[5modes]')

    # Determine the three main settings: architecture, convergence type and unconverged coupling setting
    mdao_architecture, convergence_type, allow_unconverged_couplings = get_mdao_setup(mdao_definition)

    # Determine the feedback coupling
    feedback_couplings = fpg.get_direct_coupling_nodes('Q3D[FLC]-EMWET--seq', 'Q3D[VDE]-SMFA--seq', 'MTOW',
                                                       direction='backward', print_couplings=False)

    # Define settings of the problem formulation
    fpg.graph['problem_formulation'] = dict()
    fpg.graph['problem_formulation']['function_order'] = function_order
    fpg.graph['problem_formulation']['mdao_architecture'] = mdao_architecture
    fpg.graph['problem_formulation']['convergence_type'] = convergence_type
    fpg.graph['problem_formulation']['allow_unconverged_couplings'] = allow_unconverged_couplings
    if mdao_architecture in ['unconverged-DOE', 'converged-DOE']:
        fpg.graph['problem_formulation']['doe_settings'] = dict()
        fpg.graph['problem_formulation']['doe_settings']['doe_method'] = 'Custom design table'
        if fpg.graph['problem_formulation']['doe_settings']['doe_method'] in ['Latin hypercube design',
                                                                              'Monte Carlo design']:
            fpg.graph['problem_formulation']['doe_settings']['doe_seed'] = 6
            fpg.graph['problem_formulation']['doe_settings']['doe_runs'] = 5
        elif fpg.graph['problem_formulation']['doe_settings']['doe_method'] in ['Full factorial design']:
            fpg.graph['problem_formulation']['doe_settings']['doe_runs'] = 5

    # Define the special_input_nodes (you can also take these from the visualizations package)
    special_input_nodes = ['/cpacs/toolspecific/sCAM/wing_length_morph/required_length',
                           '/cpacs/toolspecific/sCAM/wing_dihedral_morph/required_wing_dihedral',
                           '/cpacs/toolspecific/sCAM/wing_root_chord_morph/required_root_chord',
                           '/cpacs/toolspecific/sCAM/wing_taper_morph/required_taper1',
                           '/cpacs/toolspecific/sCAM/wing_taper_morph/required_taper2',
                           '/cpacs/toolspecific/sCAM/wing_sweep_morph/required_sweep1',
                           '/cpacs/toolspecific/sCAM/wing_sweep_morph/required_sweep2']

    # Settings of design variables
    sample_ranges = [[16.32982, 16.33982, 16.34982],              # required_length
                     [5.900, 6.000, 6.100],                       # required_wing_dihedral
                     [6.2923, 6.3923, 6.4923],                    # required_root_chord
                     [0.4151, 0.4251, 0.4351],                    # required_taper1
                     [0.1545182485, 0.1645182485, 0.1745182485],  # required_taper2
                     [33.1273, 33.2273, 33.3273],                 # required_sweep1
                     [28.3037, 28.4037, 28.5037]]                 # required_sweep2
    lower_bounds = [value[0] for value in sample_ranges]
    nominal_values = [value[1] for value in sample_ranges]
    upper_bounds = [value[2] for value in sample_ranges]

    # Settings of constraint variables
    cnstrnt_lower_bounds = [-1e99, -1e99]
    cnstrnt_upper_bounds = [0.0, 0.0]

    special_output_nodes = ['/cpacs/mdodata/objectives/mtow/normalized_mtow',
                            '/cpacs/mdodata/constraints/wingLoading/latestValue',
                            '/cpacs/mdodata/constraints/fuelTankVolume/latestValue']

    qoi_nodes = ['/cpacs/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure/massDescription/mass',
                 '/cpacs/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/fuel/massDescription/mass',
                 '/cpacs/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/designMasses/mTOM/mass']

    # Function to check the graph for collisions and holes. Collisions are solved based on the function order and holes
    # will simply be removed.
    fpg.make_all_variables_valid()

    # Depending on the architecture, set the design variables, objective, constraints, and QOIs as expected.
    if mdao_architecture in ['unconverged-OPT', 'MDF', 'IDF', 'unconverged-DOE', 'converged-DOE']:
        # Set design variables
        fpg.mark_as_design_variable(special_input_nodes,
                                    lower_bounds=lower_bounds,
                                    nominal_values=nominal_values,
                                    upper_bounds=upper_bounds,
                                    samples=sample_ranges)
    if mdao_architecture in ['unconverged-OPT', 'MDF', 'IDF']:
        # Set objective and constraints
        fpg.mark_as_objective(special_output_nodes[0])
        fpg.mark_as_constraint(special_output_nodes[1:],
                               lower_bounds=cnstrnt_lower_bounds,
                               upper_bounds=cnstrnt_upper_bounds)
    elif mdao_architecture in ['unconverged-MDA', 'converged-MDA', 'unconverged-DOE', 'converged-DOE']:
        # TODO: This should work for all options
        if mdao_architecture == 'unconverged-DOE':
            qoi_nodes += special_output_nodes
        else:
            qoi_nodes = special_output_nodes
        fpg.mark_as_qoi(qoi_nodes)

    # For the unconverged-MDA-Jacobi remove the Q3D[FLC]-EMWET--seq function
    if mdao_definition in ['unconverged-MDA-J', 'unconverged-DOE-J', 'unconverged-OPT-J']:
        fpg.remove_function_nodes('Q3D[FLC]-EMWET--seq')
        function_order.remove('Q3D[FLC]-EMWET--seq')

    # Add some constraint attributes
    if mdao_architecture in ['IDF', 'MDF']:
        fpg.node['/cpacs/mdodata/constraints/fuelTankVolume/latestValue']['constraint_type'] = 'inequality'
        fpg.node['/cpacs/mdodata/constraints/wingLoading/latestValue']['constraint_type'] = 'inequality'
        fpg.node['/cpacs/mdodata/constraints/fuelTankVolume/latestValue']['constraint_operator'] = '>='
        fpg.node['/cpacs/mdodata/constraints/wingLoading/latestValue']['constraint_operator'] = '>='
        fpg.node['/cpacs/mdodata/constraints/fuelTankVolume/latestValue']['reference_value'] = 0.0
        fpg.node['/cpacs/mdodata/constraints/wingLoading/latestValue']['reference_value'] = 0.0

    # Remove all unused system outputs
    output_nodes = fpg.find_all_nodes(subcategory='all outputs')
    for output_node in output_nodes:
        if output_node not in special_output_nodes:
            fpg.remove_node(output_node)

    # Add the function problem roles (pre-coupling, coupled, post-coupling)
    fpg.add_function_problem_roles()

    # Add some more (optional) metadata
    for node in fpg.get_function_nodes():
        if 'Q3D' in node or 'MTOW' in node:
            single_or_multi = "Single" if 'unconverged-MDA' in mdao_architecture else "Multiple"
            execution_info = {
                'remote_component_info': {
                    'job_settings': {
                        'single_or_multi_execution': single_or_multi,
                        'remote_engineer': {'contact_u_i_d': 'ivangent'},
                        'job_name': 'job_' + fpg.node[node]['label'].replace(' ', ''),
                        'notification_message': 'Hi Imco, could you please run this tool ' + fpg.node[node]['label'].replace(' ', '') + ' for me for my ' + mdao_architecture + ' AGILE workflow execution. Thanks.'
                    },
                    'data_exchange_settings': {
                        'urlsite': 'https://teamsites-extranet.dlr.de/ly/AGILE/',
                        'folder': 'CMDOWS_parser_tests'
                    }
                }
            }
            fpg.node[node]['execution_info'] = execution_info

    # Create a DSM and a VISTOMS visualization of the RCG
    if create_vis:
        fpg.create_dsm(file_name='FPG_'+mdao_definition, function_order=function_order, include_system_vars=True,
                       summarize_vars=True, destination_folder=pdf_dir)
        fpg.vistoms_add(vistoms_dir, function_order=function_order)

    # Save CMDOWS file
    fpg.save('FPG_' + mdao_definition,
             destination_folder=kdms_dir)
    fpg.save('FPG_' + mdao_definition,
             file_type='cmdows',
             description='WP6 TU Delft Wing Design FPG file',
             creator='Lukas Mueller',
             version='0.1',
             destination_folder=cmdows_dir,
             pretty_print=True)
    # Check integrity of CMDOWS
    fpg.check_cmdows_integrity()

    # Save the FPG as kdms
    fpg.save('FPG_'+mdao_definition, destination_folder=kdms_dir)
    # Save the FPG as cmdows (and do an integrity check)
    fpg.save('FPG_'+mdao_definition, file_type='cmdows', destination_folder=cmdows_dir,
             description='FPG CMDOWS file of the wing design problem from Delft University of Technology',
             creator='Lukas Mueller',
             version='0.1',
             pretty_print=True,
             integrity=True)

    # Get Mdao graphs
    # TODO: Find out why this is different from the Sellar problem
    mdg = fpg.get_mdg(name='mpg wing design')
    mpg = fpg.get_mpg(name='mpg wing design', mdg=mdg)
    mdg.graph['name'] = rcg.graph['name'] + ' - ' + mdao_definition + ' - Mdao'
    mdg.graph['description'] = 'Solution strategy to solve the wing design problem using the strategy: ' \
                               + str(mdao_architecture) + ('_' + str(convergence_type) if convergence_type else '') + '.'

    # Copy mathematical functions to additional output edges (for MDF and IDF additional output edges are created)
    # TODO: This should be automated in the KADMOS method get_mdg()
    if mdao_architecture in ['IDF', 'MDF', 'unconverged-OPT']:
        mdg.edge['OBJ']['/cpacs/architectureNodes/finalOutputVariables/cpacsCopy/mdodata/objectives/mtow/normalized_mtow']['equations'] = mdg.edge['OBJ']['/cpacs/mdodata/objectives/mtow/normalized_mtow']['equations']
        mdg.edge['CNSTRNT-merged[2modes]']['/cpacs/architectureNodes/finalOutputVariables/cpacsCopy/mdodata/constraints/wingLoading/latestValue']['equations'] = mdg.edge['CNSTRNT-merged[2modes]']['/cpacs/mdodata/constraints/wingLoading/latestValue']['equations']
        mdg.edge['CNSTRNT-merged[2modes]']['/cpacs/architectureNodes/finalOutputVariables/cpacsCopy/mdodata/constraints/fuelTankVolume/latestValue']['equations'] = mdg.edge['CNSTRNT-merged[2modes]']['/cpacs/mdodata/constraints/fuelTankVolume/latestValue']['equations']

    # Add some more problem roles to avoid undefined uIDs in the CMDOWS file
    if mdao_architecture == 'IDF':
        mdg.node['/cpacs/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/fuel/massDescription/mass']['problem_role'] = 'design variable'
        mdg.node['/cpacs/architectureNodes/consistencyConstraintVariables/cpacsCopy/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure/massDescription/gc_mass']['problem_role'] = 'constraint'
        mdg.node['/cpacs/architectureNodes/consistencyConstraintVariables/cpacsCopy/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/designMasses/mZFM/gc_mass']['problem_role'] = 'constraint'
        mdg.node['/cpacs/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/designMasses/mZFM/mass']['problem_role'] = 'design variable'
        mdg.node['/cpacs/architectureNodes/consistencyConstraintVariables/cpacsCopy/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/fuel/massDescription/gc_mass']['problem_role'] = 'constraint'
        mdg.node['/cpacs/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/designMasses/mTOM/mass']['problem_role'] = 'design variable'
        mdg.node['/cpacs/architectureNodes/consistencyConstraintVariables/cpacsCopy/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/designMasses/mTOM/gc_mass']['problem_role'] = 'constraint'
        mdg.node['/cpacs/vehicles[AGILE_DC1_vehicleID]/aircraft/model[agile_v13_modelID]/analyses/massBreakdown/mOEM/mEM/mStructure/mWingsStructure/mWingStructure/massDescription/mass']['problem_role'] = 'design variable'

    # Create a DSM and a VISTOMS visualization of the RCG
    if create_vis:
        mdg.create_dsm(file_name='Mdao_'+mdao_definition, include_system_vars=True, destination_folder=pdf_dir,
                       summarize_vars=True, mpg=mpg)
        mdg.vistoms_add(vistoms_dir, mpg=mpg)

    # Save the Mdao as kdms
    mdg.save('Mdao_'+mdao_definition, destination_folder=kdms_dir, mpg=mpg)
    # Save the Mdao as cmdows (and do an integrity check)
    mdg.save('Mdao_'+mdao_definition, file_type='cmdows', destination_folder=cmdows_dir,
             mpg=mpg,
             description='Mdao CMDOWS file of the wing design problem from Delft University of Technology',
             creator='Lukas Mueller',
             version='0.1',
             pretty_print=True,
             integrity=True
             )


print 'Done!'
