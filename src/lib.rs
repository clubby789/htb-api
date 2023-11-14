use hackthebox_rs::HackTheBox;
use std::collections::HashMap;

use pyo3::create_exception;
use pyo3::prelude::*;
use pyo3::types::{PyBool, PyString};
use serde_json::Value;

#[pyclass(frozen)]
struct HTBClient(HackTheBox);

#[pymethods]
impl HTBClient {
    #[new]
    fn new(token: String) -> Self {
        Self(HackTheBox::new_authenticated(token))
    }

    fn do_get_request<'py>(
        slf: PyRef<Self>,
        py: Python<'py>,
        endpoint: &PyString,
        authenticated: Option<bool>,
    ) -> PyResult<PyObject> {
        let slf: Py<Self> = slf.into();
        let endpoint = endpoint.to_string_lossy().into_owned();
        pyo3_asyncio::tokio::future_into_py(py, async move {
            let val = slf
                .get()
                .0
                .do_get_request::<Value>(&endpoint, authenticated.unwrap_or(true))
                .await
                .map_err(|err| HTBException::new_err(err.to_string()))?;
            Ok(Python::with_gil(|py| value_to_py(py, val)))
        })
        .map(|p| p.into())
    }
}

fn value_to_py(py: Python, value: Value) -> PyObject {
    match value {
        Value::Null => py.None(),
        Value::Bool(b) => PyBool::new(py, b).to_object(py),
        Value::Number(n) => {
            if let Some(n) = n.as_u64() {
                n.to_object(py)
            } else if let Some(n) = n.as_i64() {
                n.to_object(py)
            } else if let Some(n) = n.as_f64() {
                n.to_object(py)
            } else if let Some(n) = n.as_u64() {
                n.to_object(py)
            } else {
                unreachable!()
            }
        }
        Value::String(s) => s.to_object(py),
        Value::Array(arr) => {
            let v = arr
                .into_iter()
                .map(|v| value_to_py(py, v))
                .collect::<Vec<_>>();
            v.to_object(py)
        }
        Value::Object(o) => {
            let hm = o
                .into_iter()
                .map(|(k, v)| (k, value_to_py(py, v)))
                .collect::<HashMap<_, _>>();
            hm.to_object(py)
        }
    }
}

create_exception!(hackthebox, HTBException, pyo3::exceptions::PyException);

/// A Python module implemented in Rust.
#[pymodule]
fn hackthebox(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<HTBClient>()?;
    Ok(())
}
