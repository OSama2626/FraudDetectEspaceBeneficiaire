import { SignUp, SignUpStep, SignUpButton } from "@clerk/elements";
import { ClerkLoaded, ClerkLoading, useSignUp } from "@clerk/clerk-react";
import { useState } from "react";

export default function SignUpPage() {
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
