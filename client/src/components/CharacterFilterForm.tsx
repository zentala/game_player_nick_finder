import React, { useState } from 'react';

const CharacterFilterForm: React.FC = () => {
  const [nickname, setNickname] = useState('');
  const [game, setGame] = useState('');
  const [year, setYear] = useState('');

  const handleFilterSubmit = () => {
    // Tutaj wywołaj logikę filtrowania
  };

  return (
    <form className="row gy-2 gx-3 align-items-end">
      <div className="col-auto">
        <input type="text" className="form-control" placeholder="ShadowWarrior01" value={nickname} onChange={(e) => setNickname(e.target.value)} />
      </div>
      <div className="col-auto">
        <select className="form-select" value={game} onChange={(e) => setGame(e.target.value)}>
          {/* Opcje gier */}
        </select>
      </div>
      <div className="col-auto">
        <input type="number" className="form-control" placeholder="2001" value={year} onChange={(e) => setYear(e.target.value)} />
      </div>
      <div className="col-auto">
        <button type="button" className="btn btn-primary mb-3" onClick={handleFilterSubmit}>Filter</button>
      </div>
    </form>
  );
};

export default CharacterFilterForm;
