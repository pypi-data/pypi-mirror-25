# -*- coding: utf-8 -*-
"""API for cloud-based FUN3D

This module contains the functions necessary to launch FUN3D cases on Google Compute engine. 

Example:
     An example case is provided in the examples directory. To run the directory::

     $ python fun3d_example.py

     This example will launch the specified case. To obtain the results, log in to an interactive python shell and type::

     >> get_result(case)

"""
try:
    import rest
    #from rest import post, put, get, delete, put_file, put_dir, upload_dir, APIError
except ImportError as e:
    #from fun3dapi.rest import post, put, get, delete, put_file, put_dir, upload_dir, APIError
    import fun3dapi.rest as rest

import os.path
import requests
import subprocess

class Account(object):
    """
    Provides details of the user account (e.g. accumulated runtime, disk space, etc)
    """

    def info(self):
        """
        Returns:
             A dict of the following form:

               {
                  'hours_used' : Total core-hours used,
                  'price' : Total price, from start of service,
                  'disk_usage' : Disk usage, in GB,
                  'cases_running' : Number of running cases,
               }
        """
        print('Here')
        return rest.get('/account/info')

class Mesh(object):
    """
    An object representing a FUN3D mesh.

    Note:
         The mesh object never stores the mesh in memory.

    """
    def __init__(self,mesh):
        """
        Attributes:
            mesh (str || Mesh): Either the unique name of the mesh, or another mesh object.
        """
        if isinstance(mesh,Mesh):
            self.name = mesh.name
        else:
            self.name = mesh


    def info(self):
        """
        Returns:
             A dict of the following form::

               {
                  'size' :    Size of mesh in bytes,
                  'upload_time' : time uploaded,
                  'status' : (None or 'Deleted'),
                  'filename' : Name of the mesh file,
                  'nickname' : Nickname for the mesh,
                  'id' : unique integer id of the mesh,
               }

        """

        return rest.get('/mesh/info',{'nickname' : self.name})

    def delete(self):
        """
        Permanently deletes a mesh from the library

        Raises:
             ResourceInUseError: If the mesh is in use by a simulation.

        """
        return rest.delete('/mesh/delete',{'nickname' : self.name})

class Case(object):
    """
    A Case object provides the interface for querying the status of a submitted case. 

    """
    def __init__(self,case):
        """
        Attributes:
            case (str || Case): Either the unique name of the mesh, or another mesh object.
        """

        if isinstance(case,Case):
            self.name = case.name
        else:
            self.name = case

    def status(self):
        """
        Returns:
           status (str) : either RUNNING, DONE, or CANCELED
        """
        return rest.get('/case/status',{'nickname' : self.name}).text

    def info(self):
        """
        Returns:
             A dict of the following form::

               {
                  'start_time' : Time case was submitted,
                  'runtime' : Cumulative runtime in hours,
                  'meshname' : Name of the mesh,
                  'nickname' : Identifying nickname of the case,
                  'price' : Current price in USD',
                  'status' : Current status (Success || Error || Running || Paused || Canceled || Creating cluster || Allocating Resources),
               }

        """

        return  rest.get('/case/info',{'nickname' : self.name})

    def casedir(self,destination):
        """
        Retrieves the current case directory, and all of its files.
        Note that if the case contains significant data, this method
        may take a while to complete.
        Args:
            destination (str): The location on the local computer at which to save
            the directory.
        """
        cmd ='rsync -aze "ssh -i {0}" {1}:/mnt/data/cases/{2} {3}' \
                                .format(os.path.expanduser('~/.simulation/simulation'),
                                        rest.ip,
                                        self.name,
                                        destination)
        subprocess.check_output(cmd,shell=True)
    def stdout(self):
        """
        Obtaines the current stdout from the simulatoin.

        Returns:
        stdout (file) A string containing the stdout of the simulation
        """
        return rest.get('/case/stdout',{'nickname' : self.name}).text

    def stderr(self):
        """
        Obtaines the current stderr from the simulatoin.

        Returns:
        stdout (file) A string containing the stderr of the simulation
        """
        return rest.get('/case/stderr',{'nickname' : self.name}).text

    def residual_file(self):
        """
        Fetches the current residual history file (.hist)

        Returns:
             history (file): A string containing the complete case resuidual history.
        """
        return rest.get('/case/residualhistory',{'nickname' : self.name}).text

    def plot_convergence(self):
        try:
            import matplotlib.pyplot as pyplot
        except ImportError as e:
            print('Please install matplotlib to enable plotting functionality.')
            raise

        history = self.residual_file()
        if not len(history):
            raise RuntimeError('No residual history to plot')


        history = history.split('\n')
        variables = [x.strip('"') for x in history[1].split('=')[1].split()]
        nplot = variables.index('C_D')
        residuals = [[float(i) for i in line.split()[1:nplot-1]] for line in history[3:-2]]
        clcd = [[float(i) for i in line.split()[nplot-1:nplot+1]] for line in history[3:-2]]
        cx = [[i]*2 for i in range(0,len(clcd))]
        cr = [[i]*(nplot-2) for i in range(0,len(residuals))]

        fig = pyplot.figure(figsize=(16,8))
        plt1 = fig.add_subplot(1,2,1)
        plt1.plot(residuals)
        plt1.set_yscale('log')
        plt1.set_xlabel('Iteration')
        plt1.legend(variables[1:nplot-1], loc='upper right')
        plt2 = fig.add_subplot(1,2,2)
        plt2.plot(clcd)
        plt2.legend(variables[nplot-1:nplot+1],loc='upper right')
        plt2.set_xlabel('Iteration')
        pyplot.show()


    def pause(self):
        """
        Pauses a running case.

        Note:
             Paused cases can be re-started with the ``restart()`` method.
        """
        response = rest.post('/case/pause',{'nickname' : self.name})

    def resume(self):
        """
        Resumes a paused case
        """
        response = rest.post('/case/resume',{'nickname' : self.name})

    def delete(self):
        """
        Permanently deletes a case
        """
        response = rest.delete('/case/delete',{'nickname' : self.name})

