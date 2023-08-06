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

#include <sys/mman.h>
#include <Python.h>
#include "map_owner.h"

/*
 * Destructor
 */
static void do_dealloc(PyMapOwnerObject *self)
{
	/* Unmap the data */
	if (munmap(self->map_addr, self->map_size) < 0)
		PyErr_SetFromErrno(PyExc_RuntimeError);
}

/*
 * List of methods
 */
static PyMethodDef methods[] = {
	{ "msync", (PyCFunction) map_owner_msync,
	  METH_VARARGS | METH_KEYWORDS,
	  "Synchronise a file with a memory map (msync(2) wrapper)" },

	{ "mlock", (PyCFunction) map_owner_mlock,
	  METH_VARARGS,
	  "Lock the array in memory (mlock(2) wrapper)" },

	{ "munlock", (PyCFunction) map_owner_munlock,
	  METH_VARARGS,
	  "Unlock the array in memory (munlock(2) wrapper)" },

	{ NULL, NULL, 0, NULL }
};

/*
 * MapOwner type definition
 */
PyTypeObject PyMapOwner_Type = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"shared_array.map_owner",		/* tp_name		*/
	sizeof (PyMapOwnerObject),		/* tp_basicsize		*/
	0,					/* tp_itemsize		*/
	(destructor) do_dealloc,		/* tp_dealloc		*/
	0,					/* tp_print		*/
	0,					/* tp_getattr		*/
	0,					/* tp_setattr		*/
	0,					/* tp_reserved		*/
	0,					/* tp_repr		*/
	0,					/* tp_as_number		*/
	0,					/* tp_as_sequence	*/
	0,					/* tp_as_mapping	*/
	0,					/* tp_hash		*/
	0,					/* tp_call		*/
	0,					/* tp_str		*/
	0,					/* tp_getattro		*/
	0,					/* tp_setattro		*/
	0,					/* tp_as_buffer		*/
	Py_TPFLAGS_DEFAULT,			/* tp_flags		*/
	0,					/* tp_doc		*/
	0,					/* tp_traverse		*/
	0,					/* tp_clear		*/
	0,					/* tp_richcompare	*/
	0,					/* tp_weaklistoffset	*/
	0,					/* tp_iter		*/
	0,					/* tp_iternext		*/
	methods,				/* tp_methods		*/
	0,					/* tp_members		*/
	0,					/* tp_getset		*/
	0,					/* tp_base		*/
	0,					/* tp_dict		*/
	0,					/* tp_descr_get		*/
	0,					/* tp_descr_set		*/
	0,					/* tp_dictoffset	*/
	0,					/* tp_init		*/
	0,					/* tp_alloc		*/
	0,					/* tp_new		*/
	0,					/* tp_free		*/
	0,					/* tp_is_gc		*/
	0,					/* tp_bases		*/
	0,					/* tp_mro		*/
	0,					/* tp_cache		*/
	0,					/* tp_subclasses	*/
	0,					/* tp_weaklist		*/
	0,					/* tp_del		*/
	0,					/* tp_version_tag	*/
};
