import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';


const Header: React.FC = () => {
  const { t } = useTranslation();

  const isLoggedIn = false;

  return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary">
    <div className="container">
      <Link className="navbar-brand" to="/">{t('navGamePlayerNickFinder')}</Link>
      <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent">
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarSupportedContent">
        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
          <li className="nav-item">
            <Link className="nav-link" to="/">{t('navHome')}</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/characters">{t('navCharacters')}</Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/games">{t('navGames')}</Link>
          </li>
        </ul>
        {isLoggedIn ? (
          <ul className="navbar-nav mb-2 mb-lg-0 d-flex">
            <li className="nav-item dropdown">
              <Link className="nav-link dropdown-toggle" to="#" role="button" data-bs-toggle="dropdown">
                [Avatar + Username]
              </Link>
              <ul className="dropdown-menu dropdown-menu-end">
                <li><Link className="dropdown-item" to="#">{t('navProfile')}</Link></li>
                <li><Link className="dropdown-item" to="#">{t('navChangePassword')}</Link></li>
                <li><Link className="dropdown-item" to="#">{t('navAdminPanel')}</Link></li>
                <li><hr className="dropdown-divider" /></li>
                <li><Link className="dropdown-item" to="#">{t('navLogOut')}</Link></li>
              </ul>
            </li>
          </ul>
        ) : (
          <ul className="navbar-nav mb-2 mb-lg-0 d-flex">
            <li className="nav-item">
              <Link className="nav-link" to="#">{t('navLogIn')}</Link>
            </li>
            <li className="nav-item">
              or
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="#">{t('navRegister')}</Link>
            </li>
          </ul>
        )}
      </div>
    </div>
  </nav>
  );
};

export default Header;
