
import { useFormik } from "formik";
import * as yup from "yup";

const Comment = () => {
      // Define Yup validation schema
      const formSchema = yup.object().shape({
        username: yup.string(250).required("Username is required"),
        
      });
    
      // Setup Formik
      const formik = useFormik({
        initialValues: {
          username: ""
        },

        validationSchema: formSchema,
        onSubmit: (values, { resetForm }) => {
          fetch("http://127.0.0.1:5000/comments", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(values),
          })
            .then((res) => {
              if (res.ok) {
                return res.json();
              } else {
                return res.json().then((errorData) => {
                  throw new Error(errorData.message || "Signup failed");
                });
              }
            })
            .then((data) => {
              console.log("User created:", data);
              resetForm();
              alert("Signup successful!");
            })
            .catch((error) => {
              console.error("Error:", error);
              alert("Something went wrong.");
            });
        },
      });
    
      return (
        <div  className="bg-gray-500 text-white h-screen flex itemss-center justify-center">
        <form className=" w-full max-w-sm pt-20" onSubmit={formik.handleSubmit}>
          <h2 className="text-center">Leave a comment</h2>
    
        
          <input
            name="username"
            value={formik.values.username}
            onChange={formik.handleChange}
            className="ml-6 mt-5 p-2 border border-gray-300 rounded"
          />

        <p className="text-red-400 italic text-sm">{formik.errors.last_name}</p>

         <button type="submit" className="bg-purple-700 w-60 ml-10 ml-2 text-white rounded p-1 mt-2">Sign Up</button>

          </form>
          </div>
          
)}
export default Comment