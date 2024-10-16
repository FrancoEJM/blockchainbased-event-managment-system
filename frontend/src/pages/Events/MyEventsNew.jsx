import MyEventsListNew from "../../components/Events/MyEventsListNew";
import NavbarTest from "../../components/NavbarTest";
function MyEvents() {
  const user_id = localStorage.id_usuario;
  return (
    <>
      <NavbarTest />
      <MyEventsListNew user_id={user_id} />
    </>
  );
}
export default MyEvents;
