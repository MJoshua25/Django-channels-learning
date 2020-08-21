from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.conf.urls import url

from chat.consumers import ChatChonsumer

application = ProtocolTypeRouter({
	# Empty for now (http->django views is added by default)
	'websocket':AllowedHostsOriginValidator( # verification des hosts
		AuthMiddlewareStack( # permet d'avoir les informations de l'utilisateur dans les websocket
			URLRouter(
				[
					url(r"^messages/(?P<username>[\w.@+-]+)", ChatChonsumer),
				]
			)
		)
	)
})
