/*************
Python bindings for Cadbiom functions (http://https://gitlab.irisa.fr/0000B8EG/Cadbiom)

Copyright (c) 2016-2017, Pierre Vignet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
**********************************/

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
//#include <iostream>
//#define CADBIOM_VERSION "0.1.0"

#if PY_MAJOR_VERSION == 2 && PY_MINOR_VERSION <= 5
#define PyUnicode_FromString  PyString_FromString
#endif

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

#ifdef IS_PY3K
    #define IS_INT(x)  PyLong_Check(x)

    #define MODULE_INIT_FUNC(name) \
        PyMODINIT_FUNC PyInit_ ## name(void); \
        PyMODINIT_FUNC PyInit_ ## name(void)
#else
    #define IS_INT(x)  (PyInt_Check(x) || PyLong_Check(x))

    #define MODULE_INIT_FUNC(name) \
        static PyObject *PyInit_ ## name(void); \
        PyMODINIT_FUNC init ## name(void); \
        PyMODINIT_FUNC init ## name(void) { PyInit_ ## name(); } \
        static PyObject *PyInit_ ## name(void)
#endif

#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#pragma GCC diagnostic ignored "-Wwrite-strings"


static PyObject *outofconflerr = NULL;

PyDoc_STRVAR(get_unshift_code_doc,
"get_unshift_code(var_num, shift_step)\n\
\n\
:param arg1: DIMACS literal coding of a shifted variable x_i\n\
:param arg2: Shift step dependant on the run\n\
:return: DIMACS literal coding of  x_0 with same value\n\
:type arg1: <int>\n\
:type arg2: <int>\n\
:rtype: <int>"
);

static PyObject* get_unshift_code(PyObject *self, PyObject *args, PyObject *kwds)
{
    #ifndef NDEBUG
    /* Debugging code */
    printf("get unshift code\n");
    #endif

    int var_num;
    int shift_step;

    static char* kwlist[] = {"var_num", "shift_step", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "ii", kwlist,
                                     &var_num,
                                     &shift_step)) {
        return NULL;
    }

    int var_code = (abs(var_num) - 1) % shift_step + 1;

//     std::cout << "var_num: " << var_num << std::endl;
//     std::cout << "shift_step: " << shift_step << std::endl;
//     std::cout << "var_code: " << var_code << std::endl;

    if (var_code <= shift_step) {
        // std::cout << "result: " << var_code * ((var_num < 0) ? -1 : 1) << std::endl;
        return Py_BuildValue("i", var_code * ((var_num < 0) ? -1 : 1));
    }

    PyErr_SetString(PyExc_ValueError, "Not a DIMACS code of an initial variable.");
    return NULL;
}

PyDoc_STRVAR(shift_clause_doc,
"shift_clause(ncl, shift_step)\n\
Implementation of the shift operator. Shift a clause one step.\n\
\n\
.. warning:: Before the call you MUST lock the unfolder with:\n\
\"self.__locked = True\".\n\
\n\
:param arg1: DIMACS clause\n\
:param arg2: Shift step dependant on the run\n\
:return: DIMACS literal coding of  x_0 with same value\n\
:type arg1: <list>\n\
:type arg2: <int>\n\
:rtype: <list>"
);

