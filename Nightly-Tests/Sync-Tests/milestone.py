from iota import TryteString, trits_from_int, ProposedTransaction, ProposedBundle, Tag, Address, Iota
import finalize
from yaml import full_load
import sys

index = 1 
args = sys.argv

print("Starting")
for arg in args: 
    if arg == '-i':
        index = args[int(args.index(arg)) + 1]

def int_to_trytes(int_input, length):
    trits = trits_from_int(int(int_input))
    trytes = TryteString.from_trits(trits)
    if len(trytes) < length:
        trytes += '9' * (length - len(trytes))
    return trytes

yaml_file = full_load(open('./output.yml', 'r'))
nodes = {}
keys = yaml_file.keys()
for key in keys:
    if key != 'seeds' and key != 'defaults':
        nodes[key] = yaml_file[key]
    
host = yaml_file['nodes']['nodeA']['host']
port = yaml_file['nodes']['nodeA']['ports']['api']

api = Iota('http://{}:{}'.format(host, port))

txn = ProposedTransaction(
address = Address('KSAFREMKHHYHSXNLGZPFVHANVHVMKWSGEAHGTXZCSQMXTCZXOGBLVPCWFKVAEQYDJMQALKZRKOTWLGBSC'),
value = 0
)

bundle = ProposedBundle()
bundle.add_transaction(txn)
bundle.add_transaction(txn)

index_trytes = str(int_to_trytes(index, 9))

bundle[0]._legacy_tag = Tag(index_trytes)
    
finalize.finalize(bundle)
bundle_trytes = bundle.as_tryte_strings()

tips = api.get_transactions_to_approve(depth=3)
branch = tips['branchTransaction']
trunk = tips['trunkTransaction']


milestone_bundle = api.attach_to_tangle(trunk,branch, bundle_trytes,3)
api.broadcast_and_store(milestone_bundle.get('trytes'))
print("Milestone {} attached and stored: {}".format(index, milestone_bundle))
