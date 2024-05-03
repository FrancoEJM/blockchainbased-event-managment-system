function StepOne() {
  return (
    <form>
      <div className="grid grid-cols-12 gap-4">
        <div className="col-span-6 row-span-1">
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
        <div className="col-span-3 row-span-1">
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
        <div className="col-span-3 row-span-1">
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
        <div className="col-span-6">
          <label
            className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
            htmlFor="grid-first-name"
          >
            Descripcion
          </label>
          <textarea
            className="appearance-none block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3 row-span-5"
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
            className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3 row-span-5"
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
            className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3 row-span-5"
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
            className=" block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3 row-span-5"
            id="grid-first-name"
            type="text"
            placeholder="Ingrese una descripción para su evento"
          >
            <option value="1">1</option>
            <option value="2">2</option>
          </select>
        </div>
      </div>
    </form>
  );
}
export default StepOne;
