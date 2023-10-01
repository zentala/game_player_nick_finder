import React from 'react';
import CharacterFilterForm from '../components/CharacterFilterForm';
import CharacterTable from '../components/CharacterTable';

const Characters: React.FC = () => {
  return (
    <div>
      <h1>Character List</h1>
      <CharacterFilterForm />
      <CharacterTable />
    </div>
  );
};

export default Characters;
