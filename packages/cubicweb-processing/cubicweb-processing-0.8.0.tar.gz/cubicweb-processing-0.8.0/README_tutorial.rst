Handling processes via the ``processing`` cube
==============================================

Introduction
~~~~~~~~~~~~

The purpose of this tutorial is to show programmers how to use the
``processing`` cube for running (chained) processes.


Basic steps in using the ``processing`` cube
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We start by adding the dependency to the ``processing`` cube to our
application cube.

First, to simplify the code, we create a shorter name for the entity creation
method::

    ce = session.create_entity

Then, in our application cube, we create a set of ``Executable`` entities.
Each ``Executable`` has a required ``name`` attribute of type ``String``.
Hence, assuming we create two executables::

    my_exe = ce('Executable', name=u'my executable')
    other_exe = ce('Executable', name=u'other_executable')
    self.commit()

Once an ``Executable`` is created, we may attach parameter definitions to it,
that is, ``ParameterDefinition`` entities.

An ``Executable`` can have an arbitrary number of
``ParameterDefinition`` s related to it via the ``parameter_of`` relation.

Each ``ParameterDefinition`` has a set of required attributes, namely:

- a ``name``, of type ``String``;
- a ``value_type``, also of type ``String``, among the following: ``Float``,
  ``Int``, ``String`` and ``File``;
- a ``param_type``, of type ``String``, either ``input`` or ``output``.

Each ``ParameterDefinition`` has an optional ``description`` attribute
of type ``String``. Hence, for our two executables::

    my_in_pdef = ce('ParameterDefinition', name=u'my_in_p',
                    value_type=u'Float', param_type=u'input',
                    parameter_of=my_exe,
                    description=u'Input parameter definition')
    my_out_pdef = ce('ParameterDefinition', name=u'out_p',
                     value_type=u'String', param_type=u'output',
                     parameter_of=my_exe,
                     description=u'Output parameter definition')
    other_in_pdef = ce('ParameterDefinition', name=u'other_in_p',
                       value_type=u'String', param_type=u'input',
                       parameter_of=other_exe,
                       description=u'Input parameter definition')
    other_out_pdef = ce('ParameterDefinition', name=u'out_p',
                        value_type=u'Int', param_type=u'output',
                        parameter_of=other_exe,
                        description=u'Output parameter definition')
    self.commit()

Alternatively, input and output parameter definitions can be added to an
``Executable`` by means of the ``add_input`` and ``add_output`` methods,
respectively::

    my_exe.add_input(u'my_in_p', u'Float')
    my_exe.add_output(u'out_p', u'String')
    other_exe.add_input(u'other_in_p', u'String')
    other_exe.add_output(u'out_p', u'Int')
    self.commit()

Please note that both output parameter definitions have the same name.
We will shortly see why.

Once a set of ``Executable`` s have been created, we can create a ``Run`` s.
A ``Run`` is an "instantiated" ``Executable``, with particular parameter
*values*.

To create a ``Run``, we start from an ``Executable``, which we associate
to the ``Run`` via the ``executable`` relation. Assuming our two
``Executable`` s, ``my_exe`` and ``other_exe``, we create two ``Run`` s,
``my_run`` and ``other_run``::

    my_run = ce('Run', executable=my_exe)
    other_run = ce('Run', executable=other_exe)
    self.commit()

For each ``ParameterDefinition``
associated to these ``Executable``, we create a
``ParameterValue{Float | Int | String | File}``.

Each ``ParameterValue`` entity is associated to precisely one
``ParameterDefinition`` via the ``param_def`` relation and has the ``value``
optional attribute, of respective types ``Float``, ``Int`` and ``String``
for non-file ``ParameterValue`` s, and the ``value_file`` relation associating
the ``ParameterValue`` to a ``File`` object, for ``ParameterValueFile``.

Each ``ParameterValue`` is associated to the ``Run`` via the ``value_of_run``
relation.


The chaining of two ``Run`` s is performed by properly plugging the output
parameter value(s) of one run to the input parameter value(s) of the other
run(s). This is done by:

- initializing the ``from_run`` relation of the the ``ParameterValue``
  of an input  ``ParameterDefinition`` of the second ``Run``, to
  the first ``Run``;
- initializing the ``from_output`` relation of the ``ParameterValue``
  of an input ``ParameterDefinition`` of the second ``Run``, to the appropriate
  (output)  ``ParameterDefinition`` of the ``Executable`` associated to the
  first ``Run``::

    my_in_pvalue = ce('ParameterValueFloat', param_def=my_in_pdef,
                       value_of_run=my_run, value=5.)
    my_out_pvalue = ce('ParameterValueString',
                       param_def=my_out_pdef, value_of_run=my_run)

    other_in_pvalue = ce('ParameterValueString', param_def=other_in_pdef,
                         value_of_run=other_run, from_run=my_run,
                         from_output=my_out_pdef)
    other_out_pvalue = ce('ParameterValueInt', param_def=other_out_pdef,
                          value_of_run=other_run)
    self.commit()

Alternatively, we may directly initialize the input parameter value of the
first run and link the output of the first run to the input of the second run,
and so on. In our example, we can start by initializing the value of the input
parameter of the first run::

    my_run['my_in_p'] = 5.

We notice that this is done much easier from the user's standpoint.
Nevertheless, behind the scenes, a ``ParameterValueFloat`` is created,
as seen above.

