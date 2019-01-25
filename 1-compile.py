from solc import compile_files

sols = ['contract.sol']

compliled_contract = compile_files(sols)

print("CONTRACT")
print(compliled_contract)
print("==============================END====================================")
