import React, { useContext } from "react";
import { GlobalContext } from "../context/GlobalState";

export const ResultCard = ({ game, type }) => {
  const {
    addGameToPlayedlist,
    playedlist,
    played,
    addGameToRecommend,
    recommend,
  } = useContext(GlobalContext);

  let storedGame = playedlist.find((o) => o.id === game.id);
  let storedGamePlayed = played.find((o) => o.id === game.id);
  let storedRecommendGame = recommend.find((o) => o.id === game.id);

  const playedlistDisabled = storedGame
    ? true
    : storedGamePlayed
    ? true
    : false;

  const recommendDisabled = storedRecommendGame ? true : false;
  return (
    <div className="result-card">
      <div className="poster-wrapper">
        {/* {game.poster_path ? ( */}
        <img
          // src={`https://image.tmdb.org/t/p/w200${game.poster_path}`}
          src={`https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/${game.steam_gameId}/library_600x900_2x.jpg?t=1568756407`}
          alt={`${game.title} Poster`}
        />
        {/* ) : (
          <div className="filler-poster"></div>
        )} */}
      </div>

      <div className="info">
        <div className="header">
          <h3 className="title">{game.title}</h3>
          <h4 className="release-date">
            {game.release_date ? game.release_date.substring(0, 4) : "-"}
          </h4>
        </div>
        {/* //////////////////////////////////////////// */}

        {type === "recommend" && (
          <>
            <button
              className="ctrl-btn"
              onClick={() => addGameToRecommend(game)}
              disabled={recommendDisabled}
            >
              <i className="fa-fw far fa-eye"></i>
            </button>

            {/* <button
            className="ctrl-btn"
            onClick={() => removeGameFromPlayedlist(game.id)}
          >
            <i className="fa-fw fa fa-times"></i>
          </button> */}
          </>
        )}

        {/* ////////////////////////////////////////////////////////////// */}
        {type === "result" && (
          <>
            <div className="controls">
              <button
                className="btn"
                disabled={playedlistDisabled}
                onClick={() => addGameToPlayedlist(game)}
              >
                Add to want to play
              </button>
              <button
                className="btn"
                disabled={playedlistDisabled}
                onClick={() => addGameToPlayedlist(game)}
              >
                Add to played
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
