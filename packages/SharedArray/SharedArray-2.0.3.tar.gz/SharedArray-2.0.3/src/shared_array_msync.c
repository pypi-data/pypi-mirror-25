/* 
 * This file is part of SharedArray.
 * Copyright (C) 2014-2017 Mathieu Mirmont <mat@parad0x.org>
 * 
 * SharedArray is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 * 
 * SharedArray is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with SharedArray.  If not, see <http://www.gnu.org/licenses/>.
 */

#define NPY_NO_DEPRECATED_API	NPY_1_8_API_VERSION
#define PY_ARRAY_UNIQUE_SYMBOL	SHARED_ARRAY_ARRAY_API
#define NO_IMPORT_ARRAY

#include <Python.h>
#include <numpy/arrayobject.h>
#include "shared_array.h"
#include "map_owner.h"

/*
 * Method: SharedArray.msync()
 */
PyObject *shared_array_msync(PyObject *self, PyObject *args, PyObject *kwds)
{
	static char *kwlist[] = { "array", "flags", NULL };
	PyObject *array;
	PyObject *map_owner;
	PyObject *flags;

	/* Parse the arguments */
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "O!O!", kwlist,
					 &PyArray_Type, &array,
					 &PyLong_Type, &flags))
		return NULL;

	/* Get the base object */
	if (!(map_owner = PyArray_BASE((PyArrayObject *) array))) {
		PyErr_Format(PyExc_RuntimeError,
			     "Can't find the base object of the given numpy array");
		return NULL;
	}

	/* Make sure that the base object is of a MapOwner */
	if (!PyMapOwner_Check(map_owner)) {
		PyErr_Format(PyExc_RuntimeError,
			     "The base object of the given numpy array isn't a SharedArray");
		return NULL;
	}
	
	/* Call the msync method */
	return PyObject_CallMethod(map_owner, "msync", "O", flags);
}
