import React, { useState } from 'react';
import { Bell, Upload, FileText, Clock, CheckCircle, XCircle, AlertCircle, Search, Filter, Menu, X } from 'lucide-react';

export interface Check {
  id: number;
  numero: string;
  montant: number;
  banque: string;
  dateDepot: string;
  statut: 'en_cours' | 'approuve' | 'rejete' | 'en_attente';
  agent: string;
  motifRejet?: string;
}

export interface Notification {
  id: number;
  message: string;
  date: string;
  lu: boolean;
}

// Simulation de données (à remplacer par des appels API)
const mockChecks: Check[] = [
  {
    id: 1,
    numero: "CHQ001234",
    montant: 5000,
    banque: "Attijariwafa Bank",
    dateDepot: "2024-11-28",
    statut: "en_cours",
    agent: "Mohamed Alami"
  },
  {
    id: 2,
    numero: "CHQ001235",
    montant: 12500,
    banque: "BMCE Bank",
    dateDepot: "2024-11-27",
    statut: "approuve",
    agent: "Fatima Zahrae"
  },
  {
    id: 3,
    numero: "CHQ001236",
    montant: 3200,
    banque: "Banque Populaire",
    dateDepot: "2024-11-26",
    statut: "rejete",
    agent: "Ahmed Bennani",
    motifRejet: "Signature non conforme"
  }
];

const mockNotifications: Notification[] = [
  {
    id: 1,
    message: "Votre chèque CHQ001235 a été approuvé",
    date: "2024-11-28 10:30",
    lu: false
  },
  {
    id: 2,
    message: "Nouveau commentaire de l'agent sur CHQ001234",
    date: "2024-11-28 09:15",
    lu: false
  }
];

const banques: string[] = [
  "Attijariwafa Bank",
  "BMCE Bank",
  "Banque Populaire",
  "Crédit du Maroc",
  "CIH Bank",
  "Société Générale Maroc"
];

