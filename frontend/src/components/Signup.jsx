import React from "react";
import { useFormik } from "formik";
import * as yup from "yup";
import { useNavigate, Link } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";

const SignupForm = () => {
  const navigate = useNavigate();
  // 1) Validation schema
  const formSchema = yup.object().shape({
    username:   yup.string().required("Username is required"),
    email:      yup.string().email("Invalid email").required("Email is required"),
    password:   yup.string().min(6, "Password must be at least 6 characters").required("Password is required"),
    first_name: yup.string().required("First name is required"),
    last_name:  yup.string().required("Last name is required"),
  });

  // 2) Formik setup
  const formik = useFormik({
    initialValues: {
      username:   "",
      email:      "",
      password:   "",
      first_name: "",
      last_name:  "",
    },
    validationSchema: formSchema,
    onSubmit: (values, { resetForm }) => {
      fetch("https://pixi-fy.onrender.com/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      })
        .then((res) => {
          if (!res.ok) {
            return res.json().then((e) => { throw new Error(e.message || "Signup failed"); });
          }
          return res.json();
        })
        .then((data) => {
          toast.success("Signup successful!");
          resetForm();
          navigate("/login");
        })
        .catch((err) => {
          console.error("Error:", err);
          toast.error(err.message || "Something went wrong.");
        });
    },
  });

  return (
    <div className="bg-gray-500 text-white h-screen flex items-center justify-center">
      <form
        onSubmit={formik.handleSubmit}
        className="w-full max-w-md bg-gray-700 p-8 rounded-lg shadow-md"
      >
        <h2 className="text-2xl text-center mb-6">User Signup</h2>

        {/* Username */}
        <label className="block">Username</label>
        <input
          {...formik.getFieldProps("username")}
          className="w-full mt-1 p-2 border border-gray-300 rounded bg-white text-black"
          placeholder="Enter your username"
        />
        {formik.touched.username && formik.errors.username && (
          <p className="text-red-400 italic text-sm">{formik.errors.username}</p>
        )}

        {/* Email */}
        <label className="block mt-4">Email</label>
        <input
          {...formik.getFieldProps("email")}
          className="w-full mt-1 p-2 border border-gray-300 rounded bg-white text-black"
          placeholder="you@example.com"
        />
        {formik.touched.email && formik.errors.email && (
          <p className="text-red-400 italic text-sm">{formik.errors.email}</p>
        )}

        {/* Password */}
        <label className="block mt-4">Password</label>
        <input
          type="password"
          {...formik.getFieldProps("password")}
          className="w-full mt-1 p-2 border border-gray-300 rounded bg-white text-black"
          placeholder="••••••••"
        />
        {formik.touched.password && formik.errors.password && (
          <p className="text-red-400 italic text-sm">{formik.errors.password}</p>
        )}

        {/* First Name */}
        <label className="block mt-4">First Name</label>
        <input
          {...formik.getFieldProps("first_name")}
          className="w-full mt-1 p-2 border border-gray-300 rounded bg-white text-black"
          placeholder="John"
        />
        {formik.touched.first_name && formik.errors.first_name && (
          <p className="text-red-400 italic text-sm">{formik.errors.first_name}</p>
        )}

        {/* Last Name */}
        <label className="block mt-4">Last Name</label>
        <input
          {...formik.getFieldProps("last_name")}
          className="w-full mt-1 p-2 border border-gray-300 rounded bg-white text-black"
          placeholder="Doe"
        />
        {formik.touched.last_name && formik.errors.last_name && (
          <p className="text-red-400 italic text-sm">{formik.errors.last_name}</p>
        )}

        <button
          type="submit"
          className="mt-6 w-full bg-purple-700 hover:bg-purple-800 transition text-white py-2 rounded"
        >
          Sign Up
        </button>

        <div className="mt-4 text-center">
          <span>Already have an account? </span>
          <Link to="/login" className="text-blue-300 hover:text-blue-500">
            Login here
          </Link>
        </div>
      </form>
      <ToastContainer />
    </div>
  );
};

export default SignupForm;
