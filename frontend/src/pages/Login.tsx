import { SignIn } from "@clerk/clerk-react";
import AuthLayout from "./AuthLayout.tsx";

export default function Login() {
  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#f8f9fa",
      }}
    >
      <AuthLayout>
        <SignIn signUpUrl="/signup" forceRedirectUrl={"/dashboard"}/>
      </AuthLayout>
    </div>
  );
}


