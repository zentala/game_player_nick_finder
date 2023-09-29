import React from 'react';
import CharacterFilter from './CharacterFilter';

interface Character {
  id: number;
  nickname: string;
  games: string[];
}

const characters: Character[] = [
  { id: 1, nickname: 'ShadowWarrior01', games: ['Game1', 'Game2'] },
  // ... więcej postaci
];

const CharacterList: React.FC = () => {
  const handleFilter = (nickname: string, game: string) => {
    // Tutaj dodasz logikę filtrowania
  };

  return (
    <div>
      <h1>Character List</h1>
      <CharacterFilter onFilter={handleFilter} />
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Nick</th>
            <th>Games</th>
          </tr>
        </thead>
        <tbody>
          {characters.map((character, index) => (
            <tr key={character.id}>
              <td>{index + 1}</td>
              <td>{character.nickname}</td>
              <td>{character.games.join(', ')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CharacterList;
