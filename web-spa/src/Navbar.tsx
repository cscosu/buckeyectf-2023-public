import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";

function Navbar() {
  const query = useQuery({
    queryKey: ["admin"],
    queryFn: (): Promise<{ isAdmin: boolean }> =>
      fetch("/api/isAdmin").then((r) => r.json()),
  });

  return (
    <nav>
      <Link to="/">Home</Link>
      {query.data?.isAdmin && <Link to="/admin">Admin</Link>}
    </nav>
  );
}

export default Navbar;
