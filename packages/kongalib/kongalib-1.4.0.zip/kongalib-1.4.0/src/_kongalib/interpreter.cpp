/** @file mga/module/interpreter.cpp
 *
 *		Sub-interpreter for Python scripts execution.
 *
 *		$Revision: 10370 $
 *		$Date: 2013-04-09 18:56:39 +0200 (Mar, 09 Apr 2013) $
 *		$Author: lillo $
 *
 *		\defgroup mga_module MGA Python extension module
 *		The MGA Python extension module is a wrapper around the \ref mga_client and part of the \ref CL for Python.
 */

/*@{*/

#include "module.h"

#ifdef __CL_WIN32__
#include <io.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#endif

#define DEBUG		0



static int
interpreter_timeout_handler(MGA::InterpreterObject *interpreter, PyObject *frame, int what, PyObject *arg)
{
	int result = 0;
	if (interpreter->fTimeOut > 0) {
		if ((CL_GetTime() - interpreter->fStartTime) > interpreter->fTimeOut) {
			result = -1;
			PyEval_SetTrace(NULL, NULL);
			PyObject *module = PyImport_ImportModule("kongalib.scripting");
			if (module) {
				PyObject *dict = NULL;
				PyObject *func = NULL;
		
				dict = PyModule_GetDict(module);
				func = PyDict_GetItemString(dict, "timeout_handler");
				if (func) {
					PyObject *res = NULL;
					Py_INCREF(func);
					res = PyObject_CallFunctionObjArgs(func, NULL);
					Py_DECREF(func);
					
					if (res) {
						Py_DECREF(res);
						result = 0;
					}
				}
				Py_DECREF(module);
			}
			if (result == 0)
				interpreter->fTimeOut = 0;
			interpreter->fStartTime = CL_GetTime();
			PyEval_SetTrace((Py_tracefunc)interpreter_timeout_handler, (PyObject *)interpreter);
		}
	}
	return result;
}


class InterpreterJob : public CL_Job
{
public:
	InterpreterJob(MGA::InterpreterObject *interpreter)
		: CL_Job(), fInterpreter(interpreter)
	{
	}
	
