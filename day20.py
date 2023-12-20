
input=r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

input=r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

input=r"""%mh -> rz
%nd -> jx
%xt -> cx
%dp -> mh
%pz -> zg, bf
%rp -> jb, bf
%jb -> bf, kp
%rj -> xt, cx
%hg -> dl, bf
%pt -> gm, vv
%pf -> xk, qr
%cv -> jp, cx
%zg -> bb
%qn -> gm, bh
%kp -> pz
%kg -> gm, pt
%sl -> rp
%dz -> bf, dc
%hm -> cx, tz
%dc -> fk
%xk -> qr, sf
&kr -> gf
%bq -> qr, mg
%sf -> qr
&cx -> ff, vx, zs
%hr -> fq, gm
%ls -> lf, gm
%mf -> cx, sx
%vq -> gm
%sx -> cx, rj
&gm -> kg, kf, fq, nc, lf
%jx -> qr, zz
%tz -> mf, cx
%jp -> cx, kt
%bb -> hg, bf
%zz -> pf, qr
&qr -> dp, bq, nd, rz, mg, qk, mh
%nc -> gb
%kt -> hm, cx
%mg -> dp
%dl -> bf
&zs -> gf
&bf -> dz, zg, kr, sl, fk, kp, dc
%bh -> vq, gm
&kf -> gf
%fq -> qn
%vl -> vx, cx
&qk -> gf
%fk -> sl
%tj -> nd, qr
%gb -> ls, gm
%lf -> hr
%vx -> cv
%ff -> vl, cx
broadcaster -> kg, dz, ff, bq
%vv -> nc, gm
&gf -> rx
%rz -> tj"""


from enum import Enum

class NodeType(Enum):
    BROADCASTER = 1,    # a broadcaster just repeats inputs to the outputs
    FLIPFLOP=2,         # a flip flop just returns the inverse of the last pulse (%)
    CONJUNCTION=3       # a conjunction updates input, if all are high it sends low, otherwise it sends high (&)

class Node:
    node_index: int # urgh this should not live in here
    name: str
    output_node_indices: list[int]
    node_type: NodeType
    flipflip_on: bool
    conjunction_inputs: dict[int,bool] 

    def __init__(self, _name: str, _node_index: int, _node_type: NodeType, _output_indices: list[int]):
        self.name = _name
        self.node_index = _node_index
        self.node_type = _node_type
        self.output_node_indices = _output_indices
        if self.node_type == NodeType.CONJUNCTION:
            self.conjunction_inputs = {} # default to remembering a low pulse -hmmmmm is this gonna bite me?
        elif self.node_type == NodeType.FLIPFLOP:
            self.flipflip_on = False # initially off, low pulse -> flip and send

class NodePulse:
    origin_index: int
    target: Node # TODO should be an index really
    pulse_is_high: bool

    def __init__(self, _origin_index: int, _target: Node, _pulse_is_high: bool):
        self.origin_index = _origin_index
        self.target = _target
        self.pulse_is_high = _pulse_is_high

def parse_nodes(input):
    node_indices: dict[str,int] = {}
    # first grab the names and indices
    for line_idx,line in enumerate(input.split('\n')):
        name,outputs=line.split("->")
        if name[0]=='%' or name[0]=='&':
            name = name[1:]
        else:
            broadcaster_index=line_idx
        node_indices[name.strip()]=line_idx

    nodes: list[Node] = []
    for line_idx,line in enumerate(input.split('\n')):
        name,outputs_str=line.split("->")
        if name[0]=='%':
            node_type = NodeType.FLIPFLOP
            name = name[1:]
        elif name[0]=='&':
            node_type = NodeType.CONJUNCTION
            name = name[1:]
        else:
            node_type = NodeType.BROADCASTER
        outputs = outputs_str.split(',')

        output_indices = []
        for x in outputs:
            x = x.strip()
            if x in node_indices:
                output_indices.append(node_indices[x])
            else:
                output_indices.append(-1) # chuck this one away
        
        nodes.append(Node(name, line_idx, node_type, output_indices))

    # initialise conjunctions to False
    for node in nodes:
        for output in node.output_node_indices:
            if output == -1:
                continue
            if nodes[output].node_type == NodeType.CONJUNCTION:
                nodes[output].conjunction_inputs[node.node_index] = False
    
    return nodes, broadcaster_index

