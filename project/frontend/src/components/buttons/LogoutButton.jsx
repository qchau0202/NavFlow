import { useNavigate } from "react-router-dom";

const LogoutButton = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <button
      className="p-2 text-md font-bold bg-red-500 text-white rounded-md hover:bg-red-600"
      onClick={handleLogout}
    >
      Logout
    </button>
  );
};

export default LogoutButton;