	virtual CL_Status Run() {
#if DEBUG
		fprintf(stderr, "InterpreterJob::Run() enter\n");
#endif
		if ((Py_IsInitialized()) && (MGA::gInitialized)) {
			PyObject *object, *item, *module, *dict, *func, *code, *scriptingModule = NULL;
			uint32 i;
			bool write_pyc = false, load_module = true;
			long PyImport_GetMagicNumber(void);
			long magic;
			CL_TimeStamp mtime;
			
			PyEval_AcquireLock();
			fInterpreter->fState = Py_NewInterpreter();
			
			module = PyImport_AddModule("__main__");
			dict = PyModule_GetDict(module);
			
			item = PyCodec_Encoder("ascii");
			Py_XDECREF(item);
			
			for (;;) {
#if DEBUG
				fprintf(stderr, "InterpreterJob::Run() starting loop\n");
#endif
				while ((fInterpreter->fRunning) && (!fInterpreter->fExecute)) {
					Py_BEGIN_ALLOW_THREADS
					fInterpreter->fLock.Lock();
					fInterpreter->fReady.Signal();
					fInterpreter->fCond.Wait(&fInterpreter->fLock, 10);
					fInterpreter->fLock.Unlock();
					Py_END_ALLOW_THREADS
				}
				if (!fInterpreter->fRunning) {
#if DEBUG
					fprintf(stderr, "InterpreterJob::Run() exiting loop\n");
#endif
					break;
				}
#if DEBUG
				fprintf(stderr, "InterpreterJob::Run() got execute request\n");
#endif
				object = PyList_New(fInterpreter->fArgv.Count());
				for (i = 0; i < fInterpreter->fArgv.Count(); i++) {
					item = PyUnicode_DecodeUTF8(fInterpreter->fArgv[i].c_str(), fInterpreter->fArgv[i].size(), "replace");
					PyList_SET_ITEM(object, i, item);
				}
				PySys_SetObject("argv", object);
				Py_DECREF(object);
				
				object = PyList_New(fInterpreter->fPath.Count());
				for (i = 0; i < fInterpreter->fPath.Count(); i++) {
					item = PyUnicode_DecodeUTF8(fInterpreter->fPath[i].c_str(), fInterpreter->fPath[i].size(), "replace");
					PyList_SET_ITEM(object, i, item);
				}
				PySys_SetObject("path", object);
				Py_DECREF(object);
				
				if (load_module) {
#if DEBUG
					fprintf(stderr, "InterpreterJob::Run() loading kongalib.scripting\n");
#endif
					scriptingModule = PyImport_ImportModule("kongalib.scripting");
					load_module = false;
					if (!scriptingModule) {
#if DEBUG
						fprintf(stderr, "InterpreterJob::Run() kongalib.scripting exception!\n");
#endif
						PyErr_Print();
						PyThreadState_SetAsyncExc(fOwnerState->thread_id, PyErr_Occurred());
						fInterpreter->fExecute = false;
						fInterpreter->fReady.Signal();
						break;
					}
				}
				if (scriptingModule) {
					func = PyDict_GetItemString(PyModule_GetDict(scriptingModule), "init_interpreter");
					if (func) {
#if DEBUG
						fprintf(stderr, "InterpreterJob::Run() running init_interpreter\n");
#endif
						Py_INCREF(func);
						object = PyObject_CallFunctionObjArgs(func, NULL);
						Py_XDECREF(object);
						Py_DECREF(func);
						if (!object) {
#if DEBUG
							fprintf(stderr, "InterpreterJob::Run() init_interpreter exception!\n");
#endif
							PyErr_Print();
							PyThreadState_SetAsyncExc(fOwnerState->thread_id, PyErr_Occurred());
							fInterpreter->fExecute = false;
							fInterpreter->fReady.Signal();
							break;
						}
					}
					else {
#if DEBUG
						fprintf(stderr, "InterpreterJob::Run() init_interpreter not found!\n");
#endif
					}
				}
				
				fInterpreter->fStartTime = CL_GetTime();
			
				if (!fInterpreter->fHasCode) {
					code = NULL;
					uint32 info = CL_StatFile(fInterpreter->fFileName, NULL, NULL, &mtime);
					string pyc_fileName = fInterpreter->fFileName + "c";
					FILE *f = fopen(pyc_fileName.c_str(), "rb");
					if (f) {
						magic = PyMarshal_ReadLongFromFile(f);
						if (magic != PyImport_GetMagicNumber()) {
							PyErr_SetString(PyExc_RuntimeError, "Bad magic number in .pyc file");
						}
						else {
							CL_TimeStamp pyc_mtime = CL_TimeStamp((int)PyMarshal_ReadLongFromFile(f));
							if ((info) && (mtime > pyc_mtime)) {
								fclose(f);
								f = NULL;
							}
							else {
								code = PyMarshal_ReadLastObjectFromFile(f);
								if ((!code) || (!PyCode_Check(code))) {
									Py_XDECREF(code);
									PyErr_SetString(PyExc_RuntimeError, "Bad code object in .pyc file");
								}
							}
						}
						if (f)
							fclose(f);
					}
					
					if (!f) {
						CL_Blob data;
						CL_Status status = CL_ReadFile(fInterpreter->fFileName, &data);
						if (status != CL_OK) {
							PyErr_Format(PyExc_IOError, "Cannot open input file '%s'", fInterpreter->fFileName.c_str());
						}
						else {
							const char *script;
							script << data;
							code = Py_CompileString(script, fInterpreter->fFileName.c_str(), Py_file_input);
							write_pyc = true;
						}
					}
				}
				else {
					code = Py_CompileString(fInterpreter->fScript.c_str(), fInterpreter->fFileName.c_str(), Py_file_input);
				}
				if (code) {
					if (write_pyc) {
#if DEBUG
						fprintf(stderr, "InterpreterJob::Run() writing .pyc\n");
#endif
						string pyc_fileName = fInterpreter->fFileName + "c";
						CL_DeleteFile(pyc_fileName);
	#ifdef WIN32
						int fd = _open(pyc_fileName.c_str(), _O_EXCL|_O_CREAT|_O_WRONLY|_O_TRUNC|_O_BINARY, _S_IREAD|_S_IWRITE);
	#else
						int fd = open(pyc_fileName.c_str(), O_EXCL|O_CREAT|O_WRONLY|O_TRUNC
	#ifdef O_BINARY
							|O_BINARY
	#endif
							, S_IROTH|S_IRGRP|S_IRUSR|S_IWUSR);
	#endif
						if (fd >= 0) {
							FILE *f = fdopen(fd, "wb");
							if (f) {
								PyMarshal_WriteLongToFile(PyImport_GetMagicNumber(), f, Py_MARSHAL_VERSION);
								PyMarshal_WriteLongToFile((int)mtime, f, Py_MARSHAL_VERSION);
								PyMarshal_WriteObjectToFile(code, f, Py_MARSHAL_VERSION);
								if (fflush(f) || ferror(f)) {
									fclose(f);
									CL_DeleteFile(pyc_fileName);
								}
								else {
									fclose(f);
								}
							}
						}
					}
#if DEBUG
					fprintf(stderr, "InterpreterJob::Run() executing code\n");
#endif
					PyEval_SetTrace((Py_tracefunc)interpreter_timeout_handler, (PyObject *)fInterpreter);
					object = PyEval_EvalCode((PyCodeObject *)code, dict, dict);
					PyEval_SetTrace(NULL, NULL);
					Py_DECREF(code);
				}
				else {
#if DEBUG
					fprintf(stderr, "InterpreterJob::Run() no code to execute!\n");
#endif
					object = NULL;
				}
				
				if (!object) {
					if (!PyErr_ExceptionMatches(PyExc_SystemExit))
						PyErr_Print();
					PyErr_Clear();
				}
				else
					Py_DECREF(object);
				
				if (scriptingModule) {
#if DEBUG
					fprintf(stderr, "InterpreterJob::Run() running exit_interpreter\n");
#endif
					func = PyDict_GetItemString(PyModule_GetDict(scriptingModule), "exit_interpreter");
					if (func) {
						Py_INCREF(func);
						object = PyObject_CallFunctionObjArgs(func, NULL);
						if (object)
							Py_DECREF(object);
						else
							PyErr_Clear();
						Py_DECREF(func);
					}
				}
				fInterpreter->fExecute = false;
			}
			Py_XDECREF(scriptingModule);
			
			module = PyImport_ImportModule("threading");
			
			if (!module)
				PyErr_Clear();
			
			if (module) {
				dict = PyModule_GetDict(module);
#if PY_MAJOR_VERSION >= 3
				func = PyDict_GetItemString(dict, "current_thread");
#else
				func = PyDict_GetItemString(dict, "currentThread");
#endif
				if (func) {
					PyObject *res = NULL;
					Py_INCREF(func);
					res = PyEval_CallObject(func, (PyObject *)NULL);
					if (!res) {
						PyErr_Clear();
					}
					Py_XDECREF(res);
					Py_DECREF(func);
				}
				
				func = PyDict_GetItemString(dict, "_shutdown");
				if (func) {
					PyObject *res = NULL;
					Py_INCREF(func);
					res = PyEval_CallObject(func, (PyObject *)NULL);
					if (!res) {
						PyErr_Clear();
					}
					Py_XDECREF(res);
					Py_DECREF(func);
				}
				
				Py_DECREF(module);
			}
			
#if PY_MAJOR_VERSION >= 3
			func = NULL;
			module = PyImport_ImportModule("atexit");
			if (module) {
				dict = PyModule_GetDict(module);
				func = PyDict_GetItemString(dict, "_run_exitfuncs");
			}
			else
				PyErr_Clear();
#else
			module = NULL;
			func = PySys_GetObject("exitfunc");
#endif
			if (func) {
				PyObject *res = NULL;
				Py_INCREF(func);
				PySys_SetObject("exitfunc", (PyObject *)NULL);
				res = PyEval_CallObject(func, (PyObject *)NULL);
				if (res) {
					Py_DECREF(res);
				}
				else {
					if (!PyErr_ExceptionMatches(PyExc_SystemExit))
						PyErr_Print();
	                PyErr_Clear();
	        	}
				Py_DECREF(func);
			}
			Py_XDECREF(module);
			
			PyThreadState *tstate = fInterpreter->fState;
			PyThreadState *tstate_next = NULL;
	
			PyThreadState_Swap(NULL);
	
			tstate = tstate->interp->tstate_head;
			while (tstate) {
				tstate_next = tstate->next;
				if (tstate != fInterpreter->fState) {
					PyThreadState_Swap(tstate);
					PyThreadState_Clear(tstate);
					PyThreadState_Swap(NULL);
					PyThreadState_Delete(tstate);
				}
				tstate = tstate_next;
			}
	
			PyThreadState_Swap(fInterpreter->fState);
			Py_EndInterpreter(fInterpreter->fState);
			fInterpreter->fState = NULL;
			fInterpreter->fExecute = false;
			PyEval_ReleaseLock();
		}
#if DEBUG
		fprintf(stderr, "InterpreterJob::Run() exit\n");
#endif
		return CL_OK;
	}

