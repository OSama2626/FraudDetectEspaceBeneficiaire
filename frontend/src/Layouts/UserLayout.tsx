import { Outlet } from "react-router-dom";

export default function UserLayout() {
    return (
        <div className="d-flex w-100 h-100">
            <Outlet />
        </div>
    );
}