static PyObject* shift_clause(PyObject *self, PyObject *args, PyObject *kwds)
{
    // https://docs.python.org/2/c-api/iter.html
    #ifndef NDEBUG
    /* Debugging code */
    printf("shift clause\n");
    #endif

    int shift_step;
    PyObject *ncl;

    static char* kwlist[] = {"ncl", "shift_step", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "Oi", kwlist,
                                     &ncl,
                                     &shift_step)) {
        return NULL;
    }

    PyObject *iterator = PyObject_GetIter(ncl);
    if (iterator == NULL) {
        /* propagate error */
        PyErr_SetString(PyExc_SystemError, "could not create iterator on parameter (1)");
        return NULL;
    }

    // Declare a new list with the size of the given one
    PyObject *shifted_clause = PyList_New(PySequence_Size(ncl));
    if (shifted_clause == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed to create a list");
        return NULL;
    }

    PyObject *lit;
    PyObject *shifted_lit;
    Py_ssize_t i = 0;
    while ((lit = PyIter_Next(iterator)) != NULL) {
        #ifndef NDEBUG
        /* Debugging code */
        if (!IS_INT(lit))  {
            PyErr_SetString(PyExc_TypeError, "integer expected in list");
            return NULL;
        }
        #endif

        // Mieux vaut rester avec des PyObject pour faire les additions ou pas ???
        long lit_val = PyLong_AsLong(lit);

        if (lit_val > 0) {
            #ifdef IS_PY3K
            shifted_lit = PyLong_FromLong(lit_val + shift_step);
            #else
            shifted_lit = PyInt_FromLong(lit_val + shift_step);
            #endif
        } else {
            #ifdef IS_PY3K
            shifted_lit = PyLong_FromLong(lit_val - shift_step);
            #else
            shifted_lit = PyInt_FromLong(lit_val - shift_step);
            #endif
        }

        // Add shifted_lit (use SET_ITEM instead of PyList_Append)
        // => shifted_clause is a new list there will be no leak of previously inserted items
        PyList_SET_ITEM(shifted_clause, i, shifted_lit);

        i++;

        /* release reference when done */
        // Append does not steal a reference, so shifted_lit refcount = 2
        // after Py_DECREF, shifted_lit refcount = 1, but stored in the list so the pointer var can be reused
        // SET_ITEM steals a reference, so : no Py_DECREF on items !
        Py_DECREF(lit);
    }

    /* release reference when done */
    Py_DECREF(iterator);

    if (PyErr_Occurred()) {
        /* propagate error */
        Py_DECREF(shifted_clause);
        return PyErr_SetFromErrno(outofconflerr);
    }

    // Return list of all shifted literals
    return shifted_clause;
}

PyDoc_STRVAR(forward_code_doc,
"forward_code(clause, var_code_table, shift_step)\n\
Translation from names to num codes. The translation depends on the shift direction.\n\
\n\
Numerically code a clause with the numeric code found in self.__var_code_table for\n\
a base variable x and numeric_code + shift_step for x'\n\
variable integer coding increases in futur steps\n\
\n\
:param arg1: a Clause object\n\
:param arg2: Var code table from the model\n\
:param arg3: Shift step dependant on the run\n\
:return: the DIMACS coding of the forward shifted clause\n\
:type arg1: <list>\n\
:type arg2: <dict>\n\
:type arg3: <int>\n\
:rtype: <list>"
);