	void ResetOwner()
	{
		fOwnerState = PyThreadState_Get();
	}
	
private:
	MGA::InterpreterObject		*fInterpreter;
	PyThreadState				*fOwnerState;
};



static MGA::InterpreterObject *
interpreter_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
	return new (type->tp_alloc(type, 0)) MGA::InterpreterObject();
}


static void
interpreter_dealloc(MGA::InterpreterObject *self)
{
	self->~InterpreterObject();
	self->ob_type->tp_free((PyObject*)self);
}


static PyObject *
interpreter_execute(MGA::InterpreterObject *self, PyObject *args, PyObject *kwds)
{
	char *kwlist[] = { "script", "filename", "argv", "path", "timeout", NULL };
	PyObject *script = NULL, *argv = NULL, *path = NULL;
	
	self->fScript = "";
	self->fHasCode = false;
	self->fFileName = "__script__";
	self->fTimeOut = 0;
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OO&OOi", kwlist, &script, MGA::ConvertString, &self->fFileName, &argv, &path, &self->fTimeOut)) {
		return NULL;
	}
	if ((script) && (script != Py_None)) {
		if (!MGA::ConvertString(script, &self->fScript))
			return NULL;
		self->fHasCode = true;
	}
	
	self->fArgv.Clear();
	if (argv) {
		PyObject *seq = PySequence_Fast(argv, "Expected sequence object");
		if (!seq) {
			return NULL;
		}
		for (Py_ssize_t i = 0; i < PySequence_Fast_GET_SIZE(seq); i++) {
			string v;
			if (!MGA::ConvertString(PySequence_Fast_GET_ITEM(seq, i), &v)) {
				Py_DECREF(seq);
				return NULL;
			}
			self->fArgv.Append(v);
		}
		Py_DECREF(seq);
	}
	if (self->fArgv.Count() == 0)
		self->fArgv.Append(self->fFileName);
	
	self->fPath.Clear();
	if (path) {
		PyObject *seq = PySequence_Fast(path, "Expected sequence object");
		if (!seq)
			return NULL;
		for (Py_ssize_t i = 0; i < PySequence_Fast_GET_SIZE(seq); i++) {
			string v;
			if (!MGA::ConvertString(PySequence_Fast_GET_ITEM(seq, i), &v)) {
				Py_DECREF(seq);
				return NULL;
			}
			self->fPath.Append(v);
		}
		Py_DECREF(seq);
	}
	
