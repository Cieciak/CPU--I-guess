import ram

main_module = ram.RAM(size = 16)

main_module.write(0, 34)

print(main_module.read(0))