static PyObject* forward_code(PyObject *self, PyObject *args, PyObject *kwds)
{
    #ifndef NDEBUG
    /* Debugging code */
    printf("forward code\n");
    #endif

    int shift_step;
    PyObject *clause;
    PyObject *var_code_table;

    static char* kwlist[] = {"clause", "var_code_table", "shift_step", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOi", kwlist,
                                     &clause,
                                     &var_code_table,
                                     &shift_step)) {
        return NULL;
    }

    // Get attr list_of_literals of clause object
    PyObject* literals = PyObject_GetAttrString(clause, "list_of_literals");
    if (literals == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed get attribute 'list_of_literals' on clause object");
        return NULL;
    }

    PyObject *iterator = PyObject_GetIter(literals);
    if (iterator == NULL) {
        PyErr_SetString(PyExc_SystemError, "could not create iterator on 'list_of_literals' attribute");
        return NULL;
    }

    // Declare a new list with the size of 'literals'
    PyObject *num_clause = PyList_New(PySequence_Size(literals));
    if (num_clause == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed to create a list");
        return NULL;
    }
    // Append does not steal a reference, so we need Py_DECREF
    // SET_ITEM steals a reference, so: no Py_DECREF on items !

    PyObject *lit;
    PyObject *lit_cod;
    PyObject *lit_name;
    PyObject *lit_sign;
    PyObject *name_last_char;
    PyObject *res;
    PyObject *name_prefix;
    PyObject *name_value;
    PyObject *multiply_result;
    #ifdef IS_PY3K
    PyObject *last_char = PyUnicode_FromString("`");
    PyObject *py_shift_step = PyLong_FromLong(shift_step);
    PyObject *minus_one = PyLong_FromLong(-1);
    #else
    PyObject *last_char = PyString_FromString("`");
    PyObject *py_shift_step = PyInt_FromLong(shift_step);
    PyObject *minus_one = PyInt_FromLong(-1);
    #endif
    Py_ssize_t i = 0;
    while ((lit = PyIter_Next(iterator)) != NULL) {

        // get name and sign attributes of the literal in clause
        lit_name = PyObject_GetAttrString(lit, "name");
        lit_sign = PyObject_GetAttrString(lit, "sign");
        #ifdef IS_PY3K
        Py_ssize_t name_size = PyBytes_GET_SIZE(lit_name);
        #else
        Py_ssize_t name_size = PyString_GET_SIZE(lit_name);
        #endif
        //std::cout << "name size" << name_size << std::endl;

        // Get last char of the name
        // new ref
        name_last_char = PySequence_ITEM(lit_name, name_size - 1);
        // If last char is '`'
        res = PyObject_RichCompare(name_last_char, last_char, Py_EQ);
        if (res == Py_True) {
            // Get prefix of the name
            name_prefix = PySequence_GetSlice(lit_name, 0, name_size-1);
            if (name_prefix == NULL) {
                PyErr_SetString(PyExc_SystemError, "failed to get slice from lit name");
                return NULL;
            }
            //std::cout << PyString_AsString(name_prefix) << std::endl;

            // Borrowed reference
            name_value = PyDict_GetItem(var_code_table, name_prefix);
            if (name_value == NULL) {
                PyErr_SetString(PyExc_KeyError, "name_value not found in dict");
                return NULL;
            }

            // Add shift_step to the value corresponding to the given name
            lit_cod = PyNumber_Add(name_value, py_shift_step);
            Py_DECREF(name_prefix);
            // Because name_value reference IS borrowed (owned by PyDict_GetItem)
            // we don't do Py_DECREF(name_value);

            // Add new lit_cod (use SET_ITEM instead of PyList_Append)
            // => num_clause is a new list there will be no leak of previously inserted items
            // Append does not steal a reference, so shifted_lit refcount = 2
            // after Py_DECREF, shifted_lit refcount = 1, but stored in the list so the pointer var can be reused
            // SET_ITEM steals a reference, so : no Py_DECREF on items !

            // Ret int 1 if lit is false, -1 on failure
            if (PyObject_Not(lit_sign)) {

                multiply_result = PyNumber_Multiply(lit_cod, minus_one);
                PyList_SET_ITEM(num_clause, i, multiply_result);
                Py_DECREF(lit_cod);
                // Because PyList_SET_ITEM steals the reference of multiply_result, we don't do Py_DECREF(multiply_result);
            } else {

                PyList_SET_ITEM(num_clause, i, lit_cod);
                // Because lit_cod is built in place (the reference is not borrowed)
                // and because PyList_SET_ITEM steals the reference of lit_cod, we don't do Py_DECREF(lit_cod);
            }

        } else {

            // Borrowed reference
            lit_cod = PyDict_GetItem(var_code_table, lit_name);
            if (lit_cod == NULL) {
                PyErr_SetString(PyExc_SystemError, "lit_name not found in dict");
                return NULL;
            }

            // Ret int 1 if lit is false, -1 on failure
            if (PyObject_Not(lit_sign)) {

                multiply_result = PyNumber_Multiply(lit_cod, minus_one);
                PyList_SET_ITEM(num_clause, i, multiply_result);
                // Because PyList_SET_ITEM steals the reference of multiply_result, we don't do Py_DECREF(multiply_result);
            } else {

                PyList_SET_ITEM(num_clause, i, lit_cod);
                Py_INCREF(lit_cod);
                // Because lit_cod reference IS borrowed (owned by PyDict_GetItem),
                // we don't do Py_DECREF(lit_cod) and because PyList_SET_ITEM steals the reference of lit_cod,
                // we do an INCREF on it.
            }
        }

        i++;

        /* release reference when done */
        Py_DECREF(res);
        Py_DECREF(lit_name);
        Py_DECREF(name_last_char);
        Py_DECREF(lit_sign);
        Py_DECREF(lit);
    }

    /* release reference when done */
    Py_DECREF(iterator);
    Py_DECREF(last_char);
    Py_DECREF(py_shift_step);
    Py_DECREF(minus_one);
    Py_DECREF(literals);

    if (PyErr_Occurred()) {
        /* propagate error */
        Py_DECREF(num_clause);
        return PyErr_SetFromErrno(outofconflerr);
    }

    // Return list of all num_clause
    return num_clause;
}

