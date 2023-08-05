from .util.logging import get_logger
from .persistload import PersistLoadBasic, PersistLoadWithParameters
from logging import DEBUG, INFO


# Base classes
class Persistable:
    """
    A persistable logged object useful for ML use-cases.
    
    Basic instructions, create an object that in
    """

    def __init__(
        self, workingdatapath=None,
        persistloadtype="Basic",
        from_persistable_object=None
    ):
        """

        Parameters
        ----------
        working_subdir          : str or pathlib.Path
            Name of working directory, which is by default under the local-data directory, but can by overridden by
            passing a full pathlib.Path argument
        persistloadtype                    : str
            Use either  basic - simple file names, no parameter tracking
                        wparams - same as basic but with parameter tracking
        from_persistable_object : Persistable
            Construct a persistable object from another persistable object
        """

        # Either construct the persistable object from another persistable object,
        # or enforce that working_subdir and localdatapath are provided
        if from_persistable_object:
            workingdatapath = from_persistable_object.persistload.workingdatapath
            persistloadtype = from_persistable_object.persistload.get_type()
        elif workingdatapath is None:
            raise ValueError("Working directory must be specified")

        # Choose PersistLoad object type:
        if persistloadtype == "Basic":
            PersistLoadObj = PersistLoadBasic
        elif persistloadtype == "WithParameters":
            PersistLoadObj = PersistLoadWithParameters
        else:
            raise ValueError("persistloadtype currently only supports 'Basic' and 'WithParameters'")

        # Instantiate PersistLoad object:
        self.persistload = PersistLoadObj(workingdatapath)

        # Add a logger:
        class_name = self.__class__.__name__
        self.logger = get_logger(
            class_name,
            file_loc=(self.persistload.workingdatapath / f"{class_name}.log"),
            file_level=DEBUG,
            console_level=INFO
        )
        self.logger.info(f"---- NEW PERSISTABLE SESSION ---- ({self.persistload.workingdatapath})")
