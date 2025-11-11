import AuthLayout from "./AuthLayout.tsx";
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
        {/* Custom Sign Up Form or Placeholder */}
        <h2>Sign Up</h2>
        {/* Add your sign-up form here */}
      </AuthLayout>
    </div>
  );
}