def add_mesh(meshfile,name=None):
    """
    Adds mesh from local disk to mesh library. If name is not specified, the name of the mesh will be the basename of the meshfile.
    The mesh name must be unique.
    Args:
         meshfile (str): Path to a valid FUN3D mesh.
         name (str): optional name to reference the mesh

    Returns:
         class: In instance of Mesh class.
    """
    basename = os.path.basename(meshfile)
    if name is None:
        name = basename[:basename.find('.')]

    try:
        response = rest.post('/mesh/add',{'nickname' : name, 'filename' : basename})
    except Exception as e:
        rest.post('/mesh/delete',{'nickname' : name})
        print('Error adding mesh!')
        raise

    try:
        response = rest.post('/upload/meshes/' + name + '/' + basename,{},filename=meshfile)
    except Exception as e:
        rest.post('/mesh/delete',{'nickname' : name})
        print('Error uploading mesh!')
        raise

    return Mesh(name)

def list_meshes():
    """
    Lists all meshes in the user mesh library.

    Returns:
         list(str): A list of the name of all valid meshes.

    """
    return rest.get('/mesh/list')

def submit_case(input_dir,mesh_name,name=None):
    """
    Submits a FUN3D case with input configuration file ``input_dir``
    The mesh is identified by mesh_name.

    Args:
         input_dir (str): ``input_dir`` must either be a .zip or .tar.gz file containing all files needed to run the case, except for the mesh.

         mesh_name (str): The unique name identifier of a valid mesh in the mesh library.

         casename (str): An optional, unique name to be assigned to the case. If omitted, the input_directory base name will be used, and must be unique.

    Returns:
         case (Case): A case object providing interface to the submitted instance.
    """


    basename = os.path.basename(input_dir)

    if name is None:
        name = basename

    try:
        response = rest.upload_dir('/upload/cases/' + name,input_dir)
    except Exception as e:
        print('Could not upload directory {0}!'.format(input_dir))
        rest.post('/case/delete',{'nickname' : name})
        raise

    try:
        response = rest.post('/case/create',{'nickname' : name, 'name_mesh' : mesh_name, 'filename' : basename})
    except Exception as e:
        print('Error creating case!')
        rest.post('/case/delete',{'nickname' : name})
        raise

    try:
        response = rest.post('/case/run',{'nickname' : name})
    except Exception as e:
        print('Error running case!')
        raise

    return Case(name)

def list_cases():
    """
    Lists all cases in the user mesh library.

    Returns:
    list((str,Case)): A list of tuples containing the unique case name and Case class instances.

    """
    return rest.get('/case/list')
