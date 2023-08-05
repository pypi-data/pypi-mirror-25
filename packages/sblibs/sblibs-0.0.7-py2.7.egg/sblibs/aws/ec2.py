import boto
from operator import itemgetter

def get_all_instances(region='us-east-1'):
    instances = []
    index = 1
    conn = boto.ec2.connect_to_region(region)
    reservations = conn.get_all_instances()
    for res in reservations:
        for inst in res.instances:
            id = inst.id
            name = inst.tags.get('Name', 'NoName')
            location = inst.placement
            launch_time = str(inst.launch_time)
            size = inst.instance_type
            public_ip = inst.ip_address or ''
            private_ip = inst.private_ip_address or ''
            pub_dns = inst.public_dns_name or ''
            priv_dns = inst.private_dns_name or ''
            vpc_id = inst.vpc_id or ''
            subnet_id = inst.subnet_id or ''
            env = inst.tags.get('Env', '')
            role = inst.tags.get('Role', '')
            master = inst.tags.get('master', '')
            cfn_logical_id = inst.tags.get('aws:cloudformation:logical-id', '')
            cfn_stack_id = inst.tags.get('aws:cloudformation:stack-id', '')
            cfn_stack_name = inst.tags.get('aws:cloudformation:stack-name', '')
            as_group_name = inst.tags.get('aws:autoscaling:groupName', '')
            # Stringing tags that are not relevant to indexing
            other_tags = {}
            for (key, val) in inst.tags.items():
                if 'aws' not in key and 'Name' not in key and 'Hostname' not in key:
                    other_tags[key] = str(val)
            tags_txt = ', '.join("{!s}={!r}".format(key, val) for (key, val) in sorted(other_tags.items()))
            monitored = inst.monitored
            instances.append({'id': id, 'name': name, 'location': location,
                                'size': size,
                                'pub_ip': public_ip, 'priv_ip': private_ip, 'pub_dns': pub_dns,
                                'priv_dns': priv_dns,
                                'status': inst.state, 'vpc_id': vpc_id, 'subnet_id': subnet_id,
                                'monitored': monitored, 'tags': dict(inst.tags), 'tags_txt': tags_txt,
                                'env': env, 'role': role, 'master': master,
                                'cfn_logical_id': cfn_logical_id, 'cfn_stack_id': cfn_stack_id,
                                'cfn_stack_name': cfn_stack_name,
                                'as_group_name': as_group_name,
                                'launch_time': launch_time})
    sorted_instances = sorted(instances, key=itemgetter('env', 'role', 'launch_time'))
    for s in sorted_instances:
        s['index'] = index
        index += 1
    return sorted_instances