PyDoc_STRVAR(forward_init_dynamic_doc,
"forward_init_dynamic(clause, var_code_table, shift_step, [aux_clauses])\n\
Dynamics initialisations. Set dynamic constraints for a forward one step: X1 = f(X0)\n\
\n\
Numerically code a clause with the numeric code found in self.__var_code_table for\n\
a base variable x and numeric_code + shift_step for x'\n\
variable integer coding increases in futur steps\n\
\n\
:param arg1: List of Clause objects\n\
:param arg2: Var code table from the model\n\
:param arg3: Shift step dependant on the run\n\
:param arg4: List of auxiliary Clause objects\n\
:return: A list of lists of DIMACS coding of the forward shifted clause\n\
:type arg1: <list>\n\
:type arg2: <dict>\n\
:type arg3: <int>\n\
:type arg4: <list>\n\
:rtype: <list <list>>"
);

static PyObject* forward_init_dynamic(PyObject *self, PyObject *args, PyObject *kwds)
{
    #ifndef NDEBUG
    /* Debugging code */
    printf("forward init dynamic\n");
    #endif

    int shift_step;
    PyObject *clauses;
    // The C variables corresponding to optional arguments should be initialized to their default value —
    // when an optional argument is not specified, PyArg_ParseTuple() does not touch the contents of the corresponding C variable(s).
    PyObject *aux_clauses = PyList_New(0);
    PyObject *var_code_table;

    static char* kwlist[] = {"clauses", "var_code_table", "shift_step", "aux_clauses", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOi|O", kwlist,
                                     &clauses,
                                     &var_code_table,
                                     &shift_step,
                                     &aux_clauses)) {
        return NULL;
    }

    PyObject *num_clause = PyList_New(PySequence_Size(clauses) + PySequence_Size(aux_clauses));
    if (num_clause == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed to create a list");
        return NULL;
    }

    // Default clauses ////////////////////////////////////////////////////////

    PyObject *iterator = PyObject_GetIter(clauses);
    if (iterator == NULL) {
        /* propagate error */
        PyErr_SetString(PyExc_SystemError, "could not create iterator on list");
        return NULL;
    }

    PyObject *clause;
    PyObject *arglist;
    Py_ssize_t i = 0;
    while ((clause = PyIter_Next(iterator)) != NULL) {

        // Build parameters of forward_code
        // {"clause", "var_code_table", "shift_step", NULL};
        arglist = Py_BuildValue("(OOi)", clause, var_code_table, shift_step);
        PyList_SET_ITEM(num_clause, i, forward_code(self, arglist, NULL));

        /* release reference when done */
        // no DECREF on the return of forward_code, because PyList_SET_ITEM steals reference
        Py_DECREF(arglist);
        Py_DECREF(clause);

        i++;
    }

    /* release reference when done */
    Py_DECREF(iterator);

    // Auxiliary clauses //////////////////////////////////////////////////////

    iterator = PyObject_GetIter(aux_clauses);
    if (iterator == NULL) {
        /* propagate error */
        PyErr_SetString(PyExc_SystemError, "could not create iterator on list");
        return NULL;
    }

    while ((clause = PyIter_Next(iterator)) != NULL) {

        // Build parameters of forward_code
        // {"clause", "var_code_table", "shift_step", NULL};
        arglist = Py_BuildValue("(OOi)", clause, var_code_table, shift_step);
        PyList_SET_ITEM(num_clause, i, forward_code(self, arglist, NULL));

        /* release reference when done */
        // no DECREF on the return of forward_code, because PyList_SET_ITEM steals reference
        Py_DECREF(arglist);
        Py_DECREF(clause);

        i++;
    }

    /* release reference when done */
    Py_DECREF(iterator);

    PyObject* dynamic_constraints = PyList_New(1);
    // NULL on failure
    PyList_SET_ITEM(dynamic_constraints, 0, num_clause);

    if (PyErr_Occurred()) {
        /* propagate error */
        Py_DECREF(dynamic_constraints);
        // No decref (SET_ITEM) Py_DECREF(num_clause);
        return PyErr_SetFromErrno(outofconflerr);
    }

    // Return list of all dynamic_constraints
    return dynamic_constraints;
}

PyDoc_STRVAR(shift_dynamic_doc,
"shift_dynamic(dynamic_constraint, shift_step)\n\
Shift clauses representing the dynamics X' = f(X,I,C)\n\
\n\
:param arg1: List of Clause objects (dynamic_constraints)\n\
:param arg2: Shift step dependant on the run\n\
:return: A list of DIMACS coding of the forward shifted clause\n\
:type arg1: <list>\n\
:type arg2: <int>\n\
:rtype: <list <list>>"
);

