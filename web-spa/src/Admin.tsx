import { useQuery } from "@tanstack/react-query";

import "./styles.css";
import Navbar from "./Navbar";

const FLAG = "YmN0Zns3aDNfdWw3MW00NzNfNXA0XzE1XzRfcjM0YzdfNXA0fQo=";

function Admin() {
  const query = useQuery({
    queryKey: ["admin"],
    queryFn: (): Promise<{ isAdmin: boolean }> =>
      fetch("/api/isAdmin").then((r) => r.json()),
  });

  if (query.data === undefined || !query.data.isAdmin) return <>Unauthorized</>;

  return (
    <>
      <div id="ocean" className="full vignette">
        <Navbar />
        <div className="content">
          <h1>Admin page</h1>
          <p>{atob(FLAG)}</p>
        </div>
      </div>
    </>
  );
}

export default Admin;
