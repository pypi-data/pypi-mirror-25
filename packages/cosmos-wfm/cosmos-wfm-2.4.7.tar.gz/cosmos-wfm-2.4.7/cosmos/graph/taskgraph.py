# import functools
# import os
#
# import networkx as nx
#
# from ..util.helpers import duplicates, str_format
# from ..util.sqla import get_or_create
# from cosmos.api import Stage
#
# def get_or_create_task(successful_tasks, params, stage, parents, default_drm, output_dir_pre_interpolation, tool=None):
#     output_dir = str_format(output_dir_pre_interpolation, params)
#     output_dir = os.path.join(stage.workflow.output_dir, output_dir)
#
#     existing_task = successful_tasks.get(frozenset(params.items()), None)
#     if existing_task:
#         return existing_task
#     else:
#         if tool is not None:
#             tool.output_dir = output_dir
#         else:
#             tool = stage.tool_class(params=params, output_dir=output_dir)
#
#         return tool._generate_task(stage=stage, parents=parents, default_drm=default_drm)
#
#
# def render_recipe(workflow, recipe, default_drm):
#     """
#     Generates a stagegraph and taskgraph described by a Recipe
#     :returns: (nx.DiGraph taskgraph, nx.DiGraph stagegraph)
#     """
#     task_g = nx.DiGraph()
#
#     # This replicates the recipe_stage_G, a graph of RecipeStage objects, into a a graph of Stage objects
#     f = functools.partial(recipe_stage2stage, workflow=workflow)
#     # want to add stages in the correct order
#     convert = {recipe_stage: f(recipe_stage) for recipe_stage in nx.topological_sort(recipe.recipe_stage_G)}
#     stage_g = nx.relabel_nodes(recipe.recipe_stage_G, convert, copy=True)
#     for i, stage in enumerate(nx.topological_sort(stage_g)):
#         stage.number = i + 1
#         stage.parents = stage_g.predecessors(stage)
#         if not stage.resolved:
#             successful_tasks = {frozenset(t.params.items()): t for t in
#                                 stage.tasks}  # successful because failed jobs have been deleted.
#             if stage.is_source:
#                 for source_tool in stage.recipe_stage.source_tools:
#                     task = get_or_create_task(successful_tasks, source_tool.params, stage, [], default_drm,
#                                               stage.output_dir_pre_interpolation, tool=source_tool)
#                     task_g.add_node(task)
#             else:
#                 for new_task_params, parent_tasks in stage.rel.__class__.gen_task_params(stage):
#                     task = get_or_create_task(successful_tasks, new_task_params, stage, parent_tasks, default_drm,
#                                               stage.output_dir_pre_interpolation)
#                     task_g.add_edges_from([(p, task) for p in parent_tasks])
#
#         stage.resolved = True
#
#         tagz = [frozenset(t.params.items()) for t in stage.tasks]
#         if len(tagz) != len(set(tagz)):
#             d = next(duplicates(map(dict, tagz)))
#             raise AssertionError('Duplicate params detected in %s: %s' % (stage, d))
#
#     return task_g, stage_g
#
#
# def recipe_stage2stage(recipe_stage, workflow):
#     """
#     Creates a Stage object from a RecipeStage object
#     """
#     session = workflow.session
#     stage, created = get_or_create(session=session, workflow=workflow, model=Stage, name=recipe_stage.name)
#
#     # if not created:
#     # workflow.log.info('Loaded Stage %s' % stage.name)
#     # else:
#     # workflow.log.info('Created Stage %s' % stage.name)
#
#     for k, v in recipe_stage.properties.items():
#         if k != 'tasks':
#             setattr(stage, k, v)
#
#     recipe_stage.stage = stage
#     stage.recipe_stage = recipe_stage
#     return stage