import { useParams } from "react-router-dom";
import NavBar from "../../components/Navbar";

function EventPage() {
  const { id } = useParams();
  console.log(id);

  return (
    <div>
      <NavBar />

      <div className="container mx-auto my-5 p-5 h-full">
        <div className="md:flex no-wrap md:-mx-2 h-full">
          {/* <!-- Left Side --> */}
          <div className="w-full md:w-2/3 md:mx-2 h-full">
            {/* <!-- Event --> */}
            <div className="bg-white p-3 border-t-4 border-violet-300 h-full ">
              <h1 className="text-gray-900 font-bold text-xl leading-8 my-1">
                Aprende blockchain
              </h1>
              <h3 className="text-gray-600 font-lg text-semibold leading-6">
                Tecnología
              </h3>
              <p className="overflow-y-auto text-sm text-gray-500 hover:text-gray-600 leading-6 pr-16 max-h-fit">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce
                vel sem in erat bibendum laoreet. Suspendisse massa dui,
                elementum sit amet venenatis eget, facilisis id massa. Sed
                luctus felis arcu. Nam justo diam, tempor sit amet interdum ac,
                convallis quis metus. Nunc molestie leo ut quam tempus suscipit.
                Pellentesque vel est dolor. Sed in tincidunt nibh. Nam ultrices
                nisi ac enim auctor pellentesque. Maecenas venenatis mattis
                congue. Phasellus efficitur vel lorem a ultrices. Morbi euismod
                porta ex, sed efficitur diam auctor at. Nulla in euismod metus.
                Pellentesque varius risus sed rutrum lobortis. Maecenas
                elementum ullamcorper sapien non ullamcorper. Lorem ipsum dolor
                sit amet, consectetur adipiscing elit. Quisque sit amet aliquet
                metus. Mauris cursus eros et nisl condimentum, id hendrerit
                ipsum scelerisque. Phasellus pretium convallis iaculis. Cras
                vulputate lacus nec magna interdum, at vestibulum tellus
                faucibus. Integer malesuada egestas facilisis. Maecenas sit amet
                sollicitudin mi, ut pulvinar libero. Mauris pellentesque ante ac
                lectus euismod vestibulum sed id augue. Lorem ipsum dolor sit
                amet, consectetur adipiscing elit. Fusce vel sem in erat
                bibendum laoreet. Suspendisse massa dui, elementum sit amet
                venenatis eget, facilisis id massa. Sed luctus felis arcu. Nam
                justo diam, tempor sit amet interdum ac, convallis quis metus.
                Nunc molestie leo ut quam tempus suscipit. Pellentesque vel est
                dolor. Sed in tincidunt nibh. Nam ultrices nisi ac enim auctor
                pellentesque. Maecenas venenatis mattis congue. Phasellus
                efficitur vel lorem a ultrices. Morbi euismod porta ex, sed
                efficitur diam auctor at. Nulla in euismod metus. Pellentesque
                varius risus sed rutrum lobortis. Maecenas elementum ullamcorper
                sapien non ullamcorper. Lorem ipsum dolor sit amet, consectetur
                adipiscing elit. Quisque sit amet aliquet metus. Mauris cursus
                eros et nisl condimentum, id hendrerit ipsum scelerisque.
                Phasellus pretium convallis iaculis. Cras vulputate lacus nec
                magna interdum, at vestibulum tellus faucibus. Integer malesuada
                egestas facilisis. Maecenas sit amet sollicitudin mi, ut
                pulvinar libero. Mauris pellentesque ante ac lectus euismod
                vestibulum sed id augue. Lorem ipsum dolor sit amet, consectetur
                adipiscing elit. Fusce vel sem in erat bibendum laoreet. varius
                risus sed rutrum lobortis. Maecenas elementum ullamcorper sapien
                non ullamcorper. Lorem ipsum dolor sit amet, consectetur
                adipiscing elit. Quisque sit amet aliquet metus. Mauris cursus
                eros et nisl condimentum, id hendrerit ipsum scelerisque.
                Phasellus pretium convallis iaculis. Cras vulputate lacus nec
                magna interdum, at vestibulum tellus faucibus. Integer malesuada
                egestas facilisis. Maecenas sit amet sollicitudin mi, ut
                pulvinar libero. Mauris pellentesque ante ac lectus euismod
                vestibulum sed id augue. Lorem ipsum dolor sit amet, consectetur
                adipiscing elit. Fusce vel sem in erat bibendum laoreet.
              </p>
              <ul className="bg-gray-100 text-gray-600 hover:text-gray-700 hover:shadow py-2 px-3 mt-3 divide-y rounded shadow-sm">
                <li className="flex items-center py-3">
                  <span className="font-semibold">Fecha</span>
                  <span className="ml-auto">
                    <span className="mx-3 font-semibold">11/04/2024</span>
                    <span className="bg-violet-400 py-1 px-2 mx-3 rounded text-white text-sm">
                      19:00
                    </span>
                    <span className="bg-violet-400 py-1 px-2 mx-3 rounded text-white text-sm">
                      20:00
                    </span>
                  </span>
                </li>
                <li className="flex items-center py-3">
                  <span className="font-semibold">Modalidad</span>
                  <span className="ml-auto font-semibold">Presencial</span>
                </li>
                <li className="flex items-center justify-between py-2">
                  <span className="font-semibold">Evento público</span>
                  <span className="font-semibold ">
                    <button className=" bg-violet-500 hover:bg-violet-400 text-white font-bold py-2 px-4 border-b-4 border-violet-800 hover:border-violet-500 shadow-md">
                      + Inscribirse
                    </button>
                  </span>
                </li>
              </ul>
            </div>
            {/* <!-- End of event card --> */}
            <div className="my-4"></div>
          </div>
          {/* <!-- Right Side --> */}
          <div className="w-full md:w-1/3 mx-2 h-64">
            {/* <!-- Map Section --> */}
            <div className="bg-white p-3 shadow-sm rounded-sm mb-6">
              <div className="text-center block w-full text-blue-800 text-sm font-semibold rounded-lg hover:bg-gray-100 focus:outline-none focus:shadow-outline focus:bg-gray-100 hover:shadow-xs p-3 my-4 min-h-80">
                map
              </div>
            </div>
            {/* <!-- End of Map --> */}

            <div className="my-4"></div>

            {/* <!-- Image --> */}
            <div className="bg-white p-3 shadow-sm rounded-sm">
              <div className="text-center block w-full text-blue-800 text-sm font-semibold rounded-lg hover:bg-gray-100 focus:outline-none focus:shadow-outline focus:bg-gray-100 hover:shadow-xs p-3 my-4 min-h-80">
                image
              </div>
              {/* <!-- End of Image --> */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EventPage;
