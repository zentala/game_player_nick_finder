import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store/store';
import { setLanguage } from '../store/languageSlice';
import i18n from '../i18n/i18n';

const LangSwitch: React.FC = () => {
  const dispatch = useDispatch();
  const language = useSelector((state: RootState) => state.language.value);

  const handleChangeLanguage = (newLang: string) => {
    dispatch(setLanguage(newLang));
    i18n.changeLanguage(newLang);
    localStorage.setItem('selectedLanguage', newLang);
  };

  return (
    <div>
      <button 
        type="button"
        className={`btn btn-sm mr-2 ${language === 'en' ? 'btn-outline-primary' : 'btn-outline-secondary'}`} 
        onClick={() => handleChangeLanguage('en')}
      >
        EN
      </button>
      &nbsp;
      <button 
        type="button"
        className={`btn btn-sm mr-2 ${language === 'pl' ? 'btn-outline-primary' : 'btn-outline-secondary'}`} 
        onClick={() => handleChangeLanguage('pl')}
      >
        PL
      </button>
      {/* Add more buttons for other languages here */}
    </div>
  );
};

export default LangSwitch;
