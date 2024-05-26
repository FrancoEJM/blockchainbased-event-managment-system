import MyEventsList from "../../components/Events/MyEventsList";
import Navbar from "../../components/Navbar";

function MyEvents() {
  const user_id = localStorage.id_usuario;
  return (
    <>
      <Navbar />
      <MyEventsList user_id={user_id} />
    </>
  );
}
export default MyEvents;
