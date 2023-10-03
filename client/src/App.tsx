import React, { useEffect } from 'react';
import { RootState } from './store/store';
import AppRouter from './components/AppRouter';
import { useDispatch, useSelector } from 'react-redux';
import { setLanguage } from './store/languageSlice';
import i18n from './i18n/i18n';

const App: React.FC = () => {
  const dispatch = useDispatch();
  const language = useSelector((state: RootState) => state.language.value);

  useEffect(() => {
    const savedLanguage = localStorage.getItem('selectedLanguage');
    if (savedLanguage) {
      dispatch(setLanguage(savedLanguage));
      i18n.changeLanguage(savedLanguage);
    }
  }, [dispatch]);

  useEffect(() => {
    i18n.changeLanguage(language);
  }, [language]);

  return (
    <div className="App">
      <AppRouter />
    </div>
  );
};

export default App;
