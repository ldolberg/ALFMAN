#!/usr/bin/python
import iptc

def delete_output_accept_rule(rule):
	chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "OUTPUT")
	chain.delete_rule(rule)
	return rule


def set_output_accept_rule(src,dst,sport,dport):
	rule = create_rule_output_accept(dport, src, dst, sport)
	chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "OUTPUT")
	chain.insert_rule(rule)
	print dport,src,dst,sport
	return rule

def create_rule_output_accept(dport, src, dst, sport):
    rule = iptc.Rule()
    rule.protocol = "tcp"
    match = iptc.Match(rule,'tcp')
    match.sport = sport
    match.dport = dport
    rule.add_match(match)
    match = iptc.Match(rule,'owner')
    match.socket_exists = ''
    rule.add_match(match)
    rule.dst = dst
    rule.src = src
    rule.target = iptc.Target(rule,'ACCEPT')
    #print "rule created for %s" [dport,src,dst,sport]
    return rule

def get_output_accept_rules():
	return iptc.Chain(iptc.Table(iptc.Table.FILTER), "OUTPUT").rules

def get_counters(dport, src, dst, sport):
	rule = create_rule_output_accept(dport, src, dst, sport)
	for r in get_output_accept_rules:
		if rule == r:
			pass

def read_output_iptables():
	table = iptc.Table(iptc.Table.FILTER)
	table.refresh()
	res = []
	chain = iptc.Chain(table, 'OUTPUT')
	for rule in chain.rules:
	        line = rule_counter(res, rule)
	        res.append(line)
	        #map(lambda y: dict({y.name : y.parameters}),rule.matches)])
	return res
def compare_accept_rules(r,s):
	res=[ r.src == s.src and r.dst == s.dst]
	res.append(r.protocol == s.protocol)
	for sm in s.matches:
		for rm in s.matches:
			if rm.name == sm.name:
				res.append(sm.parameters == rm.parameters)
	return all(res)
def rule_counter(rule):
    (packets, bytes) = rule.get_counters()
    line = {'src':rule.src, 'dst':rule.dst ,'packets': packets, 'bytes':bytes} 
    for match in rule.matches:
            if match.name == "tcp":
                    for k in match.parameters:
                            line[k] = match.parameters[k]
            else:
                    line[match.name] = match.parameters
    return line

if __name__ ==  "__main__":
	print read_output_iptables()