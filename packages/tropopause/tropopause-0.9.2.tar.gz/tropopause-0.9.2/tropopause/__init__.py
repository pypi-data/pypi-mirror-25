import os
import re
import string
import troposphere.ec2 as ec2
from collections import OrderedDict
from troposphere import FindInMap, Output, Condition, AWSObject, Ref, GetAtt, Parameter, Base64, Join, encode_to_dict
from troposphere import Template as TropoTemplate

DNS_SUFFIXES = {
    'us-east-1': 'ec2.internal',
    'us-east-2': 'us-east-2.compute.internal',
    'us-west-1': 'us-west-1.compute.internal',
    'us-west-2': 'us-west-2.compute.internal',
    'ca-central-1': 'ca-central-1.compute.internal',
    'eu-west-1': 'eu-west-1.compute.internal',
    'eu-central-1': 'eu-central-1.compute.internal',
    'eu-west-2': 'eu-west-2.compute.internal',
    'ap-northeast-1': 'ap-northeast-1.compute.internal',
    'ap-northeast-2': 'ap-northeast-2.compute.internal',
    'ap-southeast-1': 'ap-southeast-1.compute.internal',
    'ap-southeast-2': 'ap-southeast-2.compute.internal',
    'ap-south-1': 'ap-south-1.compute.internal',
    'sa-east-1': 'sa-east-1.compute.internal',
}

DISKS_PER_INSTANCE_TYPE = {
    'c1.medium': 1,
    'c1.xlarge': 4,
    'c3.2xlarge': 2,
    'c3.4xlarge': 2,
    'c3.8xlarge': 2,
    'c3.large': 2,
    'c3.xlarge': 2,
    'c4.2xlarge': 0,
    'c4.4xlarge': 0,
    'c4.8xlarge': 0,
    'c4.large': 0,
    'c4.xlarge': 0,
    'cc2.8xlarge': 4,
    'cg1.4xlarge': 2,
    'cr1.8xlarge': 2,
    'd2.2xlarge': 6,
    'd2.4xlarge': 12,
    'd2.8xlarge': 24,
    'd2.xlarge': 3,
    'f1.16xlarge': 4,
    'f1.2xlarge': 1,
    'g2.2xlarge': 1,
    'g2.8xlarge': 2,
    'hi1.4xlarge': 2,
    'hs1.8xlarge': 24,
    'i2.2xlarge': 2,
    'i2.4xlarge': 4,
    'i2.8xlarge': 8,
    'i2.xlarge': 1,
    'i3.16xlarge': 8,
    'i3.2xlarge': 1,
    'i3.4xlarge': 2,
    'i3.8xlarge': 4,
    'i3.large': 1,
    'i3.xlarge': 1,
    'm1.large': 2,
    'm1.medium': 1,
    'm1.small': 1,
    'm1.xlarge': 4,
    'm2.2xlarge': 1,
    'm2.4xlarge': 2,
    'm2.xlarge': 1,
    'm3.2xlarge': 2,
    'm3.large': 1,
    'm3.medium': 1,
    'm3.xlarge': 2,
    'm4.10xlarge': 0,
    'm4.16xlarge': 0,
    'm4.2xlarge': 0,
    'm4.4xlarge': 0,
    'm4.large': 0,
    'm4.xlarge': 0,
    'p2.16xlarge': 0,
    'p2.8xlarge': 0,
    'p2.xlarge': 0,
    'r3.2xlarge': 1,
    'r3.4xlarge': 1,
    'r3.8xlarge': 2,
    'r3.large': 1,
    'r3.xlarge': 1,
    'r4.16xlarge': 0,
    'r4.2xlarge': 0,
    'r4.4xlarge': 0,
    'r4.8xlarge': 0,
    'r4.large': 0,
    'r4.xlarge': 0,
    't1.micro': 0,
    't2.2xlarge': 0,
    't2.large': 0,
    't2.medium': 0,
    't2.micro': 0,
    't2.nano': 0,
    't2.small': 0,
    't2.xlarge': 0,
    'x1.16xlarge': 1,
    'x1.32xlarge': 2,
}


