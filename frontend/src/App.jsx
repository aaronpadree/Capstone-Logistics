// import React from 'react';
// import { Routes, Route, Navigate } from 'react-router-dom'; 
// import Main from './components/Main';
// import { Toaster } from 'react-hot-toast';
// import Dashboard from './pages/Dashboard';
// import Evaluate from './pages/Evaluate';
// import Purchase from './pages/Purchase';
// import Product from './pages/Products';
// import Supplier from './pages/Suppliers';
// import Department from './pages/Departments'
// import PurchaseList from './pages/PurchaseList'
// import EvaluateList from './pages/EvaluateList';
// import Damage from './pages/Damage';
// import Inventory from './pages/Inventory'
// import Maintenance from './pages/Maintenance';
// import ProductSupplier from './pages/ProductSupplier';
// import DepartmentRequest from './pages/DepartmentRequest';

// const App = () => {
//   return (
//     <>
//       <Toaster /> {/* Notifications component from react-hot-toast */}
//       <Routes>
//         {/* Main wrapper for protected routes */}
//         <Route path="/" element={<Main />}>
//           {/* Dashboard Route */}
//           <Route path="/dashboard" element={<Dashboard />} />
          
//           {/* Evaluate Route */}
//           <Route path="/evaluate" element={<Evaluate />} />

//           {/* EvaluateList Route */}
//           <Route path="/evaluate-list" element={<EvaluateList />} />

//           {/* Damage Route */}
//           <Route path="/evaluate-list" element={<EvaluateList />} />

//            {/* Damage Route */}
//            <Route path="/damage" element={<Damage />} />

//           {/* Purchase Route */}
//           <Route path="/purchase-request" element={<Purchase />} />

//           {/* Purchase Route */}
//           <Route path="/purchase-request-list" element={<PurchaseList />} />

//           {/* Purchase Route */}
//           <Route path="/inventory" element={<Inventory />} />

//           {/* Maintenance Route */}
//           <Route path="/maintenance" element={<Maintenance />} />

//           {/* Maintenance Route */}
//           <Route path="/product-supplier" element={<ProductSupplier />} />

//           {/* Products Route */}
//           <Route path="/products" element={<Product />} />

//           {/* Supplier Route */}
//           <Route path="/suppliers" element={<Supplier />} />

//           {/* Supplier Route */}
//           <Route path="/departments" element={<Department />} />
          
//            {/* Department request Route */}
//           <Route path="/department-request" element={<DepartmentRequest />} />

//         </Route>
//         {/* Redirect all other paths */}
//         <Route path="*" element={<Navigate to="/dashboard" />} />
//       </Routes>
//     </>
//   );
// };

// export default App;
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom'; 
import Main from './components/Main';
import { Toaster } from 'react-hot-toast';
import Dashboard from './pages/Dashboard';
import Evaluate from './pages/Evaluate';
import Purchase from './pages/Purchase';
import Product from './pages/Products';
import Supplier from './pages/Suppliers';
import Department from './pages/Departments';
import PurchaseList from './pages/PurchaseList';
import EvaluateList from './pages/EvaluateList';
import Damage from './pages/Damage';
import Inventory from './pages/Inventory';
import Maintenance from './pages/Maintenance';
import ProductSupplier from './pages/ProductSupplier';
import DepartmentRequest from './pages/DepartmentRequest';
import Login from "./components/Login";

const App = () => {
  return (
    <>
      <Toaster /> {/* Notifications component from react-hot-toast */}
      <Routes>
        {/* Public route for Login */}
        <Route
          path="/login"
          element={isAuthenticated() ? <Navigate to="/dashboard" replace /> : <Login />}
        />

        {/* Main wrapper for protected routes */}
        <Route
          path="/"
          element={isAuthenticated() ? <Main /> : <Navigate to="/login" replace />}
        >
          {/* Dashboard Route */}
          <Route path="/dashboard" element={<Dashboard />} />
          
          {/* Evaluate Route */}
          <Route path="/evaluate" element={<Evaluate />} />

          {/* EvaluateList Route */}
          <Route path="/evaluate-list" element={<EvaluateList />} />

          {/* Damage Route */}
          <Route path="/damage" element={<Damage />} />

          {/* Purchase Route */}
          <Route path="/purchase-request" element={<Purchase />} />

          {/* PurchaseList Route */}
          <Route path="/purchase-request-list" element={<PurchaseList />} />

          {/* Inventory Route */}
          <Route path="/inventory" element={<Inventory />} />

          {/* Maintenance Route */}
          <Route path="/maintenance" element={<Maintenance />} />

          {/* ProductSupplier Route */}
          <Route path="/product-supplier" element={<ProductSupplier />} />

          {/* Products Route */}
          <Route path="/products" element={<Product />} />

          {/* Supplier Route */}
          <Route path="/suppliers" element={<Supplier />} />

          {/* Departments Route */}
          <Route path="/departments" element={<Department />} />
          
          {/* Department Request Route */}
          <Route path="/department-request" element={<DepartmentRequest />} />
        </Route>

        {/* Redirect all other paths */}
        <Route path="*" element={<Navigate to="/dashboard" />} />
      </Routes>
    </>
  );
};

export default App;
