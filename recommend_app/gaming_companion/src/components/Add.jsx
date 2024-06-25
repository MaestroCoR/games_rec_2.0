import React, { useState } from "react";
import { ResultCard } from "./ResultCard";

export const Add = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const onChange = (e) => {
    e.preventDefault();
    setQuery(e.target.value);

    fetch(`http://127.0.0.1:8080/search?query=${e.target.value}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        setResults(data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setResults([]);
      });
  };

  return (
    <div className="add-page">
      <div className="container">
        <div className="add-content">
          <div className="input-wrapper">
            <input
              type="text"
              placeholder="Пошук гри"
              value={query}
              onChange={onChange}
            />
          </div>
          {results.length > 0 && (
            // <ul className="results">
            <ul>
              {results.map((game) => (
                <li key={`${game.gameId}`}>
                  <ResultCard game={game} type="result" />
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};
