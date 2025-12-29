const { exec } = require('child_process');

exec('pipenv run gunicorn game_player_nick_finder.wsgi:application --bind 0.0.0.0:7600', (err, stdout, stderr) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log(stdout);
});
