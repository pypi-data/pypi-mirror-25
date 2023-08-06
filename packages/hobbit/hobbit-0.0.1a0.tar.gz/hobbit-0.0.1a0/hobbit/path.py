"""
The module contains classes and functions for writing and traversing the path of the scrapping.

The scrapping path is writen using the :class: `hobbit.path.Path`.
Example:
    Path(start_actions).to(next_actions, other_path)
                       .to(finish_actions)
    or
    _from(start_actions).to(next_actions, other_path)
                        .to(finish_actions)
"""
from copy import deepcopy
from itertools import starmap

from .actions import Action
from .utils import flatten, foreach


"""
                                              Path.
===================================================================================================
"""

class Path:
    """
    The action path for scrapping.

    The path is a directed graph. The nodes of the graph are steps of `hobbit.path.Step` or `hobbit.path.Path`.
    Graph content is determined by the adjacency list.
    """

    def __init__(self, *start_actions):
        """
        Path containing steps for scraping.

        Args:
            *start_actions (Iterator of :class: `hobbit.actions.Action` or :class: `hobbit.path.Path`): Actions or paths of actions.
        """
        self._adjacencies = {} #List of adjacencies. {`hobbit.path.Step`: [related `hobbit.path.Step`s]}
        self.steps_count = 0 #The number of steps is the number of vertices of the graph. Used to assign internal IDs to steps.

        self.to(*start_actions)

    def to(self, *actions):
        """
        Add the following steps to the path.

        Args:
            *start_actions (Iterator of :class: `hobbit.actions.Action` or :class: `hobbit.path.Path`): Actions or paths.
        """
        last_steps = self.last_nodes
        for action in flatten(actions):
            self._append_node(self._get_node(action), last_nodes)

    def _append_node(self, node, last_steps):
        """
        Add a step or path to the adjacency list.

        Args:
            node (:class: `hobbit.path.Step` or :class: `hobbit.path.Path`): Node of graph of path.
            last_steps (Iterable :class: `hobbit.path.Step` or :class: `hobbit.path.Path`): Last uncomleted nodes.
        """
        for last_step in last_steps:
            self._adjacencies[last_step].add(node)
        if not node.is_finish and node not in self.adjacencies.keys():
            self._adjacencies[node] = set()

    @staticmethod
    def _get_node(self, action):
        """
        Get :class: `hobbit.path.Step` for action or :class: `hobbit.path.Path` for :class: `hobbit.path.Path`.

        Args:
            action (:class: `hobbit.path.Step` or :class: `hobbit.path.Path`): Content of node.
        """
        node = None
        if isinstance(action, Step):
            node = Step(self.steps_count, action, self)
            self.steps_count += 1
        elif isinstance(action, Path):
            node = action
        else:
            raise TypeError
        return node

    def next_steps_for(self, step):
        """
        Get the following steps for the step...

        Args:
            step (:class: `hobbit.path.Step`): The step for which you want to get the following steps.
        """
        self.expand_for(step)
        return self._adjacencies.get(step, [])

    def expand_for(self, step):
        """Expand all the paths in the adjacency list for step."""
        foreach(self._expand_path, filter(lambda step: isinstance(step, Path),
                self._adjacencies.get(step, [])))

    def _expand_path(self, path):
        """
        Replace the path to its contents.

        Args:
            path (:class: `hobbit.path.Path`): The path that needs to be expanded.
        """
        if isinstance(path, Path):
            for origin in self.get_origins_for(path):
                self._adjacencies[origin].extend(path.start_nodes)
                self._adjacencies[origin].remove(path)
            if not path.is_finish:
                self._adjacencies.pop(path)
            self._adjacencies.update(path._adjacencies)
            foreach(self._adjacencies(finish_node).extend(self._adjacencies[path]),
                    path.finish_nodes)
        else:
            raise TypeError

    def get_origins_for(self, step):
        """
        Get origin steps for current step.

        Args:
            step (:class: `hobbit.path.Step` or :class: `hobbit.path.Path`): The step for which you want to get the following steps.
        """
        return (origin_step for origin_step, adjacencies in self if step in adjacencies)

    @property
    def last_nodes(self):
        """Last uncomleted nodes."""
        return set(node for node, adjacencies in self._adjacencies.items() if adjacencies)

    @property
    def start_nodes(self):
        """Start nodes."""
        return set(self._adjacencies.keys()) - \
               set(node for adjacencies in self._adjacencies.values() for node in adjacencies)

    @property
    def is_finish(self):
        """Is the path complete?"""
        return True if not self.path_nodes and self.finish_nodes else False

    @property
    def path_nodes(self):
        """Get all path nodes of graph of path."""
        return set(node for node in self.nodes if isinstance(node, Path))

    @property
    def nodes(self):
        """Get all nodes of graph of path."""
        return set(node for node in adjacencies for adjacencies in self._adjacencies.values())\
               .union(set(self._adjacencies.keys()))

    @property
    def finish_nodes(self):
        """Get all finish nodes of graph of path."""
        return set(node for node in adjacencies for adjacencies in self._adjacencies.values()) -\
               set(self._adjacencies.keys())

    def __iter__(self):
        return self

    def __next__(self):
        for node, adjacencies in self._adjacencies.items():
            yield node, adjacencies

    def __hash__(self):
        """Hash for determinate path"""
        return hash(id(self))


