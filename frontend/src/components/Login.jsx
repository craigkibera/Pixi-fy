import React from "react";
import { useFormik } from "formik";
import * as yup from "yup";
import { useNavigate, Link } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";

const LoginForm = () => {
  const navigate = useNavigate();

  // 1) Validation schema
  const formSchema = yup.object().shape({
    email: yup.string().email("Invalid email").required("Email is required"),
    password: yup.string().required("Password is required"),
  });

  // 2) Formik setup
  const formik = useFormik({
    initialValues: { email: "", password: "" },
    validationSchema: formSchema,
    onSubmit: (values) => {
      fetch("https://pixi-fy.onrender.com/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      })
        .then((res) => {
          if (!res.ok) {
            return res.json().then((e) => {
              throw new Error(e.message || "Login failed");
            });
          }
          return res.json();
        })
        .then((data) => {
          const userId = data.user?.id ?? data.id;
          sessionStorage.setItem("userId", userId);
          toast.success("Login successful!");
          navigate("/home");
        })
        .catch((err) => {
          console.error("Login error:", err);
          toast.error(err.message || "Login failed");
        });
    },
  });

  return (
    <div className="bg-gray-500 text-white h-screen flex items-center justify-center">
      <form
        className="w-full max-w-sm bg-gray-700 p-6 rounded-lg"
        onSubmit={formik.handleSubmit}
      >
        <h1 className="text-center text-2xl mb-4">User Login</h1>

        <label className="block">Email</label>
        <input
          type="email"
          {...formik.getFieldProps("email")}
          className="w-full mt-1 p-2 border border-gray-300 rounded bg-white text-black"
        />
        {formik.touched.email && formik.errors.email && (
          <p className="text-red-400 italic text-sm">{formik.errors.email}</p>
        )}

        <label className="block mt-4">Password</label>
        <input
          type="password"
          {...formik.getFieldProps("password")}
          className="w-full mt-1 p-2 border border-gray-300 rounded bg-white text-black"
        />
        {formik.touched.password && formik.errors.password && (
          <p className="text-red-400 italic text-sm">{formik.errors.password}</p>
        )}

        <button
          type="submit"
          className="mt-6 bg-purple-700 w-full text-white rounded p-2 hover:bg-purple-800 transition"
        >
          Login
        </button>

        <div className="mt-4 text-center">
          <span>Don't have an account? </span>
          <Link to="/signup" className="text-blue-300 hover:text-blue-500">
            Sign up
          </Link>
        </div>
      </form>
      <ToastContainer />
    </div>
  );
};

export default LoginForm;
