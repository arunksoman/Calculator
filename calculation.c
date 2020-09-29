#include <Python.h>
float Csubtract(float num1, float num2)
{
    return num1 - num2;
}
float Cmultiplication(float num1, float num2){
    return num1 * num2;
} 
static PyObject* subtract(PyObject* self, PyObject* args)
{
    float num1, num2;
    if (!PyArg_ParseTuple(args, "f", &num1, &num2))
        return NULL;
 
    return Py_BuildValue("f", Csubtract(num1, num2));
}

static PyObject* multiplication(PyObject* self, PyObject* args)
{
    float num1, num2;
    if (!PyArg_ParseTuple(args, "f", &num1, &num2))
        return NULL;
 
    return Py_BuildValue("f", Cmultiplication(num1, num2));
}
static PyObject* version(PyObject* self)
{
    return Py_BuildValue("s", "Version 1.0");
}
 
static PyMethodDef myMethods[] = {
    {"subtract", subtract, METH_VARARGS, "C bridge for subtraction"},
    {"multiplication", multiplication, METH_VARARGS, "C bridge for multiplication"},
    {"version", (PyCFunction)version, METH_NOARGS, "Returns the version."},
    {NULL, NULL, 0, NULL}
};
 
static struct PyModuleDef calculation = {
	PyModuleDef_HEAD_INIT, 
    "calculation", "Floating point arithmetic Module", -1, myMethods
};

PyMODINIT_FUNC PyInit_calculation(void)
{
    return PyModule_Create(&calculation);
}