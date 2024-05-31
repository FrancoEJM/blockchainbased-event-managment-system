import { useState, useEffect } from "react";
import axios from "axios";
import DatePicker from "react-datepicker";
import es from "date-fns/locale/es";
import "react-datepicker/dist/react-datepicker.css";
import "./styles.css";
import { useNavigate } from "react-router-dom";

function DataCollectionForm({ event_id }) {
  const navigate = useNavigate();
  const [values, setValues] = useState({
    event_id: event_id,
    fullname: "",
    gender: "",
  });
  const [birthdate, setBirthdate] = useState(null);
  const [gender, setGender] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const fetchGenders = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_BACKEND_URL}/api/gender`
        );
        setGender(response.data);
      } catch (error) {
        console.error("Error obteniendo los géneros", error);
      } finally {
        setLoading(false);
      }
    };
    fetchGenders();
  }, []);

  useEffect(() => {
    if (birthdate) {
      try {
        const formatted_date = birthdate.toISOString().split("T")[0];
        setValues((prevValues) => ({
          ...prevValues,
          birthdate: formatted_date,
        }));
        console.log(values);
      } catch (error) {
        console.error("Error al enviar el formulario:", error.message);
      }
    }
  }, [birthdate]);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setValues({
      ...values,
      [name]: value,
    });
    console.log(values);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/user/unregistered_details`,
        values
      );
      if (response.status === 200) {
        setShowModal(true);
        setTimeout(() => {
          setShowModal(false);
          navigate("/");
        }, 5000);
      } else {
        console.error("Error al enviar el formulario:", response.statusText);
      }
    } catch (error) {
      console.error("Error al enviar el formulario:", error.message);
    }
  };

  const currentYear = new Date().getFullYear();
  const years = [];
  for (let i = currentYear; i >= currentYear - 100; i--) {
    years.push(i);
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center w-full h-screen">
        <div className="text-xl font-semibold">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="flex justify-center items-center w-full h-screen">
      <div className="max-w-screen-sm w-full mx-4">
        <div className="bg-white px-6 py-8 border-2 border-gray-200 shadow-lg rounded-lg">
          <h1 className="text-3xl font-semibold mb-4">
            ¡Bienvenido al evento!
          </h1>
          <h3 className="text-base font-normal mb-6">
            Por favor, llena el siguiente formulario para poder mejorar tu
            experiencia en futuros eventos
          </h3>
          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label
                htmlFor="fullname"
                className="font-medium text-gray-700 mb-2 block"
              >
                Nombre completo
              </label>
              <input
                type="text"
                name="fullname"
                id="fullname"
                placeholder="Ingresa tu nombre completo"
                onChange={handleInputChange}
                className="w-full py-3 px-4 border border-gray-400 rounded-lg focus:outline-none focus:border-violet-400"
              />
            </div>

            <div className="flex mb-6">
              <div className="w-1/2 mr-2">
                <label
                  htmlFor="birthdate"
                  className="font-medium text-gray-700 mb-2 block"
                >
                  Fecha de nacimiento
                </label>
                <DatePicker
                  selected={birthdate}
                  onChange={(date) => setBirthdate(date)}
                  dateFormat="dd/MM/yyyy"
                  placeholderText="dd/mm/yyyy"
                  locale={es}
                  showYearDropdown
                  scrollableYearDropdown
                  maxDate={new Date()}
                  yearDropdownItemNumber={100}
                  className="w-full py-3 px-4 border border-gray-400 rounded-lg focus:outline-none focus:border-violet-400"
                />
              </div>
              <div className="w-1/2 ml-2">
                <label
                  htmlFor="gender"
                  className="font-medium text-gray-700 mb-2 block"
                >
                  Género
                </label>
                <div className="relative">
                  <select
                    name="gender"
                    id="gender"
                    onChange={handleInputChange}
                    value={values.gender}
                    className="appearance-none w-full py-3 px-4 border border-gray-400 rounded-lg focus:outline-none focus:border-violet-400"
                  >
                    <option value="" disabled hidden>
                      Seleccione una opción
                    </option>
                    {gender.map((option) => (
                      <option key={option.id_genero} value={option.id_genero}>
                        {option.descripcion}
                      </option>
                    ))}
                  </select>
                  <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                    <svg
                      className="fill-current h-4 w-4"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 20 20"
                    >
                      <path d="M10 12l-4-4h8z" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
            <div className="flex justify-center">
              <button
                type="submit"
                className="bg-violet-400 text-white rounded-lg py-3 px-8 text-lg font-bold hover:bg-violet-500 transition-colors"
              >
                Enviar
              </button>
            </div>
          </form>
        </div>
      </div>
      {showModal && (
        <div className="fixed top-0 left-0 w-full h-full flex justify-center items-center bg-gray-900 bg-opacity-50">
          <div className="bg-white p-8 rounded-lg flex flex-col items-center mx-4">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-16 w-16 text-green-500 mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M5 13l4 4L19 7"
              />
            </svg>
            <h2 className="text-xl font-bold text-gray-800 mb-2">
              ¡Muchas gracias!
            </h2>
            <p className="text-lg text-gray-800 text-center">
              Tus datos han sido enviados correctamente.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default DataCollectionForm;
