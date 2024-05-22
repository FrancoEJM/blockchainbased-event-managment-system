/* eslint-disable react/prop-types */
import { useState } from "react";

function StepOne({ modalidad, idioma, privacidad, onUpdate }) {
  const [invitados, setInvitados] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [modalidadAct, setModalidad] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;
    onUpdate((prevData) => ({
      ...prevData,
      [name]: value,
      lista: invitados,
    }));
  };

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  //Manejar invitados
  const handleInputKeyPress = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      const trimmedValue = inputValue.trim();
      if (trimmedValue !== "") {
        const newInvitados = [...invitados, trimmedValue];
        setInvitados(newInvitados);
        setInputValue("");
        onUpdate((prevData) => ({
          ...prevData,
          lista: newInvitados,
        }));
      }
    }
  };
  const handleRemoveInvitado = (index) => {
    const nuevosInvitados = [...invitados];
    nuevosInvitados.splice(index, 1);
    setInvitados(nuevosInvitados);
    onUpdate((prevData) => ({
      ...prevData,
      lista: nuevosInvitados,
    }));
  };

  const sortOptionsById = (options) => {
    return options.sort((a, b) => a.id_idioma - b.id_idioma);
  };

  return (
    <form>
      <div className="grid grid-cols-12 gap-4">
        <div className="col-span-6">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="name"
          >
            Nombre
          </label>
          <input
            className="appearance-none block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="name"
            name="name"
            type="text"
            placeholder="Ingrese el nombre del evento"
            onChange={handleChange}
          />
        </div>
        <div className="col-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="fecha"
          >
            Fecha:
          </label>
          <input
            className="appearance-none block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="fecha"
            name="fecha"
            type="date"
            pattern="\d{1,2}/\d{1,2}/\d{4}"
            placeholder="dd/mm/yyyy"
            onChange={handleChange}
          />
        </div>
        <div className="col-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="desde"
          >
            Desde:
          </label>
          <input
            className="appearance-none block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="desde"
            name="desde"
            type="time"
            step="60"
            placeholder="HH:mm"
            onChange={handleChange}
          />
        </div>
        <div className="col-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="hasta"
          >
            Hasta:
          </label>
          <input
            className="appearance-none block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="hasta"
            name="hasta"
            type="time"
            step="60"
            placeholder="HH:mm"
            onChange={handleChange}
          />
        </div>
        <div className="col-span-6 row-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="descripcion"
          >
            Descripcion
          </label>
          <textarea
            className="appearance-none block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3 h-36 resize-none"
            id="descripcion"
            name="descripcion"
            type="text"
            placeholder="Ingrese una descripción para su evento"
            onChange={handleChange}
          />
        </div>
        <div className="col-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="privacidad"
          >
            Privacidad
          </label>
          <select
            className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="privacidad"
            name="privacidad"
            type="text"
            onChange={handleChange}
          >
            <option value="">Seleccione una opción</option>
            {privacidad.map((option) => (
              <option key={option.id_privacidad} value={option.id_privacidad}>
                {option.descripcion}
              </option>
            ))}
          </select>
        </div>
        <div className="col-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="idioma"
          >
            Idioma
          </label>
          <select
            className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="idioma"
            name="idioma"
            type="text"
            onChange={handleChange}
          >
            <option value="">Seleccione una opción</option>
            {sortOptionsById(idioma).map((option) => (
              <option key={option.id_idioma} value={option.id_idioma}>
                {option.descripcion}
              </option>
            ))}
          </select>
        </div>
        <div className="col-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="modalidad"
          >
            Modalidad
          </label>
          <select
            className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="modalidad"
            name="modalidad"
            type="text"
            placeholder="Ingrese una descripción para su evento"
            onChange={(e) => {
              handleChange(e);
              setModalidad(e.target.value);
            }}
          >
            <option value="">Seleccione una opción</option>
            {modalidad.map((option) => (
              <option key={option.id_modalidad} value={option.id_modalidad}>
                {option.descripcion}
              </option>
            ))}
          </select>
        </div>
        <div className="col-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="lista"
          >
            Lista de invitados
          </label>
          <input
            className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="lista"
            type="text"
            placeholder="Ingrese un invitado y presione Enter"
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleInputKeyPress}
          />
        </div>
        <div className="col-span-2">
          <div className="overflow-y-auto h-16 mb-2">
            {invitados.map((invitado, index) => (
              <div
                key={index}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  borderBottom: "1px solid #ccc",
                  padding: "5px",
                }}
              >
                <span>{invitado}</span>
                <button
                  onClick={() => handleRemoveInvitado(index)}
                  style={{
                    background: "none",
                    border: "none",
                    cursor: "pointer",
                  }}
                >
                  X
                </button>
              </div>
            ))}
          </div>
        </div>
        <div className="col-span-2">
          {modalidadAct === "2" && (
            <div>
              <label
                className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
                htmlFor="url"
              >
                URL
              </label>
              <input
                className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
                id="url"
                name="url"
                type="text"
                placeholder="Ingrese la URL del evento"
                onChange={handleChange}
              />
            </div>
          )}
        </div>
      </div>
    </form>
  );
}

export default StepOne;
