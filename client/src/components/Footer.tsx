import React from 'react';
import LangSwitch from './LangSwitch';

const Footer: React.FC = () => {
  return (
    <div className="container">
      <footer className="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
        <p className="col-md-3 mb-0 text-body-secondary">&copy; 2023 <a href="/" className="nav-link d-inline">Game Player Nick Finder</a></p>
        
        <ul className="nav col-md-3 justify-content-center">
          <li className="nav-item">
            <a href="https://github.com/zentala/game_player_nick_finder" target="_blank" rel="noopener noreferrer" className="nav-link px-2 text-body-secondary">
              <i className="bi bi-github"></i> GitHub
            </a>
          </li>
        </ul>

        <LangSwitch />
        
        <ul className="nav col-md-3 justify-content-end list-unstyled d-flex">
          <li className="ms-3"><a className="text-body-secondary" href="#"><i className="bi bi-twitter"></i></a></li>
          <li className="ms-3"><a className="text-body-secondary" href="#"><i className="bi bi-instagram"></i></a></li>
          <li className="ms-3"><a className="text-body-secondary" href="#"><i className="bi bi-facebook"></i></a></li>
        </ul>
      </footer>
    </div>
  );
};

export default Footer;