#if DEBUG
	fprintf(stderr, "execute() enter\n");
#endif
	((InterpreterJob *)self->fJob)->ResetOwner();
	self->fExecute = true;
	Py_BEGIN_ALLOW_THREADS
	self->fLock.Lock();
	self->fCond.Signal();
#if DEBUG
	fprintf(stderr, "execute() signaled job, now waiting\n");
#endif
	while (self->fExecute) {
		self->fReady.Wait(&self->fLock, 50);
	}
	self->fLock.Unlock();
	Py_END_ALLOW_THREADS

#if DEBUG
	fprintf(stderr, "execute() exit\n");
#endif
	if (PyErr_Occurred())
		return NULL;
	
	Py_RETURN_NONE;
}


static PyObject *
interpreter_stop(MGA::InterpreterObject *self, PyObject *args, PyObject *kwds)
{
	if (self->fState) {
		PyThreadState *state = PyThreadState_Swap(self->fState);
		if (PyEval_GetFrame())
			PyThreadState_SetAsyncExc(self->fState->thread_id, PyExc_SystemExit);
		PyThreadState_Swap(state);
	}
	
	Py_RETURN_NONE;
}


static PyObject *
interpreter_is_running(MGA::InterpreterObject *self, PyObject *args, PyObject *kwds)
{
	PyObject *result = (self->fState ? Py_True : Py_False);
	Py_INCREF(result);
	return result;
}


static PyObject *
interpreter_set_timeout(MGA::InterpreterObject *self, PyObject *args, PyObject *kwds, uint32 action)
{
	char *kwlist[] = { "timeout", NULL };
	PyObject *timeout = NULL;
	
	uint32 oldTimeout = self->fTimeOut;
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O", kwlist, &timeout)) {
		return NULL;
	}
	if ((!timeout) || (timeout == Py_None)) {
		self->fTimeOut = 0;
	}
	else {
		long t = PyInt_AsLong(timeout);
		if (PyErr_Occurred()) {
			return NULL;
		}
		self->fTimeOut = t;
	}
	self->fStartTime = CL_GetTime();
	if (oldTimeout == 0)
		Py_RETURN_NONE;
	else
		return PyInt_FromLong(oldTimeout);
}


