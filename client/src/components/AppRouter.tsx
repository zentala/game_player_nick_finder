import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import Home from '../pages/Home';
import Characters from '../pages/Characters';
import Games from '../pages/Games';

const AppRouter: React.FC = () => {
  return (
    <Router>
    <div>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/characters" element={<Characters />} />
        <Route path="/games" element={<Games />} />
      </Routes>
      <Footer />
    </div>
    </Router>
  );
};

export default AppRouter;