class Template(TropoTemplate):
    def __init__(self):
        TropoTemplate.__init__(self)
        self.ordered_resources = OrderedDict()
        self.metadata = OrderedDict()
        self.conditions = OrderedDict()
        self.mappings = OrderedDict()
        self.outputs = OrderedDict()
        self.parameters = OrderedDict()
        self.resources = OrderedDict()

    def iref(self, key, default=None):
        if key not in self.parameters:
            if default:
                self.parameters[key] = Parameter(key, Type='String', Default=default)
            else:
                self.parameters[key] = Parameter(key, Type='String')
        return Ref(self.parameters[key])

    def imap(self, mapping, key_lvl1, key_lvl2, value):
        if mapping not in self.mappings:
            self.mappings[mapping] = {}
        if key_lvl1 not in self.mappings[mapping]:
            self.mappings[mapping][key_lvl1] = {}
        self.mappings[mapping][key_lvl1][key_lvl2] = value
        return FindInMap(mapping, key_lvl1, key_lvl2)

    def __iadd__(self, other):
        if isinstance(other, Output):
            self.add_output(other)
        elif isinstance(other, Parameter):
            self.add_parameter(other)
        elif isinstance(other, Condition):
            self.add_condition(other)
        elif isinstance(other, AWSObject):
            self.add_resource(other)
            self.ordered_resources[other.title] = other

        return self

    def find(self, needle, first=True):
        out = []
        for k, v in self.ordered_resources.items():
            if type(needle) != str and isinstance(v, needle):
                out.append(v)
            elif type(needle) == str and re.match(needle, v.title):
                out.append(v)
        if first and len(out) == 1:
            return out[0]
        return out

    def to_dict(self):
        t = OrderedDict()
        if self.version:
            t['AWSTemplateFormatVersion'] = self.version
        if self.description:
            t['Description'] = self.description
        if self.parameters:
            t['Parameters'] = self.parameters
        if self.metadata:
            t['Metadata'] = self.metadata
        if self.conditions:
            t['Conditions'] = self.conditions
        if self.mappings:
            t['Mappings'] = self.mappings
        if self.outputs:
            t['Outputs'] = self.outputs
        t['Resources'] = self.resources
        return encode_to_dict(t)


class T(string.Template):
    delimiter = '%'
    idpattern = r'[a-z][_a-z0-9]*'


def readify(f):
    if hasattr(f, 'read'):
        out = f.read()
    else:
        if not ('\n' in f) and os.path.exists(f):
            with open(f, 'r') as fd:
                out = fd.read()
        else:
            out = f
    return out


def network_acls(name, inp, mangle_name=True):
    acl_spec = readify(inp)

    acl_entries = []
    for line in acl_spec.splitlines():
        if not line or line.startswith('#'):
            continue
        pieces = re.split('\s+(?![^[]*\])', line)
        if len(pieces) < 7:
            continue

        def network_acl_add(cidr_block, cidr_block_idx=None):
            acl_props = {
                'NetworkAclId': Ref(name),
                'RuleNumber': int(pieces[1]) + cidr_block_idx if cidr_block_idx else int(pieces[1]),
                'Protocol': int(pieces[2]),
                'RuleAction': pieces[3],
                'CidrBlock': fix_refs(cidr_block),
                'Egress': pieces[6]
            }
            if pieces[5] != '-':
                port_range = pieces[5].split(':')
                acl_props['PortRange'] = ec2.PortRange(From=port_range[0], To=port_range[1])
            if len(pieces) > 7:
                icmp = pieces[7].split(':')
                acl_props['Icmp'] = ec2.ICMP(Code=int(icmp[0]), Type=int(icmp[1]))

            acl_name = pieces[0]
            if mangle_name:
                acl_name = '%s%sEntry' % (pieces[0], name)
                if cidr_block_idx:
                    acl_name = '%s%s' % (acl_name, cidr_block_idx + 1)
            acl_entries.append(ec2.NetworkAclEntry(acl_name, **acl_props))

        pieces[4] = pieces[4].replace('[','').replace(']','').split(',')
        if isinstance(pieces[4], list):
            if len(pieces[4]) > 1:
                for cidr_block_idx, cidr_block in enumerate(pieces[4]):
                    network_acl_add(cidr_block.strip().strip('\''), cidr_block_idx)
            else:
                network_acl_add(pieces[4][0].strip().strip('\''))

    return acl_entries