static PyObject* shift_dynamic(PyObject *self, PyObject *args, PyObject *kwds)
{
    #ifndef NDEBUG
    /* Debugging code */
    printf("shift dynamic\n");
    #endif

    int shift_step;
    PyObject* constraints;

    static char* kwlist[] = {"dynamic_constraint", "shift_step", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "Oi", kwlist,
                                     &constraints,
                                     &shift_step)) {
        return NULL;
    }

    if (!PySequence_Check(constraints)) {
        PyErr_SetString(PyExc_TypeError, "list expected");
        return NULL;
    }

    Py_ssize_t size = PySequence_Size(constraints);
    if (size == 0) {
        // Empty list, return empty list
        return PyList_New(0);
    }
    //printf("List size: %d\n", size);

    PyObject *shifted_clauses = PyList_New(PySequence_Size(constraints));
    if (shifted_clauses == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed to create a list");
        return NULL;
    }

    // Iterate on last item
    PyObject *iterator = PyObject_GetIter(constraints);
    if (iterator == NULL) {
        /* propagate error */
        PyErr_SetString(PyExc_SystemError, "could not create iterator on list");
        return NULL;
    }

    PyObject *shifted_clause;
    PyObject *clause;
    PyObject *arglist;
    Py_ssize_t i = 0;
    while ((clause = PyIter_Next(iterator)) != NULL) {

        // Build parameters of shift_clause
        // shifted_clause = shift_clause(self, clause, shift_step);
        arglist = Py_BuildValue("(Oi)", clause, shift_step);
        shifted_clause = shift_clause(self, arglist, NULL);
        Py_DECREF(arglist);

        if(shifted_clause == NULL) {
            /* Pass error back */
            Py_DECREF(shifted_clauses);
            Py_DECREF(iterator);
            return NULL;
        }

        PyList_SET_ITEM(shifted_clauses, i, shifted_clause);

        /* release reference when done */
        // no DECREF on the return of shift_clause, because PyList_SET_ITEM steals reference
        Py_DECREF(clause);

        i++;
    }
    /* release reference when done */
    Py_DECREF(iterator);

    return shifted_clauses;
}

PyDoc_STRVAR(unflatten_doc,
"unflatten(solution, len_shift_step_init, shift_step)\n\
Transform a flat DIMACS representation of a trajectory into a list<list<int>>\n\
each sublist represents a state vector. Auxiliary variables introduced by\n\
properties compiling are ignored.\n\
\n\
:param arg1: List of Clause objects (dynamic_constraints)\n\
:param arg2: \n\
:param arg3: Shift step dependant on the run\n\
:return: A list of state vectors (list<int>) in DIMACS format\n\
:type arg1: <list>\n\
:type arg2: <int>\n\
:type arg3: <int>\n\
:rtype: <list <list <int>>>"
);

static PyObject* unflatten(PyObject *self, PyObject *args, PyObject *kwds)
{
    #ifndef NDEBUG
    /* Debugging code */
    printf("unflatten\n");
    #endif

    int shift_step;
    int len_shift_step_init;
    PyObject* solution;

    static char* kwlist[] = {"solution", "len_shift_step_init", "shift_step", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "Oii", kwlist,
                                     &solution,
                                     &len_shift_step_init,
                                     &shift_step)) {
        return NULL;
    }

    Py_ssize_t solution_size = PySequence_Size(solution);
    // print(len_shift_step_init, len(self.__solution)) (47633, 238164)
    // Len: (238164 - 47633) / 47633 = 4
    // PyObject *lv_traj = PyList_New((solution_size - shift_step) / shift_step);
    PyObject *lv_traj = PyList_New(0);
    if (lv_traj == NULL) {
        PyErr_SetString(PyExc_SystemError, "failed to create a list");
        return NULL;
    }

    Py_ssize_t step = 0;
    Py_ssize_t dec = 0;
    PyObject *unshift_code;
    PyObject *item;
    PyObject *tmp_traj;
    PyObject *arglist;
    while ((dec + shift_step) < solution_size) {

        tmp_traj = PyList_New((Py_ssize_t)len_shift_step_init);

        for (Py_ssize_t i = 0; i < (Py_ssize_t)len_shift_step_init; i++) {

            // Get item of solution (int)
            // New reference.
            item = PySequence_GetItem(solution, i + dec);
            if(item == NULL) {
                return NULL;
            }

            // Build parameters of get_unshift_code
            // {"var_num", "shift_step", NULL};
            #ifdef IS_PY3K
            arglist = Py_BuildValue("(ii)", PyLong_AS_LONG(item), shift_step);
            #else
            arglist = Py_BuildValue("(ii)", PyInt_AS_LONG(item), shift_step);
            #endif

            Py_DECREF(item);
            unshift_code = get_unshift_code(self, arglist, NULL);
            Py_DECREF(arglist);
            if(unshift_code == NULL) {
                /* Pass error back */
                Py_DECREF(unshift_code);
                return NULL;
            }

            PyList_SET_ITEM(tmp_traj, i, unshift_code);
        }

        //PyList_SET_ITEM(lv_traj, step, tmp_traj);
        PyList_Append(lv_traj, tmp_traj);
        Py_DECREF(tmp_traj);

        step++;
        // first index of time step
        dec = step * shift_step;

    }

    if (PyErr_Occurred()) {
        /* propagate error */
        Py_DECREF(lv_traj);
        return PyErr_SetFromErrno(outofconflerr);
    }

    // Return list of all trajectories
    return lv_traj;
}

