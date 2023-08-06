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

#ifndef __MAP_OWNER_H__
#define __MAP_OWNER_H__

#include <Python.h>

/* MapOwner object */
typedef struct {
	PyObject_HEAD
	void	*map_addr;
	size_t	map_size;
} PyMapOwnerObject;

/* Class type definition */
extern PyTypeObject PyMapOwner_Type;

/* Methods */
extern PyObject *map_owner_msync(PyMapOwnerObject *self, PyObject *args, PyObject *kwds);
extern PyObject *map_owner_mlock(PyMapOwnerObject *self, PyObject *args);
extern PyObject *map_owner_munlock(PyMapOwnerObject *self, PyObject *args);

/* C API */
#define PyMapOwner_Check(op)	PyObject_TypeCheck(op, &PyMapOwner_Type)

#endif /* !__MAP_OWNER_H__ */
