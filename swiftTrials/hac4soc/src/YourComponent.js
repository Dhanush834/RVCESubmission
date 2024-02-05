import React from 'react';

function YourComponent({ output }) {
  return (
    <div>
      {output.map((data, index) => (
        <div key={index}>
          <p>Canonical SMILES: {data['Canonical SMILES']}</p>
          <p>InChIKey: {data.InChIKey}</p>
          <p>Superclass: {data.Superclass}</p>
          <p>Class: {data.Class}</p>
          <p>Subclass: {data.Subclass}</p>
          <p>Molecular Framework: {data['Molecular Framework']}</p>
          <p>Pathway: {data.Pathway}</p>
        </div>
      ))}
    </div>
  );
}
