import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import DatePicker from "react-datepicker";
import es from "date-fns/locale/es";
import "react-datepicker/dist/react-datepicker.css";
import "./styles.css";

import { useForm, Controller } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";

const schema = yup.object().shape({
  name: yup.string().required("El nombre es requerido"),
  lastname: yup.string().required("El apellido es requerido"),
  email: yup
    .string()
    .email("Correo electrónico no válido")
    .required("El correo electrónico es requerido"),
  phone_number: yup
    .string()
    .length(8, "El número telefónico debe tener 8 caracteres")
    .required("El número telefónico es requerido"),
  password: yup
    .string()
    .min(6, "La contraseña debe tener al menos 6 caracteres")
    .required("La contraseña es requerida"),
  password_c: yup
    .string()
    .oneOf([yup.ref("password"), null], "Las contraseñas no coinciden")
    .required("La confirmación de la contraseña es requerida"),
  birthdate: yup.date().required("La fecha de nacimiento es requerida"),
});

function RegisterForm() {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    setError,
  } = useForm({
    resolver: yupResolver(schema),
  });

  const navigate = useNavigate();

  const onSubmit = (data) => {
    const mappedValues = mapFields(data);
    axios({
      url: import.meta.env.VITE_BACKEND_URL + "/api/users",
      method: "POST",
      data: mappedValues,
    })
      .then((res) => {
        if (res.status === 200) {
          handleRedirect();
        }
      })
      .catch((err) => {
        if (err.response && err.response.status === 400) {
          setError("email", {
            type: "manual",
            message: "El correo electrónico ya está en uso",
          });
        } else {
          setError("email", {
            type: "manual",
            message: "Error en la solicitud",
          });
        }
      });
  };

  const handleRedirect = () => {
    navigate("/");
  };

  const mapFields = (values) => {
    const formattedBirthdate = values.birthdate
      ? `${values.birthdate.getFullYear()}-${(values.birthdate.getMonth() + 1)
          .toString()
          .padStart(2, "0")}-${values.birthdate
          .getDate()
          .toString()
          .padStart(2, "0")}`
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
    <form onSubmit={handleSubmit(onSubmit)} className="mt-8">
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
            {...register("name")}
            className={`w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none ${
              errors.name ? "border-red-500" : "focus:border-violet-400"
            }`}
          />
          {errors.name && (
            <p className="text-red-500 text-sm">{errors.name.message}</p>
          )}
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
            {...register("lastname")}
            className={`w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none ${
              errors.lastname ? "border-red-500" : "focus:border-violet-400"
            }`}
          />
          {errors.lastname && (
            <p className="text-red-500 text-sm">{errors.lastname.message}</p>
          )}
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
          {...register("email")}
          className={`w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none ${
            errors.email ? "border-red-500" : "focus:border-violet-400"
          }`}
          placeholder="Ingresa tu correo electrónico"
        />
        {errors.email && (
          <p className="text-red-500 text-sm">{errors.email.message}</p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="col-span-2 sm:col-span-1">
          <div className="pt-3">
            <label className="font-medium text-gray-700 mb-2">
              Fecha de nacimiento
            </label>
            <Controller
              name="birthdate"
              control={control}
              render={({ field }) => (
                <DatePicker
                  {...field}
                  selected={field.value}
                  onChange={(date) => field.onChange(date)}
                  dateFormat="dd/MM/yyyy"
                  placeholderText="dd/mm/yyyy"
                  locale={es}
                  className={`w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none ${
                    errors.birthdate
                      ? "border-red-500"
                      : "focus:border-violet-400"
                  }`}
                />
              )}
            />
            {errors.birthdate && (
              <p className="text-red-500 text-sm">{errors.birthdate.message}</p>
            )}
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
                {...register("phone_number")}
                className={`w-full py-3 px-4 border-0 rounded-r-lg focus:outline-none focus:ring-0 ${
                  errors.phone_number
                    ? "border-red-500"
                    : "focus:border-violet-400"
                }`}
                placeholder="Ingrese su número"
              />
            </div>
            {errors.phone_number && (
              <p className="text-red-500 text-sm">
                {errors.phone_number.message}
              </p>
            )}
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
          {...register("password")}
          className={`w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none ${
            errors.password ? "border-red-500" : "focus:border-violet-400"
          }`}
        />
        {errors.password && (
          <p className="text-red-500 text-sm">{errors.password.message}</p>
        )}
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
          {...register("password_c")}
          className={`w-full py-3 px-4 mt-1 mb-3 border border-gray-400 rounded-lg focus:outline-none ${
            errors.password_c ? "border-red-500" : "focus:border-violet-400"
          }`}
        />
        {errors.password_c && (
          <p className="text-red-500 text-sm">{errors.password_c.message}</p>
        )}
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
