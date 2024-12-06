import { Routes, Route } from "react-router";

import Auth from '@/auth/components/Auth.jsx';
import Inventory from '@/inventory/components/Inventory.jsx';
import AuthRoute from "./AuthRoutes";

const AppRoutes = () => {
  return (
    <Routes>
      <Route index element={<Auth />} />

      <Route element={
          <AuthRoute isAuthenticated={true}>
            <Route path="/inventory" element={<Inventory />} />
            
          </AuthRoute>
        }
      />
    </Routes>
  );
};

export default AppRoutes;