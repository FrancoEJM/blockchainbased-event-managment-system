import { useState } from "react";
import { useNavigate } from "react-router-dom";

import axios from "axios";
import DatePicker from "react-datepicker";
import es from "date-fns/locale/es";

import "react-datepicker/dist/react-datepicker.css";
import "./styles.css";

function RegisterForm() {
  const [values, setValues] = useState({
    name: "",
    lastname: "",
    email: "",
    phone_number: "",
    password: "",
    password_c: "",
  });

  const [birthdate, setBirthdate] = useState(null);

  const handleDateChange = (date) => {
    setBirthdate(date);
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setValues({
      ...values,
      [name]: value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const mappedValues = mapFields(values);
    axios({
      url: import.meta.env.VITE_BACKEND_URL + "/api/users",
      method: "POST",
      data: mappedValues,
    })
      .then((res) => {
        if (res.status == 200) {
          handleRedirect();
        }
      })
      .catch((err) => console.log(err));
  };

  const navigate = useNavigate();
  const handleRedirect = () => {
    navigate("/");
  };

  const mapFields = (values) => {
    const formattedBirthdate = birthdate
      ? `${birthdate.getFullYear()}-${(birthdate.getMonth() + 1)
          .toString()
          .padStart(2, "0")}-${birthdate.getDate().toString().padStart(2, "0")}`
      : "";

    return {
      correo_electronico: values.email,
      hash_contrasena: values.password,
      nombre: values.name,
      apellido: values.lastname,
      telefono: values.phone_number,
      fecha_nacimiento: formattedBirthdate,
    };
  };

  return (
    <form onSubmit={handleSubmit} className="mt-8">
      <div className="grid grid-cols-2 gap-6">
        <div className="col-span-2 sm:col-span-1">
          <label htmlFor="name" className="font-medium text-gray-700 mb-2">
            Nombre
          </label>
          <input
            type="text"
            name="name"
            id="name"
            placeholder="Ingresa tu nombre"
            onChange={handleInputChange}
            className="w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none focus:border-violet-400"
          />
        </div>
        <div className="col-span-2 sm:col-span-1">
          <label htmlFor="lastname" className="font-medium text-gray-700 mb-2">
            Apellido
          </label>
          <input
            type="text"
            name="lastname"
            id="lastname"
            placeholder="Ingresa tu apellido"
            onChange={handleInputChange}
            className="w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none focus:border-violet-400"
          />
        </div>
      </div>

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

      <div className="grid grid-cols-2 gap-6">
        <div className="col-span-2 sm:col-span-1">
          <div className="pt-3">
            <label className="font-medium text-gray-700 mb-2">
              Fecha de nacimiento
            </label>
            <DatePicker
              selected={birthdate}
              onChange={handleDateChange}
              name="birthdate"
              id="birthdate"
              dateFormat="dd/MM/yyyy"
              placeholderText="dd/mm/yyyy"
              locale={es}
              style={{ width: "100% !important" }}
              className="w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none focus:border-violet-400"
            />
          </div>
        </div>
        <div className="col-span-2 sm:col-span-1">
          <div className="pt-3">
            <label className="font-medium text-gray-700 mb-2">
              Número telefónico
            </label>
            <div className="flex items-center w-full mt-1 mb-3 border border-gray-400 rounded-lg focus-within:border-violet-400">
              <span className="px-4 py-3 bg-gray-100 border-r border-gray-400 rounded-l-lg">
                +56
              </span>
              <input
                type="text"
                name="phone_number"
                id="phone_number"
                className="w-full py-3 px-4 border-0 rounded-r-lg focus:outline-none focus:ring-0"
                placeholder="Ingrese su número"
                onChange={handleInputChange}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="pt-3">
        <label className="font-medium text-gray-700 mb-2">Contraseña</label>
        <input
          type="password"
          name="password"
          id="password"
          placeholder="Ingresa tu contraseña"
          onChange={handleInputChange}
          className="w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none focus:border-violet-400"
        />
      </div>

      <div className="pt-3">
        <label className="font-medium text-gray-700 mb-2">
          Confirma tu contraseña
        </label>
        <input
          type="password"
          name="password_c"
          id="password_c"
          placeholder="Ingresa tu contraseña nuevamente"
          onChange={handleInputChange}
          className="w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none focus:border-violet-400"
        />
      </div>

      <div className="mt-8 flex justify-center h-12">
        <button
          type="submit"
          className="active:scale-[.99] active:duration-75 hover:scale-[1.01] transition-all bg-violet-400 text-white rounded-3xl w-2/3 text-lg font-bold"
        >
          Registrarse
        </button>
      </div>

      <div className="mt-8 flex justify-center items-center">
        <p className="font-medium text-base">¿Ya tienes una cuenta?</p>
        <button
          type="button"
          onClick={handleRedirect}
          className="text-violet-400 text-base font-medium ml-2 hover:scale-[1.01] hover:text-violet-900"
        >
          Iniciar Sesión
        </button>
      </div>
    </form>
  );
}
export default RegisterForm;
