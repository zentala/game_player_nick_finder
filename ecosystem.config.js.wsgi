module.exports = {
  "apps" : [{
    "name"        : "gpnf",
    "script"      : "/home/zentala/htdocs/io.zentala.gpnf/venv/bin/gunicorn",
    "interpreter" : "/home/zentala/htdocs/io.zentala.gpnf/venv/bin/python",
    "args"	  : "game_player_nick_finder.wsgi:application -b 0.0.0.0:8000",
    "watch"       : true,
    "env"	  : {
	"DJANGO_SETTINGS_MODULE": "game_player_nick_finder.settings",
	"PYTHONPATH": "/home/zentala/htdocs/io.zentala.gpnf"
    }
  }]
};
