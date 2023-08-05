#include <Python.h>
#include "sleepless.h"

static PyObject *
sleepless_keep_awake(PyObject *self, PyObject *args) {
    CFStringRef cfstr;
    Py_UNICODE *str;
    int len;
    PyObject *ret;

    if (!PyArg_ParseTuple(args, "u#", &str, &len)) return NULL;
    cfstr = CFStringCreateWithCharacters(NULL, str, len);
    ret = Py_BuildValue("i", sleeplessKeepAwake(cfstr));
    CFRelease(cfstr);
    return ret;
}


static PyObject *
sleepless_allow_sleep(PyObject *self, PyObject *args) {
    return Py_BuildValue("i", sleeplessAllowSleep());
}


static PyMethodDef SleeplessMethods[] = {
    {"keep_awake", sleepless_keep_awake, METH_VARARGS,
     "Tell OS to stay awake\n"
     "One argument: text to send to OS (plain ASCII or Unicode)\n"
     "Stays in effect until next 'allow_sleep' call\n"
     "Multiple calls allowed)"},

    {"allow_sleep", sleepless_allow_sleep, METH_VARARGS,
     "Allow OS to go to sleep\n"
     "Stays in effect until next 'keep_awake' call\n"
     "Multiple calls allowed)"},

    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC initsleepless(void) {
    (void)Py_InitModule("sleepless", SleeplessMethods);
}