Now, in order to actually chain ``my_run`` and ``other_run``, we can
dispense with the ``from_run`` / ``from_output`` attribute dance and just use
``other_run``'s ``link_input_to_output`` method::

    other_run.link_input_to_output('other_in_p', my_run, 'out_p')

This literally reads as: "link ``other_run``'s input, ``other_in_p``,
to ``my_run``'s output, ``out_p``".  ore specifically, it instructs the
computer to assign ``other_in_p``'s parameter value to ``out_p``'s parameter
value, whatever that is.

Now the run chain is ready to be executed. Nonetheless, before being able to
actually execute the run chain, we need to:

- attach code excerpts to the ``Executable`` s used by the ``Run`` s in
  the chain. To this end, for Python code for instance, it suffices to add
  a ``python_code`` ``RelationDefinition`` to the schema of our application
  cube. The ``subject`` of this relation definition is set to ``Executable``,
  and its ``object``, to ``String``::

    class python_code(RelationDefinition):
        subject = 'Executable'
        object = 'String'

  In this case, the executables can be defined as follows::

    my_exe = ce('Executable', name=u'my executable',
                python_code=u'"my_exe" + str(run["my_in_p"])')
    other_exe = ce('Executable', name=u'other_executable',
                   python_code=(u'1000 + int(run["other_in_p"]' +
                                u'.split("my_exe")[-1].split(".")[0])'))

- perform the appropriate transition on the first run, to take it out of the
  "``ready``" state, the ``wft_run_complete_params`` transition brought it to.
  This transition is triggered by a hook in the ``processing`` cube when the
  input parameters of the run have their values assigned.
  This is done by adapting the run to an "``IWorkflowable``" entity and firing
  the ``wft_run_queue`` transition::

    my_run.cw_adapt_to('IWorkflowable').fire_transition('wft_run_queue')
    self.commit()

- enable a means to actually *evaluate* and execute the code referred to by
  ``python_code``. This can be done in a series of hooks, handling the
  transitions from the ``wfs_run_ready`` state towards the
  ``wfs_run_completed`` state. These hooks are implemented in our application
  cube.

  Bearing in mind that the only transition implemented,  on ``Run`` s, in the
  hooks of the ``processing`` cube, is ``wft_run_complete_params``, we must
  implement the hooks which trigger the other transitions (viz. ``wft_run_run``
  and ``wft_run_complete`` at least) ourselves.

  The set of hooks that have to be created should, a minima, allow our runs to
  get from the "``waiting``" state (stemmed from the firing of the
  ``wft_run_queue`` transition) to the ``completed`` state, unless something
  goes wrong with the code execution.

  To this end, we can (see ``test/data/hooks.py``):

  + first, create an operation, ``FireTransitionOp``, for correctly handling
    the transition firing process (see ``test/data/hooks.py``)::

        class FireTransitionOp(hook.Operation):

            def postcommit_event(self):
            # temporarily free the original session's cnxset first: during
            # postcommit, it has not be done yet and we don't want the
            # internal session below to exhaust the pool
            self.session.free_cnxset(ignoremode=True)
            with self.session.repo.internal_session() as session:
                run = session.entity_from_eid(self.run.eid)
                run.cw_adapt_to('IWorkflowable').fire_transition(self.tr_name)
                session.commit()
            self.session.set_cnxset()

  + second, use this operation in a generic hook for firing transitions.
    This hook should be overridden for each particular transition, because the
    selector and transition type are different.
    This generic transition firing hook should not be used by itself::

        class FireTransitionHook(hook.Hook):
            __abstract__ = True
            events =  ('after_add_entity',)

            @property
            def run(self):
                return self.entity.for_entity

            def fire_transition(self, tr_name):
                FireTransitionOp(self._cw, run=self.run, tr_name=tr_name)

  + third, implement hooks for handling the transition from the ``waiting``
    state to the ``running`` state::

        class RunRunHook(FireTransitionHook):
            __regid__ = 'my_application.run_run'
            __select__ = (hook.Hook.__select__ &
                          on_fire_transition('Run', 'wft_run_queue'))

            def __call__(self):
                self.fire_transition('wft_run_run') # go the 'running' state


   + fourth, implement the hook which handles execution of the code and the
     transition towards the ``completed`` state. This hook should be selected
     when the transition "``wft_run_run``" is fired (the transitions are
     defined in ``workflows.py``). The code should have the following form::

        class RunCompleteRunHook(FireTransitionHook):
            __regid__ = 'my_application.run_complete'
            __select__ = (hook.Hook.__select__ &
                          on_fire_transition('Run', 'wft_run_run'))

            def __call__(self):
                if run.exe.python_code:
                    run.set_ovalues(out_p=eval(run.exe.python_code,
                                               {'run': run}))
                # go to the 'completed' state:
                self.fire_transition('wft_run_complete)

     Please notice that the names of the output values set by the evaluation of
     ``python_code`` must match  the names of the output parameter definitions.
     This is why, in our example, both output parameter definitions had the
     same name, ``out_p``.

Once the runs are executed, we can inspect their state, via
``my_run.cw_adapt_to('IWorkflowable').state`` and
``other_run.cw_adapt_to('IWorkflowable')``.

The outputs of the runs can be inspected by means of ``my_run.ovalue_dict`` and
``other_run.ovalue_dict``. More specifically, to get the output *value* of the
second run, we can do ``other_run.ovalue_dict['out_p']``.
