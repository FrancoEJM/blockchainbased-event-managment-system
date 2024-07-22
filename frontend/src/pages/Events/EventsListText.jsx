import { ButtonGroup, Button } from "flowbite-react";
import { HiOutlinePlus } from "react-icons/hi";
import NavbarTest from "../../components/NavbarTest";
function EventsListText() {
  return (
    <>
      <NavbarTest />
      <div className="mx-auto bg-gray-100 h-screen flex px-8">
        <div className="flex flex-col w-full items-center justify-center space-y-4">
          {/* Evento 1 */}
          <div className="flex flex-col w-full bg-white rounded-lg shadow-lg sm:w-3/4 md:w-1/2 lg:w-3/5">
            <div
              className="w-full h-64 bg-top bg-cover rounded-t-lg"
              style={{
                backgroundImage:
                  'url("https://www.si.com/.image/t_share/MTY4MTkyMjczODM4OTc0ODQ5/cfp-trophy-deitschjpg.jpg")',
              }}
            ></div>
            <div className="flex flex-col w-full md:flex-row">
              <div className="flex flex-row justify-around p-4 font-bold leading-none text-violet-700 uppercase bg-violet-300 md:flex-col md:items-center md:justify-center md:w-1/4 md:rounded-bl-lg">
                <div className="md:text-3xl">Jan</div>
                <div className="md:text-6xl">13</div>
                <div className="md:text-xl">7 PM</div>
              </div>
              <div className="p-4 font-normal text-gray-800 md:w-3/4">
                <h1 className="mb-4 text-4xl font-bold leading-none tracking-tight text-gray-800">
                  2020 National Championship
                </h1>
                <p className="leading-normal">
                  The College Football Playoff (CFP) determines the national
                  champion of the top division of college football. The format
                  fits within the academic calendar and preserves the sport’s
                  unique and compelling regular season.
                </p>
                <div className="flex flex-row items-center mt-4 text-gray-700">
                  <div className="w-1/2 font-semibold uppercase">
                    Mercedes-Benz Superdome
                  </div>
                  <div className="w-1/2 flex justify-end">
                    <ButtonGroup>
                      <Button className="ring-cyan-700 border border-gray-200 bg-white text-gray-900 focus:text-cyan-700 focus:ring-4 enabled:hover:bg-gray-100 enabled:hover:text-violet-700 dark:border-gray-600 dark:bg-transparent dark:text-gray-400 dark:enabled:hover:bg-gray-700 dark:enabled:hover:text-white">
                        <span className="hidden sm:inline">
                          Quiero saber más
                        </span>
                        <span className="sm:hidden mt-1">
                          <HiOutlinePlus />
                        </span>
                      </Button>
                      <Button className="ring-cyan-700 border border-gray-200 bg-white text-gray-900 focus:text-cyan-700 focus:ring-4 enabled:hover:bg-gray-100 enabled:hover:text-violet-700 dark:border-gray-600 dark:bg-transparent dark:text-gray-400 dark:enabled:hover:bg-gray-700 dark:enabled:hover:text-white">
                        Inscribirme
                      </Button>
                    </ButtonGroup>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Evento 2 */}
          <div className="flex flex-col w-full bg-white rounded-lg shadow-lg sm:w-3/4 md:w-1/2 lg:w-3/5">
            <div
              className="w-full h-64 bg-top bg-cover rounded-t-lg"
              style={{
                backgroundImage: 'url("https://example.com/another-image.jpg")',
              }}
            ></div>
            <div className="flex flex-col w-full md:flex-row">
              <div className="flex flex-row justify-around p-4 font-bold leading-none text-violet-700 uppercase bg-violet-200 md:flex-col md:items-center md:justify-center md:w-1/4 rounded-b-lg md:rounded-b-none md:rounded-l-lg">
                <div className="md:text-3xl">Feb</div>
                <div className="md:text-6xl">14</div>
                <div className="md:text-xl">8 PM</div>
              </div>
              <div className="p-4 font-normal text-gray-800 md:w-3/4">
                <h1 className="mb-4 text-4xl font-bold leading-none tracking-tight text-gray-800">
                  Another Event
                </h1>
                <p className="leading-normal">
                  Description of another event. The format fits within the
                  academic calendar and preserves the sport’s unique and
                  compelling regular season.
                </p>
                <div className="flex flex-row items-center mt-4 text-gray-700">
                  <div className="w-1/2">Another Venue</div>
                  <div className="w-1/2 flex justify-end">
                    <img
                      src="https://example.com/another-logo.png"
                      alt=""
                      className="w-8"
                    ></img>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default EventsListText;
