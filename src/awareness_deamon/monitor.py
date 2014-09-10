#!/usr/bin/python
import redis
import config
import json
import logger
import netstat
import iptables
import driver
import sys

r = redis.StrictRedis(host=config.redis['host'], port=config.redis['port'], db=0)

def create_rules_from_netstat():    
    ns = netstat.netstat()
    #print ns.keys()
    rules={}
    for k in ns.keys():
        v = filter(lambda x: not netstat.is_localhost(x[1]) and not netstat.is_localhost(x[3]), ns[k])
        if v :#and driver.is_logged(k):
            #r.set("%s.proc"%k,json.dumps(v))
            for stream in v:
                pid = k
                src = stream[1]
                dst = stream[3]
                sport = stream[2]
                dport = stream[4]
                #print 'iptables -I OUTPUT -j ACCEPT -m owner --socket-exists --source %s --destination %s -p tcp --sport %s --dport %s' % (src,dst,sport,dport)
                #print "rule is gonna be created %s" % [src,dst,sport,dport]
                # rule = iptables.create_rule_output_accept(dport, src, dst, sport)
                # '''check if the rule does not exists'''
                # if not any([iptables.compare_accept_rules(rule, existing_rule) for existing_rule in iptables.get_output_accept_rules()]):
                #     rule = iptables.set_output_accept_rule(src,dst,sport,dport)
                # try:sta
                #     rules[pid].append(rule)
                # except KeyError:
                #     rules[pid] = [rule]
                # except Exception, e:
                #     #print e
                #     #logger.log_error(e)
                #     pass
    return rules

'''
def create_rules_from_netstat():    
    ns = netstat.netstat()
    rules = {}
    for k in ns: #Per each socket lookup process id and generate a rule
        v = filter(lambda x: not netstat.is_localhost(x[1]) and not netstat.is_localhost(x[3]), ns[k])
        if v and driver.is_logged(k):
            r.set("%s.proc"%k,json.dumps(v))
            for stream in v:
                pid = k
                src = stream[1]
                dst = stream[3]
                sport = stream[2]
                dport = stream[4]
                #print 'iptables -I OUTPUT -j ACCEPT -m owner --socket-exists --source %s --destination %s -p tcp --sport %s --dport %s' % (src,dst,sport,dport)
                print "rule is gonna be created %s" % [src,dst,sport,dport]
                rule = iptables.set_output_accept_rule(src,dst,sport,dport)
                try:
                    rules[pid].append(rule)
                except KeyError:
                    rules[pid] = [rule]
                except Exception, e:
                    print e
                    logger.log_error(e)
                    raise e
	return rules
'''
def clear_rules_from_iptables():
    # rules = iptables.get_output_accept_rules()
    # for rule in rules: #Per each socket lookup process id and generate a rule
    #     src = rule.src.split("/")[0]
    #     dst = rule.dst.split("/")[0]
    #     tcp_match =[match for match in rule.matches if match.name == 'tcp']
    #     if len(tcp_match)>0:         
    #         match = tcp_match[0]
    #         sport = match.parameters['sport']
    #         dport = match.parameters['dport']
    #         content = netstat._load()
    #         if not any(map(lambda x:netstat.TCP_EXTRACTOR_RULE(src,sport,dst,dport).search(x),content)):
    #             iptables.delete_output_accept_rule(rule)
    pass

def fetch_process_network_counters(pid):
    res = []
    ns = netstat.netstat()
    v = filter(lambda x: not netstat.is_localhost(x[1]) and not netstat.is_localhost(x[3]), ns[pid] if pid in ns.keys()  else [] ) 
    if v and driver.is_logged(pid):
		for stream in v:
			src = stream[1]+"/255.255.255.255"
			dst = stream[3]+"/255.255.255.255"
			sport = stream[2]
			dport = stream[4]
			for rule in iptables.get_output_accept_rules():
				if rule.src == src and rule.dst == dst:
					tcp_match =[match for match in rule.matches if match.name == 'tcp']
					if len(tcp_match) > 0:
						match = tcp_match[0]
						if match.parameters['sport'] == sport and match.parameters['dport'] == dport:
							#print "%s:%s -> %s:%s"%(src,sport,dst,dport),"%s packets, %s bytes" % rule.get_counters()
							res.append(rule.get_counters())
	
		return res
    else:
		return "%s not logged in"%pid 

if __name__ == '__main__':
    #print "e"
    create_rules_from_netstat()
    fetch_process_network_counters('26240')
    #sys.argv[1])
