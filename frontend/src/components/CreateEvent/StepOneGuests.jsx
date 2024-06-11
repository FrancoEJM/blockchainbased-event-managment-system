import React, { useState } from "react";
import * as Papa from "papaparse";

function StepOneGuests({ onUpdate }) {
  const [data, setData] = useState([]);
  const [errorText, setErrorText] = useState("");
  const [originalGuests, setOriginalGuest] = useState([]);

  const validEmailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const validDateRegex = /^\d{2}\/\d{2}\/\d{4}$/;
  const validGenders = ["M", "F", "O", "D"];

  const handleFileUpload = (e) => {
    const file = e.target.files[0];

    Papa.parse(file, {
      complete: (result) => {
        const parsedData = result.data.slice(1);

        // Validaciones y ajustes de datos
        const guests = parsedData.map((row) => {
          let nombre = row[0];
          let correo_electronico = row[1] ? row[1].trim() : "";
          let genero =
            row[2] && ["M", "F", "O", "D"].includes(row[2].trim().toUpperCase())
              ? row[2].trim().toUpperCase()
              : "D";
          let fecha_nacimiento = isValidDate(row[3])
            ? formatDate(row[3])
            : "01/01/1900"; // Fallback date

          return { nombre, correo_electronico, genero, fecha_nacimiento };
        });
        setOriginalGuest(guests);

        // Filtrar solo los invitados con correo electrónico válido
        const filteredGuests = guests.filter((guest) => {
          const { correo_electronico, fecha_nacimiento, genero } = guest;

          // Verificar si el correo electrónico es válido
          const isEmailValid = validEmailRegex.test(correo_electronico);

          // Verificar si la fecha de nacimiento es válida
          const isDateValid = validDateRegex.test(fecha_nacimiento);

          // Verificar si el género es válido
          let isGenderValid = validGenders.includes(genero);
          if (!isGenderValid) {
            guest.genero = "D";
            isGenderValid = true;
          }

          return isEmailValid && isDateValid && isGenderValid;
        });

        onUpdate(filteredGuests);
        setData(filteredGuests);
      },
      error: (err) => {
        setErrorText(err.message);
      },
    });
  };

  // Función para validar el formato de fecha dd/mm/yyyy
  const isValidDate = (dateString) => {
    const regexDate = /^\d{1,2}\/\d{1,2}\/\d{4}$/;
    return regexDate.test(dateString);
  };

  // Función para formatear la fecha a dd/mm/yyyy
  const formatDate = (dateString) => {
    const parts = dateString.split("/");
    return `${parts[0].padStart(2, "0")}/${parts[1].padStart(2, "0")}/${
      parts[2]
    }`;
  };

  return (
    <>
      <div className="col-span-2">
        <label
          className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
          htmlFor="lista"
        >
          Lista de invitados
        </label>
        <label className="flex items-center px-4 py-2 bg-white rounded-md border cursor-pointer hover:shadow-lg">
          <svg
            className="w-8 h-8 mr-2"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M11 0h5a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h5V0z"
            />
            <path
              fillRule="evenodd"
              d="M7 0v6a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V0H7z"
              className="text-white"
            />
          </svg>
          <span className="text-md leading-normal">Selecciona un archivo</span>
          <input
            type="file"
            className="hidden"
            onChange={handleFileUpload}
            accept=".csv, .xls, .xlsx"
          />
        </label>
      </div>
      {data.length > 0 && (
        <div className="col-span-2">
          <div className="w-full bg-green-100 text-grey-darker border border-red rounded py-3 px-4 mt-6 ">
            Se han añadido correctamente {data.length} invitados
          </div>
        </div>
      )}
      {data.length < originalGuests.length && (
        <div className="col-span-2">
          <div className="w-full bg-red-100 text-grey-darker border border-red rounded py-3 px-4 mt-6 ">
            No se han podido ingresar {originalGuests.length - data.length}{" "}
            invitados, por favor revise su CSV.
          </div>
        </div>
      )}
    </>
  );
}

export default StepOneGuests;
