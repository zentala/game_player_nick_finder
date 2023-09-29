import React, { useState } from 'react';

interface CharacterFilterProps {
  onFilter: (nickname: string, game: string) => void;
}

const CharacterFilter: React.FC<CharacterFilterProps> = ({ onFilter }) => {
  const [nickname, setNickname] = useState('');
  const [game, setGame] = useState('');

  const handleFilter = () => {
    onFilter(nickname, game);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Nickname"
        value={nickname}
        onChange={(e) => setNickname(e.target.value)}
      />
      <input
        type="text"
        placeholder="Game"
        value={game}
        onChange={(e) => setGame(e.target.value)}
      />
      <button onClick={handleFilter}>Filter</button>
    </div>
  );
};

export default CharacterFilter;