def vpc_security_rules(inp):
    sg_spec = readify(inp)
    out = []
    for line in sg_spec.splitlines():
        if not line or line.startswith('#'):
            continue
        pieces = re.split('\s+', line)
        resource_name = pieces[0]
        sg_type = pieces[1]
        first = pieces[2]
        second = pieces[3]
        protocol = pieces[4]
        port_range = pieces[5].split(':')

        kwargs = {
            "FromPort": int(port_range[0]),
            "ToPort": int(port_range[1]),
            "IpProtocol": protocol
        }

        if sg_type == 'ingress':
            if re.match(r'^[0-9\.\/]*$', first):
                kwargs['CidrIp'] = first
            else:
                kwargs['SourceSecurityGroupId'] = Ref(first)
            kwargs['GroupId'] = Ref(second)
            out.append(ec2.SecurityGroupIngress(resource_name, **kwargs))
        else:
            if pieces[0] == 'ingress':
                kwargs["SourceSecurityGroupId"] = Ref(pieces[1])
            else:
                kwargs["DestinationSecurityGroupId"] = Ref(pieces[1])
    return out


def security_group_rules(inp):
    ingress = []
    egress = []
    sg_spec = readify(inp)
    for line in sg_spec.splitlines():
        if not line or line.startswith('#') or line.strip() == "":
            continue

        pieces = re.split('\s+(?![^[]*\])', line)
        port_range = pieces[3].split(':')

        def security_group_add(ip):
            kwargs = {
                "FromPort": int(port_range[0]),
                "ToPort": int(port_range[1]),
                "IpProtocol": pieces[2]
            }
            if re.match(r'^[0-9\.\/]*$', ip):
                kwargs["CidrIp"] = ip
            else:
                if pieces[0] == 'ingress':
                    kwargs["SourceSecurityGroupId"] = Ref(ip)
                else:
                    kwargs["DestinationSecurityGroupId"] = Ref(ip)

            sgr = ec2.SecurityGroupRule(**kwargs)
            if pieces[0] == 'ingress':
                ingress.append(sgr)
            elif pieces[0] == 'egress':
                egress.append(sgr)

        pieces[1] = pieces[1].replace('[','').replace(']','').split(',')
        if isinstance(pieces[1], list):
            for ip in list(pieces[1]):
                security_group_add(ip.strip().strip('\''))
    return ingress, egress


def substitute_file(path, substitutions={}):
    return substitute(path, substitutions)


def substitute(inp, substitutions={}):
    inp = readify(inp)
    out = T(inp).substitute(**substitutions)
    return out


def security_group(name, inp, vpc_id, substitutions={}, description=""):
    inp = readify(inp)
    ingress, egress = security_group_rules(substitute(inp, substitutions))

    if description == "":
        description = name

    return ec2.SecurityGroup(
        name,
        GroupDescription=description,
        SecurityGroupEgress=egress,
        SecurityGroupIngress=ingress,
        VpcId=vpc_id
    )


def name_zone(start, i=None, az_i=None):
    id_piece = ""
    az_piece = ""
    if i is not None:
        id_piece = "%d" % i
    if az_i != None:
        az_piece = "AZ%d" % az_i
    return "%s%s%s" % (start, id_piece, az_piece)


def net_name(prefix, what, i=None, az_i=None):
    return name_zone(prefix + what, i, az_i)


def subnet_name(prefix, i=None, az_i=None):
    return net_name(prefix, "Subnet", i, az_i)


def route_table_name(prefix, i=None, az_i=None):
    return net_name(prefix, "RouteTable", i, az_i)


def route_name(prefix, i=None, az_i=None):
    return net_name(prefix, "Route", i, az_i)


REFS_PATTERN = r'(Ref\([a-zA-Z0-9:]*\)|GetAtt\([a-zA-Z0-9:]*,\s*[a-zA-Z0-9:]*\))'


def fix_refs(t):
    if re.match(REFS_PATTERN, t):
        if t[0:3] == "Ref":
            return Ref(t[4:-1])
        else:
            pattern2 = r'GetAtt\(([a-zA-Z0-9:]*),\s*([a-zA-Z0-9:]*)\)'
            tmp = re.search(pattern2, t)
            if tmp and len(tmp.groups(1)) == 2:
                return GetAtt(tmp.groups(1)[0], tmp.groups(1)[1])
            else:
                raise "ERROR parsing string: " + t
    else:
        return t


def split_content(s):
    lines = [l + "\n" for l in s.split("\n")]
    pieces = [re.split(REFS_PATTERN, l) for l in lines]
    flatten = [i for sl in pieces for i in sl]
    return [fix_refs(x) for x in flatten]


def make_content(s):
    return Join('', split_content(s))


def make_user_data(s):
    return Base64(make_content(s))


def merge(*dicts):
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result
