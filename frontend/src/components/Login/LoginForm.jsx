import { useState } from "react";
import { useNavigate } from "react-router-dom";

import axios from "axios";

function LoginForm() {
  const [values, setValues] = useState({
    email: "",
    password: "",
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setValues({
      ...values,
      [name]: value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("username", values.email);
    formData.append("password", values.password);

    axios({
      url: import.meta.env.VITE_BACKEND_URL + "/api/token",
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      data: formData,
    })
      .then((res) => {
        if (res.status === 200) {
          let token = res.data.access_token;
          localStorage.setItem("token", token);
          setId(localStorage.getItem("token"));
        }
      })
      .catch((err) => console.log(err));
  };

  const navigate = useNavigate();
  const handleRedirect = () => {
    navigate("/register");
  };

  const loginRedirect = () => {
    navigate("/events");
  };

  const setId = async (token) => {
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_BACKEND_URL}/api/users/me`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      const id_usuario = response.data.id_usuario;
      localStorage.setItem("id_usuario", id_usuario);
      loginRedirect();
    } catch (error) {
      console.error(error);
      throw new Error("No se pudo obtener el ID de usuario");
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="pt-3">
          <label className="font-medium text-gray-700 mb-2">
            Correo electrónico
          </label>
          <input
            type="email"
            name="email"
            id="email"
            onChange={handleInputChange}
            className="w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none focus:border-violet-400"
            placeholder="Ingresa tu correo electrónico"
          />
        </div>
        <div className="pt-3">
          <label className="font-medium text-gray-700 mb-2">Contraseña</label>
          <input
            type="password"
            name="password"
            id="password"
            onChange={handleInputChange}
            className="w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none focus:border-violet-400"
            placeholder="Ingresa tu contraseña"
          />
        </div>
        <div className="mt-8 flex justify-center h-12">
          <button
            type="submit"
            className=" active:scale-[.99] active:duration-75 hover:scale-[1.01] transition-all bg-violet-400 text-white rounded-3xl w-2/3 text-lg font-bold"
          >
            Iniciar Sesión
          </button>
        </div>
        <div className="mt-8 flex justify-center items-center">
          <p className="font-medium text-base">¿Aún no tienes cuenta?</p>
          <button
            type="button"
            onClick={handleRedirect}
            className="text-violet-400 text-base font-medium ml-2 hover:scale-[1.01] hover:text-violet-900"
          >
            Registrate aquí
          </button>
        </div>
      </form>
    </>
  );
}
export default LoginForm;
