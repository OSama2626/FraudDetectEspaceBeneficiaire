import { UserButton } from "@clerk/clerk-react";

export default function Dashboard() {
    return (
        <div>
            <nav style={{ padding: "1rem", backgroundColor: "#fff", boxShadow: "0 2px 4px rgba(0,0,0,0.1)" }}>
                <span style={{ fontWeight: "bold" }}>Clerk React App</span>
                <div style={{ float: "right" }}>
                    <UserButton afterSignOutUrl="/login" />
                </div>
            </nav>

            <div style={{ padding: "2rem" }}>
                <h1>Welcome!</h1>
                <p>This is your dashboard. Use the navigation bar to manage your account.</p>

                <h2>Quick Links</h2>
                <ul>
                    <li><a href="#">Profile</a></li>
                    <li><a href="#">Settings</a></li>
                    <li><a href="#">Support</a></li>
                </ul>

                <h2>Statistics</h2>
                <p>
                    <strong>Active Sessions:</strong> 3<br />
                    <strong>Last Login:</strong> Today
                </p>
            </div>
        </div>
    );
}
 