static PyObject *
interpreter_get_time_left(MGA::InterpreterObject *self, PyObject *args, PyObject *kwds)
{
	uint32 time = CL_GetTime();
	uint32 result;
	
	if ((time - self->fStartTime) > self->fTimeOut)
		result = 0;
	else
		result = self->fTimeOut - (time - self->fStartTime);
	return PyInt_FromLong(result);
}


static PyMethodDef interpreter_methods[] = {
	{	"execute",				(PyCFunction)interpreter_execute,		METH_VARARGS | METH_KEYWORDS,	"execute(script, filename, argv, path, timeout)\n\nExecutes a script in the interpreter" },
	{	"stop",					(PyCFunction)interpreter_stop,			METH_VARARGS | METH_KEYWORDS,	"stop()\n\nStops any execution of this interpreter" },
	{	"is_running",			(PyCFunction)interpreter_is_running,	METH_NOARGS,					"is_running() -> bool\n\nReturns True if interpreter is currently running, False otherwise" },
	{	"set_timeout",			(PyCFunction)interpreter_set_timeout,	METH_VARARGS | METH_KEYWORDS,	"set_timeout(timeout)\n\nSets timeout for this interpreter" },
	{	"get_time_left",		(PyCFunction)interpreter_get_time_left,	METH_NOARGS,					"get_time_left() -> int\n\nReturns remaining time before interpreter timeout" },
	{	NULL }
};



PyTypeObject MGA::InterpreterType = {
	PyObject_HEAD_INIT(NULL)
    0,										/* ob_size */
    "_kongalib.Interpreter",				/* tp_name */
    sizeof(MGA::InterpreterObject),			/* tp_basicsize */
	0,										/* tp_itemsize */
	(destructor)interpreter_dealloc,		/* tp_dealloc */
	0,										/* tp_print */
	0,										/* tp_getattr */
	0,										/* tp_setattr */
	0,										/* tp_compare */
	0,										/* tp_repr */
	0,										/* tp_as_number */
	0,										/* tp_as_sequence */
	0,										/* tp_as_mapping */
	0,										/* tp_hash */
	0,										/* tp_call */
	0,										/* tp_str */
	0,										/* tp_getattro */
	0,										/* tp_setattro */
	0,										/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE,	/* tp_flags */
	"Interpreter objects",					/* tp_doc */
	0,										/* tp_traverse */
	0,										/* tp_clear */
	0,										/* tp_richcompare */
	0,										/* tp_weaklistoffset */
	0,										/* tp_iter */
	0,										/* tp_iternext */
	interpreter_methods,					/* tp_methods */
	0,										/* tp_members */
	0,										/* tp_getset */
	0,										/* tp_base */
	0,										/* tp_dict */
	0,										/* tp_descr_get */
	0,										/* tp_descr_set */
	0,										/* tp_dictoffset */
	0,										/* tp_init */
	0,										/* tp_alloc */
	(newfunc)interpreter_new,				/* tp_new */
};


namespace MGA {
	
	InterpreterObject::InterpreterObject()
		: fRunning(true), fExecute(false), fState(NULL)
	{
		fJob = CL_New(InterpreterJob(this));
		MGA::gDispatcher->AddJob(fJob);
		trackInterpreter(this);
	}
	
	InterpreterObject::~InterpreterObject()
	{
		fRunning = false;
		fCond.Signal();
		Py_BEGIN_ALLOW_THREADS
		while (!MGA::gDispatcher->WaitForJob(fJob, 50)) {
			PyGILState_STATE gstate;
			gstate = PyGILState_Ensure();
			
			if ((MGA::gIdleCB) && (MGA::gIdleCB != Py_None)) {
				PyObject *result = PyObject_CallFunctionObjArgs(MGA::gIdleCB, NULL);
				if (!result) {
					PyErr_Print();
					PyErr_Clear();
				}
				else
					Py_DECREF(result);
			}
			PyGILState_Release(gstate);
		}
		Py_END_ALLOW_THREADS
		CL_Delete(fJob);
		untrackInterpreter(this);
	}
	
	void
	InitInterpreter()
	{
	}
};


