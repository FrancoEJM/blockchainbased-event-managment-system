import { useState } from "react";

function StepOne() {
  const [invitados, setInvitados] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [modalidad, setModalidad] = useState("");

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleInputKeyPress = (event) => {
    if (event.key === "Enter" && inputValue.trim() !== "") {
      event.preventDefault(); // Evitar que el formulario se envíe al presionar Enter
      setInvitados([...invitados, inputValue]);
      setInputValue("");
    }
  };

  const handleRemoveInvitado = (index) => {
    const nuevosInvitados = [...invitados];
    nuevosInvitados.splice(index, 1);
    setInvitados(nuevosInvitados);
  };

  const handleSubmit = (event) => {
    event.preventDefault(); // Evitar que el formulario se envíe al presionar Enter
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="grid grid-cols-12 gap-4">
        <div className="col-span-6">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="grid-first-name"
          >
            Nombre
          </label>
          <input
            className="appearance-none block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="grid-first-name"
            type="text"
            placeholder="Ingrese el nombre del evento"
          />
        </div>
        <div className="col-span-3">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="grid-first-name"
          >
            Desde:
          </label>
          <input
            className="appearance-none block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="grid-first-name"
            type="time"
            step="60"
            placeholder="HH:mm"
          />
        </div>
        <div className="col-span-3">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="grid-first-name"
          >
            Hasta:
          </label>
          <input
            className="appearance-none block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="grid-first-name"
            type="time"
            step="60"
            placeholder="HH:mm"
          />
        </div>
        <div className="col-span-6 row-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="grid-first-name"
          >
            Descripcion
          </label>
          <textarea
            className="appearance-none block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3 h-36"
            id="grid-first-name"
            type="text"
            placeholder="Ingrese una descripción para su evento"
          />
        </div>
        <div className="col-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="grid-first-name"
          >
            Privacidad
          </label>
          <select
            className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="grid-first-name"
            type="text"
            placeholder="Ingrese una descripción para su evento"
          >
            <option value="1">1</option>
            <option value="2">2</option>
          </select>
        </div>
        <div className="col-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="grid-first-name"
          >
            Idioma
          </label>
          <select
            className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="grid-first-name"
            type="text"
            placeholder="Ingrese una descripción para su evento"
          >
            <option value="1">1</option>
            <option value="2">2</option>
          </select>
        </div>
        <div className="col-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="grid-first-name"
          >
            Modalidad
          </label>
          <select
            className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="grid-first-name"
            type="text"
            placeholder="Ingrese una descripción para su evento"
            onChange={(e) => setModalidad(e.target.value)}
          >
            <option value="1">1</option>
            <option value="2">2</option>
          </select>
        </div>
        <div className="col-span-2">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="grid-first-name"
          >
            Lista de invitados
          </label>
          <input
            className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
            id="grid-first-name"
            type="text"
            placeholder="Ingrese un invitado y presione Enter"
            value={inputValue}
            onChange={handleInputChange}
            onKeyPress={handleInputKeyPress}
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
          {modalidad === "2" && (
            <div>
              <label
                className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
                htmlFor="grid-first-name"
              >
                Url
              </label>
              <input
                className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
                id="grid-first-name"
                type="text"
                placeholder="Ingrese la URL del evento"
              />
            </div>
          )}
        </div>
      </div>
    </form>
  );
}
export default StepOne;
