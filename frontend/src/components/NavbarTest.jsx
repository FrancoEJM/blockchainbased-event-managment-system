import { NavLink, Link } from "react-router-dom";
import avatarPlaceholder from "../assets/avatarPlaceholder.png";
import { Navbar, Dropdown, Avatar } from "flowbite-react";
import Logo from "../assets/LoginCube.png";
function NavbarTest() {
  return (
    <Navbar fluid rounded>
      <Navbar.Brand href="#">
        <img src={Logo} className="mr-3 h-6 sm:h-9" alt="Logo" />
        <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
          Nombre
        </span>
      </Navbar.Brand>
      <div className="flex md:order-2">
        <Dropdown
          arrowIcon={false}
          inline
          label={
            <Avatar
              alt="User settings"
              img="https://flowbite.com/docs/images/people/profile-picture-5.jpg"
              rounded
            />
          }
        >
          <Dropdown.Header>
            <span className="block text-sm">Bonnie Green</span>
            <span className="block truncate text-sm font-medium">
              name@flowbite.com
            </span>
          </Dropdown.Header>
          <Dropdown.Item>Dashboard</Dropdown.Item>
          <Dropdown.Item>Settings</Dropdown.Item>
          <Dropdown.Item>Earnings</Dropdown.Item>
          <Dropdown.Divider />
          <Dropdown.Item>Sign out</Dropdown.Item>
        </Dropdown>
        <Navbar.Toggle />
      </div>
      <Navbar.Collapse>
        <Navbar.Link href="#" active>
          Home
        </Navbar.Link>
        <Navbar.Link href="#">About</Navbar.Link>
        <Navbar.Link href="#">Services</Navbar.Link>
        <Navbar.Link href="#">Pricing</Navbar.Link>
        <Navbar.Link href="#">Contact</Navbar.Link>
      </Navbar.Collapse>
    </Navbar>

    // <header className="flex items-center justify-center py-4 bg-violet-400">
    //   <nav className="max-w-[85rem] w-full mx-10 px-4 flex items-center justify-between">
    //     <div className="group relative cursor-pointer py-2">
    //       <div className="flex items-center justify-between space-x-5 bg-violet-20 px-4 mx-6">
    //         <div className="max-w-12 border-2 border-violet-500">
    //           <img
    //             className="object-cover w-full"
    //             src={avatarPlaceholder}
    //             alt="LoginCube"
    //           />
    //         </div>
    //         <span>
    //           <svg
    //             xmlns="http://www.w3.org/2000/svg"
    //             fill="none"
    //             viewBox="0 0 24 24"
    //             strokeWidth="1.5"
    //             stroke="currentColor"
    //             className="h-6 w-6 text-white"
    //           >
    //             <path
    //               strokeLinecap="round"
    //               strokeLinejoin="round"
    //               d="M19.5 8.25l-7.5 7.5-7.5-7.5"
    //             />
    //           </svg>
    //         </span>
    //       </div>

    //       <div className="invisible absolute z-50 flex w-full flex-col bg-gray-100 py-1 px-4 text-gray-800 shadow-xl group-hover:visible">
    //         <Link
    //           to="/me"
    //           className="my-2 block border-b border-gray-100 py-1 font-semibold text-gray-500 hover:text-black md:mx-2"
    //         >
    //           Mi perfil
    //         </Link>

    //         <Link
    //           to="/created"
    //           className="my-2 block border-b border-gray-100 py-1 font-semibold text-gray-500 hover:text-black md:mx-2"
    //         >
    //           Mis eventos
    //         </Link>

    //         <Link
    //           to="/general-stats"
    //           className="my-2 block border-b border-gray-100 py-1 font-semibold text-gray-500 hover:text-black md:mx-2"
    //         >
    //           Estadísticas
    //         </Link>

    //         <Link
    //           to="/signed"
    //           className="my-2 block border-b border-gray-100 py-1 font-semibold text-gray-500 hover:text-black md:mx-2"
    //         >
    //           Mis inscripciones
    //         </Link>
    //       </div>
    //     </div>
    //     <NavLink
    //       to="/events"
    //       className="flex-none text-2xl text-white font-semibold"
    //     >
    //       <div className="font-bold leading-none tracking-tight text-gray-900">
    //         Explora
    //       </div>
    //     </NavLink>
    //     <NavLink to="/new-event" className="flex-none text-xl font-semibold">
    //       <div className="disabled:opacity-50 disabled:hover:opacity-50 hover:opacity-95 justify-center ring-none rounded-lg shadow-lg font-semibold py-2 px-4 font-dm focus:outline-none focus-visible:outline-2 focus-visible:outline-offset-2 bg-violet-700 border-b-violet-900 disabled:border-0 disabled:bg-violet-700 disabled:text-white ring-white text-white border-b-4 hover:border-0 active:border-0 hover:text-gray-100 active:bg-violet-900 active:text-gray-300 focus-visible:outline-violet-700 text-sm sm:text-base">
    //         Crea un nuevo evento!
    //       </div>
    //     </NavLink>
    //   </nav>
    // </header>
  );
}
export default NavbarTest;
