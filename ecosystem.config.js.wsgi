module.exports = {
  apps: [{
    name: "gpnf",
    script: "/home/zentala/.local/share/virtualenvs/io.zentala.gpnf-4IYRmZtE/bin/gunicorn",
    args: "game_player_nick_finder.wsgi:application --bind 0.0.0.0:8000",
    watch: true,
    env: {
      DJANGO_SETTINGS_MODULE: "game_player_nick_finder.settings.production",
      PYTHONPATH: "/home/zentala/htdocs/io.zentala.gpnf",
      NODE_ENV: "production"
    }
  }]
};