def _from(*start_actions):
    """
    Factory to create a path.

    Useless. For beauty.

    Replaces the following code:
        Path(start_actions)

    Args:
        *start_actions (Iterator of :class: `hobbit.actions.Action` or :class: `hobbit.path.Path`): Actions or paths.
    """
    return Path(start_actions)


"""
                                              Step.
===================================================================================================
"""

class Step:
    """
    Step of path.

    Step provides information about the current action to be produced with the
    result obtained in the previous step and go to the next steps in the current path.
    """

    def __init__(self, _id, action, current_path, result_of_last_action=None):
        """
        Step of path.

        A path step that displays the current state of the path.

        A step is created when building a path.
        When constructing a path, it is given the initial state.
        The initial path of the step is the one in which it was created.
        During the passage of the path, it can change by actions and become
        different for steps created from one path.

        Args:
            _id (int):                              Unique step identifier in path.
            action (:class: `hobbit.actions.Action`):  The action to process
                                                    the result obtained in the previous step.
            current_path (:class: `hobbit.path.Path`): The path corresponding to the current
                                                    execution of the path.

        kwargs:
            result_of_last_action (:class: `bs4.element.Tag`): The result of the action
                                                               of the previous step.
        """
        if not isinstance(action, Action):
            raise TypeError

        self._id = int(id)
        self.action = action
        self.current_path = current_path
        self._origin_path = current_path # For hash
        self.result_of_last_action = result_of_last_action

    def reinitialize(current_path, result_of_last_action):
        """
        Reinitialize the step state.

        The step changes its state during the passage of the path.
        After the previous step, the next step is to get the path and the data to process.

        Args:
            current_path (:class: `hobbit.path.Path`):            The path corresponding to the current
                                                               execution of the path.
            result_of_last_action (:class: `bs4.element.Tag`): The result of the action
                                                               of the previous step.
        """
        if not sinstance(current_path, Path):
            raise TypeError

        self.current_path = current_path
        self.result_of_last_action = result_of_last_action

        return self

    @property
    def is_finish(self):
        """Is the step action terminating?"""
        return self.action.is_finish

    def __call__(self, hobbit):
        """Execute the action for the current path with the current data."""
        return self.action(hobbit, self.current_path, self.result_of_last_action)

    def __hash__(self):
        """Hash to determine the step in the path adjacency list."""
        return hash(self._id) ^ hash(self._origin_path)
