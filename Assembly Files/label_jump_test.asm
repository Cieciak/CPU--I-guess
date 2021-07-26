moi x, 1
render_loop:
add
write_vram:
ldt x, 256
ldt a, 4
jo end
jmp render_loop

end:
hlt