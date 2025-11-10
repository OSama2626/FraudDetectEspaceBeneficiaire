import { BrowserRouter as Router, Routes, Route} from "react-router-dom" ;
import Dashboard from "./pages/Dashboard.tsx" ;
import Login from "./pages/Login.tsx";
import Signup from "./pages/Signup.tsx" ;
import LandingPage from "./pages/LandingPage.tsx";
import { SignedIn, SignedOut } from "@clerk/clerk-react";
import Layout from "./Layouts/Layout.tsx";
import UserLayout from "./Layouts/UserLayout.tsx";



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SignedOut><Layout /></SignedOut>}>
          <Route index element={<LandingPage />} />
          <Route path="login" element={<Login />} />
          <Route path="signup" element={<Signup />} />
        </Route>

        <Route path="/dashboard" element={<SignedIn><UserLayout /></SignedIn>}>
          <Route path="/dashboard" element={<Dashboard />} />
        </Route>
      </Routes>
    </Router>
  ) ;
}

export default App ;