button_presses:int = 0
conj_high: dict[int, list[int]] = {}

def do_pulse(origin_index: int, target_index: int, pulse_is_high: bool, nodes: list[Node], next_node_pulses: list[NodePulse]):
    #print(f"{nodes[origin_index].name} -{pulse_is_high}-> {target_index} ",end="")

    if target_index == -1:
        # chuck this one away
        if not pulse_is_high:
            print(button_presses)
            exit(0)

        # ok, so we're tracking a conjunction -  we want all the inputs to be high so we get a low
        # let's see if there's a periodic repeat for each
        for conj_in in nodes[origin_index].conjunction_inputs:
            if nodes[origin_index].conjunction_inputs[conj_in]:
                if not conj_in in conj_high:
                    conj_high[conj_in] = []
                conj_high[conj_in].append(button_presses)
                
        missing = False
        for conj_in in nodes[origin_index].conjunction_inputs:
            if not conj_in in conj_high:
                missing = True
        if not missing:
            total:int = 1
            for conj_in in nodes[origin_index].conjunction_inputs:
                total *= conj_high[conj_in][0]
            print(total)
            exit(0)
        
        
        
    else:
        #print(f"{nodes[target_index].name}")
        next_node_pulses.append(NodePulse(origin_index, nodes[target_index], pulse_is_high))

def run_node_pulse(node_pulse: NodePulse, nodes: list[Node]):
    next_node_pulses = []
    origin_index = node_pulse.target.node_index # generated pulses originate from this node
    if node_pulse.target.node_type == NodeType.BROADCASTER:
        for node_idx in node_pulse.target.output_node_indices:
            do_pulse(origin_index, node_idx, node_pulse.pulse_is_high, nodes, next_node_pulses)
    elif node_pulse.target.node_type == NodeType.FLIPFLOP:
        ### Flip-flop modules (prefix %) are either on or off; they are initially off. 
        # If a flip-flop module receives a high pulse, it is ignored and nothing happens. 
        # However, if a flip-flop module receives a low pulse, it flips between on and off. 
        # If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
        if not node_pulse.pulse_is_high:
            node_pulse.target.flipflip_on = not node_pulse.target.flipflip_on
            for node_idx in node_pulse.target.output_node_indices:
                do_pulse(origin_index, node_idx, node_pulse.target.flipflip_on, nodes, next_node_pulses)
    elif node_pulse.target.node_type == NodeType.CONJUNCTION:
        ### Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their 
        # connected input modules; they initially default to remembering a low pulse for each input. 
        # When a pulse is received, the conjunction module first updates its memory for that input. 
        # Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
        node_pulse.target.conjunction_inputs[node_pulse.origin_index] = node_pulse.pulse_is_high
        all_high = True
        for origin in node_pulse.target.conjunction_inputs:
            #print(f"{origin}: {node_pulse.target.conjunction_inputs[origin]}")
            if not node_pulse.target.conjunction_inputs[origin]:
                all_high = False
                break
        if all_high:
            for node_idx in node_pulse.target.output_node_indices:
                do_pulse(origin_index, node_idx, False, nodes, next_node_pulses)
        else:
            for node_idx in node_pulse.target.output_node_indices:
                do_pulse(origin_index, node_idx, True, nodes, next_node_pulses)
    return next_node_pulses
            

def press_button(nodes: list[Node], broadcaster_index:int):
    node_pulses: list[NodePulse] = [NodePulse(-1,nodes[broadcaster_index],False)] # button causes a low pulse to broadcaster
    next_node_pulses: list[NodePulse] = []
    while(True):
        while len(node_pulses) > 0:
            node_pulse = node_pulses.pop()
            more_nodes = run_node_pulse(node_pulse, nodes)
            next_node_pulses.extend(more_nodes)
        node_pulses,next_node_pulses = next_node_pulses,node_pulses # swap list ptrs
        if len(node_pulses) == 0:
            break


def run():
    global button_presses

    nodes, broadcaster_index = parse_nodes(input)

    while(True):
        button_presses+=1 
        press_button(nodes, broadcaster_index)

run()