import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { Navbar, Dropdown, Avatar, Button } from "flowbite-react";
import Logo from "../assets/LoginCube.png";
import AvatarLogo from "../assets/avatarPlaceholder.png";
import { useNavigate } from "react-router-dom";

function NavbarTest() {
  const [userDetails, setUserDetails] = useState({
    nombre: "",
    apellido: "",
    correo_electronico: "",
  });
  const [avatarUrl, setAvatarUrl] = useState(AvatarLogo);

  useEffect(() => {
    const fetchUserDetails = async () => {
      try {
        const token = localStorage.getItem("token"); // Obtener el token del localStorage
        console.log("useEffect is running"); // Debugging useEffect
        const baseUrl = import.meta.env.VITE_BACKEND_URL; // URL base del backend
        const response = await axios.get(`${baseUrl}/api/user/me/details`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        setUserDetails({
          nombre: response.data.nombre,
          apellido: response.data.apellido,
          correo_electronico: response.data.correo_electronico,
        });
      } catch (error) {
        console.error("Error fetching user details", error);
      }
    };

    fetchUserDetails();
  }, []);

  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("id_usuario");

    navigate("/");
  };

  return (
    <Navbar fluid rounded>
      <Navbar.Brand href="/events">
        <img src={Logo} className="mr-3 h-6 sm:h-9" alt="Logo" />
        <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
          Eventos
        </span>
      </Navbar.Brand>
      <div className="flex md:order-2">
        <Dropdown
          arrowIcon={false}
          inline
          label={<Avatar alt="User settings" img={avatarUrl} rounded />}
        >
          <Dropdown.Header>
            <span className="block text-sm">{`${userDetails.nombre} ${userDetails.apellido}`}</span>
            <span className="block truncate text-sm font-medium">
              {userDetails.correo_electronico}
            </span>
          </Dropdown.Header>
          <Link to={`/created-new`}>
            <Dropdown.Item>Mis eventos</Dropdown.Item>
          </Link>
          <Link className="hide-on-mobile" to={`/general-stats`}>
            <Dropdown.Item>Estadísticas</Dropdown.Item>
          </Link>
          {/* <Link to={`/signed`}>
            <Dropdown.Item>Mis inscripciones</Dropdown.Item>
          </Link> */}
          <Dropdown.Divider />
          <Dropdown.Item onClick={handleLogout}>Cerrar sesión</Dropdown.Item>
        </Dropdown>
        <Navbar.Toggle />
      </div>
      <Navbar.Collapse>
        <Navbar.Link
          className="hover:text-violet-700 md:hover:text-violet-700 sm:hover:text-violet-700 lg:hover:text-violet-700"
          href="/events"
        >
          <Button color="gray">Eventos</Button>
        </Navbar.Link>
        <Navbar.Link
          className="hide-on-mobile bg-violet-50 hover:text-violet-700 md:hover:text-violet-700 sm:hover:text-violet-700 lg:hover:text-violet-700"
          href="/new-event-new"
        >
          <Button gradientMonochrome="purple">Nuevo Evento</Button>
        </Navbar.Link>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default NavbarTest;
