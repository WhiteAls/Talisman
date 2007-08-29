#===istalismanplugin===
# -*- coding: utf-8 -*-

def handler_presence_presence(prs):
	type = prs.getType()
	who = prs.getFrom()
	if not type:
		type = 'available'
	if type == 'subscribe':
		JCON.send(xmpp.Presence(to=who, typ='subscribed'))
		#JCON.send(xmpp.Presence(to=who, typ='subscribe'))
	elif type == 'unsubscribe':
		JCON.send(xmpp.Presence(to=who, typ='unsubscribed'))
		#JCON.send(xmpp.Presence(to=who, typ='unsubscribe'))
	elif type == 'subscribed':
		pass
	elif type == 'unsubscribed':
		pass
	elif type == 'available':
		pass
	elif type == 'unavailable':
		pass

def handler_presence_ra_change(prs):
	while prs:
		roles={'none':0, 'visitor':0, 'participant':10, 'moderator':15}
		affiliations={'none':0, 'member':0, 'admin':5, 'owner':15}
		groupchat = prs.getFrom().getStripped()
		nick = prs.getFrom().getResource()
		jid = get_true_jid(groupchat+'/'+nick)
		try:
			if jid in GLOBACCESS or jid in ACCBYCONF[groupchat]:
				return
		except:
			pass
		if GROUPCHATS[groupchat].has_key(nick):
			item = findPresenceItem(prs)
			if item == None:
				jid = groupchat+'/'+nick
			else:
				jid = item['jid']
				if jid != None:
#					time.sleep(0.5)
					role = item['role']
					aff = item['affiliation']
					if role in roles.keys():
						accr = roles[role]
					else:
						accr = 0
					if aff in affiliations.keys():
						acca = affiliations[aff]
					else:
						acca = 0
					access = int(accr)+int(acca)
					change_access_temp(groupchat, jid, access)
					return

register_presence_handler(handler_presence_presence)
register_presence_handler(handler_presence_ra_change)