export default function BeneficiarySpace() {
  const [activeTab, setActiveTab] = useState('cheques');
  const [cheques, setCheques] = useState<Check[]>(mockChecks);
  const [notifications, setNotifications] = useState<Notification[]>(mockNotifications);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('tous');
  const [newCheck, setNewCheck] = useState({
    numero: '',
    montant: '',
    banque: '',
    fichier: null as File | null
  });

  const getStatusBadge = (statut: Check['statut']) => {
    const configs = {
      en_cours: { color: 'bg-blue-100 text-blue-800', icon: Clock, label: 'En cours' },
      approuve: { color: 'bg-green-100 text-green-800', icon: CheckCircle, label: 'Approuvé' },
      rejete: { color: 'bg-red-100 text-red-800', icon: XCircle, label: 'Rejeté' },
      en_attente: { color: 'bg-yellow-100 text-yellow-800', icon: AlertCircle, label: 'En attente' }
    };
    const config = configs[statut] || configs.en_attente;
    const Icon = config.icon;
    return (
      <span className={`px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1 ${config.color}`}>
        <Icon className="w-4 h-4" />
        {config.label}
      </span>
    );
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setNewCheck({ ...newCheck, fichier: file });
    }
  };

  const handleSubmitCheck = () => {
    const nouveauCheque: Check = {
      id: cheques.length + 1,
      numero: newCheck.numero,
      montant: parseFloat(newCheck.montant),
      banque: newCheck.banque,
      dateDepot: new Date().toISOString().split('T')[0],
      statut: 'en_attente',
      agent: 'En attente d\'affectation'
    };
    setCheques([nouveauCheque, ...cheques]);
    setShowUploadModal(false);
    setNewCheck({ numero: '', montant: '', banque: '', fichier: null });

    const nouvelleNotif: Notification = {
      id: notifications.length + 1,
      message: `Votre chèque ${newCheck.numero} a été déposé avec succès`,
      date: new Date().toLocaleString('fr-FR'),
      lu: false
    };
    setNotifications([nouvelleNotif, ...notifications]);
  };

  const filteredCheques = cheques.filter(cheque => {
    const matchSearch = cheque.numero.toLowerCase().includes(searchTerm.toLowerCase()) ||
      cheque.banque.toLowerCase().includes(searchTerm.toLowerCase());
    const matchFilter = filterStatus === 'tous' || cheque.statut === filterStatus;
    return matchSearch && matchFilter;
  });

  const unreadCount = notifications.filter(n => !n.lu).length;

  const menuItems = [
    { id: 'cheques', label: 'Mes Chèques', emoji: '💳', count: cheques.length },
    { id: 'historique', label: 'Historique', emoji: '📋', count: null },
    { id: 'notifications', label: 'Notifications', emoji: '🔔', count: unreadCount }
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <aside className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-white border-r transform transition-transform duration-300 ease-in-out ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}>
        <div className="h-full flex flex-col">
          {/* Logo / Header */}
          <div className="p-6 border-b">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-gray-900">💼 Chèques</h2>
                <p className="text-sm text-gray-600 mt-1">Espace Bénéficiaire</p>
              </div>
              <button
                onClick={() => setSidebarOpen(false)}
                className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Menu Items */}
          <nav className="flex-1 p-4 space-y-2">
            {menuItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id);
                  setSidebarOpen(false);
                }}
                className={`w-full flex items-center justify-between px-4 py-3 rounded-lg transition ${activeTab === item.id
                    ? 'bg-blue-50 text-blue-700 font-medium'
                    : 'text-gray-700 hover:bg-gray-100'
                  }`}
              >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{item.emoji}</span>
                  <span>{item.label}</span>
                </div>
                {item.count !== null && item.count > 0 && (
                  <span className={`px-2 py-1 text-xs rounded-full ${activeTab === item.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-200 text-gray-700'
                    }`}>
                    {item.count}
                  </span>
                )}
              </button>
            ))}
          </nav>

          {/* New Check Button */}
          <div className="p-4 border-t">
            <button
              onClick={() => setShowUploadModal(true)}
              className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 transition flex items-center justify-center gap-2 font-medium"
            >
              <Upload className="w-5 h-5" />
              Nouveau chèque
            </button>
          </div>

          {/* User Info */}
          <div className="p-4 border-t bg-gray-50">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                MB
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">Mohamed Benali</p>
                <p className="text-xs text-gray-600 truncate">m.benali@email.com</p>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          onClick={() => setSidebarOpen(false)}
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
        />
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="bg-white shadow-sm border-b sticky top-0 z-30">
          <div className="px-4 py-4 flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
              >
                <Menu className="w-6 h-6" />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  {menuItems.find(item => item.id === activeTab)?.emoji}{' '}
                  {menuItems.find(item => item.id === activeTab)?.label}
                </h1>
                <p className="text-sm text-gray-600">
                  {activeTab === 'cheques' && `${filteredCheques.length} chèque(s) actif(s)`}
                  {activeTab === 'historique' && `${cheques.length} chèque(s) au total`}
                  {activeTab === 'notifications' && `${unreadCount} non lue(s)`}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {unreadCount > 0 && activeTab !== 'notifications' && (
                <button
                  onClick={() => setActiveTab('notifications')}
                  className="relative p-2 hover:bg-gray-100 rounded-lg transition"
                >
                  <Bell className="w-6 h-6 text-gray-700" />
                  <span className="absolute top-0 right-0 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {unreadCount}
                  </span>
                </button>
              )}
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="flex-1 p-4 md:p-6 overflow-auto">
          {activeTab === 'cheques' && (
            <div>
              {/* Filters */}
              <div className="bg-white p-4 rounded-lg shadow-sm mb-6 flex flex-col md:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    type="text"
                    placeholder="Rechercher par numéro ou banque..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="tous">Tous les statuts</option>
                  <option value="en_attente">En attente</option>
                  <option value="en_cours">En cours</option>
                  <option value="approuve">Approuvé</option>
                  <option value="rejete">Rejeté</option>
                </select>
              </div>

              {/* Checks List */}
              <div className="space-y-4">
                {filteredCheques.map((cheque) => (
                  <div key={cheque.id} className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition">
                    <div className="flex flex-col md:flex-row md:justify-between md:items-start gap-4 mb-4">
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{cheque.numero}</h3>
                        <p className="text-sm text-gray-600">Déposé le {cheque.dateDepot}</p>
                      </div>
                      {getStatusBadge(cheque.statut)}
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                      <div>
                        <p className="text-sm text-gray-600">Montant</p>
                        <p className="text-lg font-semibold text-gray-900">{cheque.montant.toLocaleString()} MAD</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Banque</p>
                        <p className="text-lg font-medium text-gray-900">{cheque.banque}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Agent assigné</p>
                        <p className="text-lg font-medium text-gray-900">{cheque.agent}</p>
                      </div>
                    </div>

                    {cheque.motifRejet && (
                      <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                        <p className="text-sm text-red-800">
                          <strong>Motif de rejet:</strong> {cheque.motifRejet}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'historique' && (
            <div className="bg-white rounded-lg shadow-sm overflow-hidden">
              <div className="p-6 border-b">
                <h2 className="text-xl font-semibold text-gray-900">Historique complet</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Numéro
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Montant
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Banque
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Statut
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {cheques.map((cheque) => (
                      <tr key={cheque.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                          {cheque.numero}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                          {cheque.dateDepot}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap font-semibold text-gray-900">
                          {cheque.montant.toLocaleString()} MAD
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                          {cheque.banque}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          {getStatusBadge(cheque.statut)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="space-y-4">
              {notifications.map((notif) => (
                <div
                  key={notif.id}
                  className={`bg-white p-4 rounded-lg shadow-sm ${!notif.lu ? 'border-l-4 border-blue-600' : ''
                    }`}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <p className={`text-gray-900 ${!notif.lu ? 'font-semibold' : ''}`}>
                        {notif.message}
                      </p>
                      <p className="text-sm text-gray-500 mt-1">{notif.date}</p>
                    </div>
                    {!notif.lu && (
                      <span className="w-2 h-2 bg-blue-600 rounded-full"></span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>

      {/* Upload Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h2 className="text-2xl font-bold mb-4">💳 Nouveau chèque</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Numéro du chèque *
                </label>
                <input
                  type="text"
                  required
                  value={newCheck.numero}
                  onChange={(e) => setNewCheck({ ...newCheck, numero: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="CHQ001234"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Montant (MAD) *
                </label>
                <input
                  type="number"
                  required
                  value={newCheck.montant}
                  onChange={(e) => setNewCheck({ ...newCheck, montant: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="5000"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Banque ciblée *
                </label>
                <select
                  required
                  value={newCheck.banque}
                  onChange={(e) => setNewCheck({ ...newCheck, banque: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Sélectionner une banque</option>
                  {banques.map((banque) => (
                    <option key={banque} value={banque}>
                      {banque}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Image du chèque *
                </label>
                <input
                  type="file"
                  accept="image/*,.pdf"
                  onChange={handleFileChange}
                  className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => setShowUploadModal(false)}
                  className="flex-1 px-4 py-2 border rounded-lg hover:bg-gray-50 transition"
                >
                  Annuler
                </button>
                <button
                  onClick={handleSubmitCheck}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                >
                  Soumettre
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
