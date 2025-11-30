import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { Bell, Menu, LayoutDashboard, List, History, Briefcase } from 'lucide-react';
import UploadModal from '../components/UploadModal';
import { useBeneficiary } from '../BeneficiaryContext';

const BeneficiaryLayout = () => {
  const [menuOpen, setMenuOpen] = React.useState(false);
  const { notifications } = useBeneficiary();
  const unreadCount = notifications.filter((n) => !n.lu).length;

  const menuItems = [
    { to: '/beneficiary', label: 'Tableau de bord', icon: LayoutDashboard },
    { to: 'checks', label: 'Mes Chèques', icon: List },
    { to: 'history', label: 'Historique', icon: History },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation Bar */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-40">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            {/* Logo and Main Nav */}
            <div className="flex items-center gap-4">
              <button
                onClick={() => setMenuOpen(!menuOpen)}
                className="md:hidden p-2 -ml-2 hover:bg-gray-100 rounded-lg"
              >
                <Menu className="w-6 h-6" />
              </button>
              <div className="flex items-center gap-2">
                <Briefcase className="w-6 h-6 text-gray-800" />
                <h1 className="text-xl font-bold text-gray-900">Chèques</h1>
              </div>
              <nav className="hidden md:flex items-center gap-4">
                {menuItems.map((item) => (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    end
                    className={({ isActive }) =>
                      `flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition ${
                        isActive
                          ? 'bg-blue-50 text-blue-700'
                          : 'text-gray-600 hover:bg-gray-100'
                      }`
                    }
                  >
                    <item.icon className="w-5 h-5" />
                    <span>{item.label}</span>
                  </NavLink>
                ))}
              </nav>
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center gap-4">
              <div className="hidden sm:block">
                <UploadModal />
              </div>
              <NavLink to="notifications" className="relative p-2 hover:bg-gray-100 rounded-full transition">
                <Bell className="w-6 h-6 text-gray-700" />
                {unreadCount > 0 && (
                  <span className="absolute top-0 right-0 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {unreadCount}
                  </span>
                )}
              </NavLink>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                  MB
                </div>
                <div className="hidden lg:block">
                  <p className="text-sm font-medium text-gray-900 truncate">Mohamed Benali</p>
                  <p className="text-xs text-gray-600 truncate">m.benali@email.com</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        {menuOpen && (
          <div className="md:hidden bg-white border-t">
            <nav className="p-4 space-y-2">
              {menuItems.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end
                  onClick={() => setMenuOpen(false)}
                  className={({ isActive }) =>
                    `w-full flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                      isActive
                        ? 'bg-blue-50 text-blue-700 font-medium'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`
                  }
                >
                  <item.icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </NavLink>
              ))}
              <div className="pt-4 border-t">
                 <UploadModal />
              </div>
            </nav>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="container mx-auto p-4 md:p-6">
        <Outlet />
      </main>
    </div>
  );
};

export default BeneficiaryLayout;
