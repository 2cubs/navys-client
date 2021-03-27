from lib2cubs.applevelcom.basic import ClientBase, Remote, action


class Client(ClientBase):

	EVENT_SERVICE_STATUS_CHANGED: str = 'service_status_changed'

	def app(self, remote: Remote):
		pass

	@action
	def event_service_status_changed(self, service: str, config: str):
		self.trigger_event(self.EVENT_SERVICE_STATUS_CHANGED, service=service, config=config)
