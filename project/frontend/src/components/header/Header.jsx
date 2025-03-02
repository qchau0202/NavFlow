import LogoutButton from "../buttons/LogoutButton";

const Header = () => {
  return (
    <>
      <div className="flex justify-between items-center p-4 bg-gray-200">
        <h1 className="text-4xl font-bold">NavFlow</h1>
        <LogoutButton />
      </div>      
    </>
  );
}

export default Header;