/*************************** Method definitions *************************/

static PyMethodDef module_methods[] = {
    {"get_unshift_code", (PyCFunction) get_unshift_code, METH_VARARGS | METH_KEYWORDS, get_unshift_code_doc},
    {"unflatten", (PyCFunction) unflatten, METH_VARARGS | METH_KEYWORDS, unflatten_doc},
    {"shift_clause", (PyCFunction) shift_clause, METH_VARARGS | METH_KEYWORDS, shift_clause_doc},
    {"shift_dynamic", (PyCFunction) shift_dynamic, METH_VARARGS | METH_KEYWORDS, shift_dynamic_doc},
    {"forward_code", (PyCFunction) forward_code, METH_VARARGS | METH_KEYWORDS, forward_code_doc},
    {"forward_init_dynamic", (PyCFunction) forward_init_dynamic, METH_VARARGS | METH_KEYWORDS, forward_init_dynamic_doc},
    {NULL, NULL, 0, NULL}     /* Sentinel - marks the end of this structure */
};

MODULE_INIT_FUNC(_cadbiom)
{
    PyObject* m;

    #ifdef IS_PY3K
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,  /* m_base */
        "_cadbiom",             /* m_name */
        NULL,                   /* m_doc */
        -1,                     /* m_size */
        module_methods          /* m_methods */
    };

    m = PyModule_Create(&moduledef);
    #else
    m = Py_InitModule3("_cadbiom", module_methods,
                       "Example module that creates an extension type.");
    #endif

    // Return NULL on Python3 and on Python2 with MODULE_INIT_FUNC macro
    // In pure Python2: return nothing.
    if (!m) {
        Py_XDECREF(m);
        return NULL;
    }

    PyModule_AddObject(m, "__version__", PyUnicode_FromString(CADBIOM_VERSION));
    if (!(outofconflerr = PyErr_NewExceptionWithDoc("_cadbiom.InternalError", "Unsupported error.", NULL, NULL))) {
        goto error;
    }
    PyModule_AddObject(m, "OutOfConflicts",  outofconflerr);

error:
    if (PyErr_Occurred())
    {
        PyErr_SetString(PyExc_ImportError, "_cadbiom: init failed");
        Py_DECREF(m);
        m = NULL;
    }
    return m;
}

int main(void)
{
    printf("Try to invoke main() for debugging !!!!\n");


    //init_cadbiom();
    PyObject *func_result = NULL;

    /*
    // shift_clause([66036, -66037], 47633)
    PyObject *list = PyList_New(2);
    PyObject *list_elem = PyInt_FromLong(66036);
    PyObject *list_elem_1 = PyInt_FromLong(-66037);
    PyList_SET_ITEM(list, 0, list_elem);
    PyList_SET_ITEM(list, 1, list_elem_1);

    PyObject *arglist = Py_BuildValue("(Oi)", list, 47633);
    printf("ici 2\n");
    func_result = shift_clause(NULL, arglist, NULL);
    printf("LA\n");
    Py_DECREF(arglist);
    Py_DECREF(func_result);
    Py_DECREF(list);
    */

    // get_unshift_code(50, 47633)
    PyObject *arglist = Py_BuildValue("(ii)", (Py_ssize_t)50, (Py_ssize_t)47633);
    func_result = get_unshift_code(NULL, arglist, NULL);
    Py_DECREF(arglist);
    Py_DECREF(func_result);

    return EXIT_SUCCESS;
}
