j:
ldf a, 255
test
jz j

mov x, a
render_loop:
add
ldt x, 256
ldt a, 11
jo end
jmp render_loop
end:
hlt